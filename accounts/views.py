from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import logout,login
from django.shortcuts import render,redirect
# Create your views here.
def login_view(request):
    form = AuthenticationForm(request,data = request.POST or None)
    if form.is_valid():
        user_=form.get_user()
        login(request,user_)
        return redirect('/')
    return render(request,'accounts/login.html',locals())

def logout_view(request,*args,**kwargs):
    if request.method == 'POST':
        logout(request)
        return redirect('/login')
    
    return render(request,'accounts/logout.html',locals())

def registration_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get('password1'))
        return redirect('/')
    return render(request,'accounts/register.html',locals())
        
