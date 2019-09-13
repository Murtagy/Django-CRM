from django.contrib.auth.mixins import UserPassesTestMixin
from crm.models import Organisation


class OrganisationPermissionView(UserPassesTestMixin):

    def test_func(self):
        req = self.request
        user = req.user
        u_groups = [str(i) for i in user.groups.all()]
        if 'Salesman' in u_groups and 'Manager' not in u_groups:
            org_id = self.kwargs['pk']
            org = Organisation.objects.get(id=org_id)
            owner = org.owned_by
            if owner.id == user.id:
                return True
        if 'Manager' in u_groups:
            return True
        return False
