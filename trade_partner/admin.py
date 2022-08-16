from django.contrib import admin
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest

from .models import TradePartner, Category, ProductDetail


# Register your models here.
class TradePartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'bank_id_code',
                    'merchant_account_number', 'created_date')

    search_fields = ('name',)
    list_filter = ('is_active',)
    date_hierarchy = 'created_date'
    
    
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('loan_application', 'trade_partner', 'category',
                    'seller_full_name', 'seller_phone_number', 'created_date')

    search_fields = ('trade_partner', 'loan_application')
    list_filter = ('trade_partner', 'category')
    date_hierarchy = 'created_date'
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')
    search_fields = ('parent__name', 'name')
    autocomplete_fields = ('parent', )

    def get_search_results(self, request, queryset, search_term):

        if search_term:
            queryset = queryset.annotate(
                    similarity=Greatest(
                        TrigramSimilarity('name', search_term),
                        TrigramSimilarity('parent__name', search_term),
            )
            ).filter(similarity__gt=0.3).order_by('-similarity')

        return queryset, True


admin.site.register(TradePartner, TradePartnerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
