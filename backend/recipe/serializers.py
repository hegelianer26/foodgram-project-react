from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404

from .models import (
    Tag, Recipe, Ingredient, Ingridients_For_Recipe,
    Shopping_Cart, Tags_For_Recipe, Favorited)
from users.serializers import CustomUserSerializer


class TagSerializer(ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class Tags_For_RecipeSerializer(ModelSerializer):
    id = serializers.ReadOnlyField(source='tags.id')
    name = serializers.ReadOnlyField(source='tags.name')
    slug = serializers.ReadOnlyField(source='tags.slug')
    color = serializers.ReadOnlyField(source='tags.color')

    class Meta:
        model = Tags_For_Recipe
        fields = ('id', 'name', 'color', 'slug', )


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


class IngredientWriteSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'amount'
        ]


class RecipeSerializer(WritableNestedModelSerializer):
    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',)
            
    def validate_ingredients(self, data):
        ingredients = []
        for ingredient in data:
            if ingredient['id'] in ingredients:
                raise serializers.ValidationError(
                    'Ингридиенты не должны повторяться')
            ingredients.append(ingredient['id'])

            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    'Количество ингридиента должно быть больше 0')

        return data
    
    def validate_cooking_time(self, data):
        if int(data) <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0')
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(**validated_data)

        tags = []

        for tag in tags_data:
            tag_object = get_object_or_404(Tag, id=tag.id)
            tags.append(tag_object)
        new_recipe.tags.add(*tags)

        for ingredient in ingredients_data:
            ingredient_object = get_object_or_404(
                Ingredient, id=ingredient.get('id')
            )
            new_recipe.ingredients.add(
                ingredient_object,
                through_defaults={'amount': ingredient.get('amount')}
            )
        new_recipe.save()
        return new_recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        updated_recipe = super().update(instance, validated_data)
        updated_recipe.tags.clear()
        tags = []
        for tag in tags_data:
            tag_object = get_object_or_404(Tag, id=tag.id)
            tags.append(tag_object)
        updated_recipe.tags.add(*tags)
        updated_recipe.ingredients.clear()
        for ingredient in ingredients_data:
            ingredient_object = get_object_or_404(
                Ingredient, id=ingredient.get('id')
            )
            updated_recipe.ingredients.add(
                ingredient_object,
                through_defaults={'amount': ingredient.get('amount')}
            )
        return updated_recipe

    def to_representation(self, obj):
        self.fields["tags"] = TagSerializer(many=True)
        self.fields["ingredients"] = Ingridients_For_RecipeSerializer(
            source='amounts', many=True)

        return super().to_representation(obj)

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
    name = serializers.ReadOnlyField(source="recipe.name")
    image = Base64ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        model = Shopping_Cart
        fields = ('id', 'name', 'image', 'cooking_time', )


class FavoritedSerializer(WritableNestedModelSerializer):
    id = serializers.ReadOnlyField(source="recipe.id")
    name = serializers.ReadOnlyField(source="recipe.name")
    image = Base64ImageField(source="recipe.image", read_only=True)
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    class Meta:
        model = Favorited
        fields = ('id', 'name', 'image', 'cooking_time', )
