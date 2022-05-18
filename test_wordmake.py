"""
Tests wordmake.py
"""

from collections import Counter

import wordmake


def test_guess(guessword, finalword):
    """
    >>> test_guess("arose", "arose")
    ['g', 'g', 'g', 'g', 'g']
    >>> test_guess("arose", "finch")
    ['b', 'b', 'b', 'b', 'b']
    >>> test_guess("arose", "delve")
    ['b', 'b', 'b', 'b', 'g']
    >>> test_guess("arose", "clamp")
    ['y', 'b', 'b', 'b', 'b']
    >>> test_guess("arose", "soare")
    ['y', 'y', 'y', 'y', 'g']
    >>> test_guess("melee", "delve")
    ['b', 'g', 'g', 'b', 'g']
    >>> test_guess("allay", "llama")
    ['y', 'g', 'y', 'y', 'b']
    >>> test_guess("llama", "alloy")
    ['y', 'g', 'y', 'b', 'b']
    """
    if guessword is finalword:
        return ["g"] * 5
    outarray = ["b"] * 5
    letter_freq = Counter(list(finalword))
    letters_guessed = set(guessword)
    for i in letters_guessed:
        letter_indices_guess = list(find_all(guessword, i))
        pos_count = 0
        for index in letter_indices_guess:
            if guessword[index] == finalword[index]:
                outarray[index] = "g"
                pos_count += 1
        if pos_count < int(letter_freq.get(i) or 0):
            for index in letter_indices_guess:
                if outarray[index] != "g":
                    outarray[index] = "y"
                    pos_count += 1
                if pos_count == letter_freq.get(i):
                    break
    return outarray


def find_all(string, substring):
    """
    Returns a generator that finds instances of a substring in a string
    """
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            return
        yield start
        start += 1


def test_wordguess(finalword, debug=True):
    """
    Test wordmake's wordguess method
    """
    with open("/usr/share/dict/words", encoding="utf-8") as dictionary:
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

    my_counter = Counter([j for i in wordlist for j in i])
    guess_word = wordmake.wordsuggest(my_counter, wordlist, 5)
    # guess_word = "crate"
    prev_guesses = []
    guess_count = 0
    yellows = {}
    greens = {}
    blacks = {}

    updatedlist = wordlist

    while sum([len(i) for i in greens.values()]) != 5:
        if debug:
            print(f"Guessing {guess_word} for {finalword}")
        results = test_guess(guess_word, finalword)
        if debug:
            print(f"Got {results}")

        greens, yellows, blacks = wordmake.guess_eval(
            guess_word, results, greens, yellows, blacks
        )

        updatedlist = wordmake.gen_new_list(updatedlist, yellows, greens, blacks)

        my_counter = Counter([j for i in updatedlist for j in i])
        if my_counter:
            prev_guesses.append(guess_word)
            guess_word = wordmake.wordsuggest(my_counter, updatedlist, 5)
            if (
                len(prev_guesses) > 1
                and prev_guesses[-1] is guess_word
                and prev_guesses[-2] is guess_word
            ):
                raise ValueError
            print(guess_word)
            guess_count += 1

    print(f"{guess_word} was correct! Guessed in {guess_count} guesses")
    return guess_count


def main():
    """
    Runs an array of test cases
    """
    test_case = test_guess("allay", "llama")
    assert test_case == ["y", "g", "y", "y", "b"]
    test_wordguess("arose")
    test_wordguess("delve")
    test_wordguess("canny")
    test_wordguess("tepid")
    test_wordguess("zests")
    test_wordguess("being")
    test_wordguess("fully")
    test_wordguess("purer")
    test_wordguess("fishy")
    test_wordguess("crook")
    test_wordguess("masts")
    test_wordguess("pumps")
    test_wordguess("undue")
    test_wordguess("drool")
    test_wordguess("palls")
    with open("/usr/share/dict/words", encoding="utf-8") as dictionary:
        templist = dictionary.readlines()
        wordlist = list(
            dict.fromkeys(
                [
                    i.strip().lower()
                    for i in templist
                    if len(i.strip()) == 5
                    and i.strip().isalpha()
                    and i.isascii()
                    and i.islower()
                ]
            )
        )
    outlist = []
    index = 1
    for i in wordlist:
        print(f"Guessing on {i}")
        outlist.append(test_wordguess(i, False))
        print(f"----------{index/len(wordlist):.2%} done----------")
        index += 1

    print(f"Average guess score {sum(outlist)/len(outlist)}")


if __name__ == "__main__":
    main()
