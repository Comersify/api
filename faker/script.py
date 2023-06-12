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
    t = ['X', 'L', 'M', 'S', 'XL']
    for y in t:
        for p in Product.objects.all():
            x = randint(0, len(images) - 1)
            i = ProductPackage.objects.create(
                image=f"/uploads/images/{images[x]}",
                product=p,
                title=y
            )
            print(i.title)
            x += 1


def create_coupon():
    pr = Product.objects.all()
    print(len(pr))
    with open('./faker/coupon.json') as f:
        data = json.load(f)
        for i, line in enumerate(data):
            a = Coupon.objects.create(
                product=pr[i],
                code=line['code'],
                value=line['percentage'],
                end_date=line['date']
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


def fix_images():
    import os
    images_users = os.listdir('./media/test-users')
    images_products = os.listdir('./media/test-images')
    from django.core.files import File
    for p in Product.objects.all():
        i = randint(0, len(images_products)-1)
        ims = randint(1, 4)
        for m in range(ims):
            with open(f"./media/test-images/{images_products[i]}", "rb") as f:
                images_file = File(f)
                ir = ProductImage.objects.create(
                    product_id=p.id,
                    image=images_file
                )
                print(f"{p.title} => {ir.image.url}")
    return
    # for p in ProductPackage.objects.all():
    #    p.image = "/media" + p.image.url
    #    p.save()
    #    print(f"{p.title} => {p.image.url}")
    #
    # for u in User.object.all():
    #    i = randint(0, len(images)-1)
    #    u.image =  f"/media/uploads/users/{images[i]}"
    #    u.save()
    #    print(f'user: {u.username}')
