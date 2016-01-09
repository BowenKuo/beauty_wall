import mimetypes, urllib2

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

def is_image_and_ready(url):
    return is_url_image(url) and check_url(url)


if __name__ == '__main__':
	print is_image_and_ready('http://img158.imageshack.us/img158/3043/2rjg52t175cedzftn5oxpx7.jpg')