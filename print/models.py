from django.db import models
from django.urls import reverse
from bill.models import billSaleEntry
# Create your models here.


class salesDb(models.Model):

    #class Meta:
         #unique_together = (('id', 'Item_Code'),)

    #id = models.AutoField(primary_key=True,serialize=False)
    Item_Code = models.IntegerField()
    session_id =models.CharField(max_length=150)
    Item_Name = models.CharField(max_length=500, null=False)
    Item_Catogory =models.CharField(max_length=150)
    HSN_Code = models.CharField(max_length=30, null=False)
    Quatity_Sold = models.FloatField(null=False)
    Unit = models.CharField(max_length=60)
    Rate_Of_Sale = models.FloatField(null=False)
    IGST_Percent = models.FloatField()
    CGST_Percent = models.FloatField()
    SGST_Percent = models.FloatField()
    Total = models.FloatField(null=True)
    Gross_Total = models.FloatField(null=True)
    Total_CGST = models.FloatField(null=True)
    Total_SGST = models.FloatField(null=True)
    Total_IGST = models.FloatField(null=True)
    GST_Type = models.CharField(max_length=6)
    Rate_Of_Purchase = models.FloatField(null=False)
    insert_date =models.DateTimeField(auto_now=True)
    FinalSP = models.FloatField(null=True)
    FinalGST = models.FloatField(null=True)

    def __int__(self):
        return self.Total

    def get_absolute_url(self):
        return reverse("print:viewprint",kwargs={'pk':self.pk})

    @property
    def get_Rate_Of_Purchase(self):
        printVals = billSaleEntry.objects.filter(Item_Code__exact=self.Item_Code)
        for printVal in printVals:
            Rate_Of_Purchase = printVal.Rate_Of_Purchase
            break
        return Rate_Of_Purchase

    def save(self, *args,**kwargs):
        self.Rate_Of_Purchase = self.get_Rate_Of_Purchase
        super(salesDb, self).save(*args, **kwargs)
    