 
from django.urls import path
from .views import  *
urlpatterns = [
    path('about-us', about_us, name="website_about_us"),
    path('material-handling', material_handling, name="material_handling"),
    path('contact', contact_us, name="contact_us"),

]
