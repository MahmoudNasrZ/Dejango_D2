from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from myapp.models import School,Classes

def home(request):
    """Render the Home Page"""
    return render(request, 'home.html')

def AddSchoolView(request):  # Renamed for clarity
    """Render the Add School Page"""
    return render(request, 'schoolAdd.html')
def AddClassView(request):  # Renamed for clarity
    schools = School.objects.all()
    return render(request, 'classesAdd.html',{"schools":schools})



# def csrf_obtain(request):
#     """Return CSRF Token in JSON format"""
#     csrf_token = get_token(request)
#     return JsonResponse({"csrf_token": csrf_token})
