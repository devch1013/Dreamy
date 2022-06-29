from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.utils import timezone
from .forms import *
from classd.models import *
from teacher.models import *
from school.models import *
from users.models import Messenger


def error_404(request,exception):
	data = {}
	return render(request,'404.html', status=404)

def error_500(request):
	data = {}
	return render(request,'500.html', status=500)

def home_page(request):
	if request.user.user_position=="강사":
		return HttpResponseRedirect("/teacherout/")

	class_obj = Classinfo.objects.all().filter(class_date=timezone.now())
	tea_obj = Teacherinfo.objects.all().filter(tea_next_visit=timezone.now())
	if Messenger.objects.last():
		memo = Messenger.objects.last()
	else:
		memo = Messenger()
		memo.save()

	if request.method == 'POST':
		if request.POST.get("save_memo") == "todo":
			memo.todo_memo = request.POST.get('todo_memo')
			memo.todo_memo_time = timezone.now()
			memo.todo_memo_user = request.user.user_name
			memo.save()
		elif request.POST.get("save_memo") == "order":
			memo.order_memo = request.POST.get('order_memo')
			memo.order_memo_time = timezone.now()
			memo.order_memo_user = request.user.user_name
			memo.save()


	context = {"title": "select button", 'class_obj':class_obj, 'tea_obj':tea_obj,'memo':memo}
	return render(request, "home_1.html", context)

def logo_page(request):
	context = {"title": "Welcome to Ondream"}
	return render(request, "welcome.html", context)

def clear_page(request):
	context = {"title": "Welcome to Ondream"}
	return render(request, "clear.html", context)

