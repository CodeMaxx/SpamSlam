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

import requests
import json

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
	emails = Email.objects.all().order_by('-email_id')
	sender_balance = subprocess.check_output(['node', 'getBalance.js', '0'])
	receiver_balance = subprocess.check_output(['node', 'getBalance.js', '1'])
	return render(request, 'homepage.html', {'emails' : emails, 'sender_balance': sender_balance, 'receiver_balance': receiver_balance})

def check_spam(input_sentence):
	f = open('test.txt', 'w')
	f.write(input_sentence)
	f.close()
	prediction = predict_from_text()
	return prediction


def redeam(transaction, content):
	if transaction.marked_value:
		print "Buying tokens for sender..."
		buySender = subprocess.check_output(['node', 'buyOut.js', market_address, '0', '0'])
		print "Buy Sender", buySender
		print "Bought tokens for sender!"

		print "Buying tokens for receiver..."
		# Buy tokens with receiver_eth_id
		buyReceiver = subprocess.check_output(['node', 'buyOut.js', transaction.market_address, '1', str(int(transaction.marked_value))])
		print "Buy Receiver", buyReceiver
		print "Bought tokens for receiver!"

		print "checkspam:", check_spam(content)
		result = bool(check_spam(content)) # True when spam, False otherwise
		print "booled checkspam:", result
		print "Distributing money..."
		# Start the redeaming process here based on the result
		r = requests.get('localhost:8000/api/markets/' + transaction.market_address + "/?format=json")
		eventapi = json.loads(r.content)
		eventAddress = eventapi['event']['contract']['address']
		resolveSpam = subprocess.check_output(['node', 'resolveMarket.js', str(int(result))])
		print "resolveSpam", resolveSpam
		# TODO - redeem/withdraw tokens to ether
		senderCheckout = subprocess.check_output(['node', 'tokenCheckout.js', '0'])
		receiverCheckout = subprocess.check_output(['node', 'tokenCheckout.js', '1'])
	else:
		resolveNotSpam = subprocess.check_output(['node', 'resolveMarket.js', '0'])
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
		transaction = Transaction(email_id=email_id, market_address=None)
		transaction.save()
		print "Creating market..."
		market_address = str(subprocess.check_output(['node','createMarket.js']))
		print "Market created!", market_address
		depositToken = subprocess.check_output(['node','depositToken.js', market_address])
		print "Deposit Token", depositToken
		
		transaction.market_address = market_address
		transaction.save()
		if transaction.is_read:
			redeam(transaction)
		return HttpResponse('DoneSending')

@csrf_exempt
def reading(request):
	if request.method == "POST":
		marked = int(request.POST["marked"], 10)
		email_id = request.POST["email_id"]
		transaction = Transaction.objects.get(email_id=email_id)
		transaction.marked_value = bool(marked)
		transaction.is_read = True
		transaction.save()
		content = Email.objects.get(email_id=email_id).content
		if transaction.market_address is not None:
			redeam(transaction, content)
		return HttpResponse('Done')