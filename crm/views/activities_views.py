from .imports import *


# ORDERS are oved to separate tab on nav because 
# of highest importance over other activities types
class MyOrdersView(ListView):
    model = Order
    template_name = "crm/orders/my_orders.html"
    paginate_by = 15

    def get_queryset(self):
        GET = self.request.GET
        accepted_params = {
            'open': GET.get('open'),
            'closed':  GET.get('closed')
        }
        new_queryset = self.model.objects.filter(
            owned_by=self.request.user.id).order_by('modified')
        if len(GET) != 0:
            if accepted_params.get('open'):
                new_queryset = new_queryset.filter(fact_date__isnull=True).order_by('modified')
        if len(GET) != 0:
            if accepted_params.get('closed'):
                new_queryset = new_queryset.filter(fact_date__isnull=False).order_by('modified')
        return new_queryset



class AllOrdersView(ListView):
    model = Order
    template_name = "crm/orders/all_orders.html"
    paginate_by = 15
    queryset = model.objects.order_by('modified')

    def get_queryset(self):
        GET = self.request.GET
        accepted_params = {
            'open': GET.get('open'),
            'closed':  GET.get('closed')
        }
        new_queryset = self.model.objects.order_by('modified')
        if len(GET) != 0:
            if accepted_params.get('open'):
                new_queryset = new_queryset.filter(fact_date__isnull=True).order_by('modified')
        if len(GET) != 0:
            if accepted_params.get('closed'):
                new_queryset = new_queryset.filter(fact_date__isnull=False).order_by('modified')
        return new_queryset



class OrderDetailView(DetailView):
    model = Order
    template_name = "crm/orders/order_detail.html"


class OrderAddView(PermissionRequiredMixin, CreateView):
    template_name = 'crm/orders/ord_add.html'
    form_class = OrderAddForm
    permission_required = ('crm.add_order')

    def form_enrich(self,form):
        self.object =  form.save(commit=False)
        self.object.assigned = tz.now()
        self.object.assigned_by = User.objects.get(username='admin')  # admin
        self.object.created_by = str(self.request.user)
        self.object.modified_by = str(self.request.user)
        self.object.owned_by =self.request.user
        self.object.owned = tz.now()
        return None

    def form_valid(self, form):
        self.form_enrich(form)
        self.object.save()
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

    def get_context_data(self, **kwargs):
        context = super(DealDetailView, self).get_context_data(**kwargs)
        activities= self.get_related_activities()
        context['related_activities'] = activities
        context['page_obj'] = activities 
        return context

    def get_related_activities(self):
        queryset = self.object.activity_rel.all() 
        paginator = Paginator(queryset,5) #paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities


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
    template_name = 'crm/base_edit'
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

    def form_enrich(self, form):
        self.object = form.save(commit=False)
        self.object.assigned = tz.now()
        self.object.assigned_by = User.objects.get(username='admin')  # admin
        # f.create = dt.now()
        self.object.created_by = str(self.request.user)
        self.object.owned = tz.now()
        self.object.owned_by = self.request.user
        # f.modified = dt.now()
        self.object.modified_by = str(self.request.user)
        if self.request.GET.get('related_activity'):
            self.object.save()
            ra = self.request.GET.get('related_activity')
            ra_obj = Activity.objects.get(pk=ra)

            self.object.client_fk  = ra_obj.client_fk 
            self.object.activity_rel.add(ra_obj)
        return None

    def form_valid(self, form):
        self.form_enrich(form)
        self.object.save()
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
        GET = self.request.GET
        accepted_params = {
            'open': GET.get('open'),
            'closed':  GET.get('closed')
        }
        new_queryset= self.model.objects.filter(
            owned_by=self.request.user.id).order_by('modified')
        if len(GET) != 0:
            if accepted_params.get('open'):
                new_queryset = new_queryset.filter(fact_date__isnull=True)
        if len(GET) != 0:
            if accepted_params.get('closed'):
                new_queryset = new_queryset.filter(fact_date__isnull=False)
        return new_queryset



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

