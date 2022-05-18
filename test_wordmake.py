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


def test_wordguess(finalword, startingword=None, debug=True):
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
    if startingword is None:
        guess_word = wordmake.wordsuggest(my_counter, wordlist, 5)
    else:
        guess_word = startingword
    prev_guesses = []
    guessCount = 0
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
        #print(my_counter.most_common(10))
        if my_counter:
            prev_guesses.append(guess_word)
            guess_word = wordmake.wordsuggest(my_counter, updatedlist, 5)
            if (
                len(prev_guesses) > 1
                and prev_guesses[-1] is guess_word
                and prev_guesses[-2] is guess_word
            ):
                raise ValueError
            #print(guess_word)
            guessCount += 1

    #print(f"{guess_word} was correct! Guessed in {guessCount} guesses")
    return guessCount

def find_best_starting_word():
    with open("/usr/share/dict/words") as dictionary:
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
    bestword_failure = ""
    bestword_score = ""
    bestfail = 500
    bestscore = 6
    for word in wordlist:
        subindex = 1
        for i in wordlist:
            #print(f"Guessing on {i}")
            outlist.append(test_wordguess(i, word, False))
            #print(f"----------{subindex/len(wordlist):.2%} done----------")
            subindex += 1
        #print(f"Average guess score {sum(outlist)/len(outlist)}")
        if sum(outlist)/len(outlist) < bestscore:
            bestscore = sum(outlist)/len(outlist)
            bestword_score = word
        #print(f"Fails on {len([i for i in outlist if i>6])} words")
        if len([i for i in outlist if i>6]) < bestfail:
            bestfail = len([i for i in outlist if i>6])
            bestword_failure = word
        index += 1
        #print(f"***{index/len(wordlist):.2%} done***")
        if index == 2:
            break
    print(f"Least fails : {bestfail} with {bestword_failure}")
    print(f"Best score: {bestscore} with {bestword_score}")


def main():
    # b = test_guess("allay", "llama")
    # assert b == ["y", "g", "y", "y", "b"]
    # test_wordguess("arose")
    # test_wordguess("delve")
    # test_wordguess("canny")
    # test_wordguess("tepid")
    # test_wordguess("zests")
    # test_wordguess("being")
    # test_wordguess("fully")
    # test_wordguess("purer")
    # test_wordguess("fishy")
    # test_wordguess("crook")
    # test_wordguess("masts")
    # test_wordguess("pumps")
    # test_wordguess("undue")
    # test_wordguess("drool")
    # test_wordguess("palls")
    # with open("/usr/share/dict/words") as dictionary:
    #     templist = dictionary.readlines()
    #     wordlist = list(
    #         dict.fromkeys(
    #             [
    #                 i.strip().lower()
    #                 for i in templist
    #                 if len(i.strip()) == 5
    #                 and i.strip().isalpha()
    #                 and i.isascii()
    #                 and i.islower()
    #             ]
    #         )
    #     )
    # outlist = []
    # index = 1
    # for i in wordlist:
    #     print(f"Guessing on {i}")
    #     outlist.append(test_wordguess(i, False))
    #     print(f"----------{index*100/len(wordlist)}% done----------")
    #     index += 1

    # print(f"Average guess score {sum(outlist)/len(outlist)}")
    # print(f"Fails on {len([i for i in outlist if i>6])} words")
    find_best_starting_word()

if __name__ == "__main__":
    main()
