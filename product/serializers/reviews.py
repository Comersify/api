from product.models import Review
from django.db.models import OuterRef, Subquery
from django.contrib.auth import get_user_model


User = get_user_model()


class ReviewsSerializer:
    def get_reviews(self, id):
        subquery_user_image = User.objects.filter(
            id=OuterRef('id'),
            user_type='CUSTOMER'
        ).values('image')[:1]

        subquery_user_first_name = User.objects.filter(
            id=OuterRef('id'),
            user_type='CUSTOMER'
        ).values('first_name')[:1]

        subquery_user_last_name = User.objects.filter(
            id=OuterRef('id'),
            user_type='CUSTOMER'
        ).values('last_name')[:1]

        reviews = Review.objects.filter(product_id=id).annotate(
            image=Subquery(subquery_user_image),
            last_name=Subquery(subquery_user_first_name),
            first_name=Subquery(subquery_user_last_name),
        ).values('review', 'stars', 'created_at', 'image', 'last_name', 'first_name')

        return list(reviews)

    def get_reviews_stats(self, id):
        total = Review.objects.filter(product_id=id).count()
        if total == 0:
            return {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
            }
        percent = 100/total
        stats = {
            1: Review.objects.filter(product_id=id, stars=1).count() * percent,
            2: Review.objects.filter(product_id=id, stars=2).count() * percent,
            3: Review.objects.filter(product_id=id, stars=3).count() * percent,
            4: Review.objects.filter(product_id=id, stars=4).count() * percent,
            5: Review.objects.filter(product_id=id, stars=5).count() * percent
        }
        return stats
