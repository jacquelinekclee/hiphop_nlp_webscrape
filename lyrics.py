import requests
import re
from bs4 import BeautifulSoup
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import syllables
import numpy as np
import pandas as pd

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

def get_bars(string):
	"""
	Given a string of lyrics scraped from AZLyrics, return a list of strings, each string being 1 bar.
	"""
	bars = string.split('\n')
	#filter out empty strings
	bars = list(filter(lambda s: (len(s) > 0) and (s != ' '), bars))
	#filter out strings only consisting of spaces
	bars = list(filter(lambda s: s.isspace() == False, bars))
	return bars

def get_end_words(bars):
	"""
	Given a list of bars, return a list of strings, each string being the last word in a bar.
	"""
	to_return = []
	for bar in bars:
		words = bar.split()
		if len(words) > 0:
			to_return.append(words[-1])
	return to_return

def get_two_words(bars):
	"""
	Given a list of bars, return a list of lists, each list containing the last 2 words in a bar.
	"""
	to_return = []
	for bar in bars:
		words = bar.split()
		last_two = []
		if len(words) > 1:
			last_two.append(words[-2])
			last_two.append(words[-1])
		to_return.append(last_two)
	return to_return

def get_all_words(string):
	"""
	Given a string of lyrics scraped from AZLyrics, return a list of strings, each string being one word.
	"""
	return string.split()

def remove_stop_words(all_words):
	"""
	Given a list of all the words in a song, filter out the stop words (as defined by the nltk package).
	"""
	stop_words = stopwords.words('english')
	return list(filter(lambda word: word not in stop_words, all_words))

def get_unique_words(all_words_no_stops):
	"""
	Return the number of unique words, excluding stop words. This function removes repeats.
	"""
	return list(set(all_words_no_stops))

def get_total_words(all_words):
	"""
	Return the number of words.
	"""
	return len(all_words)

def get_prop_unique_words(unique_words, total_words):
	"""
	Return the proportion of unique words to all words in a song. 
	"""
	return len(unique_words) / total_words

def get_prop_stops(all_words_no_stops, total_words):
	"""
	Return the proportion of stop words to all words in a song.
	"""
	num_stops = total_words - len(all_words_no_stops)
	return num_stops / total_words

def get_average_syllables(bars):
	"""
	Calculate the average number of syllables per bar
	"""
	bar_syllables = []
	for bar in bars:
		bar_syllables.append(syllables.estimate(bar))
	return np.mean(np.asarray(bar_syllables))

def get_word_counts(all_words_no_stops, unique_words):
	"""
	Create and return a Pandas DataFrame storing the counts of each unique word (excluding stop words).
	"""
	word_counts = []
	for word in unique_words:
		word_counts.append(all_words_no_stops.count(word))
	count_df = pd.DataFrame(data={'Word':unique_words, 'Count':word_counts})
	count_df = count_df.sort_values('Count', ascending=False).reset_index(drop=True)
	return count_df

