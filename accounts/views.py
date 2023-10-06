from django.shortcuts import render, redirect

from .forms import FormularioRegistro, UserForm, ClienteForm
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView


# Create your views here.

def registrar(request):
    
    if request.method == 'POST':
        form = FormularioRegistro(data=request.POST)

        if request.POST['password1'] == request.POST['password2']:

            if form.is_valid():

                form.save()

                user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'] )

                login (request, user)
                return redirect('home')

            else:
                return render (request, 'accounts/registracion.html', {'form':form})
                
        else:
            return render (request, 'accounts/registracion.html', {'form':form})

        
    form = FormularioRegistro
    return render (request, 'accounts/registracion.html', {'form':form})


# PAGINA DE PERFIL
class PerfilView(TemplateView):
    template_name = 'accounts/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UserForm(instance=user)
        context['cliente_form'] = ClienteForm(instance=user.cliente)

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        cliente_form = ClienteForm(request.POST, request.FILES, instance=user.cliente)


        if  cliente_form.is_valid():    # user_form.is_valid() and   Esta parte se saca ya que el formulario User no se puede modificar
            #user_form.save()  # se comenta el grabado de este formulario ya que no se puede modificar
            cliente_form.save()
            # Redireccionar a la pagina de perfil (con datos actualizados)
            return redirect('perfil')

        # Si alguno de los datos no es valido
        context = self.get_context_data()
        context['user_form'] = user_form
        context['cliente_form'] = cliente_form
        return render(request, 'accounts/perfil.html', context)

