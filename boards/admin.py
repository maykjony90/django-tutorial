from django.contrib import admin

from .models import Board
# Register your models here.

# register Board class as a model into admin page
admin.site.register(Board)