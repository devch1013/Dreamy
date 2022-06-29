from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.utils import timezone
from django.db.models import Sum
from .models import *
from classd.models import *
from .forms import *

# Create your views here.

@login_required
def order_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   mat_order = dyna_mat_rel.objects.all().filter(Q(status='준비중')|Q(status='결제대기중')).exclude(dyna_mat_num=0)
   if len(Order.objects.all())==0:
      order_id = "O000001"
   else:
      order_id = "O"+ "%06d"%(int(Order.objects.all()[len(Order.objects.all())-1].order_id[1:])+1)
   if request.method == "POST":
      order_list = request.POST.getlist("mat_objs")
      if len(order_list)==0:
         order_id = '/'
      else:
         order_new = Order()
         order_new.order_id = order_id
         order_new.order_user = request.user
         order_new.category = "수업주문"
         order_new.save()
         for o in order_list:
            mat = dyna_mat_rel.objects.get(rel_id=o)
            mat.order = order_new
            mat.status = '결제대기중'
            mat.save()
            cart = mat_order
         return HttpResponseRedirect("%s/"%order_id)

   context = {'title':'order information','mat_obj':mat_order,'order_link': order_id}
   return render(request, 'order/order.html', context)

@login_required
def order_done_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   order_list = Order.objects.all()
   context = {'title':'order information','order_list':reversed(order_list)}
   return render(request, 'order/order2.html', context)

@login_required
def order_custom_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   mat_obj = Materialinfo.objects.all()
   if len(Order.objects.all())==0:
      order_id = "O000001"
   else:
      order_id = "O"+ "%06d"%(int(Order.objects.last().order_id[1:])+1)
   if request.method == "POST":
      order_list = request.POST.getlist("mat_objs")
      if len(order_list)==0:
         order_id = '/'
      else:
         order_new = Order()
         order_new.order_id = order_id
         order_new.order_user = request.user
         order_new.category = "자유주문"
         order_new.save()
         for o in order_list:
            mat = Materialinfo.objects.get(mat_id=o)
            cart = Order_Cart()
            cart.order_info = order_new
            cart.mat_info = mat

            cart.save()
            print(mat)
         return HttpResponseRedirect("%s/"%order_id)
      print(order_list)

   context = {'title':'order information','mat_obj':mat_obj,'order_link': order_id}
   return render(request, 'order/order3.html', context)

