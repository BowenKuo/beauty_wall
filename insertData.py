#!/usr/bin/env python2
import os, csv, sys, django, pprint
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_wall.settings")
django.setup()
from wall.models import *

kind = 0


def str_to_bool(s):
    if s == 'true':
         return True
    elif s == 'false':
         return False
    else:
         raise ValueError 


def loadCsvAsDict(csvfile):
	with open(csvfile, 'r') as fin:
		csv_dict = [row for row in csv.DictReader(fin, delimiter='\t')]
	return csv_dict


def importData(data):
	global kind
	processed_cnt = 0

	for row in data:
		cont = Content.objects.create(
			url = row['url'],
			title = row['title'],
			date = row['date'],
			author = row['author'],
			up = int(row['up']),
			normal = int(row['normal']),
			down = int(row['down']),
			img_list = row['img_list'],
			ip = row['ip'],
			kind = kind)
		
		cont.save()
		
		processed_cnt += 1
		print("{0} / {1}".format(processed_cnt, len(data)))
		




if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("[usage] "+sys.argv[0]+" <table.csv>")
		sys.exit(1)
	else:
		kind = input('k ? ')
		vs = loadCsvAsDict(sys.argv[1])
		importData(vs)
