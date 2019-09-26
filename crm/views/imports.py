from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import PermissionRequiredMixin  # Changed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone as tz
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import UpdateView
from django.db.models import Subquery

from urllib.parse import urlencode

from ..forms import OrganisationAddForm, IndividualAddForm
from ..forms import ActionAddForm, DealAddForm, OrderAddForm
from ..models import Client, Organisation, Individual
from ..models import Activity, Action, Deal, Order
from ..models import User
from ..permissions import OrganisationViewPermCheck

