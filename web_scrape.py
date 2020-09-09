from urllib.parse import urlparse
import urllib.robotparser
import requests
import re
from bs4 import BeautifulSoup 
import string

def can_fetch(url):
	"""
	Given a string of a URL, return True if we can scrape it, False otherwise
	"""
	parsed_uri = urlparse(url)
	domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	rp = urllib.robotparser.RobotFileParser()
	rp.set_url(domain + "/robots.txt")
	try:
		rp.read()    
		can_fetch_bool = rp.can_fetch("*", url)
	except:
		can_fetch_bool = None
	return can_fetch_bool

def get_paragraphs(url):
	"""
	Parse the given URL and return a list with all the content within each <div> section.
	"""
	response = requests.get(url, timeout=5)
	content = BeautifulSoup(response.content, "html.parser")
	return content.find_all('div')

def punctuations_list():
	"""
	Use the string package to get a list of all the punctuation marks.
	Apostrophes will be left in because of how they're used in contractions, possessive nouns, etc.
	"""
	punctuations = []
	for c in string.punctuation:
		if (c != "'"):
			punctuations.append(c)
	return punctuations

def create_string(paragraphs, song_title):
	"""
	Get rid of all the html code and put all the text into one string.
	Then, use the pattern of lyrics pages on AZLyrics to slice string so that only the lyrics are included.
	Finally, filter out all the ad-libs (words in parentheses), the artist names (in brackets), and convert the string to lowercase.
	"""
	to_return = ''
	for p in paragraphs:
		to_return += p.text
	#string slicing using the general format of AZLyrics pages
	to_return = to_return[to_return.index('Lyrics')+len('Lyrics'):to_return.index('if  ( /Android|webOS|iPhone|')]
	to_return = to_return[to_return.index(song_title)+len(song_title):]
	#remove adlibs and artist names; all text that are not lyrics
	for i in range(len(to_return)):
		char = to_return[i]
		if char == '(':
			temp = to_return[i:]
			end = 0
			for c in range(len(temp)):
				if temp[c] == ')':
					end = i+c
					break
			#empty space replaces the text in parentheses/brackets so as to not interrupt the for loop
			empty = ' ' * ((end-i)+1)
			to_return = to_return[:i] + empty + to_return[end+1:]
			continue
	for i in range(len(to_return)):
		char = to_return[i]
		if char == '[':
			temp = to_return[i:]
			end = 0
			for c in range(len(temp)):
				if temp[c] == ']':
					end = i+c
					break
			#empty space replaces the text in parentheses/brackets so as to not interrupt the for loop
			empty = ' ' * ((end-i)+1)
			to_return = to_return[:i] + empty + to_return[end+1:]
			continue
	#filter out the punctuation
	punctuations = punctuations_list()
	for p in punctuations:
		to_return = to_return.replace(p, '')
	#return the lowercase string
	return to_return.lower()

def process_url(url, song_title):
	"""
	Use/aggregate the functions above to process the url and return the string of lyrics
	"""
	if can_fetch(url) == False:
		return 'Cannot use given URL'
	else:
		return create_string(get_paragraphs(url), song_title)










