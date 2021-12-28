from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from store.models import Category, GoodsImage, Goods, Brand, OfferVendor, Vendor, Basket, GoodsInBasket, Order, \
    ReviewGoods

# class GoodsAdmin(admin.ModelAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form = super(GoodsAdmin, self).get_form(request, obj, **kwargs)
#         import pdb
#         pdb.set_trace()
#         form.fields['category'].queryset = Category.objects.filter(cildren=None)
#         return form
from store.views import GoodsViewSet


class GoodsAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['category'].queryset = Category.objects.filter(children=None)
         return super(GoodsAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Category, MPTTModelAdmin)
# admin.site.register(Product, MPTTModelAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsImage)

admin.site.register(Brand)
admin.site.register(OfferVendor)
admin.site.register(Vendor)

admin.site.register(Basket)
admin.site.register(GoodsInBasket)

admin.site.register(Order)
admin.site.register(ReviewGoods)






# admin.site.register(PropertyProduct)
# admin.site.register(Goods)
# admin.site.register(GoodsProperty)

