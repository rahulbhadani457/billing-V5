from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,ListView,DeleteView,CreateView,UpdateView,View
from .models import salesDb
from bill.models import billSaleEntry
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from .forms import printForm,estimateForm
from django.db.models import Sum
from adminreport.models import SaleReport,CustDetail
from num2words import num2words
from datetime import datetime
from django.http.response import JsonResponse
import re

# Create your views here.
ros =0
Qua =0
cgst =0
sgst =0
igst =0
total = 0
total_cgst= 0
total_igst= 0
total_sgst= 0
TotalNoGST = 0

def autocomplete(request):
    model = billSaleEntry
    q= request.GET.get('term')
    qs =model.objects.filter(Q(Item_Code__iexact=q)|Q(Item_Name__istartswith = q)).values('Item_Name')
    item_name_lst =list()
    for item in qs.values():
        #print(item)
        sp = item['Rate_Of_Sale']
        sper = item['IGST_Percent'] +item['SGST_Percent']+item['CGST_Percent']
        sp_ajax = sp+sp*(sper/100)
        val = item['Item_Name']+','+item['Item_Catogory']+',SELL:'+str(sp_ajax)+',code:'+str(item['Item_Code'])
        item_name_lst.append(val)
        #item_cat_lst.append(item['Item_Catogory'])
        #item_sp_lst.append(item['Rate_Of_Sale'])
        
    return JsonResponse(item_name_lst,safe=False)

#  bill index page
class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'index.html'

