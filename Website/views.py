from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def about_us(request):
    return render(request,"about_us.html")


def material_handling(request):
    return render(request,"material-handling.html")

def contact_us(request):
    return render(request,"contact.html")