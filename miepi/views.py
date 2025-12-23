from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# vista del login
def login_view(request):
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('miepi:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('miepi:dashboard')  # Cambié esto de index a dashboard
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'miepi/login.html')


@login_required(login_url='miepi:login')
def dashboard(request):  # Cambié el nombre de index a dashboard
    return render(request, 'miepi/dashboard.html')