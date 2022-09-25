from django_filters.widgets import BooleanWidget

from .models import Post, Comment
from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter, BooleanFilter


class CommentFilter(FilterSet):
    date = DateFilter(field_name='date',
                      lookup_expr='gte',
                      label='Создано после',
                      widget=DateInput(attrs={'type': 'date'}))
    is_accepted = BooleanFilter(widget=BooleanWidget(), label='Статус')
    date.field.error_messages = {'invalid': 'Enter date in format DD.MM.YYYY. Example: 31.12.2020'}
    date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}


    class Meta:
        model = Comment
        fields = ['date', 'is_accepted']

