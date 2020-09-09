# Has Hip-Hop Gotten Worse? - Web Scraping and NLP Project

![banner](https://github.com/jacquelinekclee/hiphop_nlp_webscrape/blob/master/rappers.JPG =1260x600)

# Table of contents

- [Background](#background)
- [Song Selection](#song-selection)
- [Lyrics Source](#lyrics-source)
- [Metrics](#metrics)
- [Goal](#goal)
- [Source Files](#source-files)

## Background
Hip-hop/rap music was founded in the 1970's and became widespread during the 80's, kicking off the decade-long era known as the "golden age" of hip-hop [(NPR)](https://www.npr.org/templates/story/story.php?storyId=7550286#:~:text=Rap%20as%20a%20genre%20began,generally%20interacting%20with%20the%20audience.).

Today, hip-hop/rap is music's most popular and commercially successful genre. Every region has its own style of rap and numerous musical and cultural trends have defined hip-hop over the years.

Many fans believe that rap music has gotten worse over the years, crediting this decline to the rise of what is called [mumble rap](https://www.cleveland.com/entertainment/2017/06/what_is_mumble_rap_25_essentia.html), a style characterized by artists rapping inchorently and/or melodically and using a variety of ad-libs as opposed to actual lyrics. But, while mumble rap has certainly risen in popularity, does this mean that "good" rap, music filled with clever and meaningful lyrics, has vanished from the genre? 

To answer this question, I will be analyzing the lyrics of the best rap song from every year from 1990 to 2020. 

[(Back to top)](#table-of-contents)

## Song Selection
Songs from 1990-2003 will be pulled from **Complex article, ["The Best Rap Song, Every Year Since 1979"](https://www.complex.com/music/best-rap-songs-since-1979/)** and the songs from 2004-2020 will be the winners of the **[Grammy Award for Best Rap Song](https://en.wikipedia.org/wiki/Grammy_Award_for_Best_Rap_Song#Recipients)** (first awarded in 2004).
* Since many artists have won the Best Rap Song award multiple times (Kanye West, JAY-Z, Kendrick Lamar), this analysis focuses more on whether or not the best of the best rap songs from more current years are just as good as those from the 90's and early 2000's rather than finding out if the hip-hop/rap genre as a whole has seen a decline in song quality.
* "The Choice Is Yours" by Black Sheep is not on AZLyrics and also not on Spotify, so I will use one of Complex's honorable mentions, "My Mind Playin' Tricks On Me" by Geto Boys.
* Complex's choice for 2002 ("Lose Yourself" by Eminem) is the same as the 2004 Best Rap Song recipient, so similarly I will use one of Complex's honorable mentions, "Grindin" by The Clipse.

[(Back to top)](#table-of-contents)

## Lyrics Source
The lyrics for each will be scraped from **[AZLyrics](https://www.azlyrics.com/)**. Since these lyrics are user submitted, the formatting of lyrics is variable. This variation is largely in how chorus lyrics are posted. For example, one song may have all the lyrics to the entire chorus typed out each time whereas another may just use '[Chorus]' or '[2x]' to avoid repetition. My hope is that this will not affect the metrics too much, as songs with shorter/less repetitive choruses can indicate a song's greater substance and lyrical quality.

[(Back to top)](#table-of-contents)

## Metrics:
* Proportion of unique words to total words, excluding stop words.
  * Evaluates the range of vocabulary in a given song.
* Proportion of stop words to total words.
  * Indicates the substance of a song's lyrics.
* Average number of syllables per bar.
  * Examines a rapper's skill, as it takes more creativity and ingenuity to fit a greater number of syllables into a bar.
* Proportion of exact end rhymes and vowel end rhymes (in every two bars or every other bar) to number of bars.
  * Also examines a rapper's lyricism.
  * Most common rhyme schemes are aabb and abab, so I will only look for these 2.
  * I will exclude bars using the same words to create the rhyme scheme. In other words, if two bars are "I like greens / She likes greens," this rhyme will not be counted as the same word is used. This will be done in attempt to accredit songs that more cleverly create rhyme schemes and to avoid inflating this metric for songs with choruses that may be extremely repetitive (e.g., ["Mama Said Knock You Out" by LL Cool J](https://www.azlyrics.com/lyrics/llcoolj/mamasaidknockyouout.html)).
  * The fucntions used to analyze rhymes use the Carnegie Mellon University Pronouncing Dictionary. Therefore, the creativity and accents rapper use to manipulate different rhymes will unfortunately not be detected. Thus, this measure will be analyzed with a grain of salt.
* The proportion of exact end rhymes and vowel end rhymes (for the **last two words** in every two bars or every other bar) to number of bars.
  * This doesn't take into account rhymes like "maintain" and "blame game" where the last two syllables of 2 bars rhyme. Rhymes like "blue pen" and "pursue hen" would count. Again, this measure will be analyzed with a grain of salt.
* Additionally, I will also be looking at the most common words (excluding stop words) for each song. This measure is much more subjective than the others, but could potentially give insight into a song's substance.

[(Back to top)](#table-of-contents)

Here are some quick definitions of terms used in this project:
* **[Bar](https://www.lexico.com/en/definition/bar)**: One line of lyrics. Detected by line break characters. Typically takes four beats.
* **[End rhymes](https://literarydevices.net/end-rhyme/)**: Rhymes that occur with the last word/syllables of a bar. Example: "I like greens / She likes beans" (greens and beans, the last word of each bar/line, rhyme).
* **[Exact rhyme](https://literarydevices.net/exact-rhyme/)**: When the vowel sound and final consonant of two words are phonetically the same, e.g. greens and beans.
* **[Vowel rhyme](https://www.thefreedictionary.com/vowel+rhyme)**: When the vowel sound of two words are phonetically the same, e.g. green and seem.
* **[Stop word](https://www.geeksforgeeks.org/removing-stop-words-nltk-python)**: A word that does not contribute much meaning, e.g. the, a, an. Search engines are programmed to ignore these words, and ignoring these words both save processing time and allow us to analyze lyrics more meaningfully.

[(Back to top)](#table-of-contents)

## Goal
As stated above, this project has some limitations in terms of the consistency of lyric data, the extent to which the packages/tools used can analyze rap lyrics, and the overall subjectivity of this topic. Ultimately, I started this project as a fun way to both explore one of my interests and utilize the skills and technical knowledge I have learned thus far. But, I certainly believe that the results of this project can give insight into how rap music has evolved over the years.

[(Back to top)](#table-of-contents)

## Source Files
* [web_scrape.py](web_scrape.py)
  * Has all the functions used for web scraping and processing the HTML. It also processes the string (lyrics) so it's ready for analyzing the lyrics.
* [lyrics.py](lyrics.py)
  * Used to break down the string of lyrics into bars and words and calculate the word based metrics.
* [rhyme.py](rhyme.py)
  * Provides the functions used to calculate the rhyme-based metrics
  * The contents of this file are adopted from the dandelion package as laid out [here](https://github.com/DiegoVicen/dandelion). Edits made by me (jacquelinekclee) are denoted in the docstrings.
  
  [(Back to top)](#table-of-contents)
