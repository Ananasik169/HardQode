from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ModelSerializer
from collections import OrderedDict
from products.models import Lesson, Product


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
    custom_fields = custom_fields = ['viewed_time', 'status', 'last_view']


class StatisticsSerializer(ModelSerializer):
    '''Сериализатор API статистики.'''

    class Meta:
        model = Product
        fields = "__all__"