#bill index page
class printview(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'print/index.html'

#calculation of GST
def gst_cal(rateOfSale,gst,quat):
    cal = rateOfSale*quat*gst
    ret_cal =cal/100
    ret_tot =float("{0:.2f}".format(ret_cal))
    return ret_tot

#calculation of total EXCLUDING  GST
def totalNoGST(rateOfSale,quat):
    cal = rateOfSale*quat
    ret_tot =float("{0:.2f}".format(cal))
    return ret_tot

#Create/update item by search result (this is on confirmation page)
def get_print_Form(request):
    q = request.POST['q']
    request.session["q"] = q
    printVals = billSaleEntry.objects.filter(Item_Code__exact=q)
    for printVal in printVals:
        initial_data ={

            "ItemCode" :printVal.Item_Code,
            "ItemName" :printVal.Item_Name
             }
    return render(request,"print/print_add_confirm.html",context=initial_data)

#Create/Update item by search result (Most valve are retived from billSaleEntry only quantity and rate of sale
# can be edited)
#It is use to calculate some values on input
def post_print_Form(request):
    
    q = request.session['q']
    placeOfSupply= request.session['placeOfSupply']
    bill_type=request.session['bill_type']
    #print("q=",q)
    #print("bill_type=",bill_type)
    printVals = billSaleEntry.objects.filter(Item_Code__exact=q)
    #print("printvals",printVals)
    if bill_type=='IN':
        my_form = printForm()
    else:
        my_form = estimateForm()
    #print("My orm",my_form)
    for printVal in printVals:
        tot_gst = printVal.IGST_Percent+printVal.SGST_Percent+printVal.CGST_Percent
        if placeOfSupply =="Bihar(10)":
            IGST_Per_Val=0
            SGST_Per_Val=float("{0:.2f}".format(tot_gst/2))
            CGST_Per_Val=float("{0:.2f}".format(tot_gst/2))
        
        else:
            IGST_Per_Val=float("{0:.2f}".format(tot_gst))
            SGST_Per_Val=0
            CGST_Per_Val=0
        #print(IGST_Per_Val,SGST_Per_Val,CGST_Per_Val)
        initial_data ={

            "Item_Code" :printVal.Item_Code,
            "Item_Name" :printVal.Item_Name,
            "Item_Catogory":printVal.Item_Catogory,
            "HSN_Code" :printVal.HSN_Code,
            "Unit" :printVal.Unit,
            "Rate_Of_Sale" :printVal.Rate_Of_Sale,
            "Rate_Of_Purchase" :printVal.Rate_Of_Purchase,
            "IGST_Percent" : IGST_Per_Val,
            "SGST_Percent" : SGST_Per_Val,
            "CGST_Percent" : CGST_Per_Val,
            "GST_Type" : printVal.GST_Type 

            }   
    if bill_type=='IN':
        my_form = printForm(request.POST or None,initial=initial_data)
    else:
        my_form = estimateForm(request.POST or None,initial=initial_data)
    
    if my_form.is_valid():
        global ros,Qua,cgst,sgst,igst,total,totalNoGST,total_cgst,total_igst,total_sgst,NoGST
        ros = my_form.cleaned_data["Rate_Of_Sale"]
        Qua = my_form.cleaned_data["Quatity_Sold"]
        cgst = my_form.cleaned_data["CGST_Percent"]
        igst = my_form.cleaned_data["IGST_Percent"]
        sgst = my_form.cleaned_data["SGST_Percent"]
        total_cgst = gst_cal(ros,cgst,Qua)
        total_igst = gst_cal(ros,igst,Qua)
        total_sgst = gst_cal(ros,sgst,Qua)
        NoGST = totalNoGST(ros,Qua)
        total = float("{0:.2f}".format(NoGST+total_cgst+total_igst+total_sgst))
        my_form.cleaned_data['Total']= total
        my_form.cleaned_data['Gross_Total']=  NoGST
        my_form.cleaned_data['Total_CGST']= total_cgst
        my_form.cleaned_data['Total_IGST']= total_igst
        my_form.cleaned_data['Total_SGST']= total_sgst
        my_form.cleaned_data['session_id'] = request.session.session_key
        #print(my_form.cleaned_data)
        salesDb(**my_form.cleaned_data).save()
        return HttpResponseRedirect(reverse('print:viewprint'))


    #del request.session["q"]
    return render(request,"print/print_form_create.html",{"form":my_form})

# create list view for all entry of printing database

def viewprint(request):
    bill_type=request.session['bill_type']
    placeOfSupply= request.session['placeOfSupply']
    
    #if bill_type=='IN':

    viewprint = salesDb.objects.filter(session_id=request.session.session_key).order_by('-insert_date')
    session_id = request.session.session_key
    session = request.user
    #print(session_id)
    #print(viewprint)
    error_list = list()
    checkList = list()
    for itemLoop in viewprint.values():
        if itemLoop['Item_Code'] not in checkList:
            checkList.append(itemLoop['Item_Code'])
        else:
            error_list.append(itemLoop['Item_Code'])
    #print(error_list)
        
    grandTotal = float("{0:.2f}".format(salesDb.objects.filter(session_id=request.session.session_key).aggregate(Sum('Total'))['Total__sum'] or 0.00))
    contexDict = {'viewprint':viewprint,
                    'grandTotal':grandTotal,
                    'bill_type':bill_type,
                    'placeOfSupply':placeOfSupply,
                    'errorList':error_list,}

    return render(request,'print/view_bill.html',context=contexDict)

def testPrint(request):
    #bill_type=request.session['bill_type']
    #placeOfSupply= request.session['placeOfSupply']
    
    #if bill_type=='IN':

    viewprint = salesDb.objects.filter(session_id=request.session.session_key)
    for i in viewprint:
        i.Rate_Of_Sale = float("{0:.2f}".format(i.Rate_Of_Sale + (i.IGST_Percent + i.CGST_Percent + i.SGST_Percent)*(i.Rate_Of_Sale/100)))
    grandTotal = float("{0:.2f}".format(salesDb.objects.filter(session_id=request.session.session_key).aggregate(Sum('Total'))['Total__sum'] or 0.00))
    contexDict = {'viewprint':viewprint,
                    'grandTotal':grandTotal
                    }
    salesDb.objects.filter(session_id=request.session.session_key).delete()

    return render(request,'print/test.html',context=contexDict)

#Update item by primary key (Most valve are retived from billSaleEntry only quantity and rate of sale
# can be edited)
#It is use to calculate some values on input  
def update_print_Form(request,pk):
    bill_type=request.session['bill_type']
    printVal = salesDb.objects.get(id =pk)
    
    initial_data ={
            "Item_Code" :printVal.Item_Code,
            "Item_Name" :printVal.Item_Name,
            "Quatity_Sold": printVal.Quatity_Sold,
            "Item_Catogory":printVal.Item_Catogory,
            "HSN_Code" :printVal.HSN_Code,
            "Unit" :printVal.Unit,
            "Rate_Of_Sale" :printVal.Rate_Of_Sale,
            "IGST_Percent" : printVal.IGST_Percent,
            "SGST_Percent" : printVal.SGST_Percent,
            "CGST_Percent" : printVal.CGST_Percent,
            "GST_Type" : printVal.GST_Type

             }     
    if bill_type=='IN':
        my_form = printForm(request.POST or None,initial=initial_data)
    else:
        my_form = estimateForm(request.POST or None,initial=initial_data)
    
    if my_form.is_valid():
        global ros,Qua,cgst,sgst,igst,total,totalNoGST,total_cgst,total_igst,total_sgst,NoGST
        my_form.cleaned_data['id']= pk
        ros = my_form.cleaned_data["Rate_Of_Sale"]
        Qua = my_form.cleaned_data["Quatity_Sold"]
        cgst = my_form.cleaned_data["CGST_Percent"]
        igst = my_form.cleaned_data["IGST_Percent"]
        sgst = my_form.cleaned_data["SGST_Percent"]
        total_cgst = gst_cal(ros,cgst,Qua)
        total_igst = gst_cal(ros,igst,Qua)
        total_sgst = gst_cal(ros,sgst,Qua)
        NoGST = totalNoGST(ros,Qua)
        total = float("{0:.2f}".format(NoGST+total_cgst+total_igst+total_sgst))
        my_form.cleaned_data['Total']= total
        my_form.cleaned_data['Gross_Total']=  NoGST
        my_form.cleaned_data['Total_CGST']= total_cgst
        my_form.cleaned_data['Total_IGST']= total_igst
        my_form.cleaned_data['Total_SGST']= total_sgst
        my_form.cleaned_data['session_id']=request.session.session_key
 
        salesDb(**my_form.cleaned_data).save()
        
        return HttpResponseRedirect(reverse('print:viewprint'))

    return render(request,"print/print_form_create.html",{"form":my_form})

#delete values from print database
class printDeleteView(DeleteView):
    template_name = 'print/printdb_confirm_delete.html'
    context_object_name = 'printDeleteView'
    model = salesDb
    success_url = reverse_lazy("print:viewprint")

#GST invoice creation
class invoicePrintView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'print/invoice bill.html'

def InvoicePrint(request):

    InvNumber = request.session['inv_no']
    bill_type=request.session['bill_type']
    cust_id = request.session['cust_id']
    
    #print("InvoicePrint"+placeOfSupply)
    if bill_type=='IN':
        Inv_type_set = 'IN'
    else:
        Inv_type_set = 'EST'
    ItemsDetails = SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).order_by('Item_Catogory')
    placeOfSupply= request.session['placeOfSupply']
    if placeOfSupply!=0:
        #print("hello1",placeOfSupply)
        duplicate_bill =False
        for items in ItemsDetails:
            inv_date = items.Inv_Date
            break
    else:
        for items in ItemsDetails:
            inv_date = items.Inv_Date
            placeOfSupply = items.place_of_supply
            #print(placeOfSupply)
            duplicate_bill = True
            break 
    
    inv_date_str = inv_date.strftime('%d-%m-%Y')
    #print(inv_date_str)

    CustDetails = CustDetail.objects.filter(Cust_Id =cust_id)
    IGSTTotal = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Igst_Tot_Sale'))['Igst_Tot_Sale__sum']))
    CGSTTotal = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Cgst_Tot_Sale'))['Cgst_Tot_Sale__sum']))
    SGSTTotal = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Sgst_Tot_Sale'))['Sgst_Tot_Sale__sum']))
    IGSTper = SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).values_list('Igst_Percent_Sale')[0]
    CGSTper = SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).values_list('Cgst_Percent_Sale')[0]
    SGSTper = SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).values_list('Sgst_Percent_Sale')[0]
    Total = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Total_Sale'))['Total_Sale__sum']))
    Taxable_Amount = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Total_No_Tax_Sale'))['Total_No_Tax_Sale__sum']))
    round_amount = round(Total)
    round_off_diff = float("{0:.2f}".format(Total-round_amount))
    
    if round_amount<Total:
        round_off_diff = float("{0:.2f}".format(Total-round_amount))

        print_round_off_diff = '-'+str(round_off_diff)
    else:
        round_off_diff = float("{0:.2f}".format(round_amount-Total))
        print_round_off_diff = '+'+str(round_off_diff)


    print(round_off_diff)
    print(print_round_off_diff)
    Total_in_word = (num2words(round_amount,lang='en_IN')).capitalize()
    total_tax = float("{0:.2f}".format(IGSTTotal +CGSTTotal+SGSTTotal))
    for i in ItemsDetails:
        cancel = i.Bill_Cancel
        #print(cancel)
        break
    sum_per = IGSTper[0]+CGSTper[0]+SGSTper[0]
    #print(sum_per)

    context_dict ={'InvNumber':InvNumber,
                    'cust_id':cust_id,
                    'ItemsDetails':ItemsDetails,
                    'CustDetails':CustDetails,
                    'IGSTTotal':IGSTTotal,
                    'CGSTTotal':CGSTTotal,
                    'SGSTTotal':SGSTTotal,
                    'Total':Total,
                    'Taxable_Amount':Taxable_Amount,
                    'Total_in_word':Total_in_word,
                    'total_tax':total_tax,
                    'placeOfSupply':placeOfSupply,
                    'inv_date':inv_date_str,
                    'duplicate_bill':duplicate_bill,
                    'cancel':cancel,
                    'sum_per':sum_per,
                    'round_amount':round_amount,
                    'print_round_off_diff':print_round_off_diff
    }
    #del request.session['q']
    #del request.session['inv_no']
    #del request.session['bill_type']
    #del request.session['cust_id']
    if (bill_type=='IN' and placeOfSupply =="Bihar(10)") :
        return render(request,"print/invoice bill.html",context=context_dict)
    elif(bill_type=='IN' and placeOfSupply !="Bihar(10)"):
        return render(request,"print/invoiceBillIgst.html",context=context_dict)
    else:
        return render(request,"print/Estimate bill.html",context=context_dict)


