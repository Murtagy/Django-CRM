from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from crm.models import Organisation
from django.utils import timezone as tz

def create_admin():
    try: 
        User.objects.get(username='admin')
        print('admin already exists')
    except User.DoesNotExist:
        user = User.objects.create_user('admin','','admin')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print('Created: ', user)
    print('WARNING! Please change admin password')

def create_groups():
    try:
        sales = Group.objects.get(name='Sales')
        print('Sales group already exists')
    except Group.DoesNotExist:
        print('Created sales group')
        sales = Group.objects.create(name='Sales')
        sales.save()
    try:
        manager = Group.objects.get(name='Manager')
        print('Manager group already exists')
    except Group.DoesNotExist:
        print('')
        manager = Group.objects.create(name='Manager')
        manager.save()

def add_permissions(group, p_list):
    p_object_list = []
    for p_name in p_list:
        p_obj = Permission.objects.get(name=p_name) 
        p_object_list.append(p_obj)
        print(f'Adding {p_obj} for {group}')
    group.permissions.set(p_object_list)

def create_org():
    if Organisation.objects.filter(name='Test organisation'):
        print('Test organisation already exists')
        return
    org = Organisation()
    org.created_by = 'Initial test'
    org.modified_by = 'Initial test'
    org.owned = tz.now()
    org.owned_by = User.objects.get(username='admin')
    org.owned_prev = '101010101101'
    org.assigned = tz.now()
    org.name = 'Test organisation'
    org.save()

class Command(BaseCommand):
    help = "Creates basic roles and admin superuser"

    def handle(self, *args, **options):
        create_admin()
        create_groups()
        add_permissions(Group.objects.get(name='Manager'),['Can view organisation', 'Can change organisation'])
        add_permissions(Group.objects.get(name='Sales'),['Can view organisation', 'Can change organisation', 'Can assign organisation'])
        create_org()
        print('All good')

if __name__ == "__main__":
    c = Command()
    c.handle()