from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from store.models import Category, ProductImage, Product, Brand, OfferVendor, Vendor, Basket, ProductInBasket, Order, \
    ReviewProduct


class ProductsAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['category'].queryset = Category.objects.filter(children=None)
        return super().render_change_form(request, context, *args, **kwargs)

        # return super(Products, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Category, MPTTModelAdmin)
# admin.site.register(Product, MPTTModelAdmin)
admin.site.register(Product, ProductsAdmin)
admin.site.register(ProductImage)

admin.site.register(Brand)
admin.site.register(OfferVendor)
admin.site.register(Vendor)

admin.site.register(Basket)
admin.site.register(ProductInBasket)

admin.site.register(Order)
admin.site.register(ReviewProduct)






# admin.site.register(PropertyProduct)
# admin.site.register(Goods)
# admin.site.register(GoodsProperty)

