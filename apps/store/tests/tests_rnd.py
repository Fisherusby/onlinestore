from rest_framework.test import APITestCase
from tools.add_rnd import create_cat, create_brands_and_vendors, create_random_goods, create_vendors_and_offers
from apps.store.models import Brand, Vendor, OfferVendor
from apps.store.models import Category, Product

class RandomBaseAPITestCase(APITestCase):
    def setUp(self):
        pass

    # def test_rnd_db(self):
    #     create_cat()
    #     create_brands_and_vendors()
    #     create_random_goods(70)
    #     create_vendors_and_offers(1, 5)
    #
    #     print(len(Category.objects.all()))
    #     print(len(Brand.objects.all()))
    #     print(len(Product.objects.all()))
    #     print(len(Vendor.objects.all()))
    #     print(len(OfferVendor.objects.all()))

