from .imports import *

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

def render_error(request):
    if request.method == 'GET':
        return render(request, 'crm/base_error.html', {'error': request.GET.get('msg')})

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
