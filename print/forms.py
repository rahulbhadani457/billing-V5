from django import forms

class printForm(forms.Form):  
    Item_Code             = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Item_Name             = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Item_Catogory         = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    HSN_Code              = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Quatity_Sold          = forms.FloatField()
    Unit                  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Rate_Of_Sale          = forms.FloatField()
    IGST_Percent          = forms.FloatField()
    CGST_Percent          = forms.FloatField()
    SGST_Percent          = forms.FloatField()
    GST_Type              = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Total                 = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Gross_Total           = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Total_CGST            = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Total_SGST            = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Total_IGST            = forms.FloatField(widget = forms.HiddenInput(), required = False)

    def clean_GST_Type(self):
        data = self.cleaned_data['GST_Type']
        if data == "N":
            raise forms.ValidationError("Try Estimate billing")
        return data

class estimateForm(forms.Form):  
    Item_Code             = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Item_Name             = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Item_Catogory         = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    HSN_Code              = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Quatity_Sold          = forms.FloatField()
    Unit                  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Rate_Of_Sale          = forms.FloatField()
    IGST_Percent          = forms.FloatField()
    CGST_Percent          = forms.FloatField()
    SGST_Percent          = forms.FloatField()
    GST_Type              = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Total                 = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Gross_Total           = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Total_CGST            = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Total_SGST            = forms.FloatField(widget = forms.HiddenInput(), required = False)
    Total_IGST            = forms.FloatField(widget = forms.HiddenInput(), required = False)

