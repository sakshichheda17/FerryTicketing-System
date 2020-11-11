from django.shortcuts import render,redirect
from run.models import Run
from run.forms import RunForm
from vessel.models import Vessel
from django.contrib import messages
# Create your views here.

def get_run(request):
    runs = Run.objects.all()
    context = {
        'runs' : runs
    }
    # print(context)
    return render(request, 'runs.html',context)

def add_run(request):
    # context = {}
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid:
            try:
                form.save()
                return redirect('/runs')
            except:
                print(form.errors)
                pass

    else:
        form = RunForm()
    context = {
        'form': form
    }
    return render(request, 'addrun.html', context)

def edit_run(request, id):
    run = Run.objects.get(id=id)
    vessels=Vessel.objects.all()
    print(request.POST)
    form = RunForm(request.POST, instance = run) 
    if request.method == "POST": 
        if form.is_valid():  
            form.save()  
            return redirect("/runs") 
        else:
            print(form.errors)
    
    # return render(request,"edit_leg.html",{'leg':leg, 'vessels': vessels}) 
    # print(form.errors)
    return render(request, 'editrun.html', {'run': run, 'vessels': vessels})

# def update_run(request, id):
#     run = Run.objects.get(id=id)
#     print(request.POST)
#     form = RunForm(request.POST, instance=run)
#     if form.is_valid:
#         try:
#             form.save()
#             return redirect('/runs')
#         except:
#             print(form.errors)
            
#     return render(request,'editrun.html',{'run': run})

def delete_run(request,id):
    run = Run.objects.get(id=id)
    run.delete()
    messages.success(request, f'The run having id {id} was deleted successfully.')
    return redirect('/runs')
