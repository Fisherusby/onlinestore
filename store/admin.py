from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from store.models import Category, ProductImage, Product, Brand, OfferVendor, Vendor, Basket, ProductInBasket, Order, \
    ReviewProduct, PhotoReviewProduct


class ProductImageInLine(admin.TabularInline):
    model = ProductImage

class ProductsAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInLine,
    ]

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['category'].queryset = Category.objects.filter(children=None)
        return super().render_change_form(request, context, *args, **kwargs)

        # return super(Products, self).render_change_form(request, context, *args, **kwargs)


# class OfferVendorAdminForm(forms.ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.filter(children=None))
#
#     class Meta:
#         model = OfferVendor
#         fields = (
#             'category',
#             'product',
#             'vendor',
#             'price',
#         )
#
#     def clean(self):
#         super(OfferVendorAdmin, self).clean()  # if necessary
#         import pdb
#         pdb.set_trace()
#         if 'product' in self._errors:
#             """
#             reset the value (something like this i
#             think to set the value b/c it doesnt get set
#             b/c the field fails validation initially)
#             """
#             product = Product.objects.get(pk=self.data['region'])
#             self.initial['region'] = product.id
#             self.cleaned_data['region'] = product
#             self.region = product
#
#             # remove the error
#             del self._errors['product']
#
#         return self.cleaned_data
#
# class OfferVendorAdmin(admin.ModelAdmin):
#     form = OfferVendorAdminForm

admin.site.register(Category, MPTTModelAdmin)
# admin.site.register(Product, MPTTModelAdmin)
admin.site.register(Product, ProductsAdmin)
# admin.site.register(ProductImage)

admin.site.register(Brand)
admin.site.register(OfferVendor)
admin.site.register(Vendor)

admin.site.register(Basket)
admin.site.register(ProductInBasket)

admin.site.register(Order)


class PhotoReviewProductInLine(admin.TabularInline):
    model = PhotoReviewProduct


class ReviewProductAdmin(admin.ModelAdmin):
    inlines = [
        PhotoReviewProductInLine,
    ]


admin.site.register(ReviewProduct, ReviewProductAdmin)


# admin.site.register(PropertyProduct)
# admin.site.register(Goods)
# admin.site.register(GoodsProperty)

