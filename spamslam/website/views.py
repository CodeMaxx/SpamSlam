# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from website.models import *
from predict import predict_from_text

import subprocess
# Create your views here.

def home(request):
	return render(request, 'homepage.html', {})

def check_spam(input_sentence):
	f = open('list.txt', 'w')
	f.write(input_sentence)
	f.close()
	prediction = predict_from_text()


def sending(request):
	if request.method == "POST":
		content = request.POST["content"]
		sender_eth_id = request.POST["sender_eth_id"]
		receiver_eth_id = request.POST["receiver_eth_id"]
		Email(content=content, sender_eth_id=sender_eth_id,receiver_eth_id=receiver_eth_id).save()
		email_id = Email.objects.latest('email_id')
		transaction = Transaction(email_id=email_id, market_address=null)
		transaction.save()
		market_address = str(subprocess.check_output(['node','createMarket.js']))
		# Buy tokens with sender_eth_id
		transaction.market_address = market_address
		transaction.save()
		if transaction.is_read:
			# Buy tokens with receiver_eth_id
			result = bool(check_spam(content)) # True when spam, False otherwise
			# Start the redeaming process here based on the result
			transaction.is_processed = True
			transaction.save()

def reading(request):
	if request.method == "POST":
		marked = request.POST["marked"]
		email_id = request.POST["email_id"]
		transaction = Transaction.objects.get(email_id=email_id)
		transaction.marked = bool(marked)
		transaction.is_read = True
		transaction.save()
		if transaction.market_address is not null:
			# Buy tokens with receiver_eth_id
			result = bool(check_spam(content)) # True when spam, False otherwise
			# Start the redeaming process here based on the result
			transaction.is_processed = True
			transaction.save()