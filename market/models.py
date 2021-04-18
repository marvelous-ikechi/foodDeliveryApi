from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel, SlugBase


class Category(BaseModel, SlugBase):
    pass


class Market(BaseModel, SlugBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='markets')
    avatar = models.URLField()
    categories = models.ManyToManyField(Category, blank=True)
    approved = models.BooleanField(default=False)

    @property
    def get_categories(self):
        return self.categories.values_list('name', flat=True)

    @property
    def catalogues(self):
        return self.markets.all()

    @classmethod
    def valid(cls):
        return cls.objects.filter(approved=True)
