import requests
from os.path import basename
from urlparse import urlsplit
import urllib2
import re
import os
import json
import requests.packages.urllib3.util.ssl_

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS='ALL'

if not os.path.exists("images"):
	os.mkdir("images")

url = 'https://www.zhihu.com/question/37787176'

url_content = urllib2.urlopen(url).read()

answers = re.findall('<meta itemprop="answerCount" content="(.*?)"', url_content)

limits = int(answers[0])
page_size = 1
offset = 0

request_headers = {
	'accept':'application/json, text/plain, */*',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
	'Connection':'keep-alive',
	'Cookie':'',
	'Host':'www.zhihu.com',
	'Referer':'https://www.zhihu.com/question/37787176',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

# https://www.zhihu.com/api/v4/questions/37787176/answers

while offset < limits:

	get_url = "https://www.zhihu.com/api/v4/questions/37787176/answers?include=data[*].is_normal,admin_closed_comment,reward_info,\
	  is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,\
	  editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,is_author,\
	  voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&offset=%d&limit=%d&sort_by=default"%(offset, page_size);

	res = requests.get(get_url, headers=request_headers)

	answer_list = res.json()["data"]

	for i in answer_list:
	
		# get picture download url
		img_urls = re.findall('data-actualsrc="(.*?_b.*?)"', ''.join(i["content"]))

		for img_url in img_urls:
			try:
				print img_url
				img_data = urllib2.urlopen(img_url).read()
				file_name = basename(urlsplit(img_url)[2])
				output = open('images/' + file_name, 'wb')
				output.write(img_data)
				output.close()
			except:
				print "download image error."
				pass
	offset += page_size
