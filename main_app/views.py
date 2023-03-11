from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Finch, Toy, Photo
from .forms import FeedingForm

import uuid
import boto3
from django.conf import settings


AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')


# Create your views here.

# about route
def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

@login_required
def finches_index(request):
  finches = Finch.objects.filter(user=request.user)
  return render(request, 'finches/index.html', { 'finches': finches })

@login_required
def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)

  ## toys
  #get list of ids of toys finch owns
  id_list = finch.toys.all().values_list('id')
  toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)

  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', { 'finch': finch, 'feeding_form' : feeding_form, 'toys': toys_finch_doesnt_have })

class FinchCreate(LoginRequiredMixin, CreateView):
  model = Finch
  fields = ['name', 'color', 'description', 'age']
  
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView):
  model = Finch
  
  fields = ['color', 'description', 'age']

class FinchDelete(LoginRequiredMixin, DeleteView):
  model = Finch
  success_url = '/finches'

@login_required
def add_feeding(request, finch_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

@login_required
def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

@login_required
def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)

# toylist
class ToyList(LoginRequiredMixin, ListView):
  model = Toy
  template_name = 'toys/index.html'


# toydetail

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy
  template_name = 'toys/detail.html'

# toycreate

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = ['name', 'color']

  # define inherited method is_valid does
  def form_valid(self, form):
    return super().form_valid(form)
  
# toyupdate

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

# toydelete
class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'


@login_required
def add_photo(request, finch_id):
    # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      
      s3.upload_fileobj(photo_file, S3_BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"

      photo = Photo(url=url, finch_id=finch_id)
      photo.save()
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
      return redirect('detail', finch_id=finch_id)
  return redirect('detail', finch_id=finch_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)



