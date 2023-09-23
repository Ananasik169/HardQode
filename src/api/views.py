from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN
)
from products.models import (
    Lesson,
    ProductAccess,
    Product
)
from api.serializers import (
    BaseLessonSerializer, 
    RetriveLessonSerializer, 
    ProductSerializer
)

class LessonViewSet(viewsets.ViewSet):
   
    def list(self, request: Request) -> Response:
        '''Возвращает данные о всех уроках, доступных пользователю.'''
        queryset = Lesson.objects.filter(
            product_set__in=Product.objects.filter(access__user=request.user)
        ).distinct()
        serializer = BaseLessonSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request: Request, pk=None) -> Response:
        '''Возвращает данные о всех уроках продукта, доступного пользователю.'''
        product = get_object_or_404(Product, id=pk)
        if ProductAccess.objects.filter(product=product, user=request.user):
            serializer = RetriveLessonSerializer(product.lessons, many=True, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_403_FORBIDDEN)


class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request: Request) -> Response:
        '''Возвращает статистику по всем продуктам.'''
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)
