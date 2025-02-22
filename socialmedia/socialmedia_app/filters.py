from django_filters import FilterSet, NumberFilter
from .models import *
from django_filters import rest_framework as filters


class  PostFilter(FilterSet):
    class Meta:
        model =  Post
        fields = {
            'hashtag': ['exact']
        }
