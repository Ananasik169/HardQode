from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, IntegerField
from rest_framework.serializers import ModelSerializer
from products.models import Lesson, Product, LessonProgress
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseLessonSerializer(ModelSerializer):
    '''Базовый сериализватор API уроков.'''
    custom_fields = ['viewed_time', 'status']

    class Meta:
        '''Метаданные.'''
        model = Lesson
        fields = ["title", "video_url", "duration"]

    def to_representation(self, instance: Lesson) -> OrderedDict:
        '''Добавляет в данные API дополнительные поля.'''
        data = super().to_representation(instance)

        try:
            lesson_progress = instance.lesson_progress.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            data.update({field: None for field in self.custom_fields})
        else:
            data.update({field: getattr(lesson_progress, field) for field in self.custom_fields})
        return data
    

class RetriveLessonSerializer(BaseLessonSerializer):
    '''Сериализатор API уроков одного продукта.'''
    custom_fields = ['viewed_time', 'status', 'last_view']


class ProductSerializer(ModelSerializer):
    '''Сериализатор API статистики.'''

    class Meta:
        '''Метаданные.'''
        model = Product
        fields = "__all__"

    def to_representation(self, instance: Product) -> OrderedDict:
        '''Добавляет в данные API дополнительные поля.'''
        data = super().to_representation(instance)

        lessons_views = LessonProgress.objects.filter(
            lesson__in=instance.lessons.all()
        ).count()
        total_viewed_time = LessonProgress.objects.filter(
            lesson__in=instance.lessons.all()
        ).aggregate(total_viewed_time=Sum('viewed_time', output_field=IntegerField())/10**6)
        product_users = User.objects.filter(
            access__product=instance
        ).distinct().count()

        access_percent = round((product_users / User.objects.all().count()) * 100, 2)
        data.update({
            'lessons_views': lessons_views, 
            'product_users': product_users, 
            'access_percent': access_percent
            } | total_viewed_time)
        return data
