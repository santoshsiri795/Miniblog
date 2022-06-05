from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,postform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import post,Contact
from django.contrib.auth.models import Group

# home

def home(request):
    posts=post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

#about

def about(request):
    return render(request,'blog/about.html')

#contact
def contact(request):
    if request.method=='POST':
        
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        message = request.POST['message']
        panda = Contact(name = name,email = email,address = address,message = message)
        print(name,email,address,message)
        panda.save()

    return render(request,'blog/contact.html')  


#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts=post.objects.all()
        return render(request,'blog/dashboard.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/login/') 


#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
    


#signup
def user_signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! you become an author')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)

    else:        
     form =SignUpForm()
    return render(request,'blog/signup.html',{'form':form})


#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method== "POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully.')
                    return HttpResponseRedirect('/dashboard/')
        else:            
            form=LoginForm()
        return render(request,'blog/login.html', {'form':form})

    else:
        return HttpResponseRedirect('/dashboard/')           


#add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=postform(request.POST)
            if form.is_valid():
             messages.success(request,'Post Added')   

             title=form.cleaned_data['title']
             desc=form.cleaned_data['desc']
             pst=post(title=title,desc=desc)
             pst.save()
             form=postform()
        else:
            form=postform()     
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#update post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=post.objects.get(pk=id)
            form=postform(request.POST,instance=pi)
            if form.is_valid():
                messages.success(request,'Post Updated')
                form.save()
        else:
          pi=post.objects.get(pk=id)
          form=postform(instance=pi)            
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#delete post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
       return HttpResponseRedirect('/login/')

