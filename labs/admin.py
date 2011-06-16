from django.contrib import admin
from labs.models import LabAccount

class LabAccountAdmin(admin.ModelAdmin):
	pass
admin.site.register(LabAccount, LabAccountAdmin)
