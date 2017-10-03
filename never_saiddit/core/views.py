from django.core.urlresolvers import reverse
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from never_saiddit.core.models import Job
from never_saiddit.core.forms import AcceptanceForm


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


class ConfirmationView(FormView):

    """Have the user make a final confirmation before beginning."""

    model = Job
    form_class = AcceptanceForm
    template_name = 'pages/confirmation.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.job = get_object_or_404(Job, pk=kwargs['pk'])
        except ValueError:
            raise Http404('Bad/missing formatted identifier')

        return super().dispatch(request, *args, **kwargs)

    def get_initial(skGelf):
        initial = super().get_initial()
        initial['has_accepted'] = True
        return initial

    # TODO: handle form_invalid, should probably redirect to a page with
    # information. Basically it should never happen in a normal use case,
    # but could plausibly happen if the browser acts up or the endpoint
    # changes in the future.

    def form_valid(self, form):
        self.job.state = Job.STATE_RECEIVED_CODE_AND_STATE
        self.job.save()
        return redirect(reverse('core:destruction', kwargs={'pk': str(self.job.identifier)}))

    # TODO: Add redirect if job is in either an error state or it has
    # not yet begun


class DestructionView(DetailView):

    model = Job
    template_name = 'pages/destruction.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.job = get_object_or_404(Job, pk=kwargs['pk'])
        except ValueError:
            raise Http404('Bad/missing formatted identifier')

        return super().dispatch(request, *args, **kwargs)

    # TODO: Add redirect if job is in either an error state or it has
    # not yet begun
