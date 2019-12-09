from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission

def create_admin():
    try: 
        User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_user('admin','','admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()
    # print('WARNING! Please change admin password')

def create_groups():
    try:
        sales = Group.objects.get(name='Sales')
    except Group.DoesNotExist:
        sales = Group.objects.create(name='Sales')
        sales.save()
    try:
        manager = Group.objects.get(name='Manager')
    except Group.DoesNotExist:
        manager = Group.objects.create(name='Manager')
        manager.save()

def add_permissions(group, p_list):
    p_object_list = []
    for p_name in p_list:
        p_obj = Permission.objects.get(name=p_name) 
        p_object_list.append(p_obj)
    group.permissions.set(p_object_list)

class Command(BaseCommand):
    help = "Creates basic roles and admin superuser"

    def handle(self, *args, **options):
        create_admin()
        create_groups()
        add_permissions(Group.objects.get(name='Manager'),['crm.view_organisation'])
        add_permissions(Group.objects.get(name='Sales'),['crm.view_organisation'])
