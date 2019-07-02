from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
# from .views import OrganisationDetailView


class Base(models.Model):
    # For any object in database

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=40)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=40)

    class Meta:
        # Does not populate DB table
        abstract = True


class BaseOwned(Base):
    # For objects which are usually split between employees
    owned = models.DateTimeField()
    owned_by = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, related_name='%(class)s_owner')

    owned_prev = models.CharField(max_length=40, blank=True, null=True)
    assigned = models.DateTimeField(null=True, blank=True)
    assigned_by = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, default=1, related_name='%(class)s_assigned_by')

    class Meta:
        # Does not populate DB table
        abstract = True


class Client(BaseOwned):
    # Parent class for all client types
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def n_open_activities(self):
        o = Activity.objects.filter(client_fk=self.id, fact_date=None).count()
        return o

    def n_open_orders(self):
        o = Order.objects.filter(client_fk=self.id, fact_date=None).count()
        return o

    def get_type(self):
        children = ['individual', 'organisation', 'lead']
        for c in children:
            try:
                _ = self.__getattribute__(c)
            except ObjectDoesNotExist:
                pass
            else:
                return c.capitalize()
        else:
            return 'Not specified'


class Organisation(Client):
    # def get_absolute_url(self):
        # return "/organistion/%i/" % self.id
    def get_absolute_url(self):
        return reverse('organisation_detail', args=[str(self.id)])


class Individual(Client):
    def get_absolute_url(self):
        return reverse('individual_detail', args=[str(self.id)])


class Lead(Client):
    def get_absolute_url(self):
        pass


class Activity(BaseOwned):
    # Parent class for activity types
    planned_date = models.DateTimeField(blank=True, null=True)
    fact_date = models.DateTimeField(blank=True, null=True)
    client_fk = models.ForeignKey(
        Client, on_delete=models.PROTECT, null=True, blank=True, related_name='%(class)s_client_fk')
    des = models.TextField(max_length=1000, null=True, blank=True)
    result = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        if self.des:
            return self.des[:20]+'...'
        else:
            return 'Activity'

    def get_absolute_url(self):
        return reverse('activity_detail', args=[str(self.id)])

    def get_type(self):
        children = ['action', 'deal', 'order']
        for c in children:
            try:
                _ = self.__getattribute__(c)
            except ObjectDoesNotExist:
                pass
            else:
                return c.capitalize()
        else:
            return 'Not specified'


class Deal(Activity):
    STATUS_TYPES = [
        ('N', 'New'),
        ('P', 'In progress'),
        ('F', 'Finished')
    ]
    status = models.CharField(choices=STATUS_TYPES, default='N', max_length=6)

    def get_absolute_url(self):
        return reverse('deal_detail', args=[str(self.id)])

    def is_new_status_allowed(self, new_status):
        banned_statuses_dict = {
            '': [],
            'N': [''],
            'P': ['N'],
            'F': ['N', 'P']
        }
        banned = banned_statuses_dict[self.status]
        return new_status not in banned


class Action(Activity):
    ACTION_TYPES = [
        ('E', 'E-mail'),
        ('C', 'Call'),
        ('V', 'Visit')
    ]
    type = models.CharField(choices=ACTION_TYPES, max_length=6)
    DIRECTION_TYPES = [
        (0, 'Incoming'),
        (1, 'Outgoing')
    ]
    direction = models.IntegerField(choices=DIRECTION_TYPES, default=1)
    STATUS_TYPES = [
        ('N', 'New'),
        ('P', 'In progress'),
        ('F', 'Finished')
    ]
    status = models.CharField(choices=STATUS_TYPES, default='N', max_length=6)
    deal_fk = models.ForeignKey(
        Deal, null=True, blank=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('action_detail', args=[str(self.id)])

    def is_new_status_allowed(self, new_status):
        banned_statuses_dict = {
            '': [],
            'N': [''],
            'P': ['N'],
            'F': ['N', 'P']
        }
        banned = banned_statuses_dict[self.status]
        return new_status not in banned


class Order(Activity):
    STATUS_TYPES = [
        ('N', 'New'),
        ('P', 'In progress'),
        ('F', 'Finished')
    ]
    status = models.CharField(choices=STATUS_TYPES, max_length=6)

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])

    def is_new_status_allowed(self, new_status):
        banned_statuses_dict = {
            '': [],
            'N': [''],
            'P': ['N'],
            'F': ['N', 'P']
        }
        banned = banned_statuses_dict[self.status]
        return new_status not in banned
