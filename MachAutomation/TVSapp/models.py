from django.db import models
from django.core.validators import RegexValidator
import datetime

# Create your models here.

class Worker(models.Model):
	PRESENCE = (
		('Present', 'Present'),
		('Absent', 'Absent'),
		)
	name = models.CharField(max_length = 100, null = True)
	empid = models.IntegerField(null = True)
	contact = models.CharField(max_length = 10, validators = [RegexValidator(r'^[1-9][0-9]{9}$')], null = True)
	presence = models.CharField(max_length = 100, null = True, choices = PRESENCE)

	def __str__(self):
		return self.name


class Machine(models.Model):
	MACHNAME = (
		('Switches', 'Switches'),
		('Solenoids', 'Solenoids'),
		('Electro Mechanical Assemblies', 'Electro Mechanical Assemblies'),
		('Computer Input Devices', 'Computer Input Devices'),
		('Sensors', 'Sensors'),
		)
	STATUS = (
		('Awaiting user', 'Awaiting user'),
		('Idle', 'Idle'),
		('Under use', 'Under use'),
		)
	machinename = models.CharField(max_length = 100, null = True, choices = MACHNAME)
	status = models.CharField(max_length = 20, null = True, choices = STATUS)

	def __str__(self):
		return self.machinename

class Task(models.Model):
	jobid = models.CharField(max_length = 10, null = True)
	worker = models.ForeignKey(Worker, null = True, on_delete=models.SET_NULL)
	machine = models.ForeignKey(Machine, null = True, on_delete=models.SET_NULL)
	production_count = models.IntegerField(default = 0)
	qc_passed = models.IntegerField(default = 0)
	target_count = models.IntegerField(null = True)
	duration = models.IntegerField(default = 0)
	allotted_duration = models.IntegerField(default = 0)
	start_time = models.DateTimeField(default = datetime.datetime.now())

	def __str__(self):
		return (self.jobid)
