# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from website.models import *
from predict import predict_from_text

# Create your views here.

def home(request):
	return render(request, 'homepage.html', {})

def check_spam(input_sentence):
	f = open('list.txt', 'w')
	f.write(input_sentence)
	f.close()
	prediction = predict_from_text()
