from django.forms import ModelForm
from django import forms
from .models import *

class WorkerForm(ModelForm):
	class Meta:
		model = Worker
		fields = ['name', 'empid', 'contact', 'presence']
		labels = {
			'name': 'Name',
			'empid': 'Employee ID',
			'contact': 'Contact Number',
			'presence': 'Presence',
		}

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['jobid','worker', 'machine', 'target_count', 'allotted_duration']
		labels = {
			'jobid': 'Job ID',
			'worker': 'Worker',
			'machine': 'Machine',
			'target_count': 'Target', 
			'allotted_duration': 'Allotted Time (in mins)',
		}

class MachineForm(ModelForm):
	class Meta:
		model = Machine
		fields = ['status']
		labels = {
			'status': 'Status' 
		}

class ProductionForm(ModelForm):
	class Meta:
		model = Task
		fields = ['production_count', 'qc_passed']
		labels = {
			'production_count': 'Quantities Produced',
			'qc_passed': 'QC passed',
		}

class PresenceForm(ModelForm):
	class Meta:
		model = Worker
		fields = ['presence']
		labels = {
			'presence': 'Presence',
		}