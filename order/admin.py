from django.contrib import admin

# Register your models here.

from .models import Catalogue

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    pass