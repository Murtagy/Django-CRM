from django.urls import reverse

from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from django.views import View
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import PermissionRequiredMixin  # Changed
from django.contrib.auth.decorators import login_required
from django.utils import timezone as tz

from urllib.parse import urlencode

from .permissions import OrganisationPermissionView
from .models import Client, Organisation, Individual
from .models import Activity, Action, Deal, Order
from .models import User
from .forms import *


@login_required(login_url='login')
def index(request):
    #     """" Function to show home-page"""

    #     num_orgs = Organisation.objects.all().count()
    #     num_activities = Activity.objects.all().count()
    #     show_orgs = Organisation.objects.order_by('-date')[:9]
    return render(
        request,
        'crm/base.html'
    )


def redirect_to_index(request):
    return index(request)


# CLIENTS
class MyClientsView(ListView):
    model = Client
    template_name = "crm/clients/my_clients.html"
    paginate_by = 15

    def get_queryset(self):
        new_context = self.model.objects.filter(
            owned_by=self.request.user.id).order_by('modified')
        return new_context


class AllClientsView(ListView):
    model = Client
    template_name = "crm/clients/all_clients.html"
    paginate_by = 15
    queryset = model.objects.order_by('modified')


def RedirectClientDetail(request, pk):
    client_id = pk
    c = get_object_or_404(Client, pk=client_id)
    if c:
        c_type = c.get_type()
        # all child's should be imported
        # access class url through globals not to list children here
        c_type_class = globals()[c_type]
        obj = get_object_or_404(c_type_class, pk=client_id)
        return redirect(c_type_class.get_absolute_url(obj))


def render_error(request):
    if request.method == 'GET':
        return render(request, 'crm/base_error.html', {'error': request.GET.get('msg')})


class OrganisationDetailView(OrganisationPermissionView, PermissionRequiredMixin, DetailView):
    model = Organisation
    template_name = 'crm/organisations/organisation_detail.html'
    permission_required = ('crm.view_organisation')


class OrganisationEditView(OrganisationPermissionView, PermissionRequiredMixin, UpdateView):
    model = Organisation
    fields = ['name']
    template_name = 'crm/base_edit.html'
    permission_required = ('crm.change_organisation')

    def form_enrich(self, f):
        f.modified_by = str(self.request.user)
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


class OrganisationAddView(PermissionRequiredMixin, CreateView):
    template_name = 'crm/organisations/org_add.html'
    form_class = OrganisationAddForm
    permission_required = ('crm.add_organisation')

    def form_enrich(self, f):
        f.assigned = tz.now()
        f.assigned_by = User.objects.get(username='admin')  # admin
        # f.create = dt.now()
        f.created_by = self.request.user
        f.owned = tz.now()
        f.owned_by = self.request.user
        # f.modified = dt.now()
        f.modified_by = self.request.user
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


class IndividualAddView(PermissionRequiredMixin, CreateView):
    template_name = 'crm/individuals/ind_add.html'
    form_class = IndividualAddForm
    permission_required = ('crm.add_individual')

    def form_enrich(self, f):
        f.assigned = tz.now()
        f.assigned_by = User.objects.get(username='admin')  # admin
        # f.create = dt.now()
        f.created_by = self.request.user
        f.owned = tz.now()
        f.owned_by = self.request.user
        # f.modified = dt.now()
        f.modified_by = self.request.user
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


class IndividualEditView(PermissionRequiredMixin, UpdateView):
    model = Individual
    fields = ['name']
    template_name = 'crm/base_edit.html'
    permission_required = ('crm.change_individual')

    def form_enrich(self, f):
        f.modified_by = str(self.request.user)
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


# ORDERS
class MyOrdersView(ListView):
    model = Order
    template_name = "crm/orders/my_orders.html"
    paginate_by = 15

    def get_queryset(self):
        new_context = self.model.objects.filter(
            owned_by=self.request.user.id).order_by('modified')
        return new_context


class AllOrdersView(ListView):
    model = Order
    template_name = "crm/orders/all_orders.html"
    paginate_by = 15
    queryset = model.objects.order_by('modified')


class OrderDetailView(DetailView):
    model = Order
    template_name = "crm/orders/order_detail.html"


class OrderAddView(PermissionRequiredMixin, CreateView):
    template_name = 'crm/orders/ord_add.html'
    form_class = OrderAddForm
    permission_required = ('crm.add_order')

    def form_enrich(self, f):
        f.assigned = tz.now()
        f.assigned_by = User.objects.get(username='admin')  # admin
        # f.create = dt.now()
        f.created_by = self.request.user
        f.owned = tz.now()
        f.owned_by = self.request.user
        # f.modified = dt.now()
        f.modified_by = self.request.user
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


class OrderEditView(PermissionRequiredMixin, UpdateView):
    model = Order
    fields = ['des', 'status']
    template_name = 'crm/base_edit.html'
    permission_required = ('crm.change_order')

    def form_enrich(self, f):
        f.modified_by = str(self.request.user)
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        db_obj = form.instance.__class__.objects.get(id=form.instance.id)
        if not db_obj.is_new_status_allowed(form.instance.status):
            url = reverse('error')
            q = urlencode({'msg': 'Bad status'})
            url = url+'?'+q
            return redirect(url)
        return super().form_valid(form)


class DealDetailView(DetailView):
    model = Deal
    template_name = "crm/deals/deal_detail.html"


