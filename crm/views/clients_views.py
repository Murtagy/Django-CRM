from .imports import *


# CLIENTS
class SearchClientsView(PermissionRequiredMixin, ListView):
    model=Client
    template_name = 'crm/clients/search_clients.html'
    paginate_by=15
    permission_required = ('crm.view_organisation')

    def get_queryset(self):
        name = self.request.GET.get('name')
        queryset = self.model.objects.filter(name__icontains=name)
        return queryset


class MyClientsView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = "crm/clients/my_clients.html"
    paginate_by = 15
    permission_required = ('crm.view_organisation')

    def get_queryset(self):
        GET = self.request.GET
        accepted_params = {
            'has_open_deals': GET.get('has_open_deals'),
            'has_open_activities':  GET.get('has_open_activities')
        }
        new_queryset = self.model.objects.filter(
            owned_by=self.request.user.id).order_by('modified')
        if len(GET) != 0:
            if accepted_params.get('has_open_deals'):
                open_deals_clients = Deal.objects.filter(fact_date__isnull=True).values('client_fk')
                new_queryset = new_queryset.filter(id__in=open_deals_clients)
        if len(GET) != 0:
            if accepted_params.get('has_open_activities'):
                open_activities_clients = Activity.objects.filter(fact_date__isnull=True).values('client_fk')
                new_queryset = new_queryset.filter(id__in=open_activities_clients)
        return new_queryset


class AllClientsView(PermissionRequiredMixin, ListView):
    model = Client
    template_name = "crm/clients/all_clients.html"
    paginate_by = 15
    permission_required = ('crm.view_organisation')
    queryset = model.objects.order_by('modified')

    def get_queryset(self):
        GET = self.request.GET
        accepted_params = {
            'has_open_deals': GET.get('has_open_deals'),
            'has_open_activities':  GET.get('has_open_activities')
        }
        new_queryset = self.model.objects.all()
        if len(GET) != 0:
            if accepted_params.get('has_open_deals'):
                open_deals_clients = Deal.objects.filter(fact_date__isnull=True).values('client_fk')
                new_queryset = new_queryset.filter(id__in=open_deals_clients)
        if len(GET) != 0:
            if accepted_params.get('has_open_activities'):
                open_activities_clients = Activity.objects.filter(fact_date__isnull=True).values('client_fk')
                new_queryset = new_queryset.filter(id__in=open_activities_clients)
        return new_queryset

       

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


class OrganisationAssignView(PermissionRequiredMixin,UpdateView):
    model = Organisation
    fields = ['owned_by']
    template_name = 'crm/base_edit.html'
    permission_required = ('crm.assign_organisation')

    def form_enrich(self,form):
            old_obj = form.instance
            self.object =  form.save(commit=False)
            self.object.assigned = tz.now()
            self.object.assigned_by = self.request.user 
            self.object.modified_by = str(self.request.user)
            self.object.owned = tz.now()
            self.object.owned_prev = str(old_obj.owned_by)
            return None

    def form_valid(self, form):
        self.form_enrich(form)
        self.object.save()
        return super().form_valid(form)


class OrganisationDetailView(OrganisationViewPermCheck, PermissionRequiredMixin, DetailView):
    model = Organisation
    template_name = 'crm/organisations/organisation_detail.html'
    permission_required = ('crm.view_organisation')


class OrganisationEditView(PermissionRequiredMixin, UpdateView):
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
        print(f.assigned    )
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


