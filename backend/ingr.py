from recipe.models import Ingredient
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import csv
with open("ingrs.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        try:
            _, created = Ingredient.objects.get_or_create(
            name=row[0],
            measurement_unit=row[1],
            )
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            event = Ingredient.objects.filter(name=row[0], measurement_unit=row[1]).order_by('id').first()
            pass
