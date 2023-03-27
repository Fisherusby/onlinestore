import string
import random
from apps.store.models import Brand, Vendor, OfferVendor
from apps.store.models import Category, Product
from .onliner_catalog import catalog
from string import ascii_uppercase

WORDS = ['Brisque', 'Mysterioso', 'Preprimary', 'Unjealously', 'Responsorium', 'Theresa', 'Metabolomes', 'Repaster',
         'Autoboot', 'Bacterian', 'Thereout', 'Free flowing', 'Honey', 'Preliminary', 'Animative', 'Upsize',
         'Crotchety', 'High seasoned', 'Temption', 'Sauvignon blanc', 'Jib headed', 'Defraud', 'Aggravates', 'Villa',
         'Postganglionic', 'Algicide', 'Empathically', 'Droughty', 'Vapourish', 'Lyricists', 'Stiff neck', 'Degreasers',
         'Thousands', 'Disparities', 'Fuckdoll', 'Dishware', 'Accurately', 'Wallflowers', 'Suppositionally', 'Micella',
         'Seeking', 'Santon', 'Twincest', 'Trappour', 'Girls', 'Fieldman', 'Bastardize', 'Alliance', 'Emptyish',
         'Elche', 'Loners', 'Lathy', 'Travale', 'Ginger', 'Unbolt', 'Conodonts', 'Unsisterliness', 'Dribblet',
         'Tremorous', 'Perigastrula', 'Interruptible', 'Propound', 'Sylvicola', 'Swordfight', 'Squander', 'Picometer',
         'Decriminalized', 'Creation', 'Doxologies', 'Tavel', 'Cryptical', 'Slapdash', 'Establishes', 'Makuta',
         'Vaishyas', 'Illaqueation', 'Corrosivity', 'Bordelaise', 'Long beach', 'Dolor', 'Buyers', 'Thermobaric',
         'Astrochemistry', 'Flench', 'Rakish', 'Lathe', 'Laking', 'Dropseed', 'Reasoning', 'Bottled', 'Nano ohm',
         'Unroof', 'Allwhither', 'Attelet', 'Afflux', 'Exorcists', 'Naples', 'Choiceful', 'Glaucus', 'Affeeble']


def rnd_model():
    size = random.randrange(1, 4)
    result = ''.join(random.choice(string.ascii_uppercase) for _ in range(size))
    result += random.choice(['', ' ', '-'])
    size = random.randrange(1, 5)
    result += ''.join(random.choice(string.digits) for _ in range(size))
    result += random.choice(['', '0'])
    return result


def add_cat_dict_in_db(cat, parant = False):
    for key, value in cat.items():
        # print(key)
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


def create_cat():
    add_cat_dict_in_db(catalog)


def create_brands_and_vendors():
    [Brand.objects.create(name=w) for w in WORDS]

    [Vendor.objects.create(name=f'Vendor {i}', email='fisherus.dev@gmail.com', address=f'Zone 51-{i}', slug='1') for i in range(20)]


def create_random_goods(count):
    products_type = Category.objects.filter(children=None)[:10]
    brands = Brand.objects.all()
    rnd_str = ascii_uppercase+'        '

    COLORS = [
        'red',
        'black',
        'green',
        'silver',
        'blue',
        'white',
    ]

    for category in products_type:
        for _ in range(count):
            Product.objects.create(
                category=category,
                brand=random.choice(brands),
                model=rnd_model(),
                production=2000+random.randint(1, 17),
                description=''.join(random.choice(rnd_str) for i in range(200)),
                color=random.choice(COLORS),
            )


# from tools.add_rnd import create_vendors_and_offers

def create_vendors_and_offers(offer_min, offer_max):
    vendors = Vendor.objects.all()
    if len(vendors) < 10:
        return False

    products = Product.objects.all()

    for product in products:
        has_offer = random.randint(1, 100)
        if has_offer < 50:
            price = random.randint(20, 1000)
            count_offers = random.randint(offer_min, offer_max)
            rnd_vendors = random.sample(range(len(vendors)), count_offers)
            for vendor in rnd_vendors:
                OfferVendor.objects.create(
                    product=product,
                    vendor=vendors[vendor],
                    price=price+random.randint(1, 10)
                )


def create_all():
    print('add cat')
    create_cat()
    print('add brands')
    create_brands_and_vendors()
    print('add goods')
    create_random_goods(30)
