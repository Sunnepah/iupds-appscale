from django.conf.urls import url
from django.conf.urls import patterns

from .views import JobFormView

urlpatterns = [
    url(r'^job-form/$',
    login_required(JobFormView.as_view()), name='job_form'),
]
