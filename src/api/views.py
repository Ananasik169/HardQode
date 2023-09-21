from rest_framework import viewsets
from rest_framework.response import Response
from products.models import Lesson, ProductAccess, Product, LessonProgress
from api.serializers import LessonSerializer



class LessonViewSet(viewsets.ViewSet):
   
    def list(self, request):
        queryset = Lesson.objects.filter(
            product_set__in=Product.objects.filter(access__user=request.user)
        )
        serailizer = LessonSerializer(queryset, many=True)
        print(serailizer.data)
        return Response(serailizer.data, status=200)

    def retrieve(self, request, id):
        pass


class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):
        pass