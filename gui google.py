from tkinter import *
import wikipedia


def get_me():
    entry_value = entry.get()
    answer.delete(1.0, END)
    try:
        answer_value = wikipedia.summary(entry_value)
        answer.insert(INSERT, answer_value)
    except:
        answer.insert(INSERT, "please check you input or internet connection")


root = Tk()

topframe = Frame(root)
entry = Entry(topframe)
entry.pack()
button = Button(topframe, text="search", command=get_me)
button.pack()
topframe.pack(side=TOP)

bottomframe = Frame(root)
scroll = Scrollbar(bottomframe)
scroll.pack(side=RIGHT, fill=Y)
answer = Text(bottomframe, width=70, height=20, yscrollcommand=scroll.set, wrap=WORD,bg="aqua")
scroll.config(command=answer.yview)
answer.pack()
bottomframe.pack()

root.mainloop()
