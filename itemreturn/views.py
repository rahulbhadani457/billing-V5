from django.shortcuts import render
from django.views.generic import TemplateView,DetailView,ListView,DeleteView,CreateView,UpdateView
from . import models
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

#  return index page
class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'index.html'

class returnindex(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'itemreturn/index.html'



class CreatereturnEntry(CreateView):
    fields = ('Item_Code','Quatity_return','Unit_Price','Igst_Percent','Cgst_Percent','Sgst_Percent','customer_name')
    model = models.returnitem
    context_object_name = 'CreatereturnEntry'
    #success_url = reverse_lazy("return:detail")
    template_name = 'itemreturn/create.html'

class returnList(ListView):

    model = models.returnitem
    context_object_name = 'viewreturn'
    template_name = 'GSTR2A/view_GSRT2A.html'
