from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login,logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# Create your views here.


def signupfunc(request):
    if request.method =='POST':
        print('this is POST')
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username,'' , password)
            return redirect('login')

        except IntegrityError:
            return render(request,'signup.html',{'error':'このユーザーネームは既に使用されています'})

    else :
        print('this is not POST')
    return render(request,'signup.html',{})

def loginfunc(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')

        else:
            return render(request,'login.html',{'context':'not logged in'})
    
    return render(request,'login.html',{'context':'get method'})
@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request,'list.html',{'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')
@login_required
def detailfunc(request,pk):
    object = get_object_or_404(BoardModel,pk=pk)
    return render(request,'detail.html',{'object':object})
def goodfunc(request,pk):
    object = BoardModel.objects.get(pk=pk)
    object.good +=1
    object.save()
    return redirect('list')
def readfunc(request,pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        print('pass')
        return redirect('list')
    else:
        object.read += 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        print('pass2')
        return redirect('list')
class CreateClass(CreateView):
    template_name='create.html'
    model = BoardModel
    fields = ('title','content','author','snsimage')
    success_url = reverse_lazy('list')