@login_required
def order_custom_detail_view(request, order_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   if len(Order.objects.all().filter(order_id=order_id))==0:
      return HttpResponseRedirect("/order/")
   obj = get_object_or_404(Order, order_id=order_id)
   order_cart_obj = Order_Cart.objects.all().filter(order_info=obj)
   form = OrderForm(request.POST,instance=obj)
   if request.method == 'POST':
      if 'save_order' in request.POST:
         print('hello')
         if form.is_valid():
            form_save = form.save(commit=False)
            form_save.order_user = request.user
            form_save.order_done = True
            form_save.order_date = timezone.now()
            for y in order_cart_obj:
               y.order_date = timezone.now()
               y.deli_state = '주문완료'
               y.save()
            count = 0
            print(request.POST.getlist('order_amount'))
            for h,shop in zip(request.POST.getlist('order_amount'),request.POST.getlist('shop')):
               if h=="":
                  order_cart_obj[count].order_amount = 0
               else:
                  order_cart_obj[count].order_amount = h
               order_cart_obj[count].shop = shop
               order_cart_obj[count].save()

               count+=1


            form_save.save()
            
   context = {'order_obj': obj, 'order_cart_obj':order_cart_obj}
   return render(request, 'order/orderdetail2.html', context)

@login_required
def order_custom_delete_view(request, order_id, mat_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")

   cart_obj = Order_Cart.objects.all().filter(Q(order_info__order_id=order_id)&Q(mat_info__mat_id=mat_id))
   if request.method == 'POST':
      cart_obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   context = {'obj': cart_obj}
   return render(request, 'order/ordercustomdelete.html', context)

@login_required
def order_rel_delete(request, order_id, rel_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   mat_obj = dyna_mat_rel.objects.all().filter(Q(order__order_id=order_id)&Q(rel_id=rel_id))[0]
   if request.method == 'POST':
      mat_obj.order=None
      mat_obj.status = '준비중'
      mat_obj.save()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   context = {'obj': mat_obj}
   return render(request, 'order/ordermatdelete.html', context)

@login_required
def order_delete_view(request, order_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   order_obj = get_object_or_404(Order, order_id=order_id)
   mat_obj = dyna_mat_rel.objects.all().filter(order=order_obj)
   if request.method == 'POST':
      for i in mat_obj:
         i.status = '준비중'
         i.save()
      order_obj.delete()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "../";</script>')
   context = {'obj': order_obj}
   return render(request, 'order/orderdelete.html', context)


@login_required
def order_detail(request, order_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   if len(Order.objects.all().filter(order_id=order_id))==0:
      return HttpResponseRedirect("/order/")
   obj = get_object_or_404(Order, order_id=order_id)
   order_cart_obj = Order_Cart.objects.all().filter(order_info=obj)
   mat_obj = dyna_mat_rel.objects.all().filter(order__order_id=order_id)
   form = OrderForm(request.POST,instance=obj)
   if request.method == 'POST':
      if 'create_order_list' in request.POST:
         print("hello")
         for k in order_cart_obj:
            k.delete()
         mat_list = []
         for i in mat_obj:
            mat_list.append(i.mat_dyna.mat_name)
         for j in list(set(mat_list)):
            cart_obj = Order_Cart()
            cart_obj.order_info = obj
            cart_obj.mat_info = get_object_or_404(Materialinfo, mat_name=j)
            cart_obj.order_amount = mat_obj.filter(mat_dyna__mat_name=j).aggregate(Sum('dyna_mat_num'))['dyna_mat_num__sum']

            cart_obj.save()
         return redirect('../%s/'%obj.order_id)
      
      elif 'save_order' in request.POST:
         print("order")
         if form.is_valid():
            form_save = form.save(commit=False)
            form_save.order_user = request.user
            form_save.order_done = True
            form_save.order_date = timezone.now()
            for d in mat_obj:
               d.status='주문완료'
               d.save()
            for y in order_cart_obj:
               y.order_date = form_save.order_date
               y.deli_state = '주문완료'
               y.save()
            count = 0
            for h,shopin in zip(request.POST.getlist('order_amount'),request.POST.getlist('shop')):
               order_cart_obj[count].order_amount = h
               order_cart_obj[count].shop = shopin
               order_cart_obj[count].save()
               count+=1
               print(h)
               print(shopin)


            form_save.save()
            return HttpResponseRedirect("../done/")
   context = {'order_obj': obj, 'mat_obj':mat_obj, 'order_cart_obj':order_cart_obj}
   return render(request, 'order/orderdetail1.html', context)


@login_required
def order_inven(request, inven_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = get_object_or_404(dyna_mat_rel, rel_id=inven_id)
   if request.method == 'POST':
      obj.mat_dyna.mat_inven = round((round(float(obj.mat_dyna.mat_inven),3) - round(float(obj.dyna_mat_num),3)),3)
      if obj.order:
         obj.order = None
      obj.mat_dyna.save()
      obj.status = '배송완료'
      obj.save()
      return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   context = {'mat_obj': obj}
   return render(request, 'order/need_inven.html', context)


@login_required
def delivery_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   qs = Order_Cart.objects.all().filter(deli_state="주문완료" or "배송중")
   
   context = {'cart':qs}
   return render(request, 'delivery/delivery.html', context)

@login_required
def delivery2_view(request):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   qs = Order_Cart.objects.all().exclude(deli_state="주문완료").exclude(deli_state="결제대기중")
   print(qs)
   context = {'cart':qs}
   return render(request, 'delivery/delivery2.html', context)

@login_required
def delivery_check_view(request,order_id, mat_id):
   if request.user.user_position == '강사':
      return HttpResponseRedirect("/")
   obj = Order_Cart.objects.all().filter(order_info__order_id=order_id).filter(mat_info__mat_id=mat_id)[0]
   mat_obj = dyna_mat_rel.objects.all().filter(Q(order=obj.order_info)&Q(mat_dyna__mat_id=mat_id))
   form = deli_check_Form(request.POST or None, instance = obj)
   if request.method == 'POST':
      if form.is_valid():
         print('done')
         form_obj = form.save(commit=False)
         form_obj.deli_check_date = timezone.now()
         if form_obj.deli_state == '배송완료':
            mat = get_object_or_404(Materialinfo, mat_id=mat_id)
            if mat.mat_inven == None:
               mat.mat_inven = form_obj.deli_amount
            else:
               mat.mat_inven = round((round(float(mat.mat_inven),3) + round(float(form_obj.deli_amount),3)),3)
            mat.save()
            for i in mat_obj:
               mat.mat_inven = round((round(float(mat.mat_inven),3) - round(float(i.dyna_mat_num),3)),3)
               mat.save()
               i.status='배송완료'
               i.save()
         else:
            for i in mat_obj:
               i.status='준비중'
               i.save()

         form_obj.save()
         return HttpResponse('<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
   context = {'obj':obj,'form':form}
   return render(request, 'delivery/confirmpop.html', context )