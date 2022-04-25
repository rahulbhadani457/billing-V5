import re
from django.db import models
from django.urls import reverse
from django.db.models import Q

# Create your models here.
class GSRT2A_supplier_id(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    GSTIN_of_Supplier=models.CharField(max_length=15)

class GSRT2A(models.Model):
    id = models.AutoField(primary_key=True)
    Supplier_name = models.CharField(max_length=100)
    GSTIN_of_Supplier=models.CharField(max_length=15)
    Invoice_number=models.CharField(max_length=20)
    Invoice_date= models.DateField()
    Received_date=models.DateField(null=True,blank=True)
    Amount_No_Tax =models.FloatField()
    SGST_Tax=models.FloatField(null=True,blank=True)
    CGST_Tax =models.FloatField(null=True,blank=True)
    IGST_Tax = models.FloatField(null=True,blank=True)
    supplier_id = models.PositiveIntegerField()
    Total_Amount =models.FloatField()
    

    @property
    def get_supplier_id(self):
        model = GSRT2A_supplier_id
        search_result =model.objects.filter(GSTIN_of_Supplier=self.GSTIN_of_Supplier).first()
        print(search_result)
        if search_result is None:
            insert_dict = {'GSTIN_of_Supplier':self.GSTIN_of_Supplier}
            model.objects.create(**insert_dict)
            search_result =model.objects.filter(GSTIN_of_Supplier=self.GSTIN_of_Supplier).first()
            #print(search_result)
            ret_val = search_result.supplier_id
        else:
            ret_val = search_result.supplier_id
        
        return ret_val
    
    @property
    def get_SGST_Tax(self):
        if self.SGST_Tax == None:
            SGST_Tax=0.0
            return SGST_Tax

    @property
    def get_CGST_Tax(self):
        if self.CGST_Tax == None:
            CGST_Tax=0.0
            return CGST_Tax

    @property
    def get_IGST_Tax(self):
        if self.IGST_Tax == None:
            IGST_Tax=0.0
            return IGST_Tax

    @property
    def get_Total_Amount(self):
        if self.SGST_Tax == None:
            self.SGST_Tax =self.get_SGST_Tax 
        if self.CGST_Tax == None:
            self.CGST_Tax =self.get_CGST_Tax
        if self.IGST_Tax == None:
            self.IGST_Tax =self.get_IGST_Tax
        Total_Amount = self.Amount_No_Tax +self.CGST_Tax+self.SGST_Tax+self.IGST_Tax
        return Total_Amount

    def save(self, *args,**kwargs):
        self.supplier_id = self.get_supplier_id
        self.Total_Amount = self.get_Total_Amount
        super(GSRT2A, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("GST2A:DetailGSTR2A",kwargs={'pk': self.pk})

class GSRT2A_payment(models.Model):
    id =models.AutoField(primary_key=True)
    GSTIN_of_Supplier=models.CharField(max_length=15)
    Supplier_name = models.CharField(max_length=100)
    Invoice_number=models.CharField(max_length=20)
    payment_Amount = models.FloatField()
    payment_left = models.FloatField()
    current_payment_Date = models.DateField()
    supplier_id = models.PositiveIntegerField()
    Comment = models.CharField(max_length=200)
    is_last = models.BooleanField()

