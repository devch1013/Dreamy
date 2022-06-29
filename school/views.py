from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from classd.models import *
from django.utils import timezone
from django.contrib import messages

# Create your views here.

@login_required
def School_table(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   qs = Schoolinfo.objects.all()
   form = SchoolModelForm(request.POST or None, request.FILES or None)
   print("form created")
   if form.is_valid():
      obj = form.save(commit=False)
      if Schoolinfo.objects.all().filter(sch_name=obj.sch_name):
         messages.info(request, '이미 있는 학교입니다.')
      else:
         
         obj.make_id()
         obj.save()
         
      form = SchoolModelForm()
   context = {'title':'School information','object_list': qs,'form':form}
   return render(request, 'school/schoolmain.html', context)

@login_required
def School_detail_view(request, sch_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   class_list = Classinfo.objects.all().filter(class_schkey=obj)
   class_list = Classinfo.objects.all().filter(Q(class_schkey__sch_id=sch_id))
   schtea_obj = Schoolteainfo.objects.all().filter(schtea_schkey = obj)
   class_thismonth_count = len(Classinfo.objects.all().filter(Q(class_date__month=str(timezone.now().month))&Q(class_schkey=obj)))
   print(class_thismonth_count)
   print(obj.sch_code)

   sch_name_obj = str(obj.sch_name)
   form = SchoolModelForm(request.POST or None, instance=obj)
   if request.method == 'POST':
      if form.is_valid():
         obj_form=form.save(commit=False)
         if sch_name_obj != obj_form.sch_name:
            if Schoolinfo.objects.all().filter(sch_name=obj_form.sch_name):
               messages.info(request, '이미 있는 학교입니다.')
            else:
               form.save()
               

         form.save()




   template_name = 'school/schooldetail.html'
   context = {'obj': obj, 'form':form,'class_count':len(class_list),'schtea_obj':schtea_obj,"class_thismonth_count":class_thismonth_count,'class_list':class_list}
   return render(request, template_name, context)


@login_required
def School_teacher_view(request, sch_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   class_list = Classinfo.objects.all().filter(class_schkey=obj)
   class_list = Classinfo.objects.all().filter(Q(class_schkey__sch_id=sch_id))
   schtea_obj = Schoolteainfo.objects.all().filter(schtea_schkey = obj)
   class_thismonth_count = len(Classinfo.objects.all().filter(Q(class_date__month=str(timezone.now().month))&Q(class_schkey=obj)))
   form_tea = SchoolteaForm(request.POST or None)

   sch_name_obj = str(obj.sch_name)
   form = SchoolModelForm(request.POST or None, instance=obj)

   if request.method == 'POST':
      if 'sch_update' in request.POST:
         if form.is_valid():
            obj_form=form.save(commit=False)
            if sch_name_obj != obj_form.sch_name:
               if Schoolinfo.objects.all().filter(sch_name=obj_form.sch_name):
                  messages.info(request, '이미 있는 학교입니다.')
               else:
                  form.save()
            form.save()

      if 'schtea_update' in request.POST:
         if form_tea.is_valid():
            obj_form = form_tea.save(commit=False)
            if Schoolteainfo.objects.all().filter(Q(schtea_schkey=obj)&Q(schtea_name=obj_form.schtea_name)):
               messages.info(request, '이미 있는 이름입니다.')
            else:
               obj_form.schtea_schkey = obj
               obj_form.make_id()
               obj_form.save()




   template_name = 'school/schooldetail2.html'
   context = {'obj': obj, 'form':form,'form_tea': form_tea,'class_count':len(class_list),'schtea_obj':schtea_obj,"class_thismonth_count":class_thismonth_count,'class_list':class_list}
   return render(request, template_name, context)

@login_required
def School_update_view(request, sch_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   sch_name_obj = str(obj.sch_name)
   form = SchoolModelForm(request.POST or None, instance=obj)
   if request.method == 'POST':
      if form.is_valid():
         obj_form=form.save(commit=False)
         if sch_name_obj != obj_form.sch_name:
            if Schoolinfo.objects.all().filter(sch_name=obj_form.sch_name):
               messages.info(request, '이미 있는 학교입니다.')
            else:
               form.save()
               return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

         form.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')

   template_name = 'school/schupdate.html'
   context = {'form': form, 'obj':obj}
   return render(request, template_name, context)

@login_required
def School_delete_view(request,sch_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   sch_obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   if request.method == 'POST':
      sch_obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   template_name = 'school/schdelete.html'
   context = {'sch_obj':sch_obj,}
   return render(request, template_name, context)

@login_required
def School_idreset(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = Schoolinfo.objects.all()
   schtea = Schoolteainfo.objects.all()
   count = 0
   for k in Schoolteainfo.objects.all():
      k.schtea_id = "H" + "%06d"%count
      count+=1
      k.save()
   count=0
   for i in reversed(obj):
      if len(Schoolinfo.objects.all().filter(sch_name=i.sch_name))>1:
         i.delete()
         continue

      i.sch_id = "S"+ "%06d"%count
      count+=1
      i.save()
      for j in schtea.filter(schtea_sch=i.sch_name):
         j.schtea_schkey = i
         
         j.save()
   return HttpResponseRedirect("/school/")

@login_required
def Schooltea_create_view(request,sch_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   form = SchoolteaForm(request.POST or None)
   sch_obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   if request.method == 'POST':
      if form.is_valid():
         obj = form.save(commit=False)
         if Schoolteainfo.objects.all().filter(Q(schtea_schkey=sch_obj)&Q(schtea_name=obj.schtea_name)):
            messages.info(request, '이미 있는 이름입니다.')
         else:
            obj.schtea_schkey = sch_obj
            obj.make_id()
            obj.save()
            return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
         form = SchoolteaForm()
   template_name = 'school/schoolteacheradd.html'
   context = {'form': form, 'sch_obj':sch_obj}
   return render(request, template_name, context)

@login_required
def Schooltea_update_view(request,sch_id,schtea_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   sch_obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   schtea_obj = get_object_or_404(Schoolteainfo, schtea_id=schtea_id)
   form = SchoolteaForm(request.POST or None, instance = schtea_obj)
   if request.method == 'POST':
      if form.is_valid():
         obj = form.save(commit=False)
         obj.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   template_name = 'school/schoolteacherupdate.html'
   context = {'form': form, 'sch_obj':sch_obj,'schtea_obj':schtea_obj}
   return render(request, template_name, context)

@login_required
def Schooltea_delete_view(request,sch_id,schtea_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   sch_obj = get_object_or_404(Schoolinfo, sch_id=sch_id)
   schtea_obj = get_object_or_404(Schoolteainfo, schtea_id=schtea_id)
   if request.method == 'POST':
      schtea_obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   template_name = 'school/schoolteacherdelete.html'
   context = {'sch_obj':sch_obj,'schtea_obj':schtea_obj}
   return render(request, template_name, context)