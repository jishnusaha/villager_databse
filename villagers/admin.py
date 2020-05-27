from django.contrib import admin
from .models import *

admin.sites.AdminSite.site_header = 'Site Administration'
admin.sites.AdminSite.site_title = 'Admin'
admin.sites.AdminSite.index_title = 'Villagers'


admin.site.register(Bari)


# admin.site.register(Villager)

@admin.register(Villager)
class VillagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'bari', 'father', 'mother', 'occupation', 'marital_status', 'lives_in_village', 'alive')
    list_filter = ('bari__name', 'lives_in_village')
    search_fields = ('name',)
