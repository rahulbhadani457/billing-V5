from django.contrib import admin
from adminreport.models import SaleReport,CustDetail,invoicenumber
# Register your models here.

admin.site.register(SaleReport)
admin.site.register(CustDetail)
admin.site.register(invoicenumber)