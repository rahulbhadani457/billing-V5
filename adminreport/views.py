import re
from datetime import datetime
from django.http.response import JsonResponse
from django.views.generic import ListView,DeleteView,UpdateView,DetailView
from datetime import datetime
from django.shortcuts import redirect, render
from .models import CustDetail,SaleReport,invoicenumber,estimatenumber,Cust_payment_record
from django.views.generic import TemplateView
from .forms import CustForm,salesForm,cancleInvoice,payment_udpate
from print.models import salesDb
from bill.models import billSaleEntry
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from datetime import date
from django.db import connection
from django.db.models import Q
from django.db.models import Sum
import os
import csv
from django import template
register = template.Library()

# Create your views here.
@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

def autocomplete_cust_search(request):
    model = CustDetail
    q= request.GET.get('term')
    qs =model.objects.filter(Q(Mob_No__istartswith=q)|Q(Customer_Name__istartswith = q)).values('Customer_Name')
    item_name_lst =list()
    for item in qs.values():
        val = item['Customer_Name']+','+item['Address']+',Mobile Num:'+item['Mob_No']+',id:'+str(item['Cust_Id'])
        item_name_lst.append(val)

    return JsonResponse(item_name_lst,safe=False)

# Create New customer and create database entry CustDetail also create new invoice number
def SubCustForm(request,id,customer_no):

    bill_type=request.session['bill_type']
    place_of_supply = request.session['placeOfSupply']
    if bill_type=='IN':
        invoicenumber.objects.create(Cust_Id=id)
        for InvNo1 in invoicenumber.objects.raw('select Inv_No from adminreport_invoicenumber where Cust_Id_id= %s',[customer_no]):
             InvNumber1 = InvNo1.Inv_No
    else:
        estimatenumber.objects.create(Cust_Id=id)
        for InvNo1 in invoicenumber.objects.raw('select Inv_No from adminreport_estimatenumber where Cust_Id_id= %s',[customer_no]):
            InvNumber1 = InvNo1.Inv_No
    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT A.Item_Code, A.Item_Name, A.Item_Catogory, A.HSN_Code, A.Quatity_Sold, A.Unit,
             A.Rate_Of_Sale, A.IGST_Percent, A.CGST_Percent, A.SGST_Percent,A.Total_IGST,A.Total_CGST, 
             A.Total_SGST, A.Gross_Total, A.Total, B.CGST_Percent, B.SGST_Percent, B.IGST_Percent,
             B.Rate_Of_Purchase, B.Quatity_Bought ,B.Quatity_in_stock
             FROM 
             bill.print_salesdb as A left join bill.bill_billsaleentry AS B on A.Item_Code=B.Item_Code where A.session_id = %s""",[request.session.session_key])
        rows = cursor.fetchall()
            
        for row in rows:
            Item_Code_tab =row[0]
            Quatity_Bought =row[19]
            Quatity_in_stock =row[20]         
            Quatity_Bought_Sale =row[4]
            Unit_Price_Purchase = row[18]
            Cgst_Percent_Purchase = row[15]
            Sgst_Percent_Purchase = row[16]
            Igst_Percent_Purchase = row[17]
            Total_Sale =row[14]
            Unit_Sale =row[5]
            Total_No_Tax_Sale =row[13]
            Quatity_in_stock_tab =Quatity_in_stock-Quatity_Bought_Sale
            #print("SubCustForm",Unit_Sale)

            if Unit_Sale =='CHK':
                Unit_Conversion_Val_GST = 4
                Converted_Unit_GST ="PCS"
            elif Unit_Sale == 'JODA':
                Unit_Conversion_Val_GST = 2
                Converted_Unit_GST ="PCS"
            else:
                Unit_Conversion_Val_GST = 1
                Converted_Unit_GST =Unit_Sale
            Total_No_Tax_Purchase= Unit_Price_Purchase*Quatity_Bought_Sale
            Cgst_Tot_Purchase =float("{0:.2f}".format(Total_No_Tax_Purchase*(Cgst_Percent_Purchase/100)))
            Sgst_Tot_Purchase = float("{0:.2f}".format(Total_No_Tax_Purchase*(Sgst_Percent_Purchase/100)))
            Igst_Tot_Purchase = float("{0:.2f}".format(Total_No_Tax_Purchase*(Igst_Percent_Purchase/100)))
            Total_Purchase = float("{0:.2f}".format(Total_No_Tax_Purchase+Cgst_Tot_Purchase+Sgst_Tot_Purchase+Igst_Tot_Purchase))
            Converted_Unit_Val_GST = float("{0:.2f}".format(Unit_Conversion_Val_GST*Quatity_Bought_Sale))
            Unit_Nett_Price_Sale = float("{0:.2f}".format(row[6]+row[6]*(row[7]+row[8]+row[9])/100))
                
            if bill_type=='IN':
                Profit = float("{0:.2f}".format(Total_No_Tax_Sale- Total_No_Tax_Purchase))
                Profit_Percent = float("{0:.2f}".format(((Profit*100)/Total_No_Tax_Purchase)))
                Inv_Type='IN'

            else:
                Profit = float("{0:.2f}".format(Total_Sale- Total_Purchase))
                Profit_Percent = float("{0:.2f}".format(((Profit*100)/Total_Purchase)))
                Inv_Type='EST'

            insert_dict ={"Inv_Type":Inv_Type,
                "Inv_No":InvNumber1,
                "Item_Code" : row[0],
                "Item_Name" : row[1],
                "Item_Catogory" : row[2],
                "Hsn_Code" : row[3],
                "Quatity_Bought_Sale" : row[4],
                "Unit_Sale" : row[5],
                "Unit_Price_Sale" : row[6],
                "Unit_Nett_Price_Sale":Unit_Nett_Price_Sale,
                "Igst_Percent_Sale" : row[7],
                "Cgst_Percent_Sale" : row[8],
                "Sgst_Percent_Sale" : row[9],
                "Igst_Tot_Sale" : row[10],
                "Cgst_Tot_Sale" : row[11],
                "Sgst_Tot_Sale" : row[12],
                "Total_No_Tax_Sale" : row[13],
                "Total_Sale" : row[14],
                "Cgst_Percent_Purchase" : row[15],
                "Sgst_Percent_Purchase" : row[16],
                "Igst_Percent_Purchase" : row[17],
                "Unit_Price_Purchase" : row[18],
                "Unit_Conversion_Val_GST" : Unit_Conversion_Val_GST,
                "Converted_Unit_GST" : Converted_Unit_GST,
                "Converted_Unit_Val_GST" : Converted_Unit_Val_GST,
                "Cgst_Tot_Purchase" : Cgst_Tot_Purchase,
                "Sgst_Tot_Purchase" : Sgst_Tot_Purchase,
                "Igst_Tot_Purchase" : Igst_Tot_Purchase,
                "Total_Purchase" : Total_Purchase,
                "Total_No_Tax_Purchase" : Total_No_Tax_Purchase,
                "Profit" : Profit,
                "Profit_Percent" : Profit_Percent,
                "Cust_Id" :id,
                'place_of_supply':place_of_supply,
                'mis1':request.user
                }
            SaleReport.objects.create(**insert_dict)
            billSaleEntry.objects.filter(Q(Item_Code=Item_Code_tab)).update(Quatity_in_stock=Quatity_in_stock_tab)
            insert_dict={}
        salesDb.objects.filter(session_id=request.session.session_key).delete()
        request.session['inv_no']= InvNumber1
        request.session['cust_id']= customer_no

def NewCustForm(request):
    
    my_form = CustForm(request.POST or None)
    place_of_supply = request.session['placeOfSupply']
    if my_form.is_valid():
        supply_state = place_of_supply.split('(')[0]
        #print(supply_state)
        my_form.cleaned_data['State'] = supply_state
        CustDetail(**my_form.cleaned_data).save()
        cust_name = (my_form.cleaned_data['Customer_Name'])
        #get customer number from inserted row
        sql  = "select Cust_Id from adminreport_custdetail where Customer_Name= '"+cust_name+"' ORDER BY Cust_Id DESC LIMIT 1"
        for id in CustDetail.objects.raw(sql):
            #print('id',id)
            #print('cust id',Cust_Id)
            customer_no =id.Cust_Id
        #print("cust id")
        #print(id)
        SubCustForm(request,id,customer_no)
        return HttpResponseRedirect(reverse('adminrep:payment'))
    else:
        print("hwllo")
 
    return render(request,"adminreport/cust_form_create.html",{"form":my_form})

def oldCustForm(request):
    q = request.GET['cust_search']
    my_form = CustForm(request.POST or None)
    if 'cust_search' in request.GET:
        q = request.GET['cust_search']
        #print(q)
        if re.search('^.+\,.+\,Mobile\sNum\:[0-9]+,id\:[0-9]+$',q):
            m = re.findall("id\:([0-9]+)$", q)
            q = m[0]
        else:
             return render(request,"adminreport/cust_form_create.html",{"form":my_form,'error':True})
        #get customer number from inserted row
        sql  = "select Cust_Id from adminreport_custdetail where Cust_Id= '"+q+"' ORDER BY Cust_Id DESC LIMIT 1"
        for id in CustDetail.objects.raw(sql):
            #print('id',id)
            #print('cust id',Cust_Id)
            customer_no =id.Cust_Id
        #print("cust id")
        #print(id)
        SubCustForm(request,id,customer_no)
        return HttpResponseRedirect(reverse('adminrep:payment'))
 
    return render(request,"adminreport/cust_form_create.html",{"form":my_form})

def payment(request):
    InvNumber = request.session['inv_no']
    bill_type=request.session['bill_type']
    initial_data = {'payment_Amount':0}
    payform = salesForm(request.POST or None,initial=initial_data)
    if bill_type=='IN':
        Inv_type_set = 'IN'
    else:
        Inv_type_set = 'EST'
        
    
    grandTotal = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Total_Sale'))['Total_Sale__sum'] or 0.00))        
    
    if payform.is_valid():

        #payform.cleaned_data['Total']= total
        if bill_type=='IN':
            Inv_type_set = 'IN'
        else:
            Inv_type_set = 'EST'
        
        
        grandTotal = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).aggregate(Sum('Total_Sale'))['Total_Sale__sum'] or 0.00))        
        cust_nums = SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=Inv_type_set)).values('Cust_Id')
        for cust_num in cust_nums:
            #print(cust_num)
            cust_num_update = cust_num['Cust_Id']
            break
        payment_made_val =payform.cleaned_data['payment_Amount']
        payment_Left =float("{0:.2f}".format(grandTotal - payment_made_val))
        payform.cleaned_data['payment_left'] = payment_Left
        payform.cleaned_data['inv_type'] = Inv_type_set
        payform.cleaned_data['inv_number'] = InvNumber
        payform.cleaned_data['total_bill_Amount'] = grandTotal
        payform.cleaned_data['current_payment_Date'] = datetime.today().strftime('%Y-%m-%d')
        payform.cleaned_data['Cust_Id'] = cust_num_update
        payform.cleaned_data['Comment'] = 'Payment while billing'
        payform.cleaned_data['is_last'] = True
        #print(payment_made_dict)
        #print(payform.cleaned_data)
        Cust_payment_record.objects.create(**payform.cleaned_data)
        
        return HttpResponseRedirect(reverse('print:InvoicePrint'))
    return render(request,"adminreport/payment.html",{"form":payform,"grandTotal":grandTotal})

def Invsearch_sub(request,Inv,q):
    pass
def Invsearch(request,Inv=None,q=None):
    
    #print('Invsearch 1st',Inv,q)
    if Inv== None:
        q = request.GET.get('q')
        Inv = request.GET.get('Inv')
        #print('Invsearch 2nd',Inv,q)
    
        if q is None:
            q = request.session['inv_no_reverse']
            Inv = request.session['bill_type_reverse']
            #print('Invsearch 3rd',Inv,q)

    search_result = SaleReport.objects.filter(Q(Inv_Type=Inv)&Q(Inv_No=q))
    grandTotal = float("{0:.2f}".format(SaleReport.objects.filter(Q(Inv_Type=Inv)&Q(Inv_No=q)).aggregate(Sum('Total_Sale'))['Total_Sale__sum'] or 0.00))
    custNo = SaleReport.objects.filter(Q(Inv_Type=Inv)&Q(Inv_No=q)).values('Cust_Id_id').first()
    try:
        for i in custNo.values():
            Cust_Id_val = i
    except Exception as e:
        return render(request, 'print/index.html',{'error':True,'Inv':Inv,'q':q})
    for i in custNo.values():
        Cust_Id_val = i
    CustDetails = CustDetail.objects.filter(Cust_Id=int(Cust_Id_val))

    data_val =Cust_payment_record.objects.filter(Q(inv_type=Inv)&Q(inv_number=q)).order_by('-id').first()
    payment_history =Cust_payment_record.objects.filter(Q(inv_type=Inv)&Q(inv_number=q)).order_by('id')
    #print(payment_history)
    try:
        left_amount =float("{0:.2f}".format( data_val.payment_left))
    except Exception as e:
        left_amount ="0"

    request.session['inv_no'] = q
    request.session['bill_type'] =Inv
    request.session['cust_id']= int(Cust_Id_val)
    request.session['placeOfSupply'] = 0
    
    returnVal ={
                'search_result':search_result,
                'CustDetails':CustDetails,
                'grandTotal':grandTotal,
                'left_amount':left_amount,
                'q':q,
                'inv':Inv,
                'payment_history':payment_history
               
    }
    
    
    return render(request, 'adminreport/Search_Inv.html', context=returnVal)


def paymentupdate(request):
    InvNumber = request.session['inv_no']
    bill_type=request.session['bill_type']


    payform = payment_udpate(request.POST or None)
    data_val =Cust_payment_record.objects.filter(Q(inv_number=InvNumber)&Q(inv_type=bill_type)).order_by('-id').first()
    payment_left_last_tansaction = data_val.payment_left
    grandTotal = data_val.total_bill_Amount
    cust_num_update = data_val.Cust_Id
    
    if payform.is_valid():     
  
        payment_made_val =payform.cleaned_data['payment_Amount']
        payment_Left =float("{0:.2f}".format(payment_left_last_tansaction - payment_made_val))
        payform.cleaned_data['payment_left'] = payment_Left
        payform.cleaned_data['inv_type'] = bill_type
        payform.cleaned_data['inv_number'] = InvNumber
        payform.cleaned_data['total_bill_Amount'] = grandTotal
        payform.cleaned_data['Cust_Id'] = cust_num_update
        payform.cleaned_data['is_last'] = True
        old_data = {'is_last':False}
        Cust_payment_record.objects.filter(Q(inv_number=InvNumber)&Q(inv_type=bill_type)).update(**old_data)
        Cust_payment_record.objects.create(**payform.cleaned_data)
        request.session['inv_no_reverse']=InvNumber 
        request.session['bill_type_reverse'] =bill_type
        return HttpResponseRedirect(reverse('adminrep:Invsearch'))
    return render(request,"adminreport/updatepayment.html",{"form":payform,"payment_left_last_tansaction":payment_left_last_tansaction,'InvNumber':InvNumber,'bill_type':bill_type})
    
def cancelInv(request):

    payform = cancleInvoice(request.POST or None)
    if payform.is_valid():
        InvNumber = request.session['inv_no']
        bill_type=request.session['bill_type']
        
        SaleReport.objects.filter(Q(Inv_No=InvNumber)&Q(Inv_Type=bill_type)).update(**payform.cleaned_data)
        request.session['inv_no_reverse']=InvNumber 
        request.session['bill_type_reverse'] =bill_type
        #HttpResponseRedirect.allowed_schemes.append('adminrep')
        return HttpResponseRedirect(reverse('adminrep:Invsearch'))
    
    return render(request,"adminreport/cancelInv.html",{"form":payform})


def GST1(request):
    if os.path.exists("salereport.csv"):
        os.remove("salereport.csv")
    
    enddate = request.GET['id_end_date']
    startdate= request.GET['id_start_date']
    cust_name = request.GET['id_cust_name']
    due_or_all = request.GET.get('id_due_or_all')
    sql ='''
    SELECT 
            a.Inv_Type,a.Inv_No,a.Inv_Date,a.Item_Name,a.Hsn_Code,a.Quatity_Bought_Sale,a.Unit_Sale,
            a.Converted_Unit_GST,a.Unit_Price_Sale,
            a.Converted_Unit_Val_GST,a.Igst_Percent_Sale,a.Cgst_Percent_Sale,a.Sgst_Percent_Sale,
            a.Igst_Tot_Sale,a.Cgst_Tot_Sale,a.Sgst_Tot_Sale,a.Total_No_Tax_Sale,a.Total_Sale,a.profit,
            a.Profit_Percent,a.Bill_Cancel,a.Bill_cancel_Date,a.comment,a.place_of_supply,
			B.Customer_Name,B.City,B.State,B.Mob_No,B.GSTN_of_Customer,B.Address,C.payment_left,
			C.total_bill_Amount
            FROM bill.adminreport_salereport 
            as a inner join bill.adminreport_custdetail AS B on a.Cust_Id_id=B.Cust_Id
            right join bill.adminreport_cust_payment_record as C
            on B.Cust_Id= C.Cust_Id and C.inv_type = a.Inv_Type and C.inv_number = a.Inv_No
            where a.Bill_Cancel IS NULL and C.is_last = True and a.Inv_Date>= %s and a.Inv_Date<= %s '''
    
    sql_download = sql
    if re.search('^.+\,.+\,Mobile\sNum\:[0-9]+,id\:[0-9]+$',cust_name):
        m = re.findall("id\:([0-9]+)$", cust_name)
        q = m[0]
        sql =  sql+ ' and C.Cust_Id = %s'
        sql_download = sql_download+ ' and C.Cust_Id = %s'
    
    sql = sql+' group by a.Inv_Type,a.Inv_No'

    if due_or_all =='Due':
        sql = sql+' having C.payment_left>1'
        sql_download = sql_download+' having C.payment_left>1'
    sql_download = sql_download+ ' order by a.Inv_Type asc ,a.Inv_no asc'
    sql = sql+' order by a.Inv_Type asc ,a.Inv_no asc'
    

    with connection.cursor() as cursor:
        try:
            cursor.execute(sql,[startdate,enddate,q])                
        except:
            #cursor.execute(sql_download,[startdate,enddate])
            cursor.execute(sql,[startdate,enddate])
        #print(sql)

        #rows = 
        columns = [col[0] for col in cursor.description]
        row_retuns = [dict(zip(columns, row)) for row in cursor.fetchall()]
        rows_download =sql_download
        #print(columns)
        total = 0

        for rows in row_retuns:
            #print(rows.get('total_bill_Amount'))
            total = total + float(rows.get('total_bill_Amount'))
            #print(rows.get('total_bill_Amount'))

        total = float("{0:.2f}".format(total))
        startdate1 = datetime.strptime(startdate, '%Y-%m-%d')
        enddate1 = datetime.strptime(enddate, '%Y-%m-%d')
 
        '''with open('salereport.csv','a+',newline='') as salereport:
            csvwriter = csv.writer(salereport)
            csvwriter.writerow(["Inv_Type","Inv_No","Inv_Date","Item_Name","Hsn_Code","Converted_Unit_GST","Converted_Unit_Val_GST","Igst_Percent_Sale","Cgst_Percent_Sale","Sgst_Percent_Sale","Igst_Tot_Sale","Cgst_Tot_Sale","Sgst_Tot_Sale","Total_No_Tax_Sale","Total_Sale","profit","Profit_Percent","Bill_Cancel","Customer_Name","GSTN_of_Customer"])
            for row in row_retuns:
                    csvwriter.writerow([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19]])
    #search_result =SaleReport.objects.filter(Q(Inv_Date__gte=startdate)&Q(Inv_Date__lte=enddate))'''
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql_download,[startdate,enddate,q])                
        except:
            #print(sql)
            cursor.execute(sql_download,[startdate,enddate])
        #print(sql)
        columns = [col[0] for col in cursor.description]
        row_return_parsings = [dict(zip(columns, row)) for row in cursor.fetchall()]        
        Hsn_Code = {}
        NoGstNum ={}
        bill_with_gst = {}

    for row in row_return_parsings:
        if row['Inv_Type'] == 'IN':
            supply=row['place_of_supply']
            if (len(row['GSTN_of_Customer']) != 15) and (supply in NoGstNum):
                NoGstNum[supply]['Total_without_tax'] = float("{0:.2f}".format(NoGstNum[supply]['Total_without_tax'] +row['Total_No_Tax_Sale']))
                NoGstNum[supply]['total_bill_Amount'] = float("{0:.2f}".format(NoGstNum[supply]['total_bill_Amount'] +row['Total_Sale']))
                NoGstNum[supply]['igst'] = float("{0:.2f}".format(NoGstNum[supply]['igst'] +row['Igst_Tot_Sale']))
                NoGstNum[supply]['cgst'] = float("{0:.2f}".format(NoGstNum[supply]['cgst'] +row['Cgst_Tot_Sale']))
                NoGstNum[supply]['sgst'] = float("{0:.2f}".format(NoGstNum[supply]['sgst'] +row['Sgst_Tot_Sale']))
            elif len(row['GSTN_of_Customer']) != 15:
                NoGstNum[supply] ={}
                NoGstNum[supply]['state'] =row['place_of_supply']
                NoGstNum[supply]['Total_without_tax'] = float("{0:.2f}".format(row['Total_No_Tax_Sale']))
                NoGstNum[supply]['total_bill_Amount'] = float("{0:.2f}".format(row['Total_Sale']))
                NoGstNum[supply]['igst'] = float("{0:.2f}".format(row['Igst_Tot_Sale']))
                NoGstNum[supply]['cgst'] = float("{0:.2f}".format(row['Cgst_Tot_Sale']))
                NoGstNum[supply]['sgst'] = float("{0:.2f}".format(row['Sgst_Tot_Sale']))
            else:
                gst_num = row['GSTN_of_Customer']
                if gst_num in bill_with_gst:
                    bill_with_gst[gst_num].append({'Inv_Type': row['Inv_Type'], 'Inv_No': row['Inv_No'], 'Inv_Date': row['Inv_Date'],'Igst_Tot_Sale': row['Igst_Tot_Sale'], 'Cgst_Tot_Sale': row['Cgst_Tot_Sale'], 'Sgst_Tot_Sale': row['Sgst_Tot_Sale'], 'Total_No_Tax_Sale': row['Total_No_Tax_Sale'], 'Total_Sale': row['Total_Sale'],'Customer_Name': row['Customer_Name'],'GSTN_of_Customer': row['GSTN_of_Customer']})
                else:
                    bill_with_gst[gst_num]=[{'Inv_Type': row['Inv_Type'], 'Inv_No': row['Inv_No'], 'Inv_Date': row['Inv_Date'],'Igst_Tot_Sale': row['Igst_Tot_Sale'], 'Cgst_Tot_Sale': row['Cgst_Tot_Sale'], 'Sgst_Tot_Sale': row['Sgst_Tot_Sale'], 'Total_No_Tax_Sale': row['Total_No_Tax_Sale'], 'Total_Sale': row['Total_Sale'],'Customer_Name': row['Customer_Name'],'GSTN_of_Customer': row['GSTN_of_Customer']}]


            index = row['Hsn_Code']+'-'+row['Converted_Unit_GST']
        
            if index in Hsn_Code:
                #quat = Hsn_Code[index]['quanity'] +row['Converted_Unit_Val_GST']
                Hsn_Code[index]['quanity'] = float("{0:.2f}".format(Hsn_Code[index]['quanity'] +row['Converted_Unit_Val_GST']))
                Hsn_Code[index]['total_bill_Amount'] = float("{0:.2f}".format(Hsn_Code[index]['total_bill_Amount'] +row['Total_Sale']))
                Hsn_Code[index]['Sale_Without_Tax'] = float("{0:.2f}".format(Hsn_Code[index]['Sale_Without_Tax'] +row['Total_No_Tax_Sale']))
                Hsn_Code[index]['igst'] = float("{0:.2f}".format(Hsn_Code[index]['igst'] +row['Igst_Tot_Sale']))
                Hsn_Code[index]['cgst'] = float("{0:.2f}".format(Hsn_Code[index]['cgst'] +row['Cgst_Tot_Sale']))
                Hsn_Code[index]['sgst'] = float("{0:.2f}".format(Hsn_Code[index]['sgst'] +row['Sgst_Tot_Sale']))
            #print("Hello")
            else:
                Hsn_Code[index]={}
                Hsn_Code[index]['Hsn_Code'] = row['Hsn_Code']
                Hsn_Code[index]['unit'] = row['Converted_Unit_GST']
                Hsn_Code[index]['quanity'] = float("{0:.2f}".format(row['Converted_Unit_Val_GST']))
                Hsn_Code[index]['total_bill_Amount'] = float("{0:.2f}".format(row['Total_Sale']))
                Hsn_Code[index]['Sale_Without_Tax'] = float("{0:.2f}".format(row['Total_No_Tax_Sale']))
                Hsn_Code[index]['igst'] = float("{0:.2f}".format(row['Igst_Tot_Sale']))
                Hsn_Code[index]['cgst'] = float("{0:.2f}".format(row['Cgst_Tot_Sale']))
                Hsn_Code[index]['sgst'] = float("{0:.2f}".format(row['Sgst_Tot_Sale']))
    #print(NoGstNum)
    #print(Hsn_Code)
    bill_with_gst_op={}
    for key,bill in bill_with_gst.items():
        #print(bill)
        for billRow in bill:
            index = str(billRow['Inv_Type']) +'-'+str(billRow['Inv_No'] )
            #print(index)
            if index in bill_with_gst_op:
                #quat = bill_with_gst_op[index]['quanity'] +row['Converted_Unit_Val_GST']
                bill_with_gst_op[index]['Igst_Tot_Sale'] = float("{0:.2f}".format(bill_with_gst_op[index]['Igst_Tot_Sale'] +billRow['Igst_Tot_Sale']))
                bill_with_gst_op[index]['Cgst_Tot_Sale'] = float("{0:.2f}".format(bill_with_gst_op[index]['Cgst_Tot_Sale'] +billRow['Cgst_Tot_Sale']))
                bill_with_gst_op[index]['Sgst_Tot_Sale'] = float("{0:.2f}".format(bill_with_gst_op[index]['Sgst_Tot_Sale'] +billRow['Sgst_Tot_Sale']))
                bill_with_gst_op[index]['Total_No_Tax_Sale'] = float("{0:.2f}".format(bill_with_gst_op[index]['Total_No_Tax_Sale'] +billRow['Total_No_Tax_Sale']))
                bill_with_gst_op[index]['Total_Sale'] = float("{0:.2f}".format(bill_with_gst_op[index]['Total_Sale'] +billRow['Total_Sale']))

            #print("Hello")
            else:
                bill_with_gst_op[index]={}
                bill_with_gst_op[index]['Inv'] = index
                bill_with_gst_op[index]['Inv_Date'] = billRow['Inv_Date']
                bill_with_gst_op[index]['Igst_Tot_Sale'] = float("{0:.2f}".format(billRow['Igst_Tot_Sale']))
                bill_with_gst_op[index]['Cgst_Tot_Sale'] = float("{0:.2f}".format(billRow['Cgst_Tot_Sale']))
                bill_with_gst_op[index]['Sgst_Tot_Sale'] = float("{0:.2f}".format(billRow['Sgst_Tot_Sale']))
                bill_with_gst_op[index]['Total_No_Tax_Sale'] = float("{0:.2f}".format(billRow['Total_No_Tax_Sale']))
                bill_with_gst_op[index]['Total_Sale'] = float("{0:.2f}".format(billRow['Total_Sale']))
                bill_with_gst_op[index]['Customer_Name'] = billRow['Customer_Name']
                bill_with_gst_op[index]['GSTN_of_Customer'] = billRow['GSTN_of_Customer']
                

    #print(bill_with_gst_op)

    return render(request, 'adminreport/gst1_rep.html', {'search_result': row_retuns,'total':total,'startdate':startdate1.strftime('%d-%m-%Y'),'enddate':enddate1.strftime('%d-%m-%Y'),
        'parse':Hsn_Code,'bill_without_gst':NoGstNum,'bill_with_gst':bill_with_gst_op})
    

def gst1Input(request):
    #print("gst1Input")
    return render(request,'adminreport/gst1.html')

class CustEntryView(ListView):

    model = CustDetail
    context_object_name = 'showCustList'
    template_name = 'adminreport/showCustList.html'

class custDetailView(DetailView):
    context_object_name = 'cust_details'
    model = CustDetail
    template_name = 'adminreport/cust_detail.html'

class updateCustEntry(UpdateView):
    fields = ('Customer_Name','Address','City','State','GSTN_of_Customer')
    model = CustDetail
    context_object_name = 'updateCustEntry'

