from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewUser
from django.contrib.auth.models import User
# Create your views here.

def loginForm(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Username or Password is Incorrect')

    return render(request,'accounts/loginForm.html')


def registerForm(request):
    if request.user.is_authenticated:
        return redirect('/')

    frm = NewUser()
    if request.method == 'POST':
        frm = NewUser(request.POST)
        if frm.is_valid():
            frm.save(commit = True)
            # print('success')        
            return redirect('loginForm')

    context = {'form':frm}
    return render(request,'accounts/registerForm.html',context)

@login_required(login_url='/accounts/loginForm/')
def logoutUser(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/accounts/loginForm/')
def changePasswordForm(request):
    return render(request,'accounts/changePasswordForm.html')

@login_required(login_url='/accounts/loginForm/')
def changePassword(request):
    if request.method == 'POST':
        # user = User.objects.get(username=request.user.username)
        user = authenticate(request, username=request.POST['username'], password=request.POST['old-password'])

        if user is not None:
            user.set_password(request.POST['new-password'])
            user.save()
            update_session_auth_hash(request, user)
            # messages.success(request, 'Password successfully updated!')
            return redirect('/',username=user.username)
        messages.error(request,'User authenticatio failed')
        return render(request,'accounts/changePasswordForm.html')
    return render(request,'accounts/loginForm.html')

