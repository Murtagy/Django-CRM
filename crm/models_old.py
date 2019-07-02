from django.db import models

# Create your models here.
class Organisation(models.Model):
    short_name = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateTimeField(auto_now = True)
    logo = models.ImageField(upload_to='crm/org/logo', max_length=100, null=True, default='crm/org/logo/sobre.png')
	
    def __str__(self):
	    return self.short_name
		
    def get_related_activity(self):
        return Activity.objects.filter(organisation=self)
	
class Activity(models.Model):

    EMAIL = "E-mail"
    CALL = "Звонок"
    
    CHOICES = [('E', EMAIL), ('C', CALL)]
    type = models.CharField(choices= CHOICES, max_length = 40, default='C')
    
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    content = models.TextField()
    description = models.TextField(default=None, blank=True, null=True)
    
    