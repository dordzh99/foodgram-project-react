from django_filters.rest_framework import (BooleanFilter, FilterSet,
                                           ModelChoiceFilter,
                                           ModelMultipleChoiceFilter, filters)
from recipes.models import Ingredient, Recipe, Tag, User


class IngredientSearchFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'author', 'is_in_shopping_cart',
            'tags', 'is_favorited'
        )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
