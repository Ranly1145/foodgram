import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe, TagRecipe

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar',
        )
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount',
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    image = Base64ImageField()
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )
    ingredients = IngredientRecipeSerializer(required=True, many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'image_url',
            'name',
            'text',
            'cooking_time',
        )

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def create_ingredients(self, ingredients, recipe):
        IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount'],
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data,
        )
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        self.create_ingredients(ingredients, recipe=instance)
        return super().update(instance, validated_data)