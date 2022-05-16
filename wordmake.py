from collections import Counter

alphabet = "abcdefghijklmnopqrstuvwxyz"
wordlist = ["table", "saber", "talon", "eager", "stuck"]

with open("/usr/share/dict/words") as dictionary:
    templist = dictionary.readlines()
    wordlist = [
        i.strip()
        for i in templist
        if len(i.strip()) == 5 and i.strip().isalpha() and i.isascii()
    ]


def word_make(char_list, length):
    outlist = []
    if length == 1:
        return char_list
    for i in char_list:
        subwords = word_make(char_list, length - 1)
        outlist.extend([i + j for j in subwords])
    return outlist


# b = word_make(list(alphabet), 5)

myCounter = Counter([j for i in wordlist for j in i])

print(myCounter.most_common(10))


def wordsuggest(counter, wordlist, depth):
    length = 5
    letters = counter.most_common(depth)
    newlist = word_make([i[0] for i in letters], length)
    outlist = []
    for word in newlist:
        if word in wordlist:
            outlist.append(word)
    if outlist:
        # print(outlist)
        bestword = outlist[0]
        bestcount = 0
        for i in outlist:
            count = sum([counter[letter] for letter in set(i)])
            # print(i, count)
            if count > bestcount:
                bestword = i
                bestcount = count
        if len(set(i)) < len(list(i)) and len(wordlist) > 1 and depth < 20:
            trialword = wordsuggest(counter, wordlist, depth + 1)
            newcount = sum([counter[letter] for letter in set(trialword)])
            if newcount > count:
                return trialword
            else:
                return bestword
        return bestword
    else:
        return wordsuggest(counter, wordlist, depth + 1)


guessWord = wordsuggest(myCounter, wordlist, 5)
print(guessWord)


yellows = {}
greens = {}
blacks = set([])

while sum([len(i) for i in greens.values()]) != 5:

    index = 0
    for i in guessWord:
        status = ""
        while not status:
            print(f"Was {i} g, y, or b?")
            status = str(input())
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
    print(newCounter.most_common(10))
    if newCounter:
        guessWord = wordsuggest(myCounter, updatedlist, 5)
        print(guessWord)
