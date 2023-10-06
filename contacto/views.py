from django.shortcuts import render, redirect
from django.urls import reverse

from django.core.mail import EmailMessage
from .forms import ContactForm

# Create your views here.

def contacto(request):
    
    #print('Tipo de petición: {} '.format(request.method) )
    
    contact_form = ContactForm()
    
    if request.method == 'POST':
        # Estoy enviando el formulario
        contact_form = ContactForm(data=request.POST)

        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            message = request.POST.get('message', '')
            
            # Enviar el correo electrónico
            email = EmailMessage(
                'Mensaje de contacto recibido desde CAMOMILA',
                'Mensaje enviado por {} <{}>:\n\n{}'.format(name,email,message),
                email,
                ['c4rl0s.l4z4r0@gmail.com'],
                reply_to=[email],
            )
            
            try:
                email.send()
                # Está todo OK
                return redirect(reverse('contacto')+'?ok')
            except:
                # Ha habido un error y retorno a ERROR
                return redirect(reverse('contacto')+'?error')
                
    return render(request, 'contacto/contacto.html',{'form':contact_form})