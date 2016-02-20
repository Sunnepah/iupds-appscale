# jobs/api.py
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from jobs.models import Jobs


class JobResource(ModelResource):
        """
        API Facet
        """
        class Meta:
            queryset = Jobs.objects.all()
            resource_name = 'job'
            allowed_methods = ['post', 'get', 'patch', 'delete']
            authentication = Authentication()
            authorization = Authorization()
            always_return_data = True
