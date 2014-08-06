from django.shortcuts import render

from amtrak_decal_form.forms import UserInfoForm


def index(request):
    form = UserInfoForm()
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)
