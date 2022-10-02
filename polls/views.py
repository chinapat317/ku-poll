from secrets import choice
from .models import Question, Choice, Votes
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now(), end_date__gte=timezone.now())

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            messages.add_message(request, messages.INFO, 'Access denied')
            return HttpResponseRedirect(reverse('polls:index'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    user = request.user
    username = user.get_username()
    if not user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Please login before vote.')
        return HttpResponseRedirect('../../../account/login/')
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        choice = question.choice_set.all()
        for each_choice in choice:
            try:
                vote = each_choice.votes_set.filter(username=username)
                for each_vote in vote:
                    each_vote.delete()
            except:
                pass
        select_choice.votes_set.create(username=username)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


