from django.urls import path
from .viewsets import SchoolViewSet,ClassesViewSet  # Import your view
from .views import home, AddSchoolView,AddClassView  # Import home & AddSchoolView

urlpatterns = [
    path("home/", home, name="home"),  # Home Page
    # School Endpoints
    path("school/list/", SchoolViewSet.as_view(), name="school_list"),  # GET: List Schools
    path("schools/add/", AddSchoolView, name="add_school_page"),  # Page to show the form
    path("school/add/", SchoolViewSet.as_view(), name="add_school"),  # POST: Add School
    path("schools/", SchoolViewSet.as_view(), name="school_list"),
    path("schools/<int:school_id>/", SchoolViewSet.as_view(), name="school_detail"),
    # Classes Endpoints
    path("classes/list/", ClassesViewSet.as_view(), name="class_list"),  # GET: List Classes
    path("classes/add/", AddClassView, name="add_class_page"),  # Page to show the form
    path("class/add/", ClassesViewSet.as_view(), name="add_class"),  # POST: Add Class
    path("classes/", ClassesViewSet.as_view(), name="class_list"),
    path("classes/<int:class_id>/", ClassesViewSet.as_view(), name="class_detail"),
]
