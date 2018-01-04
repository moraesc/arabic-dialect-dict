# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 09:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_word', models.CharField(max_length=20)),
                ('arabeasy_word', models.CharField(max_length=20)),
                ('part_of_speech', models.CharField(choices=[('V', 'Verb'), ('N', 'Noun'), ('P', 'Particle'), ('PN', 'Pronoun'), ('ADJ', 'Adjective'), ('ADV', 'Adverb'), ('PRE', 'Preposition'), ('I', 'Interjection')], max_length=3)),
                ('english_definition', models.CharField(max_length=150)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
