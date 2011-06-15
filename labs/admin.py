from django.contrib import admin
from psdb-code.labs.models import LabAccount

class LabAccountAdmin(admin.ModelAdmin):
	pass
admin.site.register(LabAccount, LabAccountAdmin)
