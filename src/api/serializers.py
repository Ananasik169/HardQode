from rest_framework.serializers import ModelSerializer
from products.models import Lesson, LessonProgress, Product, ProductAccess


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