class DealAddView(PermissionRequiredMixin, CreateView):
    template_name = 'crm/deals/deal_add.html'
    form_class = DealAddForm
    permission_required = ('crm.add_deal')

    def form_enrich(self, f):
        f.assigned = tz.now()
        f.assigned_by = User.objects.get(username='admin')  # admin
        # f.create = dt.now()
        f.created_by = self.request.user
        f.owned = tz.now()
        f.owned_by = self.request.user
        # f.modified = dt.now()
        f.modified_by = self.request.user
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


class DealEditView(PermissionRequiredMixin, UpdateView):
    model = Deal
    fields = ['des', 'status']
    template_name = 'crm/base_edit.html'
    permission_required = ('crm.change_deal')

    def form_enrich(self, f):
        f.modified_by = str(self.request.user)
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        db_obj = form.instance.__class__.objects.get(id=form.instance.id)
        if not db_obj.is_new_status_allowed(form.instance.status):
            url = reverse('error')
            q = urlencode({'msg': 'Bad status'})
            url = url+'?'+q
            return redirect(url)
        return super().form_valid(form)


class ActionDetailView(DetailView):
    model = Action
    template_name = "crm/actions/action_detail.html"


class ActionAddView(PermissionRequiredMixin, CreateView):
    template_name = 'crm/actions/act_add.html'
    form_class = ActionAddForm
    permission_required = ('crm.add_action')

    def form_enrich(self, f):
        f.assigned = tz.now()
        f.assigned_by = User.objects.get(username='admin')  # admin
        # f.create = dt.now()
        f.created_by = self.request.user
        f.owned = tz.now()
        f.owned_by = self.request.user
        # f.modified = dt.now()
        f.modified_by = self.request.user
        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        return super().form_valid(form)


class ActionEditView(PermissionRequiredMixin, UpdateView):
    model = Action
    fields = ['des', 'status']
    template_name = 'crm/base_edit.html'
    permission_required = ('crm.change_action')

    def form_enrich(self, f):
        f.modified_by = str(self.request.user)

        return f

    def form_valid(self, form):
        form.instance = self.form_enrich(form.instance)
        db_obj = form.instance.__class__.objects.get(id=form.instance.id)
        if not db_obj.is_new_status_allowed(form.instance.status):
            url = reverse('error')
            q = urlencode({'msg': 'Bad status'})
            url = url+'?'+q
            return redirect(url)
        return super().form_valid(form)


class MyActivitiesView(ListView):
    model = Activity
    template_name = "crm/activities/my_activities.html"
    paginate_by = 15

    def get_queryset(self):
        new_context = self.model.objects.filter(
            owned_by=self.request.user.id).order_by('modified')
        return new_context


class AllActivitiesView(ListView):
    model = Activity
    template_name = "crm/activities/all_activities.html"
    paginate_by = 15
    queryset = model.objects.order_by('modified')


def RedirectActivityDetail(request, pk):
    act_id = pk
    a = get_object_or_404(Activity, pk=act_id)
    if a:
        a_type = a.get_type()
        # all child's should be imported
        # access class url through globals not to list children here
        a_type_class = globals()[a_type]
        obj = get_object_or_404(a_type_class, pk=act_id)
        return redirect(a_type_class.get_absolute_url(obj))


class IndividualDetailView(DetailView):
    model = Individual
    template_name = 'crm/individuals/individual_detail.html'

# class OrganisationListView(ListView):
#     model = Organisation
#     template_name = 'crm/org/org_list.html'

#     paginate_by = 5


# def index(request):
#     """" Function to show home-page"""

#     num_orgs = Organisation.objects.all().count()
#     num_activities = Activity.objects.all().count()
#     show_orgs = Organisation.objects.order_by('-date')[:9]
#     return render(
#         request,
#         'crm/crm_main.html',
#         context={'num_orgs': num_orgs, 'num_activities': num_activities,
#                  'show_orgs': show_orgs
#                  }
#     )


# def contact(request):
#     return render(request, 'main/basic.html', {'content': ['Если вы хотите связаться со мной используйте email', 'mrabkevich@gmail.com']})


# def organisation_add(request):
#     """" Adds organistaion with some checks"""
#     messages = {'default': '',
#                 'duplicate': 'Уже есть организация с таким названием', 'success': 'Вы успешно создали организацию'
#                 }

#     if request.method == 'POST':
#         form = OrgForm(request.POST)
#         if form.is_valid():
#             new_org = form.save(commit=False)
#             check_org = Organisation.objects.filter(
#                 short_name=new_org.short_name)
#             if check_org:
#                 return rensder(request, 'crm/result.html', {'new_org': new_org, 'message': messages['duplicate']})

#             new_org.save()
#             return render(request, 'crm/result.html', {'new_org': new_org, 'message': messages['success']})

#     else:
#         form = OrgForm()
#     return render(request, 'crm/org/org_add.html', {'form': form, 'message': messages['default']})


# def organisation_edit(request, pk):
#     messages = {'default': '',
#                 }

#     org_ed = get_object_or_404(Organisation, pk=pk)
#     if request.method == 'POST':
#         form = OrgForm(request.POST, instance=org_ed)
#         if form.is_valid():
#             org_ed = form.save(commit=False)
#             #org_ed.short_name = request.user
#             #org_ed.description = request.user
#             org_ed.save()
#             return redirect('org-detail', pk=org_ed.pk)
#     else:
#         form = OrgForm(instance=org_ed)
#     return render(request, 'crm/org/org_add.html', {'form': form, 'message': messages['default']})
