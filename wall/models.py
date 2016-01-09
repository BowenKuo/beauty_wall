from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Content(models.Model):
	url = models.CharField(max_length=128, default='')
	title = models.CharField(max_length=128, default='')
	date = models.CharField(max_length=32, default='')
	author = models.CharField(max_length=32, default='')
	up = models.IntegerField()
	normal = models.IntegerField()
	down = models.IntegerField()
	img_list = models.CharField(max_length=10240, default='')
	ip = models.CharField(max_length=32, default='')
	# kind -> 1:girl , 2:boy , 3:search
	kind = models.IntegerField()