from django.contrib import admin
from .models import User, Lesson, LessonProgress, Product, ProductAccess


admin.site.register(User)
admin.site.register(Lesson)
admin.site.register(Product)
admin.site.register(ProductAccess)


@admin.register(LessonProgress)
class LessonProgress(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'viewed_time', 'status')
