from django.shortcuts import render,redirect
from run.models import Run
from run.forms import RunForm
from vessel.models import Vessel
# Create your views here.
def dashboard(request):
    return render(request,'admin_home.html',{})

def get_runs(request):
    runs = Run.objects.all()
    context = {
        'runs' : runs
    }
    print(context)
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
    print(run.vessel_name_id)
    return render(request, 'editrun.html', {'run': run, 'vessels': vessels})

def update_run(request, id):
    run = Run.objects.get(id=id)
    print(request.POST)
    form = RunForm(request.POST, instance=run)
    if form.is_valid:
        try:
            form.save()
            return redirect('/runs')
        except:
            print(form.errors)
            
    return render(request,'editrun.html',{'run': run})

def delete_run(request,id):
    run = Run.objects.get(id=id)
    run.delete()
    return redirect('/runs')