from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from accounts.models import Cliente


class FormularioRegistro(UserCreationForm):

        email = forms.EmailField(required=True)

        class Meta:
             model = User
             fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]
        
        def clean_email(self):
               email = self.cleaned_data['email']

               if User.objects.filter(email=email).exists():
                      raise forms.ValidationError('Este correo electrónico ya está registrado!!')
               return email



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [ 'imagen', 'direccion_calle', 'direccion_otros', 'localidad', 'departamento', 'codigo_postal', 'telefono', 'direccion_alternativa', 'notas' ]
