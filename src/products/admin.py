from django.contrib import admin
from .models import Lesson, LessonProgress, Product, ProductAccess


admin.site.register(Lesson)
admin.site.register(Product)
admin.site.register(ProductAccess)


@admin.register(LessonProgress)
class LessonProgress(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'last_view', 'viewed_time', 'status')
