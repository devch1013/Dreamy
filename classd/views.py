from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect,HttpResponse
from django.http import Http404
from django.utils import timezone
from .models import *
from .forms import *
from school.models import *
from classstatd.models import *
from teacher.models import *
from users.models import *

# Create your views here.


@login_required
def class_home(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   qs = Classinfo.objects.all()
   form = ClassModelForm(request.POST or None, request.FILES or None)
   sch_obj=Schoolinfo.objects.all()
   classstat_obj=Classstatinfo.objects.all()
   tea_obj=Teacherinfo.objects.all()
   stat_mat_obj=stat_mat_rel.objects.all()
   if request.method == 'POST':
      if form.is_valid():
         obj = form.save(commit=False)
         obj.user = request.user
         if Schoolinfo.objects.all().filter(sch_name=obj.class_sch):
            obj.class_schkey=Schoolinfo.objects.all().filter(sch_name=obj.class_sch)[0]
         elif obj.class_sch == "":
            pass
         else:
            new_sch = Schoolinfo()
            new_sch.sch_name=obj.class_sch
            new_sch.make_id()
            new_sch.save()
            obj.class_schkey=new_sch
         if Teacherinfo.objects.all().filter(tea_name=obj.class_tea):
            obj.class_teakey=Teacherinfo.objects.all().filter(tea_name=obj.class_tea)[0]
         elif obj.class_tea == None:
            pass
         else:
            new_tea = Teacherinfo()
            new_tea.tea_name=obj.class_tea
            new_tea.make_id()
            new_tea.make_user()
            new_tea.save()
            obj.class_teakey=new_tea
         if Classstatinfo.objects.all().filter(class_title=obj.class_stat):
            obj.class_statkey=Classstatinfo.objects.all().filter(class_title=obj.class_stat)[0]

         else:
            new_stat = Classstatinfo()
            new_stat.class_title=obj.class_stat
            new_stat.make_id()
            new_stat.save()
            obj.class_statkey=new_stat

         stat_mat_filtered = stat_mat_obj.filter(stat_mat=obj.class_statkey)
         obj.make_id()
         obj.class_pay="온드림지급"
         obj.save()
         for i in range(len(stat_mat_filtered)):
            dyna_mat_obj = dyna_mat_rel()
            dyna_mat_obj.make_id()
            dyna_mat_obj.dyna_mat = obj
            dyna_mat_obj.dyna_mat_num = 0
            dyna_mat_obj.mat_dyna = stat_mat_filtered[i].mat_statkey
            
            dyna_mat_obj.save()

         
         form = ClassModelForm()
         if Teacherpay_monthly.objects.all().filter(Q(tp_teakey=obj.class_teakey)&Q(tp_month=obj.class_date.month)&Q(tp_year=obj.class_date.year)):
            
            teapay_month = Teacherpay_monthly.objects.all().filter(Q(tp_teakey=obj.class_teakey)&Q(tp_month=obj.class_date.month)&Q(tp_year=obj.class_date.year))[0]

         else:
            teapay_month = Teacherpay_monthly()
            teapay_month.tp_year=obj.class_date.year
            teapay_month.tp_month = obj.class_date.month
            teapay_month.tp_teakey = obj.class_teakey
            teapay_month.save()
         teapay = Teacherpay()
         teapay.tp_monthly = teapay_month
         teapay.tp_pay = obj.class_tea_price
         teapay.tp_classkey = obj
         teapay.tax_cal()
         teapay.tp_content = '수업'
         teapay.save()
         teapay_month.monthly_cal()
         
         teapay_month.save()
      

   context = {'title':'class information','object_list': qs, 'hund':range(10),'form': form, 'sch_obj':sch_obj, 'classstat_obj':classstat_obj, 'tea_obj':tea_obj}
   return render(request, 'class/classd.html', context)

@login_required
def class_detail_view(request, class_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   if len(Classinfo.objects.all().filter(class_id=class_id))==0:
      return HttpResponseRedirect("../")
   obj = get_object_or_404(Classinfo, class_id=class_id)
   mat_obj = dyna_mat_rel.objects.all().filter(dyna_mat=obj)
   recipe = stat_mat_rel.objects.all().filter(stat_mat=obj.class_statkey)
   sch_tea = Schoolteainfo.objects.all().filter(schtea_schkey = obj.class_schkey)
   form_class = ClassTableCheckForm(request.POST or None,request.FILES or None, instance=obj)
   form = ClassModelForm(request.POST or None, instance=obj)
   sch_obj=Schoolinfo.objects.all()
   classstat_obj=Classstatinfo.objects.all()
   tea_obj=Teacherinfo.objects.all()
   teapay = get_object_or_404(Teacherpay, tp_classkey=obj)

   if 'stat_reset' in request.POST:
      print("stat reset!!")

      for j in mat_obj:
         inrecipe = False
         for i in recipe:
            if i.mat_statkey == j.mat_dyna:
               inrecipe = True
               break
         if inrecipe == False:
            j.delete()
      for i in recipe:
         inrecipe = False
         for j in mat_obj:
            if i.mat_statkey == j.mat_dyna:
               inrecipe = True
               break
         if inrecipe == False:
            dyna_mat_obj = dyna_mat_rel()
            dyna_mat_obj.make_id()
            dyna_mat_obj.dyna_mat = obj
            dyna_mat_obj.dyna_mat_num = 0
            dyna_mat_obj.mat_dyna = i.mat_statkey

            dyna_mat_obj.save()

   elif 'class_file_preestim_input' in request.POST:
      if request.FILES.get('class_file_preestim'):
         obj.class_file_preestim = request.FILES.get('class_file_preestim')
         obj.save()
   elif 'class_file_plan_input' in request.POST:
      if request.FILES.get('class_file_plan'):
         obj.class_file_plan = request.FILES.get('class_file_plan')
         obj.save()
   elif 'class_file_tea_input' in request.POST:
      if request.FILES.get('class_file_tea'):
         obj.class_file_tea = request.FILES.get('class_file_tea')
         obj.save()
   elif 'class_file_finestim_input' in request.POST:
      if request.FILES.get('class_file_finestim'):
         obj.class_file_finestim = request.FILES.get('class_file_finestim')
         obj.save()
   elif 'class_file_cal_input' in request.POST:
      if request.FILES.get('class_file_cal'):
         obj.class_file_cal = request.FILES.get('class_file_cal')
         obj.save()

   elif 'save_progress' in request.POST:
      
      if form_class.is_valid():
         obj_form = form_class.save(commit=False)
         if sch_tea.filter(schtea_name=obj.schtea):
            obj_form.schteakey = sch_tea.filter(schtea_name=obj_form.schtea)[0]
         for i in range(len(mat_obj)):

            mat_obj[i].dyna_mat_num=request.POST.get('dyna_mat_num%d'%(i+1))
            print(mat_obj[i].dyna_mat_num)
            mat_obj[i].save()


         if obj.class_doc_plan or obj.class_doc_preestim or obj.class_doc_tea:
            obj.class_process="서류제출"
            order = False
            for i in mat_obj:
               if (i.status == '주문완료') or (i.status == '배송완료'):
                  order=True
                  break
            if order == True:
               obj.class_process="재료주문"
               deli = False
               for i in mat_obj:
                  if i.status == '배송완료':
                     deli=True
                     break
               if deli == True:
                  obj.class_process="도착확인"
                  if obj.class_mani:
                     obj.class_process="수업준비"
                     if obj.class_div:
                        obj.class_process="수업준비"
                        if obj.class_taken:
                           obj.class_process="강사수거"
                           if obj.class_re_done:
                              obj.class_process="도구반납"
                              if obj.class_doc_finestim or (obj.class_cal_meth != None):
                                 if obj.class_deposit_check:
                                    obj.class_process="완료"
                                 
         
         obj_form.timestamp_progress = timezone.now()
         obj_form.user_progress = request.user.user_name
         print(obj_form.class_3)
         obj_form.save()
         teapay.tp_pay = obj_form.class_tea_price
         teapay.tax_cal()
         teapay.save()
         if Teacherpay_monthly.objects.all().filter(Q(tp_teakey=obj.class_teakey)&Q(tp_month=obj.class_date.month)&Q(tp_year=obj.class_date.year)):
            
            teapay_month = Teacherpay_monthly.objects.all().filter(Q(tp_teakey=obj.class_teakey)&Q(tp_month=obj.class_date.month)&Q(tp_year=obj.class_date.year))[0]

         else:
            teapay_month = Teacherpay_monthly()
            teapay_month.tp_year=obj.class_date.year
            teapay_month.tp_month = obj.class_date.month
            teapay_month.tp_teakey = obj.class_teakey
            teapay_month.save()
         teapay = Teacherpay.objects.all().filter(tp_classkey=obj)[0]
         teapay.tp_pay = obj_form.class_tea_price
         teapay.tp_pay = obj.class_tea_price
         teapay.tax_cal()
         teapay.save()
         teapay.tp_monthly.monthly_cal()
         teapay.tp_monthly.save()
   elif 'class_update' in request.POST:
      print("update")
      if form.is_valid():

         obj_form = form.save(commit=False)
         if Schoolinfo.objects.all().filter(sch_name=obj_form.class_sch):
            obj.class_schkey=Schoolinfo.objects.all().filter(sch_name=obj_form.class_sch)[0]
         elif obj_form.class_sch == "":
            pass
         else:
            new_sch = Schoolinfo()
            new_sch.sch_name=obj.class_sch
            new_sch.make_id()
            new_sch.save()
            obj.class_schkey=new_sch
         if Teacherinfo.objects.all().filter(tea_name=obj_form.class_tea):
            obj.class_teakey=Teacherinfo.objects.all().filter(tea_name=obj_form.class_tea)[0]
         elif obj_form.class_tea == "":
            pass
         else:
            new_tea = Teacherinfo()
            new_tea.tea_name=obj_form.class_tea
            new_tea.make_id()
            new_tea.save()
            new_tea.make_user()
            obj.class_teakey=new_tea
         if obj_form.class_stat != obj.class_stat:
            dyna_mat_rel.objects.all().filter(dyna_mat=obj).delete()

            if Classstatinfo.objects.all().filter(class_title=obj_form.class_stat):
               obj.class_statkey=Classstatinfo.objects.all().filter(class_title=obj_form.class_stat)[0]
            else:
               new_stat = Classstatinfo()
               new_stat.class_title=obj_form.class_stat
               new_stat.make_id()
               new_stat.save()
               obj.class_statkey=new_stat
            obj.save()
            stat_mat_filtered = stat_mat_rel.objects.all().filter(stat_mat=obj.class_statkey)

            for i in range(len(stat_mat_filtered)):
               dyna_mat_obj = dyna_mat_rel()
               dyna_mat_obj.make_id()
               dyna_mat_obj.dyna_mat = obj
               dyna_mat_obj.mat_dyna = stat_mat_filtered[i].mat_statkey
               dyna_mat_obj.save()
         obj_form.save()
         obj.memo = request.POST.get('edit_memo')
         obj.save()



   template_name = 'class/progress.html'
   context = {'form_class':form_class,'form':form,"class_obj": obj,'update_sch_obj':sch_obj, 'update_classstat_obj':classstat_obj, 'update_tea_obj':tea_obj, "sch_obj": obj.class_schkey,"sch_tea":sch_tea, 'recipe_obj':recipe, "classstat_obj": obj.class_statkey, "mat_obj":dyna_mat_rel.objects.all().filter(dyna_mat=obj)}#"schtea_obj":Schoolteainfo.objects.all().filter(schtea_schkey=obj.class_schkey)[0]}
   
   return render(request, template_name, context)




@login_required
def class_update_view(request, class_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   # 1 object -> detail view
   obj = get_object_or_404(Classinfo, class_id=class_id)
   form = ClassModelForm(request.POST or None, instance=obj)
   sch_obj=Schoolinfo.objects.all()
   classstat_obj=Classstatinfo.objects.all()
   tea_obj=Teacherinfo.objects.all()
   
   if form.is_valid():
      obj_form = form.save(commit=False)
      if Schoolinfo.objects.all().filter(sch_name=obj_form.class_sch):
         obj.class_schkey=Schoolinfo.objects.all().filter(sch_name=obj_form.class_sch)[0]
      elif obj_form.class_sch == "":
         pass
      else:
         new_sch = Schoolinfo()
         new_sch.sch_name=obj.class_sch
         new_sch.make_id()
         new_sch.save()
         obj.class_schkey=new_sch
      if Teacherinfo.objects.all().filter(tea_name=obj_form.class_tea):
         obj.class_teakey=Teacherinfo.objects.all().filter(tea_name=obj_form.class_tea)[0]
      elif obj_form.class_tea == "":
         pass
      else:
         new_tea = Teacherinfo()
         new_tea.tea_name=obj_form.class_tea
         new_tea.make_id()
         new_tea.save()
         new_tea.make_user()
         obj.class_teakey=new_tea
      if obj_form.class_stat != obj.class_stat:
         dyna_mat_rel.objects.all().filter(dyna_mat=obj).delete()

         if Classstatinfo.objects.all().filter(class_title=obj_form.class_stat):
            obj.class_statkey=Classstatinfo.objects.all().filter(class_title=obj_form.class_stat)[0]
         else:
            new_stat = Classstatinfo()
            new_stat.class_title=obj_form.class_stat
            new_stat.make_id()
            new_stat.save()
            obj.class_statkey=new_stat
         obj.save()
         stat_mat_filtered = stat_mat_rel.objects.all().filter(stat_mat=obj.class_statkey)

         for i in range(len(stat_mat_filtered)):
            dyna_mat_obj = dyna_mat_rel()
            dyna_mat_obj.make_id()
            dyna_mat_obj.dyna_mat = obj
            
            dyna_mat_obj.mat_dyna = stat_mat_filtered[i].mat_statkey

            dyna_mat_obj.save()

      form.save()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   template_name = 'class/class__update.html'
   context = {'form': form, 'obj':obj, 'sch_obj':sch_obj, 'classstat_obj':classstat_obj, 'tea_obj':tea_obj}
   return render(request, template_name, context)

@login_required
def class_delete_view(request,class_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(Classinfo, class_id=class_id)
   template_name = 'class/classdelete.html'
   if request.method == "POST":
      obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/class/";</script>')
   context = {"object": obj}
   return render(request, template_name, context)

@login_required
def class_sch_queryinput(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   class_obj = Classinfo.objects.all()
   sch_obj = Schoolinfo.objects.all()
   tea_obj = Teacherinfo.objects.all()
   data_obj = Classstatinfo.objects.all()
   code = 0
   for i in class_obj:
      code +=1
      if sch_obj.filter(sch_name=i.class_sch):
         i.class_schkey=sch_obj.filter(sch_name=i.class_sch)[0]
      elif i.class_sch==None:
         pass
      else:
         new_sch=Schoolinfo()
         new_sch.sch_name=i.class_sch
         new_sch.make_id()
         new_sch.save()
      if tea_obj.filter(tea_name=i.class_tea):
         i.class_teakey=tea_obj.filter(tea_name=i.class_tea)[0]
      elif i.class_tea==None:
         pass
      else:
         new_tea=Teacherinfo()
         new_tea.tea_name=i.class_tea
         new_tea.make_id()
         new_tea.save()
      if data_obj.filter(class_title=i.class_stat):
         i.class_statkey=data_obj.filter(class_title=i.class_stat)[0]
         i.save()
         stat_mat_filtered = stat_mat_rel.objects.all().filter(stat_mat=i.class_statkey)
         dyna_mat_rel.objects.all().filter(dyna_mat=i).delete()
         for j in range(len(stat_mat_filtered)):
            dyna_mat_obj = dyna_mat_rel()
            dyna_mat_obj.make_id()
            dyna_mat_obj.dyna_mat = i
            dyna_mat_obj.dyna_mat_num = 0
            dyna_mat_obj.mat_dyna = stat_mat_filtered[j].mat_statkey

            dyna_mat_obj.save()
      elif i.class_stat==None:
         pass
      else:
         new_stat=Classstatinfo()
         new_stat.class_title=i.class_stat
         new_stat.make_id()
         new_stat.save()

      i.class_id = "C"+ "%06d"%code
      if i.class_tea_inout == None:
         i.class_tea_inout = "반출미완료"
      i.save()

   return render(request, "home.html", {"object":class_obj})

@login_required
def teacherout_view(request):
   tea = get_object_or_404(Teacherinfo, tea_id=request.user.user_tea_id)
   class_obj = Classinfo.objects.all().filter(class_teakey=tea).filter(Q(class_taken=False)&Q(class_doc_plan=True)&Q(class_doc_preestim=True)&Q(class_doc_tea=True))
   if request.method == 'POST':
      tea.tea_next_visit = request.POST.get('tea_next_visit')
      tea.save()
      return HttpResponseRedirect("../teacherout")
   context = {'class_obj':class_obj, "tea":tea}
   template = 'teacherinout/teacherout.html'
   return render(request,template,context)

@login_required
def teacherin_view(request):
   tea = get_object_or_404(Teacherinfo, tea_id=request.user.user_tea_id)
   class_obj = Classinfo.objects.all().filter(class_teakey=tea).filter(Q(class_taken=True)&Q(class_re_done=False)&Q(class_doc_plan=True)&Q(class_doc_preestim=True)&Q(class_doc_tea=True))
   if request.method == 'POST':
      tea.tea_next_visit = request.POST.get('tea_next_visit')
      tea.save()
      return HttpResponseRedirect("../teacherin")
   context = {'class_obj':class_obj, "tea":tea}
   template = 'teacherinout/teacherin.html'
   return render(request,template,context)

@login_required
def teacherin_detail_view(request,class_id):
   tea = get_object_or_404(Teacherinfo, tea_id=request.user.user_tea_id)
   class_obj = get_object_or_404(Classinfo, class_id=class_id)
   mat_obj = dyna_mat_rel.objects.all().filter(Q(dyna_mat=class_obj)&Q(mat_dyna__category="도구"))
   recipe_obj = stat_mat_rel.objects.all().filter(stat_mat=class_obj.class_statkey)
   class_re = True
   if request.method == 'POST':
      for i in range(len(mat_obj)):
         out = request.POST.get('tool_re%d'%(i+1))
         if out == 'yes':
            mat_obj[i].tool_re = True
            mat_obj[i].save()
         else:
            mat_obj[i].tool_re = False
            class_re = False
            mat_obj[i].save()
      class_obj.class_re_done = class_re
      if class_re == True:
         class_obj.class_tea_inout = "반입완료"
         class_obj.class_tea_inout_date = timezone.now()

      class_obj.save()
   context = {'class_obj':class_obj, "tea":tea,'mat_obj':mat_obj,'recipe_obj':recipe_obj}
   template = 'teacherinout/teacherindetail.html'
   return render(request,template,context)

@login_required
def teacherout_detail_view(request,class_id):
   tea = get_object_or_404(Teacherinfo, tea_id=request.user.user_tea_id)
   class_obj = get_object_or_404(Classinfo, class_id=class_id)
   mat_obj = dyna_mat_rel.objects.all().filter(dyna_mat=class_obj)
   recipe_obj = stat_mat_rel.objects.all().filter(stat_mat=class_obj.class_statkey)
   class_taken = True
   if request.method == 'POST':
      for i in range(len(mat_obj)):
         out = request.POST.get('taken%d'%(i+1))
         if out == 'yes':
            mat_obj[i].taken = True
            mat_obj[i].save()
         else:
            mat_obj[i].taken = False
            class_taken = False
            mat_obj[i].save()
      class_obj.class_taken = class_taken
      if class_taken == True:
         class_obj.class_tea_inout = "반출완료"
         class_obj.class_tea_inout_date = timezone.now()
      class_obj.save()

   context = {'class_obj':class_obj, "tea":tea,'mat_obj':mat_obj,'recipe_obj':recipe_obj}
   template = 'teacherinout/teacheroutdetail.html'
   return render(request,template,context)