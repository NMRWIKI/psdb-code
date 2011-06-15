# Create your views here.
from django.http import HttpResponse
from labs import forms

def create_lab(request):
    extra = ''
    if request.method == 'POST':
        form = forms.LabAccountForm(request.POST)
        if form.is_valid():
            form.save()
            extra = "Thanks!"
    else:
        form = forms.LabAccountForm()

    response = """
    <form method="post">
    <table>%(the_form)s</table>
    <input type="submit" value="save" />
    </form><p>%(extra)s</p>
    """ % {
        'the_form': form.as_table(),
        'extra': extra
    }

    return HttpResponse(response)
