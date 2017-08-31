from django.http import JsonResponse
from django.views.generic.detail import DetailView



def get_job_status(request):
    data = {}
    return JsonResponse(data)
