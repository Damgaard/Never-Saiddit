from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from duster.core.models import Job


def get_job_status(request):
    try:
        job = get_object_or_404(Job, pk=str(request.GET.get('identifier', '')))
    except ValueError:
        raise Http404('Bad/missing formatted identifier')

    data = {
        'state': job.state,
        'comments_deleted': job.comments_deleted,
        'submissions_deleted': job.submissions_deleted
    }

    return JsonResponse(data)


class DestructionView(DetailView):

    model = Job
    template_name = 'pages/destruction.html'

    # def get_object(queryset=None):
    # TODO: We probably need to override this, so in case the pk is an invalid
    # hex we throw a 404 and not a 500

    # TODO: Add redirect if job is in either an error state or it has
    # not yet begun
