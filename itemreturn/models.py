from django.db import models
from django.urls import reverse


# Create your models here.
class returnitem(models.Model):
    Return_Date = models.DateField(auto_now=True)
    Item_Code = models.CharField(max_length=30)
    Quatity_return = models.PositiveIntegerField()
    Unit_Price = models.FloatField(blank=True, null=True)
    Igst_Percent = models.FloatField(blank=True, null=True)
    Cgst_Percent = models.FloatField(blank=True, null=True)
    Sgst_Percent = models.FloatField(blank=True, null=True)
    Igst_Tot = models.FloatField(blank=True, null=True)
    Cgst_Tot = models.FloatField(blank=True, null=True)
    Sgst_Tot = models.FloatField(blank=True, null=True)
    Total_No_Tax =models.FloatField()
    Total = models.FloatField()
    customer_name = models.CharField(max_length=30,blank=True, null=True)
    
    def __str__(self):
        return self.Item_Code
    
    @property
    def get_Igst_Tot(self):
        Quatity_return = self.Quatity_return
        Unit_Price =self.Unit_Price
        Igst_Percent =self.Igst_Percent
        Igst_Totl =(Quatity_return*Unit_Price*Igst_Percent)/100
        #Igst_Totl =float("{0:.2f}".format((Quatity_return*Unit_Price*Igst_Percent)/100)
        
        return Igst_Totl
    
    @property
    def get_Cgst_Tot(self):
        Quatity_return = self.Quatity_return
        Unit_Price =self.Unit_Price
        Cgst_Percent =self.Cgst_Percent
        Cgst_Totl =(Quatity_return*Unit_Price*Cgst_Percent)/100
        return Cgst_Totl

    @property
    def get_Sgst_Tot(self):
        Quatity_return = self.Quatity_return
        Unit_Price =self.Unit_Price
        Sgst_Percent =self.Sgst_Percent
        Sgst_Totl =(Quatity_return*Unit_Price*Sgst_Percent)/100
        return Sgst_Totl
    
    @property
    def get_Total_No_Tax(self):
        Quatity_return = self.Quatity_return
        Unit_Price =self.Unit_Price
        Total_No_Taxs =(Quatity_return*Unit_Price)
        return Total_No_Taxs
    
    @property
    def get_Total(self):
        Total_No_Tax = self.get_Total_No_Tax
        Sgst_Tot = self.get_Sgst_Tot
        Cgst_Tot =self.get_Cgst_Tot
        Igst_Tot = self.get_Igst_Tot
        Total =(Total_No_Tax+Sgst_Tot+Cgst_Tot+Igst_Tot)
        return Total
    
    def save(self, *args,**kwargs):
        self.Total_No_Tax = self.get_Total_No_Tax
        self.Sgst_Tot = self.get_Sgst_Tot
        self.Cgst_Tot =self.get_Cgst_Tot
        self.Igst_Tot = self.get_Igst_Tot
        self.Total = self.get_Total
        super(returnitem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("itemreturn:returnindex")