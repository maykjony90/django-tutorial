# html'i renderlarmak icin render() fonksiyonunu yukle
from django.shortcuts import render, get_object_or_404, redirect
# bu dosyayla ayni klasorde bulunan models dosyasinin
# icerisindeki 'Board' class'ini yukle 
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# GENERIC CLASS-BASED VIEW
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

'''
# Burada bir fonkisyon eklediginde urls.py dosyasindan
# URL'i urlpatterns listesine ekle.
# BU SEKMEYE('www.example.com/home' or 'www.example.com/'') 
# BIR 'REQUEST' GELDIGINDE HOME() FONKSIYONUNU CALISTIR  
def home(request):
	# BOARDS/OBJECTS DOSYASINDAN BUTUN OBJELERI GETIR.
	boards = Board.objects.all()
	# request(istegi)'i, templates/home.html dosyasini ve
	# html dosyasinin icindeki 'boards' degiskenleri icin 'boards' objesini kullan
	return render(request, 'home.html', { 'boards':boards })
'''

# GCBV 
class BoardListView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'home.html'

# Primary Key'i verilen URL'e request alir.
# The regex \d+ will match an integer of arbitrary size. This integer will be used 
# to retrieve the Board from the database. Now observe that we wrote the 
# regex as (?P<pk>\d+), this is telling Django to capture the value into 
# a keyword argument named pk.
def board_topics(request, pk):
	# Yukaridakilere gerek kalmadan shortcuts'tan get_object_or_404
	# cagirip kullanabiliriz.
	board = get_object_or_404(Board, pk=pk)
	# count the number of the topics
	queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
	page = request.GET.get('page', 1)

	paginator = Paginator(queryset, 20)

	try:
		topics = paginator.page(page)
	except PageNotAnInteger:
		# fallback to the first page
		topics = paginator.page(1)
	except EmptyPage:
		# probably the user tries to add a page number
		# in the url, so we fallback to the last page
		topics = paginator.page(paginator.num_pages)

	#topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
	return render(request, 'topics.html', {'board': board, 'topics': topics})

	

@login_required
def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)
	

	# First we check if the request is a POST or a GET. If the request came from a POST,
	#  it means the user is submitting some data to the server. So we instantiate 
	#  a form instance passing the POST data to the form:
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		# we ask Django to verify the data, check if the form is valid if we can 
		# save it in the database: if form.is_valid():. If the form was valid, 
		# we proceed to save the data in the database using form.save(). 
		# The save() method returns an instance of the Model saved into the database. 
		# So, since this is a Topic form, it will return the Topic that was created: 
		# topic = form.save(). After that, the common path is to redirect the user 
		# somewhere else, both to avoid the user re-submitting the form by pressing F5 
		# and also to keep the flow of the application.
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = request.user
			topic.save()
			post = Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=request.user
				)
			return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page
	# If the request was a GET, we just initialize a new and empty form using 
	# form = NewTopicForm().
	else:
		form = NewTopicForm()

	return render(request, 'new_topic.html', {'board': board, 'form': form})



def topic_posts(request, pk, topic_pk):
	# WARNING!
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})



@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
	model = Post
	fields = ('message', )
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'

	# With the line queryset = super().get_queryset() we are reusing the get_queryset 
	# method from the parent class, that is, the UpateView class. 
	# Then, we are adding an extra filter to the queryset, which is filtering 
	# the post using the logged in user, available inside the request object.
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True         

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


