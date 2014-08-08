from django.shortcuts import render

from amtrak_decal_form.forms import UserInfoForm, DecalSpecForm


def index(request):
    user_form = UserInfoForm()
    decal_form = DecalSpecForm()
    if request.method == 'POST':
        user_form = UserInfoForm(data=request.POST)
        decal_form = DecalSpecForm(data=request.POST)
        if user_form.is_valid() and decal_form.is_valid():
            pass

    context = {
        'user_form': user_form,
        'decal_form': decal_form,
    }
    return render(request, 'index.html', context)
