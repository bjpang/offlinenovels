import requests
from lxml import html
from lxml import etree
from io import StringIO, BytesIO



if __name__ == '__main__':
	sites = ['http://www.wuxiaworld.com']
	novels = ['Coiling Dragon']
	user_agent = 'Mozilla/5.0'
	headers = {'User_Agent': user_agent}

	with open('info.html', 'w') as f:
		for site in sites:
			page = requests.request('GET', site, headers=headers)
			content = html.fromstring(page.content)
			f.write(page.text.encode('utf8'))



