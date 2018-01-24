import requests
from lxml import html
from lxml import etree
import sys
import time

user_agent = 'Mozilla/5.0'


def query_homepage(site, novel):
	query = ""
	if site == "wuxiaworld":
		query += "//ul[@class='sub-menu']/li/a["
		if len(novel) == 1:
			print novel[0]
			query += "contains(text(), " + novel[0] + ")]/@href"
		else: 
			for word in novel:
				query += "contains(text(), '" + word + "') and "
			query = query[:len(query) - 5] + "]/@href"

	return query


def query_indexpage(site, indexpage):
	query = ""
	if site == "wuxiaworld":
		query += ("//a[contains(text(), 'Chapter') and " + 
					   "contains(@href, '" + indexpage +
					   "')]/@href")
		# query += ("//a[contains(text(), 'Chapter')]/@href")
	return query

def query_chapterpage(site):
	query = ""
	if site == "wuxiaworld":
		query += ("//div[@itemprop='articleBody']/p/text()" +
				   "|//div[@itemprop='articleBody']/p/strong/text()" + 
				   "|//div[@itemprop='articleBody']/p/b/text()")

	return query



if __name__ == '__main__':
	start_time = time.time()

	headers = {'User_Agent': user_agent}
	arguments = sys.argv

	if len(arguments) < 3:
		print "Missing arguments. Command should be python offlinenovel.py (site) (novel)"
	else:	
		site = str(sys.argv[1])
		homepage_url = "http://www." + str(sys.argv[1]) + ".com"
		novel_to_search = str(sys.argv[2]).split()
		print novel_to_search

		with open(sys.argv[2] + ".txt", 'w') as f:
			homepage = requests.request('GET', homepage_url, headers=headers)
			content = html.fromstring(homepage.content)
			query = query_homepage(site, novel_to_search)
			print query
			matching_link = content.xpath(query)[0]

			indexpage = requests.request('GET', matching_link, headers=headers)
			content = html.fromstring(indexpage.content)
			query = query_indexpage(site, matching_link)
			chapters = content.xpath(query)

			counter = 1
			for chapter in chapters:
				chapterpage = requests.request('GET', chapter, headers=headers)
				content = html.fromstring(chapterpage.content)
				query = query_chapterpage(site)
				chapter_text = content.xpath(query)
				chapter_text = chapter_text[1 : len(chapter_text) - 1]

				for line in chapter_text:
					f.write((line + "\n\n").encode('utf8', 'replace'))
				f.write("\n\n\n")
				print "chapter " + str(counter) + " done"
				counter += 1

		print("--- %s seconds ---" % (time.time() - start_time))

