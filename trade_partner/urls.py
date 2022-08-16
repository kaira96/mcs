from django.urls import path

from .lookups import TradePartnerAutocomplete, CategoryAutocomplete


urlpatterns = [
    path(r'^trade-partner-autocomplete/$',
         TradePartnerAutocomplete.as_view(),
         name='trade-partner-autocomplete'),

    path(r'^category-autocomplete/$',
         CategoryAutocomplete.as_view(),
         name='category-autocomplete'),
]
