from django.db import models
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType

class Entry(models.Model):
    PARTS_OF_SPEECH = (
        ('V', "Verb"),
        ('N', "Noun"),
        ('P', "Particle"),
        ('PN', "Pronoun"),
        ('ADJ', "Adjective"),
        ('ADV', "Adverb"),
        ('PRE', "Preposition"),
        ('I', "Interjection"),
    )
    DIALECTS = (
        ('Levantine', "Levantine"),
        ('Egyptian', "Egyptian"),
        ('Gulf', "Gulf"),
    )
    author = models.CharField(max_length=30)
    script_word = models.CharField(max_length=20)
    arabeasy_word = models.CharField(max_length=20)
    part_of_speech = models.CharField(max_length=3, choices=PARTS_OF_SPEECH)
    english_definition = models.CharField(max_length=150)
    dialect = models.CharField(max_length=9, choices=DIALECTS)

    def __str__(self):
        return ("%s, %s, %s" % (self.script_word, self.arabeasy_word, self.english_definition))

class Comment(models.Model):
    author = models.CharField(max_length=30)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    likes = models.PositiveSmallIntegerField()

    def __str__(self):
        return ("author: %s, entry: %s, likes: %s" % (self.author, self.entry, self.likes))

    #  CREATE UNIQUE PERMISSION:
    #     codename = 'cant_like_' + str(self.pk)
    #     name = 'Cant Like ' + str(self.pk)
    #     ct = ContentType.objects.get_for_model(User)
    #     p = Permission(codename=codename, name=name, content_type=ct,)
    #     p.save()

    def liked(self, user):
        codename = 'cant_like_' + str(self.pk)
        p = Permission.objects.get(codename=codename)
        user.user_permissions.add(p)

    def unliked(self, user):
        codename = 'cant_like_' + str(self.pk)
        p = Permission.objects.get(codename=codename)
        user.user_permissions.remove(p)
