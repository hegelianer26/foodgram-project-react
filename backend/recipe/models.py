from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name='Название тега', help_text='Название.')
    color = models.CharField(
        max_length=7, unique=True,
        verbose_name='Цвет (HEX)', help_text='Цвет в HEX')
    slug = models.SlugField(
        max_length=200, unique=True,
        verbose_name='Слаг', help_text='Уникальный слаг')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('slug',)
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug')]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название',
        help_text='Название.')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='Единицы измерения',
        help_text='Единицы измерения')

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient, through='Ingridients_For_Recipe',
        through_fields=('recipe', 'ingredient'),
        related_name='ingredients',
        verbose_name='Ингридиенты',
        help_text='Список ингредиентов')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор', help_text='Автор публикации (пользователь)')
    tags = models.ManyToManyField(
        Tag, through='Tags_For_Recipe',
        through_fields=('recipe', 'tags'),
        verbose_name='Тэги', help_text='Список тэгов')
    image = models.ImageField(
        upload_to='recipe/images/',
        verbose_name='Изображение', help_text='Ссылка на картинку на сайте.')
    name = models.CharField(
        max_length=150, unique=True,
        verbose_name='Название', help_text='Название.')
    text = models.TextField(
        verbose_name='Описание', help_text='Описание.')
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть меньше 1 мин')],
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах.')
    is_favorited = models.BooleanField(
        default=False, verbose_name='В избранном')
    in_shopping_cart = models.BooleanField(
        default=False, verbose_name='В списке покупок')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingridients_For_Recipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт',
        related_name='amounts', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Игридиент',
        related_name='amounts', on_delete=models.CASCADE)
    amount = models.IntegerField(
        default=1, validators=[MinValueValidator(1)],
        verbose_name='Количество', help_text='Количество')

    class Meta:
        verbose_name = 'Ингдидиент для рецепта'
        verbose_name_plural = 'Ингдидиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe')]


class Tags_For_Recipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        Tag, related_name='slugs',
        verbose_name='Тэги', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тэг для рецепта'
        verbose_name_plural = 'Тэги для рецепта'


class Favorited(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='user_favorites',
        verbose_name='Пользователь', blank=False, null=False,)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт', blank=False, null=False, )

    class Meta:
        verbose_name = 'Добавить в избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorited')]


class Shopping_Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='shopping_cart', verbose_name='Список покупок')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart', verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_cart')]
