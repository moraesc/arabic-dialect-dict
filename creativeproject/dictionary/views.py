from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core import serializers

from dictionary.forms import *
from dictionary.models import *

import logging
import operator
import re
import json

#homepage view
def homepage(request):
    return render(request, 'registration/homepage.html')

#log in view
def login(request):
    login_error = ""
    if request.method == 'POST':
        form = NameForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if form.is_valid():
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect('/dictionary/homepage')
            else:
                login_error = "Log in information not valid. Please try again."
                context = {'login_error': login_error}
                logging.warning(context)
                return render(request, 'registration/login.html', context)
                #return HttpResponseRedirect('/dictionary/login', context)
    else:
        return render(request, 'registration/login.html')

#register view
def register(request):
    register_error = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is None:
                user = form.save()
                user.set_password(password)
                dialects = request.POST.getlist('dialect', '')
                if dialects is not None:
                    for d in dialects:
                        setPermission(user, d)
                user.save()
                auth_login(request, user)
                return HttpResponseRedirect('/dictionary/homepage')
            else:
                #return HttpResponseRedirect('/dictionary/register')
                register_error = "Users already exists."
                context = {'register_error': register_error}
                return render(request, 'registration/register.html', context)
        else:
            register_error = "Error in your input. Please try again."
            context = {'register_error': register_error}
            return render(request, 'registration/register.html', context)
            return HttpResponseRedirect('/dictionary/register')
    else:
        return render(request, 'registration/register.html')

#set user permissions
def setPermission(user, permission):
    group = Group.objects.get(name__iexact=permission)
    group.user_set.add(user)

#logout view
# @login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/dictionary/homepage')
    return render(request, 'registration/logout.html')

#if input contains arabic characters
def contains_arabic_characters(word):
    a = re.compile('[\u0600-\u06FF]')
    m = a.match(word)
    return m is not None

#serialize entries - JSON
def serialize_entries(entries):
    results = {}
    i = 1
    for e in entries :
        e_id = ("entry%s" % i)
        results[e_id] = {'author':e.author, 'script_word':e.script_word, 'arabeasy_word':e.arabeasy_word,
        'part_of_speech':e.part_of_speech, 'english_definition':e.english_definition, 'dialect':e.dialect}
        i += 1
    return results

# serialize comments - JSON
def serialize_comments(comments):
    results = {}
    i = 1
    for c in comments :
        c_id = ("comment%s" % i)
        entry = serialize_entries([c.entry])
        results[c_id] = {'author':c.author, 'entry':entry, 'content':c.content, 'likes':c.likes}
        i += 1
    return results

#JSON search when clicking on button to display new dialect
def json_search(request, translation, dialect, word) :
    context = search(request, translation, dialect, word)
    entries = context['entries']
    comments = context['comments']
    context['entries'] = serialize_entries(entries)
    context['comments'] = serialize_comments(comments)
    return JsonResponse(context)

#search page
def search_page(request, translation, dialect, word) :
    context = search(request, translation, dialect, word)
    return render(request, 'registration/search.html', context)

#entries
def entries(request, translation, dialect, word) :
    context = search(request, translation, dialect, word)
    entries = context['entries']
    context['entry'] = entries[0]
    context['search_url'] = '/dictionary/search/' + translation + '/' + dialect + '/' + word
    return render(request, 'registration/comment.html', context)

#query database based on search entered
def search(request, translation, dialect, word):
        message = ""
        secondDialect = ""
        thirdDialect = ""

        #***QUERY DATABASE***
        entries = Entry.objects.filter(dialect=dialect)

        if translation=='enar':
            #enar
            results = [e for e in entries if word.lower() in e.english_definition.lower()]
        else:
            #aren
            if contains_arabic_characters(word):
                results = [e for e in entries if word == e.script_word]
            else:
                results = [e for e in entries if word.lower() == e.arabeasy_word.lower()]

        if not results:
            message = "There are no entries for this dialect!"
            results = ""

        if dialect == "Gulf":
            secondDialect = "Levantine"
            thirdDialect = "Egyptian"
        elif dialect == "Levantine":
            secondDialect = "Gulf"
            thirdDialect = "Egyptian"
        elif dialect == "Egyptian":
            secondDialect = "Gulf"
            thirdDialect = "Levantine"

        context = {'message':message, 'word':word, 'dialect':dialect,
        'translation':translation, 'secondDialect':secondDialect, 'thirdDialect':thirdDialect}

        comments = []
        for entry in results:
            comments.extend(Comment.objects.filter(entry=entry))

        context['entries'] = results
        context['comments'] = comments

        return context

def create_entry_page(request):
    return render(request, 'registration/create.html')

#submits an entry for a word
def submit_entry(request):
    message = ""
    if request.method == 'POST':
        #use a form just to check that the user has properly filled out the data
        form = EntryForm(request.POST)
        if form.is_valid() :

            #check that fields are properly filled out
            if (not contains_arabic_characters(request.POST.get('script_word'))
                    or contains_arabic_characters(request.POST.get('arabeasy_word'))
                    or contains_arabic_characters(request.POST.get('english_definition'))):
                message = "Your entry is not valid. Please only use Arabic script where appropriate."
                return render(request, 'registration/create.html', {'message': message})

            #create an entry out of the provided data
            entry = Entry(
                author=request.user.username,
                script_word=request.POST.get('script_word'),
                arabeasy_word=request.POST.get('arabeasy_word').lower(),
                part_of_speech=request.POST.get('part_of_speech'),
                english_definition=request.POST.get('english_definition'),
                dialect=request.POST.get('dialect')
            )

            #now check if the entry already exists in the database
            exists = False
            entries = Entry.objects.filter(dialect=entry.dialect)
            for e in entries:
                if e.script_word == entry.script_word or e.arabeasy_word == entry.arabeasy_word :
                    if e.part_of_speech == entry.part_of_speech :
                        exists = True
            if exists :
                message = "error: this entry already exists. if you're registered you can edit it."
                return render(request, 'registration/create.html', {'message':message})
            else:
                entry.save()
                message = "Success!"
                logging.warning(message)
                return HttpResponseRedirect('/dictionary/homepage')
        else:
            message = "Your entry is not valid. Make sure to fill out all fields."
            return render(request, 'registration/create.html', {'message': message})
    else:
        message = "not posted"
        return render(request, 'registration/create.html', {'message': message})

def comment(request):
    search_url = request.POST.get('search_url')
    return render(request, 'registration/comment.html', {'search_url':search_url})

#submit comment for an entry
def submit_comment(request):
    message=""
    if request.method == 'POST':
        entry = Entry.objects.get(pk=request.POST.get('pk'))
        comment = Comment(
            author=request.user.username,
            entry=entry,
            content=request.POST.get('content'),
            likes=0,
        )
        comment.save()
        message='success'
        logging.warning(message);
        return HttpResponseRedirect('/dictionary/homepage')
    else:
        message = "not posted"
        logging.warning(message)
        return HttpResponseRedirect('/dictionary/homepage')
