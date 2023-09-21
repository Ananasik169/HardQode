from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Lesson(models.Model):
    '''Модель урока.'''

    title = models.CharField(
        max_length=64,
        verbose_name='Название урока'
    )
    video_url = models.CharField(
        max_length=256,
        verbose_name='Ссылка на видео'
    )
    duration = models.DurationField(
        default=None,
        verbose_name='Длительность просмотра'
    )

    def __str__(self) -> str:
        '''Возвращает название урока.'''
        return self.title

    class Meta:
        '''Метаданные.'''
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class LessonProgress(models.Model):
    '''Модель прогресса прохождения урока.'''

    def viewed_time_validator(self, viewed_time):
        '''Проверяет, что просмотренное время меньше длины видео.'''
        if viewed_time > self.lesson.duration:
            raise ValidationError

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        verbose_name='Урок'
    )
    viewed_time = models.DurationField(
        validators=[viewed_time_validator],
        default=None,
        verbose_name='Просмотренное время'
    )
    last_view = models.DateTimeField(
        auto_now=True,
        verbose_name='Последний просмотр'
    )

    @property
    def status(self) -> str:
        '''Возвращает True, если просмотрено 80% урока и более.'''
        if (self.viewed_time/self.lesson.duration * 100) >= 80:
            return 'Просмотрено'
        return 'Не просмотрено'
    
    status.fget.short_description = 'Статус'

    def __str__(self) -> str:
        '''Возвращает id прогресса урока.'''
        return str(self.id)
    
    class Meta:
        '''Метаданные.'''
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогрессы уроков'


class Product(models.Model):
    '''Модель продукта.'''

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    lessons = models.ManyToManyField(
        'Lesson',
        related_name='products',
        related_query_name="product_set",
        verbose_name='Уроки'
    )

    def __str__(self) -> str:
        '''Возвращает id продукта.'''
        return str(self.id)
    
    class Meta:
        '''Метаданные.'''
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductAccess(models.Model):
    '''Модель доступа к продукту.'''

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name="access"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name="access"
    )

    def __str__(self) -> str:
        '''Возвращает id пользователя и id продукта'''
        return f'Пользователь: {self.user.id}, Продукт: {self.product.id}'
    
    class Meta:
        '''Метаданные.'''
        verbose_name = 'Доступ к продукту'
        verbose_name_plural = 'Доступы к продуктам'
