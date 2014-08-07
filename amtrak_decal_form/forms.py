from django import forms

from localflavor.us.forms import USPhoneNumberField

FORM_ERRORS = {
    'alternate_phone_number': {
        'duplicate': 'The alternate phone number must be different than the phone number',  # noqa
    }
}


class UserInfoForm(forms.Form):
    name = forms.CharField()
    department = forms.ChoiceField(
        choices=[
            (1, 'Foo'),
            (2, 'Bar'),
        ]
    )
    # TODO figure out what to do with these.
    # location = CharField()
    # address = CharField()
    phone_number = USPhoneNumberField()
    alternate_phone_number = USPhoneNumberField(required=False)
    cost_center = forms.CharField()
    wbs_element = forms.CharField()
    account = forms.CharField()

    def clean_alternate_phone_number(self):
        if 'phone_number' not in self.cleaned_data:
            return self.cleaned_data['alternate_phone_number']
        phone_number = self.cleaned_data['phone_number']
        alternate_phone_number = self.cleaned_data['alternate_phone_number']
        if phone_number == alternate_phone_number:
            raise forms.ValidationError(
                FORM_ERRORS['alternate_phone_number']['duplicate'],
            )
        return alternate_phone_number
