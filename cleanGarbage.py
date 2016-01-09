#coding='utf-8'
#!/usr/bin/env python2
import os, csv, sys, django, pprint
import mimetypes, urllib2
import time, datetime
from threading import Thread
import requests
from bs4 import BeautifulSoup
import pyipinfodb


ip_lookup = pyipinfodb.IPInfo('1c43ec26ae1f5f688392853a00b92d35bf61ee00f8de1bd66c699ca0cddf214d')

def find_ip_location(ip_address):
	global ip_lookup
	return ip_lookup.get_city(ip_address)['cityName']


def is_url_image(url):    
    mimetype,encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))

def check_url(url):
    """Returns True if the url returns a response code between 200-300,
       otherwise return False.
    """
    try:
        headers={
            "Range": "bytes=0-10",
            "User-Agent": "MyTestAgent",
            "Accept":"*/*"
        }

        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req)
        return response.code in range(200, 209)
    except Exception, ex:
        return False

def is_image_and_ready(url, arr, *args):
	if is_url_image(url) and check_url(url) == True:
		if url.find('http://photo.xuite.net/') < 0 and url.find('http://ext.pimg.tw/') < 0 and url.find('http://pic.pimg.tw/') < 0:
			arr.append(url)



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

def crawl_detail_page(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	if len(soup.select('.article-meta-value')) == 4:
		return soup.select('.article-meta-value')[3].contents[0]
	else:
		return ''


def importData(data):

	processed_cnt = 0
	delim = '\t'

	for row in data:
		if row['url'] == '':
			pass
		elif row['img_list'] == '':
			pass
		else:
			list_tmp = row['img_list'].split(';')
			new_list = []
			new_img_list = ''
			threads = []
			for x in list_tmp:
				new_t = Thread(target = is_image_and_ready, args = (x, new_list))
				new_t.start()
				threads.append(new_t)
				# thread.start_new_thread(is_image_and_ready, (x, new_list,))
				# time.sleep(0.05)

			for t in threads:
				t.join()

			time.sleep(1)

			if new_list == []:
				pass
			else:
				tmp_date = crawl_detail_page(row['url'])
				if tmp_date != '':
					row['date'] = datetime.datetime.strptime(tmp_date,'%c').strftime('%Y-%m-%d %H:%M:%S')
					new_img_list = ';'.join(new_list)
					address = find_ip_location(row['ip'])
					print row['url']+delim+row['title']+delim+row['date']+delim+row['author']+delim+str(row['up'])+delim+str(row['normal'])+delim+str(row['down'])+delim+new_img_list+delim+row['ip']+delim+address.encode('utf-8')
		
		




if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("[usage] "+sys.argv[0]+" <table.csv>")
		sys.exit(1)
	else:
		# pp = pprint.PrettyPrinter(indent=4)
		vs = loadCsvAsDict(sys.argv[1])
		importData(vs)
		# pp.pprint(vs)
		# dumbImport(mergeCsvToDict(sys.argv[1:], "question_id"))
