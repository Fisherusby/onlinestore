from tools.onliner_catalog import catalog
from store.models.product_category import Category


# In python manage/py shell
# from tools.auto_fill_db import add_cat_dict_in_db

def add_cat_dict_in_db(cat, parant = False):
    for key, value in cat.items():
        print(key)
        isset = Category.objects.filter(name=key).first()
        if not isset:
            if parant:
                isset = Category.objects.create(
                    name=key,
                    slug='1',
                    parent=parant,
                )
            else:
                isset = Category.objects.create(
                    name=key,
                    slug='1',
                )
        if type(value) == dict:
            add_cat_dict_in_db(value, isset)


add_cat_dict_in_db(catalog)
