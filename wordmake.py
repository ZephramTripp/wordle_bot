"""
Wordmake is a module containing a few methods I use to solve Wordle puzzles.
It should probably containing a class definition, but it doesn't yet.
"""

from collections import Counter
from collections import namedtuple


class Wordler:
    """
    The Wordler class encapsulates the solver half of the Wordlebot code
    """

    def __init__(self, verbosity=1):
        self.length = 5
        self.wordlist = []
        checked_letters = namedtuple("checked_letters", ["greens", "yellows", "blacks"])
        self.checked_letters = checked_letters({}, {}, {})
        self.counter = Counter([j for i in self.wordlist for j in i])
        self.game_attrs = {
            "game_over": False,
            "game_list": self.wordlist,
            "guess_count": 0,
            "final_word": None,
        }
        self.verbosity = verbosity
        self.guess_word = ""

    def add_wordlist(self, filename=None, wordlist=None):
        """
        Adds a word list to the Wordler objects
        """
        if filename:
            with open(filename, encoding="utf-8") as dictionary:
                self.wordlist = list(
                    dict.fromkeys(
                        [
                            i.strip().lower()
                            for i in dictionary.readlines()
                            if len(i.strip()) == self.length
                            and i.strip().isalpha()
                            and i.isascii()
                            and i.islower()
                        ]
                    )
                )
        if wordlist:
            self.wordlist = wordlist

    def get_wordlist(self):
        """
        Returns the wordlist member
        """
        return self.wordlist

    def wordsuggest(self, depth):
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
        letters = self.counter.most_common(depth)
        newlist = [
            j
            for j in self.game_attrs["game_list"]
            if all((k in [i[0] for i in letters] for k in j))
        ]
        if newlist:
            bestword = newlist[0]
            bestcount = 0
            for i in newlist:
                count = sum([self.counter[letter] for letter in dict.fromkeys(i)])
                if count > bestcount:
                    bestword = i
                    bestcount = count
            if (
                len(set(bestword)) < len(list(bestword))
                and len(self.wordlist) > 1
                and depth < len(self.counter)
            ):
                trialword = self.wordsuggest(depth + 1)
                newcount = sum(
                    [self.counter[letter] for letter in dict.fromkeys(trialword)]
                )
                if newcount > count:
                    return trialword
                return bestword
            return bestword
        return self.wordsuggest(depth + 1)

    def guess_eval(self, guess, result):
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
                if i in self.checked_letters.greens:
                    self.checked_letters.greens[i][index] = None
                else:
                    self.checked_letters.greens[i] = dict.fromkeys([index])
            elif result[index] == "y":
                if i in self.checked_letters.yellows:
                    self.checked_letters.yellows[i][index] = None
                else:
                    self.checked_letters.yellows[i] = dict.fromkeys([index])
            elif result[index] == "b":
                if i in self.checked_letters.blacks:
                    self.checked_letters.blacks[i][index] = None
                else:
                    self.checked_letters.blacks[i] = dict.fromkeys([index])

    def gen_new_list(self):
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
        self.game_attrs["game_list"] = [
            i for i in self.game_attrs["game_list"] if self.validate_word(i)
        ]

    def validate_word(self, word):
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
        for letter, pos in self.checked_letters.blacks.items():
            if (
                letter in word
                and letter not in self.checked_letters.yellows
                and letter not in self.checked_letters.greens
            ):
                return False
            if letter in word and (
                letter in self.checked_letters.yellows
                or letter in self.checked_letters.greens
            ):
                valid = not any((word[num] is letter for num in pos))
                if not valid:
                    return False
        for letter, pos in self.checked_letters.yellows.items():
            for num in pos:
                if word[num] is letter:
                    return False
            if letter not in word:
                return False
        for letter, pos in self.checked_letters.greens.items():
            for num in pos:
                if word[num] is not letter:
                    return False
        return valid

    def make_guess(self, startingwords):
        """
        Makes another guess
        """
        if isinstance(startingwords, list) and self.game_attrs["guess_count"] < len(
            startingwords
        ):
            self.guess_word = startingwords[self.game_attrs["guess_count"]]
        elif isinstance(startingwords, str) and self.game_attrs["guess_count"] == 0:
            self.guess_word = startingwords
        else:
            self.guess_word = self.wordsuggest(5)
        if self.verbosity:
            print(self.guess_word)
        self.game_attrs["guess_count"] += 1

    def eval_word(self, evaluator):
        """
        Evaluates the guess, either with user input or an evaluator function
        """
        if evaluator is None:
            result = collect_input(self.guess_word)
        else:
            result = evaluator(self.guess_word, self.game_attrs["final_word"])
        self.guess_eval(self.guess_word, result)
        self.gen_new_list()

    def update_gamestate(self):
        """
        Checks to see if the game is over
        """
        if sum([len(i) for i in self.checked_letters.greens.values()]) == self.length:
            self.game_attrs["game_over"] = True
        else:
            self.counter = Counter([j for i in self.game_attrs["game_list"] for j in i])

    def play(self, startingwords=None, evaluator=None, final_word=None):
        """
        The play function plays the game of Wordle against the human
        """
        self.game_attrs["game_over"] = False
        self.game_attrs["game_list"] = self.wordlist
        self.counter = Counter([j for i in self.game_attrs["game_list"] for j in i])
        if final_word:
            self.game_attrs["final_word"] = final_word

        while not self.game_attrs["game_over"]:
            self.make_guess(startingwords)
            self.eval_word(evaluator)
            self.update_gamestate()

        return self.game_attrs["guess_count"]


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


def main():
    """
    The main function plays one game of Wordle against the user,
    with the computer making guesses and the user verifying the computer's guesses
    """
    my_wordler = Wordler()
    my_wordler.add_wordlist(filename="/usr/share/dict/words")
    my_wordler.play(startingwords=["clamp", "berth"])


if __name__ == "__main__":
    main()
