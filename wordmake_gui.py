import tkinter as tk
import wordmake
from collections import Counter

window = tk.Tk()
window["bg"] = "khaki"
canvas = tk.Canvas(window, height=500, width=400, bg="khaki")
canvas.pack()
canvas.create_text(
    200, 50, text="Wordle Bot", fill="black", font=("Times New Roman", 18)
)
rectangles = []


def changeColor(id):
    color = canvas.itemcget(id, "fill")
    if color == "gray":
        canvas.itemconfigure(id, fill="yellow")
    elif color == "yellow":
        canvas.itemconfigure(id, fill="green")
    else:
        canvas.itemconfigure(id, fill="gray")


for y in range(6):
    rectangles.append([])
    for x in range(5):
        rectangles[y].append(
            canvas.create_rectangle(
                65 + x * 55,
                100 + y * 55,
                115 + x * 55,
                150 + y * 55,
                fill="gray",
            )
        )
    # if we want the third block to start on 175 and go to 225, we need the second block to end at 170 and start at 120 and the first
    # to end at 115 and start at 65

my_wordler = wordmake.Wordler(verbosity=0)
my_wordler.add_wordlist(filename="/usr/share/dict/words")
my_wordler.game_attrs["game_list"] = my_wordler.wordlist
my_wordler.counter = Counter([j for i in my_wordler.game_attrs["game_list"] for j in i])

color_map = {"gray": "b", "green": "g", "yellow": "y"}
letter_list = []


def gui_evaluate(dummy1, dummy2):
    outlist = []
    curr_row = my_wordler.game_attrs["guess_count"]
    for i in rectangles[curr_row - 1]:
        outlist.append(color_map[canvas.itemcget(i, "fill")])
    return outlist


def makeguess_gui():
    curr_row = my_wordler.game_attrs["guess_count"]
    if curr_row == 6:
        return None
    if curr_row:
        my_wordler.eval_word(gui_evaluate)
        my_wordler.update_gamestate()
        if my_wordler.game_attrs["game_over"]:
            return None
    try:
        guess_word = my_wordler.make_guess(startingwords=None)
        for index, i in enumerate(guess_word):
            id = canvas.create_text(
                93 + index * 55, 128 + curr_row * 55, text=i.upper(), fill="black"
            )
            letter_list.append(id)
            canvas.tag_bind(
                rectangles[curr_row][index],
                "<Button-1>",
                lambda event, id=rectangles[curr_row][index]: changeColor(id),
            )
    except wordmake.NoWordsLeftException:
        print("Can't print a word if none remain")


def reset():
    for i in rectangles:
        for j in i:
            canvas.itemconfig(j, fill="gray")
            canvas.tag_unbind(id, "<Button-1>")
    for i in letter_list:
        canvas.delete(i)
    global my_wordler
    my_wordler = wordmake.Wordler(verbosity=0)
    my_wordler.add_wordlist(filename="/usr/share/dict/words")
    my_wordler.game_attrs["game_list"] = my_wordler.wordlist
    my_wordler.counter = Counter(
        [j for i in my_wordler.game_attrs["game_list"] for j in i]
    )


guess_btn = tk.Button(window, text="Make a guess", command=makeguess_gui)
guess_btn.pack()
reset_btn = tk.Button(window, text="Reset", command=reset)
reset_btn.pack()


tk.mainloop()
