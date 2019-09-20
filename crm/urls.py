from django.urls import include, path
from . import views
from django.views.generic import DetailView
from . import forms


urlpatterns = [
    # idnex
    path('', views.index, name='index'),
    # auth
    path('login/', views.auth_views.LoginView.as_view(template_name='crm/auth/login.html'),
         name='login'),
    path('password_reset/', views.auth_views.PasswordResetView.as_view(template_name='crm/auth/password_reset.html'),
         name='password_reset'),
    path('logout/', views.auth_views.LogoutView.as_view(),
         name='logout'),
    path('error', views.render_error, name='error'),
    # client
    path('my_clients', views.MyClientsView.as_view(), name='my_clients'),
    path('all_clients', views.AllClientsView.as_view(), name='all_clients'),
    path('client/<int:pk>', views.RedirectClientDetail, name='client_detail'),
    # order
    path('my_orders', views.MyOrdersView.as_view(), name='my_orders'),
    path('all_orders', views.AllOrdersView.as_view(), name='all_orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('add_order', views.OrderAddView.as_view(), name='add_order'),
    path('order/<int:pk>/edit',
         views.OrderEditView.as_view(), name='order_edit'),
    # activity
    path('my_activities', views.MyActivitiesView.as_view(), name='my_activities'),
    path('all_activities', views.AllActivitiesView.as_view(), name='all_activities'),
    path('activity/<int:pk>', views.RedirectActivityDetail, name='activity_detail'),
    # deal
    path('deal/<int:pk>', views.DealDetailView.as_view(), name='deal_detail'),
    path('add_deal', views.DealAddView.as_view(), name='add_deal'),
    path('deal/<int:pk>/edit',
         views.DealEditView.as_view(), name='deal_edit'),
    # action
    path('add_action', views.ActionAddView.as_view(), name='add_action'),
    path('action/<int:pk>', views.ActionDetailView.as_view(), name='action_detail'),
    path('action/<int:pk>/edit',
         views.ActionEditView.as_view(), name='action_edit'),
    # organisation
    path('add_organisation', views.OrganisationAddView.as_view(),
         name='add_organisation'),
    path('organisation/<int:pk>', views.OrganisationDetailView.as_view(),
         name='organisation_detail'),
    path('organisation/<int:pk>/edit',
         views.OrganisationEditView.as_view(), name='organisation_edit'),
     path('organisation/<int:pk>/assign',
     views.OrganisationAssignView.as_view(),name='organisation_assign'),
    # individual
    path('add_individual', views.IndividualAddView.as_view(), name='add_individual'),
    path('individual/<int:pk>', views.IndividualDetailView.as_view(),
         name='individual_detail'),
    path('individual/<int:pk>/edit',
         views.IndividualEditView.as_view(), name='individual_edit'),
    # path('activity/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),

    # path('act/<int:pk>', DetailView.as_view(model=Activity, template_name = 'crm/act/act_detail_main.html')),
    # path('org/add', views.organisation_add, name='org-add'),
    # path('org/<int:pk>/edit', views.organisation_edit, name='org-edit'),
    # path('org/list', OrganisationListView.as_view(), name='organisation-list' ),
]
# urlpatterns += [path('crm/',
#                      include('django.contrib.auth.urls'))]
