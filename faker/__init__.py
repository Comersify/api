from product.models import Shipping
from random import randint
import json
from user.models import CustomUser as User, Store
from product.models import *
import os
from django.core.files import File
from datetime import datetime


def create_user():
    images_users = os.listdir('./faker/users')
    type_ = ["CUSTOMER", "VENDOR"]
    x = 0
    with open('./faker/userdata.json') as f:
        data = json.load(f)
        for line in data:
            user = User.objects.create(
                user_type=type_[x],
                username=line["email"].split("@")[0],
                first_name=line["first_name"],
                last_name=line["last_name"],
                password=line["password"],
                email=line["email"],
                is_active=True,
                phone_number=line["phone_number"]
            )
            if x == 0:
                x = 1
            else:
                x = 0
            print(f"User num: {user.id}")


def create_store():
    users = User.objects.filter(user_type='VENDOR')
    with open('./faker/store.json') as f:
        data = json.load(f)
        x = 1
        for line in data:
            s = Store.objects.create(
                user=users[x],
                name=line["name"],
                description=line["description"],
            )
            x += 1
            print(f"store : {s.name}")


def create_cat():
    with open('./faker/category.json') as f:
        data = json.load(f)
        x = 0
        for line in data:
            if x < 20:
                s = Category.objects.create(
                    name=line['category']
                )
            if x >= 20:
                cat = Category.objects.filter(parent__isnull=True)
                y = randint(0, 19)
                s = Category.objects.create(
                    parent=cat[y],
                    name=line['category']
                )
            x += 1

            print(f"category : {s}")


def create_product():
    users = User.objects.filter(user_type="VENDOR")
    cats = Category.objects.filter(parent__isnull=False)
    with open('./faker/product.json') as f:
        data = json.load(f)
        for line in data:
            cat = randint(0, len(cats)-1)
            user = randint(0, len(users)-1)
            p = Product.objects.create(
                user=users[user],
                title=line["title"],
                category=cats[cat],
                description=line["description"],
                price=line["price"],
                buy_price=line["bu_price"],
                in_stock=line["in_stock"],
            )
            print(f"product: {p.title}")


def create_dis():
    pr = Product.objects.all()
    print(len(pr))
    with open('./faker/discount.json') as f:
        data = json.load(f)
        for line in data:
            x = randint(0, len(pr)-1)
            print(x)
            d = Discount.objects.create(
                title=line["title"],
                percentage=line["percentage"],
                end_date=datetime.strptime(line["end_date"], "%d/%m/%Y"),
                product=pr[x]
            )
            print(f"product : {d.title}")


def create_images():
    import os
    images = os.listdir('./faker/images')
    t = ['X', 'L', 'M', 'S', 'XL']
    for p in Product.objects.all():
        qua = p.in_stock
        for y in t:
            quantity = randint(0, int(qua/2))
            randomized = randint(0, len(images)-1)
            with open(f"./faker/images/{images[randomized]}", "rb") as f:
                images_file = File(f)
                if y in t[:4]:
                    ir = ProductImage.objects.create(
                        product_id=p.id,
                        image=images_file
                    )
                i = ProductPackage.objects.create(
                    image=images_file,
                    product=p,
                    title=y,
                    quantity=quantity
                )
                print(f"{i.title} => {i.image.url}")


def create_coupon():
    pr = Product.objects.all()
    from datetime import datetime
    with open('./faker/coupon.json') as f:
        data = json.load(f)
        for i, line in enumerate(data):
            a = Coupon.objects.create(
                product=pr[i],
                code=line['code'],
                value=line['percentage'],
                end_date=datetime.strptime(line["date"], "%d/%m/%Y")
            )


def get(id):
    c = Coupon.objects.filter(product_id=id).get()
    return c.code


def set_cats():
    cats = Category.objects.all()
    x = 0

    for p in Product.objects.all():
        p.category_id = cats[x].id
        p.save()
        print(f"{x} => {len(cats)} : {len(cats) == x}")
        if len(cats) == x + 1:
            x = 0
        else:
            x += 1


def create_shipping():
    with open('./faker/shipping.json') as f:
        data = json.load(f)
        for u in User.objects.filter(user_type="VENDOR"):
            for i, line in enumerate(data['wilayas']):
                Shipping.objects.create(
                    user=u,
                    wilaya=line['name'],
                    price=line['price'],
                )


def create_orders():
    from order.models import Order
    from datetime import date
    ps = Product.objects.filter(user__username="ngaskoin9f")
    users = User.objects.filter(user_type="CUSTOMER")
    ships = Shipping.objects.filter(user__username="ngaskoin9f")

    for i in range(100):
        lp = randint(0, len(ps)-1)
        lu = randint(0, len(users)-1)
        lsp = randint(0, len(ships)-1)
        quantity = randint(1, 15)
        pack = ProductPackage.objects.filter(product=ps[lp]).last()
        Order.objects.create(
            status="DELEVRED",
            product=ps[lp],
            user=users[lu],
            pack=pack,
            quantity=quantity,
            shipping=ships[lsp],
            created_at=date(
                2023,
                randint(2, 12),
                randint(2, 25)
            )
        )


apps = [
    'ads',
    'cart',
    'chat',
    'order',
    'product',
    'tracking',
    'user',
    'wishlist'
]


def clear_migrations():
    for app in apps:
        migrations = os.listdir(f"{app}/migrations")
        migrations.remove('__init__.py')
        for migration in migrations:
            try:
                os.remove(f"{app}/migrations/{migration}")
            except:
                try:
                    cache = os.listdir(f"{app}/migrations/__pycache__")
                    for c in cache:
                        os.remove(f"{app}/migrations/__pycache__/{c}")
                    os.rmdir(f"{app}/migrations/__pycache__")
                except FileNotFoundError:
                    pass
        print(f"folder {app} is cleaned")


def run():
    # create_user()
    # create_cat()
    # create_store()
    create_product()
    create_images()
    set_cats()
    create_coupon()
    create_dis()
    create_shipping()
    create_orders()
