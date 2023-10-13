from django.contrib import admin
from django.contrib.admin import display

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    actions_on_top = False
    actions_on_bottom = False
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cooking_time',
                    'count_favorites')
    list_display_links = ('name',)
    list_filter = ('author', 'name', 'tags',)
    inlines = (IngredientsInLine,)

    @display(description='Количество в избранных')
    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
