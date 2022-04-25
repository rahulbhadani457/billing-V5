from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,ListView,DeleteView,CreateView,UpdateView
from . import models
from print.models import salesDb
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
import re

# Create your views here.


#  bill index page
class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'index.html'
class stock(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'bill/stock-main.html'


class AdminView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'admin.html'


class ReportView(TemplateView):
        # Just set this Class Object Attribute to the template page.
        # template_name = 'app_name/site.html'
    template_name = 'report.html'


# bill gst view page to use in admin place only
class gstAdminListView(ListView):
    model = models.billSaleEntry
    context_object_name = 'showsaledata_admin_gst'
    queryset = model.objects.filter(GST_Type='Y').order_by('Item_Code')
    template_name = 'admin/showsaledata_admin_gst.html'


# bill no gst view page to use in admin place only
class nogstAdminListView(ListView):
    model = models.billSaleEntry
    context_object_name = 'showsaledata_admin_nogst'
    queryset = model.objects.filter(GST_Type='N').order_by('Item_Code')
    template_name = 'admin/showsaledata_admin_nogst.html'


# bill gst view page to use in normal place only
class gstListView(ListView):

    model = models.billSaleEntry
    context_object_name = 'showsaledata_gst'
    queryset = model.objects.filter(GST_Type='Y').order_by('Item_Code')
    template_name = 'bill/showsaledata_gst.html'


# bill no gst view page to use in normal place only
class nogstListView(ListView):

    model = models.billSaleEntry
    context_object_name = 'showsaledata_nogst'
    queryset = model.objects.filter(GST_Type='N').order_by('Item_Code')
    template_name = 'bill/showsaledata_noGST.html'


class gstDetailView(DetailView):
    context_object_name = 'gst_details'
    model = models.billSaleEntry
    template_name = 'bill/gst_detail.html'


class CreateSaleEntry(CreateView):
    fields = ('Item_Name','Item_Catogory','HSN_Code','Quatity_Bought','Unit','Rate_Of_Purchase','Rate_Of_Sale','IGST_Percent','CGST_Percent','SGST_Percent','GST_Type')
    model = models.billSaleEntry
    context_object_name = 'CreateSaleEntry'
    #success_url = reverse_lazy("bill:detail")
    def get_initial(self):
        initial = super(CreateSaleEntry, self).get_initial()
        initial['GST_Type'] = 'Y'
        initial['CGST_Percent'] = 0
        initial['IGST_Percent'] = 0
        initial['SGST_Percent'] = 0
        return initial

class CreateSaleEntryView(ListView):

    model = models.billSaleEntry
    context_object_name = 'showsaledata_nogst'
    queryset = model.objects.filter(GST_Type='N').order_by('Item_Code')
    template_name = 'bill/showsaledata_noGST.html'

class updateSaleEntry(UpdateView):
    fields = ('Item_Name','Item_Catogory','HSN_Code','Quatity_Bought','Unit','Rate_Of_Purchase','Rate_Of_Sale','IGST_Percent','CGST_Percent','SGST_Percent','GST_Type')
    model = models.billSaleEntry
    
    #def get_queryset(self,*args):
        #a = models.billSaleEntry.objects.filter(Item_Code__pk=self.kwargs[pk])
        
        #print(args)
    #initial = {'Quatity_Bought': model}
    #}
    context_object_name = 'updateSaleEntry'
    #success_url = reverse_lazy("bill:viewSales")


class billDeleteView(DeleteView):
    template_name = 'bill/billsaleentry_confirm_delete.html'
    context_object_name = 'billDeleteView'
    model = models.billSaleEntry
    success_url = reverse_lazy("bill:viewSales")

class viewSales(ListView):

    model = models.billSaleEntry
    context_object_name = 'viewSales'
    template_name = 'bill/view_sales.html'

def Estimate(request):
    request.session['bill_type']='EST'
    salesDb.objects.filter(session_id=request.session.session_key).delete()
    return render(request, 'print/stateOfSupply.html')

def Invoice(request):
    request.session['bill_type']='IN'
    salesDb.objects.filter(session_id=request.session.session_key).delete()
    return render(request, 'print/stateOfSupply.html')

def search(request):
    model = models.billSaleEntry
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if re.search('^.+\,.+\,SELL\:[0-9]+\.[0-9]+\,code\:[0-9]+$',q):
            print("inside")
            result = re.split('\,',q)
            q = result[0]
        if not q:
            error = True
        else:
            search_result = model.objects.filter(Q(Item_Code__iexact=q)|Q(Item_Name__icontains=q)|Q(Item_Catogory__icontains=q))
            return render(request, 'search.html', {'search_result': search_result, 'query': q})
    return render(request, 'bill/index.html', {'error': error})

def autocomplete(request):
    model = models.billSaleEntry
    q= request.GET.get('term')
    qs =model.objects.filter(Q(Item_Code__iexact=q)|Q(Item_Name__istartswith = q)|Q(Item_Catogory__icontains=q)).values('Item_Name')
    item_name_lst =list()
    for item in qs.values():
        sp = item['Rate_Of_Sale']
        sper = item['IGST_Percent'] +item['SGST_Percent']+item['CGST_Percent']
        sp_ajax = sp+sp*(sper/100)
        val = item['Item_Name']+','+item['Item_Catogory']+',SELL:'+str(sp_ajax)+',code:'+str(item['Item_Code'])
        item_name_lst.append(val)
        
    return JsonResponse(item_name_lst,safe=False)
def autocomplete_Catogory(request):
    model = models.billSaleEntry
    q= request.GET.get('term')
    qs =model.objects.filter(Item_Catogory__istartswith = q).values('Item_Catogory')
    item_name_lst =list()
    for item in qs.values():
        val = item['Item_Catogory']
        if val not in item_name_lst:
            item_name_lst.append(val)
        
    return JsonResponse(item_name_lst,safe=False)
    #sreturn(request,'bill/base.html')



def search_form(request):
    return render(request, 'base.html')

def stateOfSupply(request):
    placeOfSupply = request.GET.get('placeOfSupply')
    request.session['placeOfSupply']=placeOfSupply
    print("Hello stateOfSupply"+placeOfSupply)
    return render(request,'print/view_bill.html')

#def 