"""
Wordmake is a module containing a few methods I use to solve Wordle puzzles.
It should probably containing a class definition, but it doesn't yet.
"""

from collections import Counter


def get_wordlist(filename):
    """
    Opens a textfile and extracts lines containing five-letter, lowercase, ASCII words

    :param filename: Name of the file to open
    :type filename: string
    :return: List of five letter words
    :rtype: list of strings
    """
    with open(filename, encoding="utf-8") as dictionary:
        wordlist = list(
            dict.fromkeys(
                [
                    i.strip().lower()
                    for i in dictionary.readlines()
                    if len(i.strip()) == 5
                    and i.strip().isalpha()
                    and i.isascii()
                    and i.islower()
                ]
            )
        )
    return wordlist


def word_make(char_list, length):
    """
    Takes a list of characters and an integer length and generates all
    combinations of the characters at that length.

    :param char_list: The list of characters to use
    :type char_list: list of strings
    :param length: Length of strings to generate
    :type length: int
    :return: The list of strings generated
    :rtype: list of strings
    """
    outlist = []
    if length == 1:
        return char_list
    for i in char_list:
        subwords = word_make(char_list, length - 1)
        outlist.extend([i + j for j in subwords])
    return outlist


def wordsuggest(counter, wordlist, depth):
    """
    Suggests the word with the greatest letter frequency usage
    from the given list and frequency data

    :param counter: The frequency data of letters in the wordlist
    :type counter: collections.Counter
    :param wordlist: The list of words to choose from
    :type wordlist: list of strings
    :param depth: The top *depth* most common letters will be considered
    :type depth: int
    :return: The best word to guess
    :rtype: string
    """
    letters = counter.most_common(depth)
    newlist = [j for j in wordlist if all((k in [i[0] for i in letters] for k in j))]
    if newlist:
        bestword = newlist[0]
        bestcount = 0
        for i in newlist:
            count = sum([counter[letter] for letter in dict.fromkeys(i)])
            if count > bestcount:
                bestword = i
                bestcount = count
        if (
            len(set(bestword)) < len(list(bestword))
            and len(wordlist) > 1
            and depth < len(counter)
        ):
            trialword = wordsuggest(counter, wordlist, depth + 1)
            newcount = sum([counter[letter] for letter in dict.fromkeys(trialword)])
            if newcount > count:
                return trialword
            return bestword
        return bestword
    return wordsuggest(counter, wordlist, depth + 1)


def collect_input(guess):
    """
    Collects user input on the accuracy of the word guessed

    :param guess: The guess to be evaluated
    :type guess: string
    :return: The user input as a list
    :rtype: list of strings
    """
    outlist = []
    for i in guess:
        status = ""
        while not status:
            print(f"Was {i} g, y, or b?")
            status = str(input())
            if status not in list("gyb"):
                status = ""
            else:
                outlist.append(status)
    return outlist


def guess_eval(guess, result, greens, yellows, blacks):
    """
    A helper function to move the results of a guess evaluation
    to the dictionaries of guessed values

    :param guess: The word guessed
    :type guess: string
    :param result: The result of the guess
    :type result: string or list of strings
    :param greens: The previous known letters with verified existence and placement
    :type greens: dictionary
    :param yellows: The previous known letters with verified existence but not placement
    :type yellows: dictionary
    :param blacks: The previous known letters with verified non-existence
    :type blacks: dictionary
    :return: The three input dictionaries with the new information added
    :rtype: three dictionaries
    """
    for index, i in enumerate(guess):
        if result[index] == "g":
            if i in greens:
                greens[i][index] = None
            else:
                greens[i] = dict.fromkeys([index])
        elif result[index] == "y":
            if i in yellows:
                yellows[i][index] = None
            else:
                yellows[i] = dict.fromkeys([index])
        elif result[index] == "b":
            if i in blacks:
                blacks[i][index] = None
            else:
                blacks[i] = dict.fromkeys([index])
    return greens, yellows, blacks


def gen_new_list(wordlist, yellows, greens, blacks):
    """
    Given a wordlist and the dictionaries containing the results of previous guesses,
    generates a new wordlist.

    :param wordlist: The previous wordlist
    :type wordlist: list of strings
    :param yellows: The previous known letters with verified existence but not placement
    :type yellows: dictionary
    :param greens: The previous known letters with verified existence and placement
    :type greens: dictionary
    :param blacks: The previous known letters with verified non-existence
    :type blacks: dictionary
    :return: The new word list
    :rtype: list of strings
    """
    updatedlist = []

    for i in wordlist:
        if validate_word(yellows, greens, blacks, i):
            updatedlist.append(i)

    return updatedlist


def validate_word(yellows, greens, blacks, word):
    """
    Checks a word against previous guesses to see if it is still a legal word

    :param yellows: The previous known letters with verified existence but not placement
    :type yellows: dictionary
    :param greens: The previous known letters with verified existence and placement
    :type greens: dictionary
    :param blacks: The previous known letters with verified non-existence
    :type blacks: dictionary
    :param wordlist: The word to evaluate
    :type wordlist: string
    :return: whether the word is legal or not
    :rtype: bool
    """
    valid = True
    for letter, pos in blacks.items():
        if letter in word and letter not in yellows and letter not in greens:
            return False
        if letter in word and (letter in yellows or letter in greens):
            valid = not any((word[num] is letter for num in pos))
            if not valid:
                return False
    for letter, pos in yellows.items():
        for num in pos:
            if word[num] is letter:
                return False
        if letter not in word:
            return False
    for letter, pos in greens.items():
        for num in pos:
            if word[num] is not letter:
                return False
    return valid


def main():
    """
    The main function plays one game of Wordle against the user,
    with the computer making guesses and the user verifying the computer's guesses
    """
    wordlist = get_wordlist("/usr/share/dict/words")

    my_counter = Counter([j for i in wordlist for j in i])

    guess_word = wordsuggest(my_counter, wordlist, 5)
    guess_word = "plant"
    print(guess_word)

    yellows, greens, blacks = {}, {}, {}

    updatedlist = wordlist

    while sum([len(i) for i in greens.values()]) != 5:

        result = collect_input(guess_word)
        greens, yellows, blacks = guess_eval(
            guess_word, result, greens, yellows, blacks
        )

        updatedlist = gen_new_list(updatedlist, yellows, greens, blacks)

        my_counter = Counter([j for i in updatedlist for j in i])
        if my_counter:
            guess_word = wordsuggest(my_counter, updatedlist, 5)
            print(guess_word)


if __name__ == "__main__":
    main()
