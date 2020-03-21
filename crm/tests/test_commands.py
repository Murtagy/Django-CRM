from django.test import TestCase

class CommandTestCase(TestCase):
    def test_defaultsetup(self):
        from crm.management.commands import defaultsetup
        c = defaultsetup.Command()
        c.handle()
