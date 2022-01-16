from django.contrib import admin

from .models import (
    Tag, Ingredient, Recipe, Ingridients_For_Recipe,
    Tags_For_Recipe, Shopping_Cart)


class Ingridients_For_RecipeAdmin(admin.TabularInline):
    model = Ingridients_For_Recipe


class Tags_For_RecipeAdmin(admin.TabularInline):
    model = Tags_For_Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('author', 'name', 'tags')
    list_display = ('id', 'author', 'name', 'favor_counts')
    inlines = [Ingridients_For_RecipeAdmin, Tags_For_RecipeAdmin]

    def favor_counts(self, obj):
        return obj.favorited_by.all().count()


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name', )
    list_display = ('id', 'name', 'measurement_unit', )

    def favor_counts(self, obj):
        return obj.favorited_by.all().count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Ingridients_For_Recipe)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tags_For_Recipe)
admin.site.register(Shopping_Cart)
