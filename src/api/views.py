from rest_framework import viewsets, status
from rest_framework.response import Response
from products.models import Lesson, ProductAccess, Product, LessonProgress
from api.serializers import LessonSerializer
from django.shortcuts import get_object_or_404


class LessonViewSet(viewsets.ViewSet):
   
    def list(self, request):
        queryset = Lesson.objects.filter(
            product_set__in=Product.objects.filter(access__user=request.user)
        )
        serailizer = LessonSerializer(queryset, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if ProductAccess.objects.filter(product=product, user=request.user).exists():
            serailizer = LessonSerializer(product.lessons, many=True)
            return Response(serailizer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):
        pass