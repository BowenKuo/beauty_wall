# coding: utf-8
from django.shortcuts import render
from .models import *
import pprint, collections, json

# Create your views here.
def show(request, k=1):
	kind_dictionary = { 1: u'正妹' , 2: u'帥哥' , 3: u'神人', }
	
	try:
		k = int(k)
		c_k = kind_dictionary[k]
	except:
		k = 1
		c_k = kind_dictionary[k]

	t = {"kind": k,
		 "chinese_kind": c_k}

	return render(request, 'wall/photo_wall.html', t)

def get_info(request, k=1):

	try:
		k = int(k)
	except:
		k = 1

	contents = []
	contents = Content.objects.filter(kind=k)
	lists = []
	for item in contents:
		photo_list = {}
		count = 0
		for x in item.img_list.split(';'):
			photo_list[count] = x.encode('ascii')
			count += 1
		item.img_list = photo_list
		lists.append(
				{
					'url': item.url,
					'title': item.title.encode('utf-8'),
					'author': item.author,
					'date': item.date,
					'up': item.up,
					'down': item.down,
					'img_list': item.img_list,
					'ip': item.ip,
				}
			)
	
	trans = json.dumps(lists)

	t = {"contents": trans}
	return render(request, 'wall/get_info.html', t)
