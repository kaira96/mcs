from .models import TradePartner, Category

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest

from dal import autocomplete


class TradePartnerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = TradePartner.objects.all()

        if self.q:
            qs = qs.annotate(
                similarity=TrigramSimilarity('name', self.q),
            ).filter(similarity__gt=0.3).order_by('-similarity')

        return qs


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Category.objects.all()

        if self.q:
            qs = qs.annotate(
                similarity=Greatest(
                    TrigramSimilarity('name', self.q),
                    TrigramSimilarity('parent__name', self.q),
                )
            ).filter(similarity__gt=0.3).order_by('-similarity')

        return qs
