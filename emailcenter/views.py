from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.utils import timezone
from .forms import *
from .models import *
from school.models import *



# Create your views here.

def email_home(request):
	return render(request, 'emailcenter/email_home.html',{})


def email_page1(request):
	st=Schoolteainfo.objects.all()
	form = EmailForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.save(commit=False)
			email.email_sendtime = timezone.now()

			email.save()
			mail=EmailMessage(subject=email.email_title, body=email.email_content.replace("\n","<br>"), to=str(email.email_receiver).split(","), bcc=[])
			mail.content_subtype='html'
			for file in request.FILES.getlist('file[]'):

				if file:
					e_file = EmailFiles()
					e_file.emailkey = email
					e_file.email_file = file
					mail.attach(file.name,file.read(), file.content_type)
					e_file.save()
					print('fileattached')
			mail.send()
	context={'schtea':st,'form':form}
	return render(request, 'emailcenter/emailcenter_1.html',context)

def email_page2(request):
	st=Schoolteainfo.objects.all()
	form = EmailForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.save(commit=False)
			email.email_sendtime = timezone.now()
			
			email.save()
			mail=EmailMessage(subject=email.email_title, body=email.email_content.replace("\n","<br>"), to=str(email.email_receiver).split(","), bcc=[])
			mail.content_subtype='html'
			for file in request.FILES.getlist('file[]'):

				if file:
					e_file = EmailFiles()
					e_file.emailkey = email
					e_file.email_file = file
					mail.attach(file.name,file.read(), file.content_type)
					e_file.save()
					print('fileattached')
			mail.send()
	context={'schtea':st,'form':form}
	return render(request, 'emailcenter/emailcenter_2.html',context)

def email_page3(request):
	st=Schoolteainfo.objects.all()
	form = EmailForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.save(commit=False)
			email.email_sendtime = timezone.now()
			
			email.save()
			mail=EmailMessage(subject=email.email_title, body=email.email_content.replace("\n","<br>"), to=str(email.email_receiver).split(","), bcc=[])
			mail.content_subtype='html'
			for file in request.FILES.getlist('file[]'):

				if file:
					e_file = EmailFiles()
					e_file.emailkey = email
					e_file.email_file = file
					mail.attach(file.name,file.read(), file.content_type)
					e_file.save()
					print('fileattached')
			mail.send()
	context={'schtea':st,'form':form}
	return render(request, 'emailcenter/emailcenter_3.html',context)

def email_page4(request):
	st=Schoolteainfo.objects.all()
	form = EmailForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			email = form.save(commit=False)
			email.email_sendtime = timezone.now()
			
			email.save()
			mail=EmailMessage(subject=email.email_title, body=email.email_content.replace("\n","<br>"), to=str(email.email_receiver).split(","), bcc=[])
			mail.content_subtype='html'
			for file in request.FILES.getlist('file[]'):

				if file:
					e_file = EmailFiles()
					e_file.emailkey = email
					e_file.email_file = file
					mail.attach(file.name,file.read(), file.content_type)
					e_file.save()
					print('fileattached')
			mail.send()
	context={'schtea':st,'form':form}
	return render(request, 'emailcenter/emailcenter_4.html',context)