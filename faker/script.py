from random import randint
import json
from user.models import CustomUser as User, Store
from product.models import *


def create_user():
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
    users = Store.objects.all()
    cats = Category.objects.filter(parent__isnull=False)
    with open('./faker/product.json') as f:
        data = json.load(f)
        for line in data:
            cat = randint(0, len(cats)-1)
            user = randint(0, len(users)-1)
            p = Product.objects.create(
                store=users[user],
                title=line["title"],
                categoryID=cats[cat],
                description=line["description"],
                price=line["price"],
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
                end_date=line["end_date"],
                product=pr[x]
            )
            print(f"product : {d.title}")


def create_images():
    import os
    images = os.listdir('./media/uploads/images')
    x = 0
    for p in Store.objects.all():
        if x == len(images):
            x = 0
        p.logo = f"/uploads/images/{images[x]}"
        p.cover = f"/uploads/images/{images[x]}"
        p.save()
        print(p.logo)
        x += 1
