from django.shortcuts import render

# Create your views here.
def get_return_view(request):
    return render(request,'return.html',{})

def get_single_view(request):
    return render(request,'single.html',{})