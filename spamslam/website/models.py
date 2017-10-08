# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.core.validators import RegexValidator

# Create your models here.

class Email(models.Model):
	email_id = models.AutoField(primary_key=True)
	content = models.TextField(blank=False)
	sender_eth_id = models.CharField(null=False, max_length=42, validators=[RegexValidator(regex='^.{42}$', message='Length has to be 42', code='nomatch')])
	receiver_eth_id = models.CharField(null=False, max_length=42, validators=[RegexValidator(regex='^.{42}$', message='Length has to be 42', code='nomatch')])

class Transaction(models.Model):
	email_id = models.ForeignKey(Email)
	market_address = models.CharField(null=True, max_length=42, validators=[RegexValidator(regex='^.{42}$', message='Length has to be 42', code='nomatch')])
	is_read = models.BooleanField(default=False)
	is_processed = models.BooleanField(default=False)
	marked_value = models.BooleanField(default=False) # True when marked as spam
