from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse

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


@require_POST
def validate_user_info(request):
    if not request.is_ajax():
        raise Http404()
    user_form = UserInfoForm(data=request.POST)
    context = {
        'success': True,
    }
    if not user_form.is_valid():
        context = {
            'success': False,
        }

    context = simplejson.dumps(context)

    return HttpResponse(context, mimetype='application/json')
