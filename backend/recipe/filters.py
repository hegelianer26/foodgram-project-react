import django_filters

from .models import Recipe, Tag


class Recipefilter(django_filters.FilterSet):
    # default for CharFilter is to have exact lookup_type
    # name = django_filters.CharFilter(lookup_type='icontains')
    # description = django_filters.CharFilter(lookup_type='icontains')

    # tricky part - how to filter by related field?
    # but not by its foreign key (default)
    # `to_field_name` is crucial here
    # `conjoined=True` makes that, the more tags, the more narrow the search
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
        conjoined=True,
    )

    class Meta:
        model = Recipe
        fields = ['tags']
