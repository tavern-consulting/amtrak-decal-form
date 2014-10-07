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
        super(
            PDFResponse,
            self,
        ).__init__(
            pdf_data,
            content_type='application/pdf',
        )
        self['Content-Disposition'] = 'attachment; filename=%s.pdf' % filename


def build_mock_up(html):
    mock_up_html = render_to_string(
        'mock_up.html',
        {
            'html': mark_safe(html),
        },
    )
    return generate_pdf(mock_up_html)


def build_mock_up_filename(today):
    return 'Mock-Up-%s' % today.strftime('%m-%d-%y')


def build_decal_info_pdf(user_form, decal_form):
    pdf_data = render_to_string(
        'pdf.html',
        {
            'user_form': user_form,
            'decal_form': decal_form,
        },
    )

    return generate_pdf(pdf_data)


def build_decal_info_filename(today):
    return 'Decal-Request-%s' % today.strftime('%m-%d-%y')


def index(request):
    user_form = UserInfoForm()
    decal_form = DecalSpecForm()
    today = date.today()

    if request.method == 'POST':
        user_form = UserInfoForm(data=request.POST)
        decal_form = DecalSpecForm(data=request.POST)
        if user_form.is_valid() and decal_form.is_valid():
            mock_up_pdf = build_mock_up(decal_form.cleaned_data['html'])
            mock_up_filename = build_mock_up_filename(today)
            if request.POST.get('action') == 'preview':
                return PDFResponse(mock_up_pdf, mock_up_filename)
            else:
                decal_info_pdf = build_decal_info_pdf(user_form, decal_form)
                decal_info_filename = build_decal_info_filename(today)

                subject = 'Decal Acquisition %s' % (
                    user_form.cleaned_data['name'],
                )
                from_email = user_form.cleaned_data['email']
                email = mail.EmailMessage(
                    subject=subject,
                    body='See attachment.',
                    from_email=from_email,
                    to=[settings.EMAIL_TO],
                )
                email.attach(
                    decal_info_filename,
                    decal_info_pdf,
                    'application/pdf',
                )
                if decal_form.cleaned_data['html'] != '<p><br></p>':
                    email.attach(
                        mock_up_filename,
                        mock_up_pdf,
                        'application/pdf',
                    )
                    email.send()
                return redirect(reverse('success'))

    context = {
        'user_form': user_form,
        'decal_form': decal_form,
    }
    return render(request, 'index.html', context)


def success(request):
    context = {}
    return render(request, 'thanks.html', context)


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