def quick_print_Form(request):
    
    q = request.GET['q']
    if 'q' in request.GET:
        q = request.GET['q']
        if re.search('^.+\,.+\,SELL\:[0-9]+\.[0-9]+\,code\:[0-9]+$',q):
            result = re.split('\,',q)
            m = re.findall("\:([0-9]+)$", result[3])
            q = m[0]
            #print(q)
   

    Quat = request.GET['Quat']
    placeOfSupply= request.session['placeOfSupply']
    bill_type=request.session['bill_type']
    try:
        q1=int(q)
    except Exception:
        dic = {'error':'"'+q+'" is invalid, select number from suggestion or enter correct Item code'}
        return render(request,'print/error_add_billing.html',context=dic)
    try:
        Quat1 = float(Quat)
    except Exception:
        dic = {'error':'"'+Quat+'" is not number Quatity should be number'}
        return render(request,'print/error_add_billing.html',context=dic)
    
    printVals = billSaleEntry.objects.filter(Item_Code__exact=q)
    dic= {}
    dic['Itemcode_got']= q
    if not printVals:
        dic = {'error':'"'+q+'" is not present enter correct Item code'}
        return render(request,'print/error_add_billing.html',context=dic)
        #return render(request,'print/error_add_billing.html',context=dic)
    else:
        #print("printvals",printVals)

        for printVal in printVals:

            global ros,Qua,cgst,sgst,igst,total,totalNoGST,total_cgst,total_igst,total_sgst,NoGST
            tot_gst = printVal.IGST_Percent+printVal.SGST_Percent+printVal.CGST_Percent
            if placeOfSupply =="Bihar(10)":
                IGST_Per_Val=0
                SGST_Per_Val=float("{0:.2f}".format(tot_gst/2))
                CGST_Per_Val=float("{0:.2f}".format(tot_gst/2))

            else:
                IGST_Per_Val=float("{0:.2f}".format(tot_gst))
                SGST_Per_Val=0
                CGST_Per_Val=0
            Qua = float(Quat)
            data ={

            "Item_Code" :printVal.Item_Code,
            "Item_Name" :printVal.Item_Name,
            "Item_Catogory":printVal.Item_Catogory,
            "HSN_Code" :printVal.HSN_Code,
            "Quatity_Sold":Quat,
            "Unit" :printVal.Unit,
            "Rate_Of_Sale" :printVal.Rate_Of_Sale,
            "Rate_Of_Purchase" :printVal.Rate_Of_Purchase,
            "IGST_Percent" : IGST_Per_Val,
            "SGST_Percent" : SGST_Per_Val,
            "CGST_Percent" : CGST_Per_Val,
            "GST_Type" : printVal.GST_Type,
            'session_id' : request.session.session_key
            }
        sellPrice = request.GET['sellPrice']

        if sellPrice !='':
            try:
                sellPrice = float(sellPrice)
            except Exception:
                dic = {'error':'"'+sellPrice+'" is not number Quatity should be number'}
                return render(request,'print/error_add_billing.html',context=dic)
            sp = (sellPrice*100)/(100+CGST_Per_Val+IGST_Per_Val+SGST_Per_Val)
            ros = float("{0:.2f}".format(sp))
            data['Rate_Of_Sale']= ros
        else:
            ros = printVal.Rate_Of_Sale

        total_cgst = gst_cal(ros,CGST_Per_Val,Qua)
        total_igst = gst_cal(ros,IGST_Per_Val,Qua)
        total_sgst = gst_cal(ros,SGST_Per_Val,Qua)
        NoGST = totalNoGST(ros,Qua)
        total = float("{0:.2f}".format(NoGST+total_cgst+total_igst+total_sgst))
        data['Total']= total
        data['Gross_Total']=  NoGST
        data['Total_CGST']= total_cgst
        data['Total_IGST']= total_igst
        data['Total_SGST']= total_sgst
        
        salesDb(**data).save()
        return HttpResponseRedirect(reverse('print:viewprint'))