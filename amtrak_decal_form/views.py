from datetime import date

from django.core import mail
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.http import require_POST

from pywkher import generate_pdf

from amtrak_decal_form.forms import UserInfoForm, DecalSpecForm


class PDFResponse(HttpResponse):
    """
    Response object to send a PDF file.

    The __init__ method takes two argments, `pdf_data` and `filename`. The
    filename is the name of the pdf file when downloading. The extension ".pdf"
    will be appended to the filename.
    """
    def __init__(self, pdf_data, filename):
        super(PDFResponse, self).__init__(pdf_data, mimetype='application/pdf')
        self['Content-Disposition'] = 'attachment; filename=%s.pdf' % filename


def index(request):
    user_form = UserInfoForm()
    decal_form = DecalSpecForm()
    if request.method == 'POST':
        user_form = UserInfoForm(data=request.POST)
        decal_form = DecalSpecForm(data=request.POST)
        if user_form.is_valid() and decal_form.is_valid():
            pdf_data = render_to_string(
                'pdf.html',
                {
                    'user_form': user_form,
                    'decal_form': decal_form,
                },
            )

            pdf = generate_pdf(pdf_data)
            today = date.today()
            filename = 'Decal-Request-%s' % today.strftime('%m-%d-%y')
            # TODO remove
            mock_up_html = render_to_string(
                'mock_up.html',
                {
                    'html': mark_safe(decal_form.cleaned_data['html']),
                },
            )
            mock_up_data = generate_pdf(mock_up_html)
            # TODO remove
            if request.POST.get('action') == 'preview':
                return HttpResponse(mock_up_html)
            else:
                subject = 'Decal Acquisition %s' % (
                    user_form.cleaned_data['name'],
                )
                from_email = user_form.cleaned_data['email']
                mock_up_html = render_to_string(
                    'mock_up.html',
                    {
                        'html': mark_safe(decal_form.cleaned_data['html']),
                    },
                )
                mock_up_data = generate_pdf(mock_up_html)
                email = mail.EmailMessage(
                    subject=subject,
                    body='See attachment.',
                    from_email=from_email,
                    to=[settings.EMAIL_TO],
                )
                mock_up_filename = 'Mock-Up-%s' % today.strftime('%m-%d-%y')
                email.attach(
                    filename,
                    pdf,
                    'application/pdf',
                )
                if decal_form.cleaned_data['html'] != '<p><br></p>':
                    email.attach(
                        mock_up_filename,
                        mock_up_data,
                        'application/pdf',
                    )
                    email.send()
                return redirect(reverse('index'))

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
            'errors': user_form.errors,
        }

    context = simplejson.dumps(context)

    return HttpResponse(context, content_type='application/json')
