from django.contrib import admin
from django.contrib.admin import display
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


class TagsInLine(admin.TabularInLine):
    model = Recipe.tags.through


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
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
    inlines = (IngredientsInLine, TagsInLine)

    @display(description='Количество в избранных')
    def count_favorites(self, obj):
        return obj.favorites.count()

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        if not obj.ingredients.exists() or not obj.tags.exists():
            raise ValidationError(
                'Рецепт должен иметь минимум один ингредиент или один тег.'
            )
        super().save_model(request, obj, form, change)


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
