from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import *
from classd.models import *
from .forms import *
from users.models import User as Userqs
from classstatd.models import *

# Create your views here.

@login_required
def teacher_home(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   qs = Teacherinfo.objects.all()
   context = {'title':'teacher information','tea_obj': qs}
   return render(request, 'teacher/teachermain.html', context)

@login_required
def teacher_pay_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")

   qs = Teacherinfo.objects.all()
   teapay = Teacherpay.objects.all()
   teapay_monthly = Teacherpay_monthly.objects.all()
   print(teapay)
   context = {'teapay_monthly':teapay_monthly ,'title':'teacher information','tea_obj': qs}
   return render(request, 'teacher/teachermain2.html', context)


@login_required
def teacher_pay_detail(request, tea_id,year,month):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")

   qs = Teacherinfo.objects.all()
   teacher = get_object_or_404(Teacherinfo, tea_id=tea_id)
   teapay_monthly = Teacherpay_monthly.objects.all().filter(Q(tp_year=year)&Q(tp_month=month)&Q(tp_teakey__tea_id=tea_id))[0]
   teapay = Teacherpay.objects.all().filter(Q(tp_monthly=teapay_monthly)&Q(tp_content='수업'))
   teapay_ex = Teacherpay.objects.all().filter(Q(tp_monthly=teapay_monthly)&(Q(tp_classkey=None)))
   if request.method=="POST":
      if 'addrow' in request.POST:
         print("addrow")
         teapay_new = Teacherpay()
         teapay_new.tp_monthly=teapay_monthly
         teapay_new.tp_pay=0
         teapay_new.save()
         return HttpResponseRedirect(".")
      if 'submit' in request.POST:
         print(range(len(teapay_ex)),request.POST.getlist('content[]'),request.POST.getlist('teapay[]'))
         for cont,pay,i in zip(request.POST.getlist('content[]'),request.POST.getlist('teapay[]'),range(len(teapay_ex))):
            print(cont)
            teapay_ex[i].tp_content = cont
            print(pay)
            if pay=="":
               teapay_ex[i].tp_pay = 0
            else:
               teapay_ex[i].tp_pay = int(pay)
            
            teapay_ex[i].tax_cal()
            teapay_ex[i].save()
            teapay_monthly.monthly_cal()
            teapay_monthly.save()
         
         for a,i in zip(request.POST.getlist('tp_pay[]'),range(len(teapay))):
            if a=="":
               teapay[i].tp_pay = 0
            else:
               teapay[i].tp_pay = int(a)
            teapay[i].tax_cal()
            teapay[i].save()
            teapay_monthly.monthly_cal()
            teapay_monthly.save()
         return HttpResponseRedirect(".")


   context = {'teapay_monthly':teapay_monthly ,'teapay':teapay,'teapay_ex':teapay_ex, 'title':'teacher information','tea_obj': qs}
   return render(request, 'teacher/teacherdetail2.html', context)



@login_required
def teacher_id_reset(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   tea_obj = Teacherinfo.objects.all()
   tea_user = Userqs.objects.all().filter(user_position = '강사')
   tea_user.delete()
   code = 0
   for i in tea_obj:
      code += 1
      i.tea_id = "T"+ "%06d"%code
      i.save()
      i.make_user()
   return HttpResponseRedirect("/")


@login_required
def teacher_detail(request, tea_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   qs = get_object_or_404(Teacherinfo, tea_id=tea_id)
   class_list = Classinfo.objects.all().filter(class_teakey__tea_id=tea_id)
   form = TeacherdetailForm(request.POST or None,request.FILES or None, instance=qs)
   tea_doc_cv_format = tea_doc_cv_form(request.POST or None,request.FILES or None, instance=qs)
   tea_doc_card_format = tea_doc_card_form(request.POST or None,request.FILES or None, instance=qs)
   tea_doc_bankacc_format = tea_doc_bankacc_form(request.POST or None,request.FILES or None, instance=qs)
   tea_doc_agree_format = tea_doc_agree_form(request.POST or None,request.FILES or None, instance=qs)
   tea_doc_sign_format = tea_doc_sign_form(request.POST or None,request.FILES or None, instance=qs)

   
   if request.method == 'POST':
      if 'tea_update' in request.POST:
         if form.is_valid():
            form.save()
      elif 'tea_doc_cv_input' in request.POST:
         if tea_doc_cv_format.is_valid():
            tea_doc_cv_format.save()
      elif 'tea_doc_card_input' in request.POST:
         if tea_doc_card_format.is_valid():
            tea_doc_card_format.save()
      elif 'tea_doc_bankacc_input' in request.POST:
         if tea_doc_bankacc_format.is_valid():
            tea_doc_bankacc_format.save()
      elif 'tea_doc_agree_input' in request.POST:
         if tea_doc_agree_format.is_valid():
            tea_doc_agree_format.save()
      elif 'tea_doc_sign_input' in request.POST:
         if tea_doc_sign_format.is_valid():
            tea_doc_sign_format.save()

   context = {'form':form,'obj': qs, 'class_obj':class_list, 'tea_doc_cv_format':tea_doc_cv_format}
   return render(request, 'teacher/teacherdetail1.html', context)

@login_required
def teacher_inout_detail(request, tea_id, class_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   tea = get_object_or_404(Teacherinfo, tea_id=tea_id)
   class_obj = get_object_or_404(Classinfo, class_id=class_id)
   tool_obj = dyna_mat_rel.objects.all().filter(Q(dyna_mat=class_obj)&Q(mat_dyna__category="도구"))
   mat_obj = dyna_mat_rel.objects.all().filter(dyna_mat=class_obj)
   recipe_obj = stat_mat_rel.objects.all().filter(stat_mat=class_obj.class_statkey)

   context = {'class_obj':class_obj, "tea":tea,'mat_obj':mat_obj,'tool_obj':tool_obj,'recipe_obj':recipe_obj}
   template = 'teacher/teacherinoutdetail.html'
   return render(request,template,context)


@login_required
def teacher_create_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   form = TeacherCreateForm(request.POST or None, request.FILES or None)


   if form.is_valid():
      obj = form.save(commit=False)
      obj.make_id()
      if Teacherinfo.objects.all().filter(tea_name=obj.tea_name):
         messages.info(request, '이미 있는 이름입니다.')
      elif obj.tea_name=="":
         messages.info(request, '이름을 입력해주세요')
      else:
         obj.save()
         obj.make_user()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
      form = TeacherCreateForm()
   context={'form':form}
   return render(request, 'teacher/teacheradd.html',context)

@login_required
def teacher_update_view(request,tea_id):
   pass