from django.db import models
from django.urls import reverse

# Create your models here.


class billSaleEntry(models.Model):
    Item_Code = models.AutoField(primary_key=True)
    Item_Name = models.CharField(max_length=500, null=False)
    Item_Catogory =models.CharField(max_length=200)
    HSN_Code = models.CharField(max_length=30, null=False)
    Quatity_Bought = models.FloatField(null=False)
    Rate_Of_Purchase = models.FloatField(null=False)
    Unit = models.CharField(max_length=50,choices=(('PCS','PCS'),('MTR','MTR'),('CHK','CHK'),('DOZ','DOZ'),('JODA','JODA')))
    Rate_Of_Sale = models.FloatField(null=False)
    IGST_Percent =models.FloatField()
    SGST_Percent = models.FloatField()
    CGST_Percent = models.FloatField()
    GST_Type = models.CharField(max_length=6, choices=(('Y','Yes'),('N','No')))
    Quatity_in_stock =models.FloatField(null=False)
    def __str__(self):
        return self.Item_Name

    def get_absolute_url(self):
        #print(Item_Name)
        return reverse("bill:detail", kwargs={'pk': self.pk})
    
    @property
    def get_Quatity_in_stock(self):
        Quatity_Bought = self.Quatity_Bought
        left =(Quatity_Bought)
        return left
    
    def save(self, *args,**kwargs):
        self.Quatity_in_stock = self.get_Quatity_in_stock
        super(billSaleEntry, self).save(*args, **kwargs)