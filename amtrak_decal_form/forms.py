from django import forms

from localflavor.us.forms import USPhoneNumberField


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
