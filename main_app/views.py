from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

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

def finches_index(request):
  finches = Finch.objects.all()
  return render(request, 'finches/index.html', { 'finches': finches })

def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)

  ## toys
  #get list of ids of toys finch owns
  id_list = finch.toys.all().values_list('id')
  toys_finch_doesnt_have = Toy.objects.exclude(id__in=id_list)

  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', { 'finch': finch, 'feeding_form' : feeding_form, 'toys': toys_finch_doesnt_have })

class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'

class FinchUpdate(UpdateView):
  model = Finch
  
  fields = ['color', 'description', 'age']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches'

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

def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)

# toylist
class ToyList(ListView):
  model = Toy
  template_name = 'toys/index.html'


# toydetail

class ToyDetail(DetailView):
  model = Toy
  template_name = 'toys/detail.html'

# toycreate

class ToyCreate(CreateView):
  model = Toy
  fields = ['name', 'color']

  # define inherited method is_valid does
  def form_valid(self, form):
    return super().form_valid(form)
  
# toyupdate

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

# toydelete
class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'



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


