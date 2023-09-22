from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ModelSerializer, CharField, DurationField
from products.models import Lesson, LessonProgress, Product, ProductAccess


class BaseLessonSerializer(ModelSerializer):
    custom_fields = ['viewed_time', 'status']

    class Meta:
        model = Lesson
        fields = ["title", "video_url", "duration"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            lesson_progress = instance.lesson_progress.get(user=self.context['request'].user)
        except ObjectDoesNotExist:
            data.update({field: None for field in self.custom_fields})
        else:
            data.update({field: getattr(lesson_progress, field) for field in self.custom_fields})
        return data
    

class RetriveLessonSerializer(BaseLessonSerializer):
    custom_fields = custom_fields = ['viewed_time', 'status', 'last_view']


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
