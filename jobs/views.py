from django.shortcuts import render
from .forms import JobForm


# Create your views here.
class JobFormView(TemplateView):
     template_name = "jobs/new.html"

     def get_context_data(self, **kwargs):
         context = super(JobFormView, self).get_context_data(**kwargs)
         context.update(JobForm=JobForm())
         return context
