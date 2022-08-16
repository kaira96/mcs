from django.urls import re_path

from .lookups import ClientAutocomplete


urlpatterns = [
   re_path(
       r'^client-autocomplete/$',
       ClientAutocomplete.as_view(),
       name='client-autocomplete'
   )
]
