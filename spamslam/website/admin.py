# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from website.models import *
# Register your models here.

class EmailAdmin(admin.ModelAdmin):
	pass


class TransactionAdmin(admin.ModelAdmin):
	pass

admin.site.register(Email, EmailAdmin)
admin.site.register(Transaction, TransactionAdmin)
