from rest_framework import status, viewsets
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from users.pagintations import CustomPagination
from rest_framework import filters
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, ShoppingCartSerializer)
from users.serializers import FavoritedSerializer
from .models import (
    Shopping_Cart, Tag, Ingredient,
    Recipe, Ingridients_For_Recipe, Favorited)
from .permissions import AuthorOrReadOnly
from .filters import Recipefilter, IngredientsFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientsFilter


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = RecipeSerializer
    permission_classes = [AuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = Recipefilter
    pagination_class = CustomPagination
    ordering_fields = ('-pub_date', )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user)
        return serializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'POST':
            if Favorited.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                data = {'detail': 'Рецепт уже в избранном!'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            instance = Favorited.objects.create(
                recipe=recipe, user=request.user
            )
            serializer = FavoritedSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if Favorited.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                Favorited.objects.get(
                    user=request.user, recipe=recipe
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'delete'], detail=True,
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'POST':
            if Shopping_Cart.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                data = {'detail': 'Уже в списке покупок!'}
                return Response(
                    data=data, status=status.HTTP_400_BAD_REQUEST)
            instance = Shopping_Cart.objects.create(
                user=request.user, recipe=recipe)
            serializer = ShoppingCartSerializer(instance)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if Shopping_Cart.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                Shopping_Cart.objects.get(
                    user=request.user, recipe=recipe
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'], detail=False,
        permission_classes=[IsAuthenticated],
        )
    def download_shopping_cart(self, request, pk=None):
        user = request.user
        queryset = Ingridients_For_Recipe.objects.filter(
            recipe__shopping_cart__user=user)
        shopping_list = {}
        for ingredient in queryset:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount}
            else:
                shopping_list[name]['amount'] += amount

        pdfmetrics.registerFont(TTFont('Times', 'times.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        filename = "shopping-list.pdf"
        response['Content-Disposition'] = (
            'attachment; filename="{}"'.format(filename))
        p = canvas.Canvas(response)
        p.setFont('Times', size=16)
        i = 0
        location = 800
        for item, value in shopping_list.items():
            i += 1
            location -= 30
            p.drawString(
                70, location, (f'{i}) { item } - {value["amount"]}'
                               f'{value["measurement_unit"]}'))

        p.showPage()
        p.save()
        return response
