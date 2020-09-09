import nltk
from itertools import dropwhile
# Download and generate CMU dictionary
nltk.download('cmudict')
pronounciation = dict(nltk.corpus.cmudict.entries())
from hyphenate import hyphenate_word
def get_phonemes(word, selection_criteria):
    """Get the phonetic representation of the syllables after the stress.
    :param word: String containing the word.
    :param selection_criteria: Function to filter the selected phonemes.
    :returns: Syllables corresponding to the word.
    :rtype: list
    """
    try:
        key = word.strip().lower()
        ending = dropwhile(lambda x: '1' not in x, pronounciation[key])
        return [p for p in ending if selection_criteria(p)]
    except KeyError:
        """
        jacquelinekclee's edit: words not in the CMU dict may be compound words.
        thus, use the hyphenate package to divide such words into its components and 
        try to get the phoneme of the last word component. 
        """
        try: 
            key = hyphenate_word(word)[-1]
            ending = dropwhile(lambda x: '1' not in x, pronounciation[key])
            return [p for p in ending if selection_criteria(p)]
        except KeyError:
            return []


def get_perfect_phonemes(word):
    """Get the phonetic representation of the sounds after the stress.
    :param word: String containing the word.
    :returns: Syllables corresponding to the word.
    :rtype: list
    """
    return get_phonemes(word, lambda p: True)


def get_vowel_phonemes(word):
    """Get the phonetic representation of the vowels after the stress.
    :param word: String containing the word.
    :returns: Vowel syllables corresponding to the word.
    :rtype: list
    """
    return get_phonemes(word, lambda p: any(ch.isdigit() for ch in p))

def _rhyme(word_a, word_b, phonemes_func):
    """Return whether two words form a rhyme.
    This function is just a general version and the shorthands available in the
    same module should be used instead, except a custom function for extracting
    phonemes is to be used.
    :param word_a: first word.
    :param word_b: second word.
    :param phonemes_func: function to extract relevant phonemes.
    :returns: True if they rhyme following the given conditions.
    :rtype: bool
    """
    return phonemes_func(word_a) == phonemes_func(word_b)


def perfect_rhyme(word_a, word_b):
    """Return whether two words form a perfect rhyme.
    :param word_a: first word.
    :param word_b: second word.
    :returns: True if they perfectly rhyme.
    :rtype: bool
    """
    return _rhyme(word_a, word_b, get_perfect_phonemes)


def vowel_rhyme(word_a, word_b):
    """Return whether two words form a vowel rhyme.
    :param word_a: first word.
    :param word_b: second word.
    :returns: True if they rhyme on vowels.
    :rtype: bool
    """
    return _rhyme(word_a, word_b, get_vowel_phonemes)

def count_rhymes(end_words):
    """
    jacquelinekclee's function:
    This function uses the functions above to count the total number of 
    end rhymes (either perfect or rhyme) and total number of unique end rhymes
    given a list of end words (last word of each bar)
    """
    prev = ''
    other = ''
    unique_rhyme_count = 0
    rhyme_count = 0
    rhymes = []
    for i in range(len(end_words)):
        curr = end_words[i]
        if i == 0:
            prev = curr
            continue
        if i == 1:
            if (perfect_rhyme(curr, prev) or vowel_rhyme(curr, prev)):
                words = (curr, prev)
                rhyme_count += 1
                if words not in rhymes:
                    unique_rhyme_count += 1
                    rhymes.append(words)
            other = prev
            prev = curr
            continue
        else:
            if (perfect_rhyme(curr, prev) or vowel_rhyme(curr, prev)):
                words = (curr, prev)
                rhyme_count += 1
                if words not in rhymes:
                    unique_rhyme_count += 1
                    rhymes.append(words)
            if (perfect_rhyme(curr, other) or vowel_rhyme(curr, other)):
                words = (curr, other)
                rhyme_count += 1
                if words not in rhymes:
                    unique_rhyme_count += 1
                    rhymes.append(words)
            if i == len(end_words) - 1:
                continue
            other = prev
            prev = curr
    return (rhyme_count, unique_rhyme_count)

def count_two_rhymes(two_end_words):
    """
    jacquelinekclee's function:
    This function uses the functions above to count the total number of 
    end rhymes (either perfect or rhyme) given a list of end words (last
    word of each bar)
    """
    prev = []
    other = []
    rhyme_count = 0
    rhymes = []
    for i in range(len(two_end_words)):
        curr = two_end_words[i]
        #don't compare anything for first bar
        if i == 0:
            prev = curr
            continue
        #only one set of words to compare to for second bar
        if i == 1:
            if (len(curr) > 0) and (len(prev) > 0):
                #count only if both sets of end words are not the same
                if (curr[0] != prev[0]) and (curr[1] != prev[1]):
                    if (perfect_rhyme(curr[0], prev[0]) or vowel_rhyme(curr[0], prev[0])):
                        if (perfect_rhyme(curr[1], prev[1]) or vowel_rhyme(curr[1], prev[1])):
                            tup = (curr[0] + ' ' + curr[1], prev[0] + ' ' + prev[1])
                            rhymes.append(tup)
                            rhyme_count += 1
            #update the variables
            other = prev
            prev = curr
            continue
        else:
            #check both prev and other if all lists are not empty
            if (len(curr) > 0) and (len(prev) > 0) and (len(other) > 0): 
                #do not count if both sets of end words are the same
                if (curr[0] != prev[0]) and (curr[1] != prev[1]):
                    if (perfect_rhyme(curr[0], prev[0]) or vowel_rhyme(curr[0], prev[0])):
                        if (perfect_rhyme(curr[1], prev[1]) or vowel_rhyme(curr[1], prev[1])):
                            tup = (curr[0] + ' ' + curr[1], prev[0] + ' ' + prev[1])
                            rhymes.append(tup)
                            rhyme_count += 1
                #do the same with bar before previous bar
                if (curr[0] != other[0]) and (curr[1] != other[1]):
                    if (perfect_rhyme(curr[0], other[0]) or vowel_rhyme(curr[0], other[0])):
                        if (perfect_rhyme(curr[1], other[1]) or vowel_rhyme(curr[1], other[1])):
                            tup = (curr[0] + ' ' + curr[1], other[0] + ' ' + other[1])
                            rhymes.append(tup)
                            rhyme_count += 1
            else:
                if (len(curr) > 0):
                    if (len(prev) > 0) or (len(other) > 0):
                        if (len(prev) == 0) and (len(other) > 0):
                            if (curr[0] != other[0]) and (curr[1] != other[1]):
                                if (perfect_rhyme(curr[0], other[0]) or vowel_rhyme(curr[0], other[0])):
                                    if (perfect_rhyme(curr[1], other[1]) or vowel_rhyme(curr[1], other[1])):
                                        tup = (curr[0] + ' ' + curr[1], other[0] + ' ' + other[1])
                                        rhymes.append(tup)
                                        rhyme_count += 1
                        if (len(other) == 0) and (len(prev) > 0):
                            if (curr[0] != prev[0]) and (curr[1] != prev[1]):
                                if (perfect_rhyme(curr[0], prev[0]) or vowel_rhyme(curr[0], prev[0])):
                                    if (perfect_rhyme(curr[1], prev[1]) or vowel_rhyme(curr[1], prev[1])):
                                        tup = (curr[0] + ' ' + curr[1], prev[0] + ' ' + prev[1])
                                        rhymes.append(tup)
                                        rhyme_count += 1
            #update the variables if not last bar
            if i < (len(two_end_words) - 1):
                other = prev
                prev = curr
    return [rhyme_count, rhymes]
