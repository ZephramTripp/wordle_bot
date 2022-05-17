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
    """
    if guessword is finalword:
        return ["g"] * 5
    outarray = ["b"] * 5
    letter_freq = Counter(list(finalword))
    guess_freq = Counter(list(guessword))
    letters_guessed = set(guessword)
    for i in letters_guessed:
        if not letter_freq.get(i):
            continue
        elif letter_freq.get(i) == 1 and guess_freq.get(i) == 1:
            if guessword.find(i) == finalword.find(i):
                outarray[guessword.find(i)] = "g"
            else:
                outarray[guessword.find(i)] = "y"
        elif letter_freq.get(i) > 1 and guess_freq.get(i) == 1:
            letter_indices = list(find_all(finalword, i))
            posRight = False
            for index in letter_indices:
                if guessword[index] is finalword[index]:
                    outarray[index] = "g"
                    posRight = True
            if not posRight:
                outarray[guessword.find(i)] = "y"
        elif letter_freq.get(i) == 1 and guess_freq.get(i) > 1:
            letter_indices = list(find_all(guessword, i))
            posRight = False
            for index in letter_indices:
                if guessword[index] == finalword[index]:
                    outarray[index] = "g"
                    posRight = True
            if not posRight:
                outarray[guessword.find(i)] = "y"
        elif letter_freq.get(i) > 1 and guess_freq.get(i) > 1:
            letter_indices_guess = list(find_all(guessword, i))
            posCount = 0
            for index in letter_indices_guess:
                if guessword[index] == finalword[index]:
                    outarray[index] = "g"
                    posCount += 1
            if posCount < letter_freq.get(i):
                for index in letter_indices_guess:
                    if outarray[index] != "g":
                        outarray[index] = "y"
                        posCount += 1
                    if posCount == letter_freq.get(i):
                        break
    return outarray


def find_all(string, substring):
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            return
        yield start
        start += 1


def test_wordguess(finalword, debug=True):
    with open("/usr/share/dict/words") as dictionary:
        templist = dictionary.readlines()
        wordlist = set(
            [
                i.strip().lower()
                for i in templist
                if len(i.strip()) == 5 and i.strip().isalpha() and i.isascii()
            ]
        )

    myCounter = Counter([j for i in wordlist for j in i])
    guessWord = wordmake.wordsuggest(myCounter, wordlist, 5)
    guessCount = 0
    yellows = {}
    greens = {}
    blacks = set([])

    while sum([len(i) for i in greens.values()]) != 5:
        if debug:
            print(f"Guessing {guessWord} for {finalword}")
        results = test_guess(guessWord, finalword)
        index = 0
        for i in guessWord:
            status = results[index]
            if status == "g":
                if i in greens.keys():
                    greens[i].add(index)
                else:
                    greens[i] = set([index])
            elif status == "y":
                if i in yellows.keys():
                    yellows[i].add(index)
                else:
                    yellows[i] = set([index])
            elif status == "b":
                blacks.add(i)
            else:
                status = ""
            index += 1

        updatedlist = []

        for i in wordlist:
            valid = True
            for letter in blacks:
                if (
                    letter in i
                    and letter not in yellows.keys()
                    and letter not in greens.keys()
                ):
                    valid = False
            for letter, pos in yellows.items():
                for num in pos:
                    if i[num] is letter:
                        valid = False
                if letter not in i:
                    valid = False
            for letter, pos in greens.items():
                for num in pos:
                    if i[num] is not letter:
                        valid = False
            if valid:
                updatedlist.append(i)

        newCounter = Counter([j for i in updatedlist for j in i])
        if newCounter:
            guessWord = wordmake.wordsuggest(myCounter, updatedlist, 5)
            guessCount += 1

    print(f"{guessWord} was correct! Guessed in {guessCount} guesses")
    return guessCount


def main():
    b = test_guess("allay", "llama")
    assert b == ["y", "g", "y", "y", "b"]
    test_wordguess("arose")
    test_wordguess("delve")
    test_wordguess("canny")
    test_wordguess("tepid")
    test_wordguess("zests")
    test_wordguess("being")
    # with open("/usr/share/dict/words") as dictionary:
    #     templist = dictionary.readlines()
    #     wordlist = set(
    #         [
    #             i.strip().lower()
    #             for i in templist
    #             if len(i.strip()) == 5
    #             and i.strip().isalpha()
    #             and i.isascii()
    #             and i.islower()
    #         ]
    #     )
    # outlist = []
    # index = 0
    # for i in wordlist:
    #     outlist.append(test_wordguess(i, False))
    #     print(f"----------{index*100/len(wordlist)}% done----------")
    #     index += 1

    # print(f"Average guess score {sum(outlist)/len(outlist)}")


if __name__ == "__main__":
    main()
