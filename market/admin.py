from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Market

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    pass
