from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer)
from django.core.paginator import Paginator

from .models import Follow, CustomUser
from recipe.models import Favorited, Recipe


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password', )
        model = CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', )

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=self.context.get('request').user, author=obj
        ).exists()


class FavoritedSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = self.context['request'].user
        id = self.context['view'].kwargs.get('recipe_id')
        if Favorited.objects.filter(id=id, user=user).exists():
            raise serializers.ValidationError('Рецепт уже в избранном')
        return data

    def create(self, validated_data):
        favorite = Favorited.objects.create(**validated_data)
        favorite.save()
        return favorite

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )


class FollowUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='author.email', read_only=True)
    id = serializers.ReadOnlyField(source='author.id', read_only=True)
    username = serializers.CharField(source='author.username', read_only=True)
    first_name = serializers.CharField(
        source='author.first_name', read_only=True)
    last_name = serializers.ReadOnlyField(
        source='author.last_name', read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Favorited
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count', )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=self.context['request'].user, author=obj.author
        ).exists()

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit') or 1
        queryset = Recipe.objects.filter(author=obj.author)
        paginator = Paginator(queryset, recipes_limit)
        recep = paginator.page(1)
        return FavoritedSerializer(recep, many=True).data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author', )
