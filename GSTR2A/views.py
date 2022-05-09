from django.http.response import JsonResponse
from django.shortcuts import render
from .forms import CreateGSTR2AForm,UpdateGSTR2AForm
from django.views.generic import TemplateView,DetailView,ListView,DeleteView,CreateView,UpdateView
from .models import GSRT2A
from django.urls import reverse_lazy,reverse
import os,csv
from django.db.models import Q
from django.db import connection
import re,datetime


#  bill index page
class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'index.html'

class GST2Aindex(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'GSTR2A/GST2A-main.html'

class CreateGST2A(CreateView):
    model = GSRT2A
    form_class = CreateGSTR2AForm

class UpdateGSTR2A(UpdateView):
    model = GSRT2A
    form_class = UpdateGSTR2AForm

class DetailGSTR2A(DetailView):
    context_object_name = 'GSTR2A'
    model = GSRT2A
    template_name = 'GSTR2A/supplier_details.html'

class GSTR2ADeleteView(DeleteView):
    template_name = 'GSTR2A/GSRT2A_confirm_delete.html'
    model = GSRT2A
    context_object_name = 'deleteGSRT2A'
    success_url = reverse_lazy("GST2A:gst2Input")

class GSTR2AList(ListView):

    model = GSRT2A
    context_object_name = 'viewGSRT2A'
    template_name = 'GSTR2A/view_GSRT2A.html'

def search(request):
    model = GSRT2A
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            viewGSRT2A = model.objects.filter(Invoice_number=q)
            return render(request, 'GSTR2A/view_GSRT2A.html', {'viewGSRT2A': viewGSRT2A, 'query': q})
    return render(request, 'bill/index.html', {'error': error})

def autocomplete_Supplier(request):
    model = GSRT2A
    q= request.GET.get('term')
    print(q)
    qs =model.objects.filter(Q(Supplier_name__icontains = q)|Q(GSTIN_of_Supplier__istartswith = q))
    item_name_lst =list()
    for item in qs.values():
        val = "GST Num:"+item['GSTIN_of_Supplier']+','+"Name:"+item['Supplier_name']
        if val not in item_name_lst:
            item_name_lst.append(val)
        #item_cat_lst.append(item['Item_Catogory'])
        #item_sp_lst.append(item['Rate_Of_Sale'])
        
    return JsonResponse(item_name_lst,safe=False)

def GSTR2AFilling(request):
    
    model = GSRT2A
    startdate = request.GET.get('id_start_date')
    enddate = request.GET.get('id_end_date')
    Supplier = request.GET.get('id_Supplier')
    due_or_all = request.GET.get('id_due_or_all')
    #print(Supplier)
    if startdate == "":
        startdate = datetime.datetime(2018, 1, 1)
    if enddate =="":
        enddate = datetime.datetime.now()
    if re.search('GST\sNum\:.+,Name\:.+$',Supplier):
        m = re.search('GST\sNum\:(.+),Name\:(.+)$',Supplier)
        qs =model.objects.filter(Q(Supplier_name__iexact=m.group(2))&Q(GSTIN_of_Supplier__istartswith = m.group(1))&Q(Invoice_date__range=(startdate, enddate))).order_by('Invoice_date')
    else:
        qs =model.objects.filter(Q(Invoice_date__range=(startdate, enddate))).order_by('Invoice_date')
    #print(qs)
    return render(request, 'GSTR2A/gst2_rep.html', {'search_result': qs})
    

def gst2Input(request):
    print("gst1Input")
    return render(request,'GSTR2A/gst2.html')

def autocomplete(request):
    model = GSRT2A
    q= request.GET.get('term')
    qs =model.objects.filter(Supplier_name__istartswith = q)
    item_name_lst =list()
    for item in qs.values():
        #print(item)
        sp = item['Supplier_name']
        if sp not in item_name_lst:
            item_name_lst.append(sp)   
    return JsonResponse(item_name_lst,safe=False)

def autocomplete_gst_no(request):
    model = GSRT2A
    q= request.GET.get('term')
    qs =model.objects.filter(GSTIN_of_Supplier__istartswith = q)
    item_name_lst =list()
    for item in qs.values():
        #print(item)
        sp = item['GSTIN_of_Supplier']
        if sp not in item_name_lst:
            item_name_lst.append(sp)   
    return JsonResponse(item_name_lst,safe=False)