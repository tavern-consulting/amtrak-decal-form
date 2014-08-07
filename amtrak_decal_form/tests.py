from django.core.urlresolvers import reverse
from django.test import TestCase

from amtrak_decal_form.forms import UserInfoForm, FORM_ERRORS


class SmokeTestCase(TestCase):
    def test_GET_index_returns_200(self):
        url = reverse('index')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_100_percent_code_coverage(self):
        from amtrak_decal_form import wsgi
        assert wsgi


class FormTestCase(TestCase):
    url = reverse('index')

    @property
    def params(self):
        return {
            'name': 'name',
            'department': 1,
            'phone_number': '123-456-7890',
            'alternate_phone_number': '123-456-0987',
            'cost_center': 'cost_center',
            'wbs_element': 'wbs_element',
            'account': 'account',
        }

    def test_form_error_for_missing_fields(self):
        r = self.client.post(self.url, {})
        for key, field in UserInfoForm.base_fields.items():
            if field.required:
                self.assertFormError(r, 'form', key, 'This field is required.')
            else:
                with self.assertRaises(AssertionError):
                    self.assertFormError(
                        r,
                        'form',
                        key,
                        'This field is required.',
                    )

    def test_no_form_errors(self):
        r = self.client.post(self.url, self.params)
        for key, field in UserInfoForm.base_fields.items():
            with self.assertRaises(AssertionError):
                self.assertFormError(
                    r,
                    'form',
                    key,
                    'This field is required.',
                )

    def test_alternate_number_must_be_different(self):
        params = self.params
        params['alternate_phone_number'] = params['phone_number']
        r = self.client.post(self.url, params)
        self.assertFormError(
            r,
            'form',
            'alternate_phone_number',
            FORM_ERRORS['alternate_phone_number']['duplicate'],
        )
