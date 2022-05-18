"""
This is the module docstring.
"""

from collections import Counter


def word_make(char_list, length):
    """
    This is the function docstring.
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
    This is the function docstring.
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
    This is the function docstring.
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
    This is the function docstring.
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
    Add documentation
    """
    updatedlist = []

    for i in wordlist:
        if validate_word(yellows, greens, blacks, i):
            updatedlist.append(i)

    return updatedlist


def validate_word(yellows, greens, blacks, word):
    """
    Add documentation
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
    This is the function docstring.
    """
    wordlist = ["table", "saber", "talon", "eager", "stuck"]

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

    guess_word = wordsuggest(my_counter, wordlist, 5)
    print(guess_word)

    yellows = {}
    greens = {}
    blacks = {}

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
