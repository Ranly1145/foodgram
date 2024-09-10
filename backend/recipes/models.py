from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    measurement_unit = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                          through='IngredientRecipe')
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    image = models.ImageField(upload_to='recipes/')
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'
