from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Poll, Choice

# Create your views here.

#def index(request):
#    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = RequestContext(request, {
#        'latest_poll_list': latest_poll_list,
#    })
#    return HttpResponse(template.render(context))
#
#def detail(request, poll_id):
#        poll = get_object_or_404(Poll, pk=poll_id)
#        return render(request, 'polls/detail.html', {'poll': poll})
#
#def results(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'polls/results.html', {'poll': poll})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'
    
    def get_queryset(self):
        """Return the last five published polls. (not including future polls)"""
        return Poll.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """ Excludes any polls that aren't published yet. """
        return Poll.objects.filter(pub_date__lte = timezone.now())
    
class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You did not select a choice.",
        })
    
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))