from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Finch, Toy
from .forms import FeedingForm


# finches = [
#   {'name': 'Timmy', 'color': 'yellow', 'description': 'pretty bird', 'age': 4},
#   {'name': 'Johnny', 'color': 'red', 'description': 'chunky bird', 'age': 6},
# ]

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
  feeding_form = FeedingForm()
  return render(request, 'finches/detail.html', { 'finch': finch, 'feeding_form' : feeding_form })

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
  success_url = '/toys'




