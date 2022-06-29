from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect,HttpResponse
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import *
from material.models import *
from classd.models import *

@login_required
def classstat_table_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = Classstatinfo.objects.all()
   template_name = 'classstatd/cladbmain.html'
   context = {"obj":obj}
   return render(request, template_name, context)

@login_required
def classstat_create_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   form = ClassstatForm(request.POST or None, request.FILES or None)
   mat_obj = Materialinfo.objects.all()
   if form.is_valid():

      obj = form.save(commit=False)
      if Classstatinfo.objects.all().filter(class_title=obj.class_title):
         messages.info(request, '이미 있는 이름입니다.')
      else:
         obj.make_id()
         obj.save()
         print(request.POST.getlist('category[]'))
         print(request.POST.getlist('materials[]'))
         print(request.POST.getlist('material_units[]'))
         print(request.POST.getlist('material_amounts[]'))
         for cate,name,unit,amount,matunit in zip(request.POST.getlist('category[]'),request.POST.getlist('materials[]'),request.POST.getlist('material_units[]'),request.POST.getlist('material_amounts[]'),request.POST.getlist('mat_unit[]')):
            print("mat made!")
            if name == '':
               pass
            else:
               material=stat_mat_rel()
               material.stat_mat=obj
               material.mat_stat = name
               material.stat_mat_unit = unit
               if amount == '':
                  material.stat_mat_amount = 0
               else:
                  material.stat_mat_amount = amount
               if Materialinfo.objects.all().filter(mat_name=name):
                  material.mat_statkey = Materialinfo.objects.all().filter(mat_name=name)[0]
               else:
                  new_mat=Materialinfo()
                  new_mat.category=cate
                  new_mat.mat_name=name
                  new_mat.mat_unit=matunit
                  new_mat.make_id()
                  new_mat.save()
                  material.mat_statkey = new_mat
               material.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

      form = ClassstatForm()
      
   template_name = 'classstatd/cladmainadd.html'
   context = {'form': form, "mat_obj":mat_obj}
   return render(request, template_name, context)

@login_required
def classstat_update_view(request, class_code):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Classstatinfo, class_code=class_code)
   code = obj.class_title
   form = ClassstatForm(request.POST or None, instance = obj)
   if form.is_valid():
      print('notvalid')
      form_obj = form.save(commit=False)
      if code != form_obj.class_title:
         if Classstatinfo.objects.all().filter(class_title=form_obj.class_title):
            messages.info(request, '이미 있는 수업입니다.')
         else:
            form_obj.save()
            return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
      else:
         form_obj.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

   template_name = 'classstatd/cladmainupdate.html'
   context = {'form': form, "obj":obj}
   return render(request, template_name, context)

@login_required
def classstat_detail_view(request, class_code):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Classstatinfo, class_code=class_code)
   stat = stat_mat_rel.objects.all().filter(stat_mat=obj)
   class_list = Classinfo.objects.all().filter(class_statkey=obj)
   class_thismonth_count = len(Classinfo.objects.all().filter(Q(class_date__month=str(timezone.now().month))&Q(class_statkey=obj)))
   class_file_image_format = class_file_image_form(request.POST or None,request.FILES or None,instance=obj)
   class_file_recipe_format = class_file_recipe_form(request.POST or None,request.FILES or None,instance=obj)
   satis = 0
   count = 0
   for i in class_list:
      if (i.class_satisfaction == None) or (i.class_done != True):
         pass
      else:
         satis += i.class_satisfaction
         count +=1
   if count == 0:
      satis = 0
   else:
      satis = satis/count
   if 'class_file_image_input' in request.POST:
      if class_file_image_format.is_valid():
         class_file_image_format.save()
   elif 'class_file_recipe_input' in request.POST:
      if class_file_recipe_format.is_valid():
         class_file_recipe_format.save()

   context = {'obj':obj, 'stat':stat,'class_count':len(class_list),"class_thismonth_count":class_thismonth_count,"satisfaction":satis}
   return render(request,'classstatd/cladbdetail.html', context )



@login_required
def mat_create_view(request, class_code):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Classstatinfo, class_code=class_code)
   form = stat_mat_Form(request.POST)
   mat_obj = Materialinfo.objects.all()
   if request.method == 'POST':
      if form.is_valid():
         print("valid!")
         obj_form = form.save(commit=False)
         if Materialinfo.objects.all().filter(mat_name=obj_form.mat_stat):
            obj_form.mat_statkey = Materialinfo.objects.get(mat_name=obj_form.mat_stat)
         else:
            new_mat=Materialinfo()
            new_mat.mat_name=obj_form.mat_stat
            new_mat.make_id()
            new_mat.category = obj_form.category
            new_mat.mat_unit = obj_form.mat_unit
            new_mat.mat_inven = 0
            new_mat.save()
            obj_form.mat_statkey = new_mat
         obj_form.stat_mat = obj
         obj_form.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   context = {'obj':obj,'mat_obj':mat_obj,'form':form}
   return render(request,'classstatd/claddetailadd.html', context )

@login_required
def mat_update_view(request, class_code, mat_name):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Classstatinfo, class_code=class_code)
   mat_obj = stat_mat_rel.objects.all().filter(Q(stat_mat=obj)&Q(mat_statkey__mat_name=mat_name))[0]
   form = stat_mat_update_Form(request.POST, instance=mat_obj)
   if request.method == 'POST':
      if form.is_valid():
         obj_form = form.save(commit=False)

         obj_form.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   print(mat_obj)
   context = {'obj':obj,'mat_obj':mat_obj,'form':form}
   return render(request,'classstatd/claddetailupdate.html', context )

@login_required
def mat_delete_view(request, class_code, mat_name):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Classstatinfo, class_code=class_code)
   mat_obj = list(stat_mat_rel.objects.all().filter(stat_mat=obj).filter(mat_statkey__mat_name=mat_name))[0]
   if request.method == 'POST':
      mat_obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   print(mat_obj)
   context = {'obj':obj, 'mat_obj':mat_obj}
   return render(request,'classstatd/claddetaildelete.html', context )

@login_required
def class_data_reset(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   classstat = Classstatinfo.objects.all()
   stat_mat = stat_mat_rel.objects.all()
   count = 0
   for i in reversed(classstat):
      if len(Classstatinfo.objects.all().filter(class_title=i.class_title))>1:
         i.delete()
         continue
      print(i.class_title)

      i.class_code = "D"+ "%06d"%count
      i.save()
      count+=1
      
      for j in reversed(stat_mat.filter(stat_mat_str=i.class_title)):
         if len(stat_mat_rel.objects.all().filter(Q(stat_mat_str=i.class_title)&Q(mat_stat=j.mat_stat)))>1:
            j.delete()
            continue
         if j.mat_stat == None:
            j.delete()
            continue
         j.stat_mat = i
         j.save()

         if Materialinfo.objects.all().filter(mat_name=j.mat_stat):
            j.mat_statkey = Materialinfo.objects.all().filter(mat_name=j.mat_stat)[0]
            j.save()
         else:
            new_mat=Materialinfo()
            new_mat.mat_name=j.mat_stat
            new_mat.mat_unit = j.mat_unit
            new_mat.category = j.category
            
            new_mat.make_id()
            new_mat.save()
            
            j.mat_statkey = new_mat
            j.save()
   print('done!')
   return HttpResponseRedirect("/")