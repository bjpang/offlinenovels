from html.parser import HTMLParser

class homeHTMLParser(HTMLParser):

	#List of Novels on this website
	novels = []

	def handle_starttag(self, tag, attrs):
		return

	def get_novels(self):
		return self.novels


class pageHTMLParser(HTMLParser):

	text = ''
