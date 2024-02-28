from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Enter just letters.')

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        validate_password(password)  # Validación de seguridad de la contraseña
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido solo debe contener letras.")
        return last_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        #04247333117
        if len(phone_number) < 10:
            raise forms.ValidationError("El número de teléfono es demasiado corto.")
        return phone_number

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido solo debe contener letras.")
        return last_name
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        #04247333117
        if len(phone_number) < 10:
            raise forms.ValidationError("El número de teléfono es demasiado corto.")
        return phone_number

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid':{"Image files only"}}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_address_line_1(self):
        address_line_1 = self.cleaned_data.get('address_line_1')
        if len(address_line_1) > 99:
            raise forms.ValidationError("La dirección 1 es demasiado larga")
        return address_line_1
    
    def clean_address_line_2(self):
        address_line_2 = self.cleaned_data.get('address_line_2')
        if len(address_line_2) > 99:
            raise forms.ValidationError("La dirección 2 es demasiado larga")
        return address_line_2
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if len(city) > 20:
            raise forms.ValidationError("La ciudad es demasiado larga")
        return city
    
    def clean_state(self):
        state = self.cleaned_data.get('state')
        if len(state) > 20:
            raise forms.ValidationError("El estado es demasiado larga")
        return state
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if len(country) > 20:
            raise forms.ValidationError("El país es demasiado larga")
        return country