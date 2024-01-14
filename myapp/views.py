from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Post
from django.http import JsonResponse
from django.conf import settings
import os

# Create your views here.
@login_required(login_url="/login") #required auth user.
def home(request):
    
    posts = Post.objects.all()[:3] #Bring only 3 posts for home.
    total_posts = Post.objects.count()#Consulting qtd of all post in db.

    if request.method == "POST":
        post_id = request.POST.get("post-id")#Getting post Id.
        post = Post.objects.filter(id=post_id).first() #Picking full Post in db. 
        if post:
            if not post.image:
                img = False
            else:
                
                imgpath = settings.BASE_DIR+post.image.url#Picking img path in file db.
                img = True #Boolean control.

            if post and post.author == request.user:
                post.delete() #Delete a post if user is authenticated.
                if img:
                    try:
                        os.remove(imgpath) #Remove img from file db.
                    except FileNotFoundError:
                        pass
            

    return render(request,'myapp/home.html',{"posts":posts, 'total_obj': total_posts})


#Load more data.
def load_more(request):

    offset = request.GET.get('offset') #Picking current Qtd of Post in home scream.
    offset_int = int(offset) # Transforming str in Int type.
    limit = 2 # set a new limit in home scream post.
    post_obj = list(Post.objects.select_related('author').values('id','title','description','created_at','image','author__username')[offset_int:offset_int+limit]) #Bring more (limit) Post for home.
    data = {
        'posts': post_obj
    } #Send data in Json Response.
    return JsonResponse(data=data)

#Create a Post when is login.
@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES) #Salve and post data and a File.
        if form.is_valid():
            post = form.save(commit=False) #Waiting for save in db.
            post.author = request.user #Bring User id for Post Pk.
            post.save() #Salve in Db.
            return redirect("/home") #Return to home index scream.
    else:
        form = PostForm() #Rendering a Post form.
    
    return render(request, 'myapp/create_post.html', {"form":form})

#Sign-up form auth.
def sign_up(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form=RegisterForm()

    return render(request,'registration/sign_up.html',{"form": form})


