from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.utils import timezone
from .models import *
from .forms import *


# Create your views here.

@login_required
def material_table(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   mat_qs = Materialinfo.objects.all()


   context = {'title':'material information','mat_obj': mat_qs}
   return render(request, 'material/matool.html', context)

@login_required
def material_create_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   form = MaterialForm(request.POST or None)
   if form.is_valid():

      obj = form.save(commit=False)

      obj.make_id()
      obj.save()
      form = MaterialForm()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   template_name = 'material/material_add.html'
   context = {'form': form}
   return render(request, template_name, context)

@login_required
def material_update_view(request, mat_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Materialinfo, mat_id=mat_id)
   form = MaterialForm(request.POST or None, instance=obj)
   if form.is_valid():
      form.save()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   template_name = 'material/mat_update.html'
   context = {'form': form,  "mat_obj":obj}
   return render(request, template_name, context)

@login_required
def material_delete_view(request,mat_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Materialinfo, mat_id=mat_id)
   template_name = 'material/mat_delete.html'
   if request.method == "POST":
      obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   context = {"object": obj}
   return render(request, template_name, context)

@login_required
def material_reset_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   mat_obj = Materialinfo.objects.all()
   count =0
   for i in reversed(mat_obj):
      if len(Materialinfo.objects.all().filter(mat_name=i.mat_name))>1:
         print(len(Materialinfo.objects.all().filter(mat_name=i.mat_name)))
         i.delete()
         continue
      
      i.mat_id = "M"+ "%06d"%count
      i.save()
      count +=1
   return HttpResponseRedirect("/")