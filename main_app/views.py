from django.shortcuts import render
from .models import Finch

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
  return render(request, 'finches/detail.html', { 'finch': finch })



