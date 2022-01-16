from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Tag, Recipe, Ingredient, Ingridients_For_Recipe, Shopping_Cart)
from users.serializers import CustomUserSerializer


class TagSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class Ingridients_For_RecipeSerializer(ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Ingridients_For_Recipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSimpleSerializer(WritableNestedModelSerializer):
    ingredients = Ingridients_For_RecipeSerializer(source='amounts', many=True)
    tags = TagSerializer(many=True)

    class Meta:
        fields = (
            'id', 'author', 'name', 'text', 'image',
            'ingredients', 'tags', 'cooking_time', )
        model = Recipe


class RecipeSerializer(WritableNestedModelSerializer):
    ingredients = Ingridients_For_RecipeSerializer(source='amounts', many=True)
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
        model = Recipe

    def get_context(self):
        return {'request': self.context}

    def get_is_favorited(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return self.context['request'].user.user_favorites.filter(
            recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return self.context['request'].user.shopping_cart.filter(
            recipe=obj).exists()


class ShoppingCartSerializer(ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Shopping_Cart
        field = ('id', 'name', 'image', 'cooking_time', )
