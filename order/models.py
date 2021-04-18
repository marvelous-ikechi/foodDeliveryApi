from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
from base.models import BaseModel, SlugBase


def get_upload_path(instance, filename):
    name = instance.__class__.__name__
    market = instance.__class__.market
    return '%s/%s/%s' % (str(name).lower(), str(market).lower(), filename)

class Pictures(models.Model):
    image = models.ImageField(upload_to=get_upload_path)

class Catalogue(BaseModel, SlugBase):
    market = models.ForeignKey('market.Market', on_delete=models.CASCADE, related_name='markets')
    category = models.ForeignKey('market.Category', on_delete=models.CASCADE)
    pictures = models.ManyToManyField(Pictures, blank=True)
    price = models.IntegerField(verbose_name='Price(in kobo)')
    rating = models.DecimalField(editable=False, max_digits=5, decimal_places=2, null=True, blank=True)
    minute = models.IntegerField()
    hour = models.IntegerField(null=True, blank=True, default=0)
    approved = models.BooleanField(default=False)

    @property
    def get_price(self):
        return "%s" % (int(self.price) / 100)
    
    @property
    def get_images(self):
        return self.pictures.values_list('image.url', flat=True)

    @property
    def get_delivery_time(self):
        return "%d:%d" % (self.hour, self.minute)

    def get_orders(self, status):
        if status:
            return self.orders.filter(status=status)
        else:
            return self.orders.all()

    @property
    def calc_rating(self):
        return self.rating if self.rating else 0, self.get_orders('completed').count()
    
    def approve(self):
        self.approved = True
        self.save(update_fields=['approved'])
        return self

    @classmethod
    def valid(cls):
        return cls.objects.filter(approved=True)


class Order(BaseModel):
    STATUS = (
        ('started', 'Started'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('failed', 'Failed'),
        ('disputed', 'Disputed'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', editable=False)
    order = models.ForeignKey(Catalogue, on_delete=models.CASCADE, related_name='orders')
    rated = models.BooleanField(default=False, editable=False)
    status = models.CharField(max_length=255, choices=STATUS, editable=False)

    @property
    def get_time(self):
        return self.order.get_delivery_time

    @property
    def time_to_deliver(self):
        time = self.get_time.split(':')
        return self.created_at + datetime.timedelta(hours=int(time[0]), minutes=int(time[1]))

    def rate(self, rate):
        rate = int(rate)
        current_rating, current_weight = self.order.calc_rating
        self.order.rating = (current_rating + rate) / (current_weight + 1)
        self.order.save(update_fields=['rating'])
        
        self.rated = True
        self.save(update_fields=['rated'])

    def update_status(self, status):
        self.status = str(status).lower()
        self.save(update_fields=['status'])

    def get_market(self):
        return self.order.market
    
