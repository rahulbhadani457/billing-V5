from django import forms
from django.forms import widgets

class CustForm(forms.Form):  
    #CustId =forms.NumberInput(widget = forms.HiddenInput(), required = False)
    Customer_Name           = forms.CharField()
    Address          = forms.CharField(required = False)
    City          = forms.CharField()
    Mob_No                 = forms.CharField()
    GSTN_of_Customer                = forms.CharField(required = False)

class DateInput(forms.DateInput):
    input_type ='date'
    
class salesForm(forms.Form):
    payment_Amount = forms.FloatField()
    
class payment_udpate(forms.Form):
    payment_Amount = forms.FloatField()
    Comment = forms.CharField(required = False)
    current_payment_Date = forms.DateField( widget = DateInput)

class cancleInvoice(forms.Form):
    Bill_Cancel = forms.ChoiceField(choices=(('Yes','Yes'),('No','No')))
    Bill_cancel_Date = forms.DateField( widget = DateInput)
    comment =forms.CharField()
