"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# boards klasorundeski views dosyasinin yukle
from boards import views
# We are giving an alias because otherwise, it would clash with the boards’ views.
# We can improve the urls.py design later on. 
# But for now, let’s focus on the authentication features.
from accounts import views as accounts_views
# We imported the views from the Django’s contrib module. We renamed it 
# to auth_views to avoid clashing with the boards.views.
from django.contrib.auth import views as auth_views


urlpatterns = [
    # BU BIR LIST, BU YUZDEN VIRGUL KOYMAYI UNUTMA!!!!
    # REGEX formatinda yaziyoruz URL'leri.
    # burada site uzantilarinin nasil olacagini ve nereden 
    # cagiralacaklarini belirtiyoruz. boards klasorundeski views dosyasinin
    # icindeki ilgili fonksyionlari cagiriyoruz.
    url(r'^$', views.BoardListView.as_view(), name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    # Inside the as_view() we can pass some extra parameters, so to override the defaults.
    # In this case, we are instructing the LoginView to look for a template at login.html.
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Notice that this view is a little bit different: LogoutView.as_view(). 
    # It’s a Django’s class-based view. So far we have only implemented 
    # classes as Python functions. The class-based views provide 
    # a more flexible way to extend and reuse views.
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    # Those views only works for logged in users. They make use of a view decorator named @login_required. 
    # This decorator prevents non-authorized users to access this page. 
    # If the user is not logged in, Django will redirect them to the login page.
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    # Below is a dynamic URL, pk stands for Primary Key
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    # Observe that now we are dealing with two keyword arguments: 
    # pk which is used to identify the Board, and now we have 
    # the topic_pk which is used to identify which topic to retrieve from the database.
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),

    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
    url(r'^admin/', admin.site.urls),
]
