from datetime import datetime, timedelta

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
    ('#000000', 'Black'),
    ('#000080', 'Navy Blue'),
    ('#005983', 'Amtrak Blue'),
    ('#BD2031', 'Cardinal Red'),
    ('#FFFF00', 'Yellow'),
    ('#FFFFFF', 'White'),
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
    ('Solid Color', 'Solid Color'),
    ('Reflective', 'Reflective'),
    ('Luminescent', 'Luminescent'),
)


ROLLING_STOCK = 'Rolling Stock'
NON_ROLLING_STOCK = 'Non-Rolling Stock'


def get_default_date():
    date = datetime.now() + timedelta(days=5)
    return date.strftime('%m/%d/%Y')


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
    email = forms.EmailField()
    cost_center = forms.IntegerField()
    wbs_element = forms.IntegerField()
    account = forms.CharField()
    date = forms.CharField(
        label='Date Requested By',
        initial=get_default_date(),
        widget=forms.TextInput({
            'class': 'datepicker',
        }),
    )

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
        initial=ROLLING_STOCK,
        widget=forms.RadioSelect(),
    )

    placard_or_decal = forms.ChoiceField(
        choices=[
            ('Placard', 'Placard'),
            ('Decal', 'Decal'),
        ],
        initial='Placard',
        widget=forms.RadioSelect(),
    )
    fleet_type = forms.ChoiceField(choices=VALID_FLEET_TYPES)
    border_color = forms.ChoiceField(
        choices=VALID_COLORS,
        required=False,
        widget=forms.Select({
            'class': 'input-small',
        }),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea({
            'rows': 6,
            'cols': 40,
        })
    )
    height = forms.CharField(
        required=False,
        label='Height (inches)',
        widget=forms.TextInput({
            'class': 'input-mini',
            'placeholder': '0.000',
        }),
    )
    width = forms.CharField(
        required=False,
        label='Width (inches)',
        widget=forms.TextInput({
            'class': 'input-mini',
            'placeholder': '0.000',
        }),
    )
    html = forms.CharField(required=False, widget=forms.Textarea)
    clear_receptive = forms.BooleanField(required=False)
    reflective_white = forms.BooleanField(required=False)
    sample_graphic = forms.BooleanField(
        label='Please send me a sample graphic',
        required=False,
    )
    sample_decal = forms.BooleanField(
        label='Please send me a sample decal',
        required=False,
    )
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
            ('5px', 'Very Thin'),
            ('10px', 'Thin'),
            ('15px', 'Medium'),
            ('20px', 'Thick'),
            ('25px', 'Very Thick'),
        ],
        widget=forms.Select({
            'class': 'input-medium',
        }),
    )
    required_substrate = forms.ChoiceField(
        label='Vinyl Type',
        choices=VALID_SUBSTRATES,
        widget=forms.Select({
            'class': 'input-large',
        }),
    )

    def clean_border_thickness(self):
        border_thickness = self.cleaned_data['border_thickness']
        if self.cleaned_data.get('border_type') == 'None':
            return ''
        return border_thickness

    def clean_height(self):
        height = self.cleaned_data['height']
        if not height:
            return '8'
        return height

    def clean_width(self):
        width = self.cleaned_data['width']
        if not width:
            return '12'
        return width
