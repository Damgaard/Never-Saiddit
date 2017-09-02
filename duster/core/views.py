from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView



def get_job_status(request):
    data = {}
    return JsonResponse(data)


class DestructionView(TemplateView):

    template_name = 'pages/destruction.html'
