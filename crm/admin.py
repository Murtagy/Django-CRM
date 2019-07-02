from django.contrib import admin
from crm.models import BaseOwned
from crm.models import Activity
from crm.models import Organisation
from crm.models import Client
from crm.models import Individual
from crm.models import Action
from crm.models import Deal
from crm.models import Base
from crm.models import Order

DEFAULT_READ_ONLY = [f.name for f in Base._meta.fields]


def set_list_display_first(list_, first_column):
    list_.remove(first_column)
    list_.insert(0, first_column)
    return list_


@admin.register(Organisation)
class Organisation(admin.ModelAdmin):
    first_column = 'name'
    all_fields = [f.name for f in Organisation._meta.fields]
    list_display = set_list_display_first(all_fields, first_column)
    list_display_links = (first_column,)
    readonly_fields = DEFAULT_READ_ONLY


@admin.register(Individual)
class Individual(admin.ModelAdmin):
    first_column = 'name'
    all_fields = [f.name for f in Individual._meta.fields]
    list_display = set_list_display_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY


@admin.register(Action)
class Action(admin.ModelAdmin):
    first_column = 'status'
    all_fields = [f.name for f in Action._meta.fields]
    list_display = set_list_display_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY


@admin.register(Deal)
class Deal(admin.ModelAdmin):
    first_column = 'status'
    all_fields = [f.name for f in Deal._meta.fields]
    list_display = set_list_display_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY


@admin.register(Order)
class Order(admin.ModelAdmin):
    first_column = 'status'
    all_fields = [f.name for f in Order._meta.fields]
    list_display = set_list_display_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY
