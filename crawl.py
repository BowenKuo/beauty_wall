# coding: utf-8
from bs4 import BeautifulSoup
from threading import Thread
import requests, re
import time, datetime
# index url setting

base = "https://www.ptt.cc" 
start_url = "/bbs/Beauty/index964.html"
delim = '\t'



def crawl_detail_page(c_dict, url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	ip_address_text = soup.find_all(text=re.compile(u"(From|來自).*[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"))
	ip_number = ''
	if ip_address_text:
		ip_address_content = ip_address_text[0]
		ip_address = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address_content)
		if ip_address:
			ip_number = ip_address.group()
	up = 0
	normal = 0
	down = 0
	img_list = ""
	img_urls = []
	if len(soup.select('.article-meta-value')) == 4:
		date_time = soup.select('.article-meta-value')[3].contents[0]
		fomrat_date_time = datetime.datetime.strptime(date_time,'%c')
		c_dict['date'] = fomrat_date_time.strftime('%Y-%m-%d %H:%M:%S')
	else:
		c_dict['date'] = ''

	for item in soup.select('img'):
		img_urls.append('http:'+item['src'])

	img_list = ';'.join(img_urls)

	for item in soup.select('.push'):
		spans = item.select('span')
		push_kind = spans[0].contents[0]
		if push_kind == u'推 ':
			up += 1
		elif push_kind == u'→ ':
			normal += 1
		elif push_kind == u'噓 ':
			down += 1

	c_dict['up'] = up
	c_dict['normal'] = normal
	c_dict['down'] = down
	c_dict['img_list'] = img_list
	c_dict['ip'] = ip_number



def search(f, item):
	global delim, base
	content = {}

	# deal with attribute 'title'
	try:
	    content['title'] = item.select('.title')[0].a.contents[0]
	except:
	    content['title'] = ""
	# deal with attribute 'author'
	try:
		content['author'] = item.select('.meta')[0].select('.author')[0].contents[0]
	except:
		content['author'] = ""
	# deal with attribute 'up', 'normal', 'down', 'img_list'
	try:
		inner_link = base+item.select('.title')[0].a['href']
		content['url'] = inner_link
		crawl_detail_page(content, inner_link)
	except:
		content['date'] = ''
		content['up'] = 0
		content['normal'] = 0
		content['down'] = 0
		content['img_list'] = ""
		content['url'] = ""
		content['ip'] = ""

	if content['url'] != '':
		# print content['url'].encode('utf-8')+delim+content['title'].encode('utf-8')+delim+content['date'].encode('utf-8')+delim+content['author'].encode('utf-8')+delim+str(content['up']).encode('utf-8')+delim+str(content['normal']).encode('utf-8')+delim+str(content['down']).encode('utf-8')+delim+content['img_list'].encode('utf-8')+delim+content['ip'].encode('utf-8')+'\n'
		f.write(content['url'].encode('utf-8')+delim+content['title'].encode('utf-8')+delim+content['date'].encode('utf-8')+delim+content['author'].encode('utf-8')+delim+str(content['up']).encode('utf-8')+delim+str(content['normal']).encode('utf-8')+delim+str(content['down']).encode('utf-8')+delim+content['img_list'].encode('utf-8')+delim+content['ip'].encode('utf-8')+'\n')


def crawl_base_pages(f, url):
	global delim, base
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	print url
	threads = []
	for item in soup.select('.r-ent'):
		new_t = Thread(target = search, args = (f, item))
		new_t.start()
		threads.append(new_t)
		# time.sleep(0.05)

	for t in threads:
		t.join()

	time.sleep(1)

	if soup.select('.action-bar'):
		if len(soup.select('.action-bar')[0].select('.btn')) > 4:
			 crawl_base_pages(f, base+soup.select('.action-bar')[0].select('.btn')[4]['href'])



if __name__ == "__main__":
	f = open('Beauty1231.csv', 'a')
	crawl_base_pages(f, base+start_url)
	f.close()
