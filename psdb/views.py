# Create your views here.
from django.http import HttpResponse

def home(request):
	"""main view"""
	return HttpResponse('hahah')
