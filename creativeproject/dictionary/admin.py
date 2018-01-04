from django.contrib import admin
from .models import *

class EntryAdmin(admin.ModelAdmin):
    fields = ['author', 'script_word', 'arabeasy_word', 'part_of_speech', 'english_definition', 'dialect']

class CommentAdmin(admin.ModelAdmin):
    fields = ['author', 'entry', 'content', 'likes']

admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)
