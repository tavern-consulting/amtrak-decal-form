from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from amtrak_decal_form.forms import (
    DecalSpecForm,
    FORM_ERRORS,
    NON_ROLLING_STOCK,
    # ROLLING_STOCK,
    UserInfoForm,
)


class SmokeTestCase(TestCase):
    def test_GET_index_returns_200(self):
        url = reverse('index')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_100_percent_code_coverage(self):
        from amtrak_decal_form import wsgi
        assert wsgi

    def test_non_ajax_POST_on_validate_user_info_page_returns_404(self):
        url = reverse('validate_user_info')
        r = self.client.post(url)
        self.assertEqual(r.status_code, 404)


class FormTestCase(TestCase):
    url = reverse('index')
    action = 'preview'

    @property
    def params(self):
        return {
            # User Form
            'name': 'name',
            'department': 'Engineering',
            'location': 'location',
            'phone_number': '123-456-7890',
            'alternate_phone_number': '123-456-0987',
            'email': 'foo@bar.com',
            'cost_center': 'cost_center',
            'wbs_element': 'wbs_element',
            'account': 'account',
            'line1': 'line1',
            'line2': 'line2',
            'city': 'Indianapolis',
            'state': 'IN',
            'zip_code': '46260',

            # Decal Form
            'rolling_stock_or_not': 'Rolling Stock',
            'placard_or_decal': 'Placard',
            'fleet_type': 'P32',
            'border_color': '#000000',
            'description': 'Description',
            'html': '<p>Test<p>',
            'border_type': 'None',
            'border_thickness': '5px',
            'required_substrate': 'Lexedge (Plastic)',

            'action': self.action,
        }

    def test_form_error_for_missing_fields(self):
        r = self.client.post(self.url, {})
        for key, field in UserInfoForm.base_fields.items():
            if field.required:
                self.assertFormError(
                    r,
                    'user_form',
                    key,
                    'This field is required.',
                )
            else:
                with self.assertRaises(AssertionError):
                    self.assertFormError(
                        r,
                        'user_form',
                        key,
                        'This field is required.',
                    )
        for key, field in DecalSpecForm.base_fields.items():
            if field.required:
                self.assertFormError(
                    r,
                    'decal_form',
                    key,
                    'This field is required.',
                )
            else:
                with self.assertRaises(AssertionError):
                    self.assertFormError(
                        r,
                        'decal_form',
                        key,
                        'This field is required.',
                    )

    def test_no_form_errors(self):
        r = self.client.post(self.url, self.params)
        for key, field in UserInfoForm.base_fields.items():
            with self.assertRaises(AssertionError):
                self.assertFormError(
                    r,
                    'user_form',
                    key,
                    'This field is required.',
                )


class UserPanelFormTestCase(TestCase):
    def test_alternate_number_must_be_different(self):
        params = {
            'phone_number': '123-456-7890',
            'alternate_phone_number': '123-456-7890',
        }
        form = UserInfoForm(data=params)
        form.is_valid()
        self.assertEqual(
            form.errors['alternate_phone_number'],
            [FORM_ERRORS['alternate_phone_number']['duplicate']],
        )


class DecalSpecFormTestCase(TestCase):
    # def test_rolling_stock_only_allows_subset_of_colors(self):
    #     params = {
    #         'rolling_stock_or_not': ROLLING_STOCK,
    #         'font_color': '#789456',
    #         'border_color': '#789456',
    #     }
    #     form = DecalSpecForm(data=params)
    #     form.is_valid()
    #     colored_fields = ['font_color', 'border_color']
    #     for colored_field in colored_fields:
    #         self.assertEqual(
    #             form.errors[colored_field],
    #             [FORM_ERRORS['multiple']['invalid_color']],
    #         )

    # def test_non_rolling_stock_allows_all_colors(self):
    #     params = {
    #         'rolling_stock_or_not': NON_ROLLING_STOCK,
    #         'font_color': '#789456',
    #         'border_color': '#789456',
    #     }
    #     form = DecalSpecForm(data=params)
    #     form.is_valid()
    #     colored_fields = ['font_color', 'border_color']
    #     for colored_field in colored_fields:
    #         assert colored_field not in form.errors

    def test_border_thickness_is_ignored_if_no_border(self):
        params = {
            'rolling_stock_or_not': NON_ROLLING_STOCK,
            'placard_or_decal': 'Placard',
            'fleet_type': 'ACS-64',
            'border_type': 'None',
            'border_thickness': '5px',
            'required_substrate': 'Lexedge (Plastic)',
        }
        form = DecalSpecForm(data=params)
        assert form.is_valid()
        self.assertEqual(form.cleaned_data['border_thickness'], '')

    def test_border_thickness_is_not_ignored_if_border_passed_in(self):
        params = {
            'rolling_stock_or_not': NON_ROLLING_STOCK,
            'placard_or_decal': 'Placard',
            'fleet_type': 'ACS-64',
            'border_type': 'Single',
            'border_thickness': '5px',
            'required_substrate': 'Lexedge (Plastic)',
        }
        form = DecalSpecForm(data=params)
        assert form.is_valid()
        self.assertEqual(form.cleaned_data['border_thickness'], '5px')


class PDFTestCase(FormTestCase):
    def test_success(self):
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/pdf')
        self.assertEqual(r.content[:4], '%PDF')


class EmailTestCase(FormTestCase):
    action = 'finish'

    def test_success(self):
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 302)
        self.assertNotEqual(r['Content-Type'], 'application/pdf')
        self.assertNotEqual(r.content[:4], '%PDF')
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(len(message.attachments), 1)
