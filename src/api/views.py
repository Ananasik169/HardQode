from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.response import Response
from products.models import Lesson, ProductAccess, Product, LessonProgress
from api.serializers import BaseLessonSerializer, RetriveLessonSerializer
from django.shortcuts import get_object_or_404


class LessonViewSet(viewsets.ViewSet):
   
    def list(self, request: Request) -> HTTP_200_OK:
        queryset = Lesson.objects.filter(
            product_set__in=Product.objects.filter(access__user=request.user)
        ).distinct()
        serailizer = BaseLessonSerializer(queryset, many=True, context={'request': request})
        return Response(serailizer.data, status=HTTP_200_OK)

    def retrieve(self, request: Request, pk=None) -> HTTP_200_OK | HTTP_403_FORBIDDEN:
        product = get_object_or_404(Product, id=pk)
        if ProductAccess.objects.filter(product=product, user=request.user):
            serailizer = RetriveLessonSerializer(product.lessons, many=True, context={'request': request})
            return Response(serailizer.data, status=HTTP_200_OK)
        return Response(status=HTTP_403_FORBIDDEN)


class StatisticsViewSet(viewsets.ViewSet):
    
    def list(self, request):
        pass