from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
import math, datetime

from .models import *
from .forms import *




# Create your views here.

def home(request):
	try:
		workers = Worker.objects.all()
		totalworkercount = workers.count()
		presentworkers = workers.filter(presence = 'Present').count()
		values = [Task.objects.aggregate(Sum('production_count')), Task.objects.aggregate(Sum('target_count')), Task.objects.aggregate(Sum('qc_passed'))]
		if(values[0]['production_count__sum'] == 0):
			percent = 0
		else:
			percent = math.ceil((values[2]['qc_passed__sum']/values[0]['production_count__sum']) * 100)
		content = {'totalworkercount': totalworkercount, 'presentworkers': presentworkers, 'production': values[0]['production_count__sum'], 'target': values[1]['target_count__sum'], 'qcpassed': values[2]['qc_passed__sum'], 'percent': percent}
	except:
		return redirect('production')
	return render(request, 'TVSapp/home.html', content)

def quality(request):
	try:
		taskall = Task.objects.all()
		task = taskall.exclude(allotted_duration = 0)
		values = [task.aggregate(Sum('allotted_duration')), task.aggregate(Sum('duration')),
		task.aggregate(Sum('production_count')), task.aggregate(Sum('target_count')),
		task.aggregate(Sum('qc_passed'))]
		availability = math.ceil((values[0]['allotted_duration__sum']/values[1]['duration__sum']) * 100)
		cycle_time = (values[0]['allotted_duration__sum']/values[3]['target_count__sum'])
		performance = math.ceil(((cycle_time * values[2]['production_count__sum'])/values[1]['duration__sum']) * 100)
		quality = math.ceil((values[4]['qc_passed__sum']/values[2]['production_count__sum']) * 100)
		oee = math.ceil(((availability/100) * (performance/100) * (quality/100)) * 100)
		content = {'availability': availability, 'performance': performance, 'quality': quality, 'oee': oee}
	except:
		return redirect('production')
	return render(request, 'TVSapp/quality.html', content)


#WORKER

def workers(request):
	workers = Worker.objects.all()
	content = {'workers': workers}
	return render(request, 'TVSapp/worker.html', content)

def worker_individual(request, pk_test):
	workers = Worker.objects.get(empid = pk_test)
	task = workers.task_set.all()
	values = [task.aggregate(Sum('production_count')), task.aggregate(Sum('target_count')), task.aggregate(Sum('qc_passed'))]
	content = {'workers': workers, 'task': task, 'production': values[0]['production_count__sum'], 'target': values[1]['target_count__sum'], 'qcpassed': values[2]['qc_passed__sum']}
	return render(request, 'TVSapp/worker_individual.html', content)

def add_worker(request):
	form = WorkerForm
	if (request.method == 'POST'):
		form = WorkerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('workers')

	content = {'form': form}
	return render(request, 'TVSapp/add_worker.html', content)

def change_presence(request, pk_test):
	workers = Worker.objects.get(empid = pk_test)
	form = PresenceForm(instance = workers)
	content = {'workers': workers, 'form': form}
	if (request.method == 'POST'):
		form = PresenceForm(request.POST, instance = workers)
		if form.is_valid():
			form.save()
			return redirect('workers')
	return render(request, 'TVSapp/change_presence.html', content)

def worker_absent(request):
	return render(request, 'TVSapp/worker_absent.html')




#PRODUCTION

def production(request):
	machines = Machine.objects.all()
	content = {'machines': machines}
	return render(request, 'TVSapp/production.html', content)

def product_individual(request, pk_test):
	machines = Machine.objects.get(id = pk_test)
	product = machines.task_set.all()
	values = [product.aggregate(Sum('production_count')), product.aggregate(Sum('target_count')), product.aggregate(Sum('qc_passed'))]
	content = {'machines': machines, 'product': product, 'production': values[0]['production_count__sum'], 'target': values[1]['target_count__sum'], 'qcpassed': values[2]['qc_passed__sum']}
	return render(request, 'TVSapp/product_individual.html', content)

