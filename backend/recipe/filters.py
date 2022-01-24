import django_filters

from .models import Recipe, Tag


class Recipefilter(django_filters.FilterSet):

    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited', 
        method='filter_is_favorited'
        )
    in_shopping_cart = django_filters.NumberFilter(
        field_name='is_favorited', 
        method='filter_in_shopping_cart'
        )

    class Meta:
        model = Recipe
        fields = ['tags', 'is_favorited', 'in_shopping_cart']

    def filter_is_favorited(self, qs, name, value):

        if value == 1:
            return qs.filter(favorited_by__user=self.request.user)
        return qs

    def filter_in_shopping_cart(self, qs, name, value):

        if value == 1:
            return qs.filter(in_shopping_cart=True)
        return qs
