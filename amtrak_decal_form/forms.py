from django import forms

from localflavor.us.forms import (
    USPhoneNumberField,
    USZipCodeField,
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
    ('Frutiger 55', 'Frutiger 55'),
    ('Frutiger Bold 55', 'Frutiger Bold 55'),
    ('Frutiger Italic 55', 'Frutiger Italic 55'),
    ('Helvetica', 'Helvetica'),
    ('Helvetica Bold', 'Helvetica Bold'),
    ('Helvetica Italic', 'Helvetica Italic'),
)


VALID_DEPARTMENTS = (
    ('Administrative Support', 'Administrative Support'),
    ('Communications', 'Communications'),
    ('Customer Service', 'Customer Service'),
    ('Engineering', 'Engineering'),
    ('Finance', 'Finance'),
    ('Government Affairs', 'Government Affairs'),
    ('Human Capital', 'Human Capital'),
    ('Information Technology', 'Information Technology'),
    ('Legal', 'Legal'),
    ('Marketing', 'Marketing'),
    ('Mechanical', 'Mechanical'),
    ('Research and Strategy', 'Research and Strategy'),
    ('Safety and Security', 'Safety and Security'),
    ('Supply Chain and Logistics', 'Supply Chain and Logistics'),
    ('Transportation', 'Transportation'),
)

VALID_FLEET_TYPES = (
    ('ACS-64', 'ACS-64'),
    ('AEM-7', 'AEM-7'),
    ('F59', 'F59'),
    ('HHP', 'HHP'),
    ('P32', 'P32'),
    ('P40', 'P40'),
    ('P42', 'P42'),

    ('Acela', 'Acela'),
    ('Amfleet I', 'Amfleet I'),
    ('Amfleet II', 'Amfleet II'),
    ('Auto Carrier', 'Auto Carrier'),
    ('California Car', 'California Car'),
    ('Comet', 'Comet'),
    ('Heritage', 'Heritage'),
    ('Horizon', 'Horizon'),
    ('NPCU', 'NPCU (specify in description)'),
    ('Superliner I', 'Superliner I'),
    ('Superliner II', 'Superliner II'),
    ('Surfliner', 'Surfliner'),
    ('Surfliner', 'Surfliner'),
    ('Viewliner II', 'Viewliner II'),
    ('Viewliner', 'Viewliner'),
)
VALID_SUBSTRATES = (
    ('Vinyl (Solid Color)', 'Vinyl (Solid Color)'),
    ('Vinyl (Reflective)', 'Vinyl (Reflective)'),
    ('Vinyl (Luminescent)', 'Vinyl (Luminescent)'),
    ('Lexedge (Plastic)', 'Lexedge (Plastic)'),
)


ROLLING_STOCK = '1'
NON_ROLLING_STOCK = '2'


class USStateSelect(forms.Select):
    """
    A Select widget that uses a list of U.S. states/territories as its choices.
    """
    def __init__(self, attrs=None):
        from localflavor.us.us_states import US_STATES
        choices = [
            (s, s) for s, _ in US_STATES
        ]
        super(USStateSelect, self).__init__(attrs, choices=choices)


class UserInfoForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput({
            'class': '',
        }),
    )
    department = forms.ChoiceField(choices=VALID_DEPARTMENTS)
    location = forms.CharField()

    line1 = forms.CharField(label='Street', required=True, max_length=50)
    line2 = forms.CharField(
        label='Street 2',
        required=False,
        max_length=50,
    )
    city = forms.CharField(label='City', max_length=50)
    state = forms.CharField(
        label='State',
        widget=USStateSelect({
            'class': 'input-mini',
        }),
        max_length=50,
    )
    zip_code = USZipCodeField(
        label='Zip Code',
        widget=forms.TextInput({
            'class': 'input-small',
        }),
    )
    phone_number = USPhoneNumberField(
        widget=forms.TextInput({
            'class': 'input-medium',
        }),
    )
    alternate_phone_number = USPhoneNumberField(
        required=False,
        widget=forms.TextInput({
            'class': 'input-medium',
        }),
    )
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
        label='Will this order be placed on rolling stock?',
        choices=[
            (ROLLING_STOCK, 'Yes'),
            (NON_ROLLING_STOCK, 'No'),
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
    fleet_type = forms.ChoiceField(choices=VALID_FLEET_TYPES)
    font_color = forms.CharField(max_length=7)
    border_color = forms.CharField(required=False, max_length=7)
    description = forms.CharField(
        required=False,
        widget=forms.Textarea({
            'rows': 6,
            'cols': 40,
        })
    )
    font_face = forms.ChoiceField(
        choices=VALID_FONTS,
        widget=forms.Select({
            'class': 'input-medium',
        }),
    )
    font_size = forms.ChoiceField(
        choices=[
            (8, 'Very Small'),
            (12, 'Small'),
            (16, 'Medium'),
            (24, 'Large'),
            (36, 'Very Large'),
        ],
    )
    html = forms.CharField(required=False, widget=forms.Textarea)
    border_type = forms.ChoiceField(
        choices=[
            ('None', 'None'),
            ('Single', 'Single'),
            ('Double', 'Double'),
        ],
        widget=forms.Select({
            'class': 'input-small',
        }),
    )
    border_thickness = forms.ChoiceField(
        choices=[
            (5, 'Very Thin'),
            (10, 'Thin'),
            (15, 'Medium'),
            (20, 'Thick'),
            (25, 'Very Thick'),
        ],
        widget=forms.Select({
            'class': 'input-medium',
        }),
    )
    required_substrate = forms.ChoiceField(
        choices=VALID_SUBSTRATES,
        widget=forms.Select({
            'class': 'input-large',
        }),
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

    def clean_border_thickness(self):
        border_thickness = self.cleaned_data['border_thickness']
        if self.cleaned_data.get('border_type') == 'None':
            return ''
        return border_thickness
