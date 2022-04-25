from django.db import models
from django.urls import reverse

# Create your models here.
class CustDetail(models.Model):
    Cust_Id =models.AutoField(primary_key=True)
    Customer_Name = models.CharField(max_length=65)
    Address = models.CharField(max_length=200, null=True)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=50,null=True)
    Mob_No = models.CharField(max_length=50,null=True)
    GSTN_of_Customer = models.CharField(max_length=50, null=True,blank=True)

    def __int__(self):
        return self.CustId
    
    def get_absolute_url(self):
        #print(Item_Name)
        return reverse("adminrep:detail", kwargs={'pk': self.pk})

class SaleReport(models.Model):
    Inv_Type =models.CharField(max_length=5)
    Inv_No =models.PositiveIntegerField()
    Inv_Date = models.DateField(auto_now=True)
    Item_Code = models.CharField(max_length=30)
    Item_Name = models.CharField(max_length=500)
    Item_Catogory =models.CharField(max_length=50)
    Hsn_Code = models.CharField(max_length=10)
    Quatity_Bought_Sale = models.FloatField()
    Unit_Sale = models.CharField(max_length=20)
    Unit_Conversion_Val_GST =models.PositiveIntegerField()
    Converted_Unit_GST =models.CharField(max_length=20)
    Converted_Unit_Val_GST =models.FloatField()
    Unit_Price_Sale = models.FloatField(blank=True, null=True)
    Unit_Nett_Price_Sale = models.FloatField(blank=True, null=True)
    Igst_Percent_Sale = models.FloatField(blank=True, null=True)
    Cgst_Percent_Sale = models.FloatField(blank=True, null=True)
    Sgst_Percent_Sale = models.FloatField(blank=True, null=True)
    Igst_Tot_Sale = models.FloatField(blank=True, null=True)
    Cgst_Tot_Sale = models.FloatField(blank=True, null=True)
    Sgst_Tot_Sale = models.FloatField(blank=True, null=True)
    Total_No_Tax_Sale =models.FloatField()
    Total_Sale = models.FloatField()
    Cgst_Percent_Purchase = models.FloatField(blank=True, null=True)
    Sgst_Percent_Purchase = models.FloatField(blank=True, null=True)
    Igst_Percent_Purchase = models.FloatField(blank=True, null=True)
    Cgst_Tot_Purchase = models.FloatField(blank=True, null=True)
    Sgst_Tot_Purchase = models.FloatField(blank=True, null=True)
    Igst_Tot_Purchase = models.FloatField(blank=True, null=True)
    Unit_Price_Purchase = models.FloatField()
    Total_Purchase = models.FloatField()
    Total_No_Tax_Purchase = models.FloatField()
    Profit = models.FloatField()
    Profit_Percent = models.FloatField()
    Bill_Cancel = models.CharField(max_length=10,choices=(('Yes','Yes'),('No','No')),null=True)
    comment =models.CharField(max_length=100,null=True)
    Bill_cancel_Date = models.DateField(null=True)
    place_of_supply = models.CharField(max_length=100)
    mis1 = models.CharField(max_length=100)
    mis2 = models.CharField(max_length=100)
    mis3 =models.CharField(max_length=100)
    Cust_Id =models.ForeignKey(CustDetail,on_delete='DO_NOTHING',related_name='customerId')


    def __int__(self):
        return self.Inv_No

class invoicenumber(models.Model):
    Inv_No =models.AutoField(primary_key=True)
    Cust_Id =models.ForeignKey(CustDetail,on_delete='DO_NOTHING',related_name='cusId')

class estimatenumber(models.Model):
    Inv_No =models.AutoField(primary_key=True)
    Cust_Id =models.ForeignKey(CustDetail,on_delete='DO_NOTHING',related_name='cusId1')


    def __int__(self):
        return self.Inv_No

class Cust_payment_record(models.Model):
    id =models.AutoField(primary_key=True)
    inv_type = models.CharField(max_length=5)
    inv_number = models.PositiveIntegerField()
    payment_Amount = models.FloatField()
    payment_left = models.FloatField()
    total_bill_Amount = models.FloatField()
    current_payment_Date = models.DateField()
    Comment = models.CharField(max_length=200)
    Cust_Id =models.PositiveIntegerField()
    is_last = models.BooleanField()


    def __int__(self):
        return self.inv_number
