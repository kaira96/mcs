from .models import Passport, Client

from django.contrib.postgres.search import TrigramSimilarity

from dal import autocomplete


class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Client.objects.filter()

        if self.q:
            qs = qs.annotate(
                similarity=TrigramSimilarity('passport__pin', self.q),
            ).filter(similarity__gt=0.6).order_by('-similarity')
            return qs

        return qs

    def get_result_label(self, result):
        return result.full_name

    def get_result_value(self, result):
        return result.pk
