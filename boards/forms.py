# The Forms API is available in the module django.forms. 
# Django works with two types of forms: forms.Form and forms.ModelForm. 
# The Form class is a general purpose form implementation.
# We can use it to process data that are not directly associated 
# with a model in our application. A ModelForm is a subclass of Form, 
# and it’s associated with a model class.
from django import forms
from .models import Topic, Post


# This is our first form. It’s a ModelForm associated with the Topic model. 
# The subject in the fields list inside the Meta class is referring 
# to the subject field in the Topic class. 
# Now observe that we are defining an extra field named message. 
# This refers to the message in the Post we want to save.
class NewTopicForm(forms.ModelForm):
	message = forms.CharField(
		widget=forms.Textarea(
		attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
		max_length=4000,
		help_text="The max length of the text is 4000.")

	# subclass
	class Meta:
		model = Topic
		fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]