def change_status(request, pk_test):
	machines = Machine.objects.get(id = pk_test)
	form = MachineForm(instance = machines)
	content = {'machines': machines, 'form': form}
	if (request.method == 'POST'):
		form = MachineForm(request.POST, instance = machines)
		if form.is_valid():
			form.save()
			return redirect('production')
	return render(request, 'TVSapp/change_status.html', content)

def add_task(request):
	form = TaskForm
	if (request.method == 'POST'):
		form = TaskForm(request.POST)
		if form.is_valid():
			worker = form.cleaned_data['worker']
			if(worker.presence == 'Present' ):
				form.save()
				return redirect('production')
			else:
				return redirect('worker_absent')

	content = {'form': form}
	return render(request, 'TVSapp/add_task.html', content)




#HUMAN MACHINE INTERFACE

def login(request):
    if request.method == 'POST':
        eid = request.POST.get('empid')
        password = request.POST.get('password')
        try: 
	        if(eid == password):
	        	worker = Worker.objects.get(empid = eid)
        	if worker is not None:
        		totaltask = worker.task_set.all()
        		task = totaltask.filter(production_count = 0, machine = 1)
        		task.update(start_time = datetime.datetime.now())
        		return redirect(reverse('HMImachine1', kwargs = {"pk_test": eid}))
        except ObjectDoesNotExist :
        	return redirect('HMI_exception')
        except UnboundLocalError :
        	return redirect('HMI_exception')
    return render(request, 'TVSapp/HMI_login.html')

def HMImachine1(request, pk_test):
	worker = Worker.objects.get(empid = pk_test)
	totaltask = worker.task_set.all()
	task = totaltask.filter(production_count = 0, machine = 1)
	if not task:
		return  redirect('HMI_notauth')
	start_time = task[0].start_time.replace(tzinfo = None)
	form = ProductionForm(instance = task[0])
	content = {'form': form, 'task': task[0], 'start_time': start_time}
	if task:
		if (request.method == 'POST'):
			form = ProductionForm(request.POST, instance = task[0])
			if form.is_valid():
				end_time = datetime.datetime.now()
				end_time = end_time.replace(tzinfo = None)
				diff = end_time - start_time
				worktime = diff.total_seconds()
				sec = int(worktime)
				total_time = sec + task[0].duration
				form.save()
				task[0].duration = total_time
				task[0].save(update_fields = ['duration'])
				return redirect('login')

	return render(request, 'TVSapp/HMI_production.html', content)

def HMI_notauth(request):
	return render(request, 'TVSapp/HMI_notauth.html')

def HMI_exception(request):
	return render(request, 'TVSapp/HMI_exception.html')




#DISPLAY SCREEN

def displaypage(request):
	machines = Machine.objects.all()
	labels = []
	production = []
	target = []
	qcpassed = []
	for i in machines:
		labels.append(i.machinename)
		product = i.task_set.all()
		values = [product.aggregate(Sum('production_count')), product.aggregate(Sum('target_count')), product.aggregate(Sum('qc_passed'))]
		production.append(values[0]['production_count__sum'])
		target.append(values[1]['target_count__sum'])
		qcpassed.append(values[2]['qc_passed__sum'])

	worker = Worker.objects.all()
	workerlabels = []
	workerproduction = []
	workertarget = []
	workerqcpassed = []
	for i in worker:
		workerlabels.append(i.name)
		product = i.task_set.all()
		values = [product.aggregate(Sum('production_count')), product.aggregate(Sum('target_count')), product.aggregate(Sum('qc_passed'))]
		workerproduction.append(values[0]['production_count__sum'])
		workertarget.append(values[1]['target_count__sum'])
		workerqcpassed.append(values[2]['qc_passed__sum'])

	content ={
		'labels': labels,
		'production': production,
		'target': target,
		'qcpassed': qcpassed,

		'workerlabels': workerlabels,
		'workerproduction': workerproduction,
		'workertarget': workertarget,
		'workerqcpassed': workerqcpassed,
	}
	return render(request, 'TVSapp/displaypage.html', content)