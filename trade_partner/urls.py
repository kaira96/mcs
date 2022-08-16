from django.urls import re_path

from .lookups import TradePartnerAutocomplete, CategoryAutocomplete


urlpatterns = [
    re_path(
        r'^trade-partner-autocomplete/$',
        TradePartnerAutocomplete.as_view(),
        name='trade-partner-autocomplete'
    ),

    re_path(
        r'^category-autocomplete/$',
        CategoryAutocomplete.as_view(),
        name='category-autocomplete'
    ),
]
