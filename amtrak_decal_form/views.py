from django.shortcuts import render

from amtrak_decal_form.forms import UserInfoForm


def index(request):
    form = UserInfoForm()
    if request.method == 'POST':
        form = UserInfoForm(data=request.POST)
        if form.is_valid():
            pass

    context = {
        'form': form,
    }
    return render(request, 'index.html', context)
