from django.http import JsonResponse
from django.views.generic.detail import DetailView

from duster.core.models import Job



def get_job_status(request):
    data = {}
    return JsonResponse(data)


class DestructionView(DetailView):

    model = Job
    template_name = 'pages/destruction.html'

    # def get_object(queryset=None):
    # TODO: We probably need to override this, so in case the pk is an invalid
    # hex we throw a 404 and not a 500
