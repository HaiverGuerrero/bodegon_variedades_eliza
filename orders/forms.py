from django import forms 
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']

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
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        #04247333117
        if len(phone) < 10:
            raise forms.ValidationError("El número de teléfono es demasiado corto.")
        return phone
    
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