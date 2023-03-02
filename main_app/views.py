from django.shortcuts import render



# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')


# Create your views here.

# about route
def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')
