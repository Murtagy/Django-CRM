from django.contrib import admin
from django import forms
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


def make_column_first(list_, first_column):
    list_.remove(first_column)
    list_.insert(0, first_column)
    return list_


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    first_column = 'name'
    all_fields = [f.name for f in Organisation._meta.fields]
    list_display = make_column_first(all_fields, first_column)
    list_display_links = (first_column,)
    readonly_fields = DEFAULT_READ_ONLY


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    first_column = 'name'
    all_fields = [f.name for f in Individual._meta.fields]
    list_display = make_column_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY


class ActionAdminForm(forms.ModelForm):
    class Meta:
        model=Action
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super(ActionAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.client_fk is not None:
            aq = self.fields['activity_rel'].queryset 
            self.fields['activity_rel'].queryset  = aq.filter(client_fk=self.instance.client_fk.id)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(ActionAdmin, self).get_form(request, obj=obj, **kwargs)

    # form = ActionAdminForm
    first_column = 'status'
    all_fields = [f.name for f in Action._meta.fields]
    list_display = make_column_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY

    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name == 'activity_rel' and self.instance:       
            kwargs['queryset'] = Activity.objects.filter(client_fk=self.instance.client_fk).exclude(id__in=[self.instance.id])
        return  super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(self.__class__, self).get_form(request, obj=obj, **kwargs)

    first_column = 'status'
    all_fields = [f.name for f in Deal._meta.fields]
    list_display = make_column_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY
    
    def formfield_for_manytomany(self,db_field,request,**kwargs):
            if db_field.name == 'activity_rel' and self.instance:       
                kwargs['queryset'] = Activity.objects.filter(client_fk=self.instance.client_fk).exclude(id__in=[self.instance.id])
                # kwargs['queryset'] = Activity.objects.filter(id__in=[self.instance.id])
            return  super().formfield_for_manytomany(db_field, request, **kwargs)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    first_column = 'status'
    all_fields = [f.name for f in Order._meta.fields]
    list_display = make_column_first(all_fields, first_column)
    readonly_fields = DEFAULT_READ_ONLY
