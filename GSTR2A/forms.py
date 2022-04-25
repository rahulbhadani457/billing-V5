from django import forms
from django.forms import ModelForm
from .models import GSRT2A
from django.contrib.admin.widgets import AdminDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'


class CreateGSTR2AForm(ModelForm):
    class Meta:
        model = GSRT2A
        fields =['Supplier_name','GSTIN_of_Supplier','Invoice_number','Invoice_date','Received_date','Amount_No_Tax','SGST_Tax','CGST_Tax',
        'IGST_Tax']
    #supplier_id = models.PositiveIntegerField()
        widgets = {
            'Invoice_date': DateInput(),
            'Received_date': DateInput(),

        }
    
class UpdateGSTR2AForm(ModelForm):
    class Meta:
        model = GSRT2A
        fields =['Invoice_number','Invoice_date','Received_date','Amount_No_Tax','SGST_Tax','CGST_Tax','IGST_Tax']
        widgets = {
            'Invoice_date': DateInput(),
            'Received_date': DateInput(),

        }
    