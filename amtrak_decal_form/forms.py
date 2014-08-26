from django import forms

from localflavor.us.forms import (
    USPhoneNumberField,
    USZipCodeField,
    USStateSelect,
)

FORM_ERRORS = {
    'alternate_phone_number': {
        'duplicate': 'The alternate phone number must be different than the phone number',  # noqa
    },
    'multiple': {
        # TODO inform the user what colors are valid.
        'invalid_color': 'The color you have chosen is not valid',
    },
}


VALID_COLORS = (
    '#000000',  # Black
    '#000080',  # Navy Blue
    '#005983',  # Amtrak Blue
    '#BD2031',  # Cardinal Red
    '#FFFF00',  # Yellow
    '#FFFFFF',  # White

    '#CLRREC',  # Clear Receptive
    '#REFFFF',  # Reflective White
)
VALID_FONTS = (
    'Frutiger 55',
    'Frutiger Bold 55',
    'Frutiger Italic 55',
    'Helvetica',
    'Helvetica Bold',
    'Helvetica Italic',
)


VALID_DEPARTMENTS = (
    'Administrative Support',
    'Communications',
    'Customer Service',
    'Engineering',
    'Finance',
    'Government Affairs',
    'Human Capital',
    'Information Technology',
    'Legal',
    'Marketing',
    'Mechanical',
    'Research & Strategy',
    'Safety & Security',
    'Supply Chain & Logistics',
    'Transportation',
)


ROLLING_STOCK = '1'
NON_ROLLING_STOCK = '2'


class UserInfoForm(forms.Form):
    name = forms.CharField()
    department = forms.ChoiceField(
        choices=[
            (1, 'Foo'),
            (2, 'Bar'),
        ]
    )
    location = forms.CharField()

    line1 = forms.CharField(label='Street', required=True, max_length=50)
    line2 = forms.CharField(
        label='Second Street Address',
        required=False,
        max_length=50,
    )
    city = forms.CharField(label='City', max_length=50)
    state = forms.CharField(
        label='State',
        widget=USStateSelect,
        max_length=50,
    )
    zip_code = USZipCodeField(label='Zip Code')

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


class DecalSpecForm(forms.Form):
    rolling_stock_or_not = forms.ChoiceField(
        choices=[
            (ROLLING_STOCK, 'Rolling Stock'),
            (NON_ROLLING_STOCK, 'Non-Rolling Stock'),
        ],
        widget=forms.RadioSelect(),
    )

    placard_or_decal = forms.ChoiceField(
        choices=[
            (1, 'Placard'),
            (2, 'Decal'),
        ],
        widget=forms.RadioSelect(),
    )
    fleet_type = forms.ChoiceField(
        choices=[
            (1, 'Fleet'),
            (2, 'Type'),
        ]
    )
    font_color = forms.CharField(max_length=7)
    border_color = forms.CharField(max_length=7)
    description = forms.CharField(widget=forms.Textarea)
    font_face = forms.ChoiceField(
        choices=[
            (1, 'Times New Roman'),
            (2, 'Arial'),
        ],
    )
    font_size = forms.CharField(max_length=3)
    html = forms.CharField(widget=forms.Textarea)
    border_type = forms.ChoiceField(
        choices=[
            (1, 'N/A'),
            (2, 'Single'),
            (3, 'Dounle'),
        ],
    )
    border_thickness = forms.CharField()
    required_substrate = forms.ChoiceField(
        choices=[
            (1, 'Vinyl'),
            (2, 'Lexedge (plastic)'),
            (3, 'Luminescent'),
        ],
    )

    def clean_font_color(self):
        font_color = self.cleaned_data['font_color']
        if self.cleaned_data.get('rolling_stock_or_not') == NON_ROLLING_STOCK:
            return font_color
        if font_color not in VALID_COLORS:
            raise forms.ValidationError(
                FORM_ERRORS['multiple']['invalid_color'],
            )
        return font_color

    def clean_border_color(self):
        border_color = self.cleaned_data['border_color']
        if self.cleaned_data.get('rolling_stock_or_not') == NON_ROLLING_STOCK:
            return border_color
        if border_color not in VALID_COLORS:
            raise forms.ValidationError(
                FORM_ERRORS['multiple']['invalid_color'],
            )
        return border_color
