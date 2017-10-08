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

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

sender_balance = 100;
receiver_balance = 100;

def home(request):
	emails = Email.objects.all().order_by('-email_id')
	global sender_balance
	global receiver_balance
	return render(request, 'homepage.html', {'emails' : emails, 'sender_balance': sender_balance, 'receiver_balance': receiver_balance})

def check_spam(input_sentence):
	f = open('test.txt', 'w')
	f.write(input_sentence)
	f.close()
	prediction = predict_from_text()
	return prediction


def redeam(transaction, content):
	global sender_balance
	global receiver_balance
	print "Buying tokens for receiver..."
	receiver_balance -= 2;
	# Buy tokens with receiver_eth_id
	print "Bought tokens for receiver!"
	if transaction.marked_value:
		# print "trans", transaction.marked_value
		print "checkspam:", check_spam(content)
		result = bool(check_spam(content)) # True when spam, False otherwise
		print "booled checkspam:", result
		print "Distributing money..."
		# Start the redeaming process here based on the result
		if result == transaction.marked_value:
			receiver_balance += 2
			sender_balance -= 10
	else:
		receiver_balance += 2
	# Update sender balance and receiver balance
	print "Transaction complete!"
	transaction.is_processed = True
	transaction.save()

@csrf_exempt
def sending(request):
	print "Sending"
	if request.method == "POST":
		content = request.POST["content"]
		sender_eth_id = request.POST["sender_eth_id"]
		receiver_eth_id = request.POST["receiver_eth_id"]
		Email(content=content, sender_eth_id=sender_eth_id,receiver_eth_id=receiver_eth_id).save()
		email_id = Email.objects.latest('email_id')
		print email_id
		transaction = Transaction(email_id=email_id, market_address=None)
		transaction.save()
		print "Creating market..."
		# market_address = str(subprocess.check_output(['node','createMarket.js']))
		print "Market created!"
		print "Buying tokens for sender..."

		# Buy tokens with sender_eth_id
		print "Bought tokens for sender!"
		market_address = '0x' + "a"*40
		transaction.market_address = market_address
		transaction.save()
		if transaction.is_read:
			redeam(transaction)
		return HttpResponse('DoneSending')

@csrf_exempt
def reading(request):
	# print "kaha hai?"
	if request.method == "POST":
		# print "post mein"
		marked = int(request.POST["marked"], 10)
		# print "Not spam", marked
		email_id = request.POST["email_id"]
		# print email_id
		transaction = Transaction.objects.get(email_id=email_id)
		transaction.marked_value = bool(marked)
		# print "marked", marked
		# print "trans marked", transaction.marked_value
		transaction.is_read = True
		transaction.save()
		content = Email.objects.get(email_id=email_id).content
		# print "her"
		if transaction.market_address is not None:
			# print "herasdfa"
			redeam(transaction, content)
		return HttpResponse('Done')