import tkinter as tk
import tkinter.filedialog as dir
from PIL import ImageTk, Image
import subprocess
import os
import json
import plate_recognition
import matplotlib.pyplot as plt


def onclick():
    testing = tk.Label(text="testing")
    # testing.pack()


window = tk.Tk()
window.title(" Licence Recognition App ")
window.geometry("600x400")

frame = tk.Frame(window, width=300, height=200, bg="grey")
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)


# canvas = tk.Canvas(window, width=300, height=200, bg="grey")
# canvas.pack()
# canvas.place(anchor='center', relx=0.5, rely=0.5)


def load_image():
    global img, path
    path = dir.askopenfilename(initialdir=os.getcwd(), title="Select image",
                               filetypes=(("png files", "*.jpg"), ("all file", "*.*")))
    img = ImageTk.PhotoImage(Image.open(path).resize((300, 200), Image.ANTIALIAS))
    label = tk.Label(frame, image=img)
    label.pack()


def run():
    result = subprocess.check_output(["python", 'plate_recognition.py', "-a", "b043ef3a2da24bbde85109c5b49b61046519a1bc", path])
    print(json.loads(result))

app_label = tk.Label(
    text=" Licence Plate Recognition ",
    font="bold"
)

app_label.grid(column=2, row=0)

empty_lane_label = tk.Label(text=" ")
empty_lane_label.grid(column=0, row=1)
empty_lane_label2 = tk.Label(text=" ")
empty_lane_label2.grid(column=0, row=3)

insert_bt = tk.Button(
    text="Insert",
    width=15,
    height=1,
    bg="grey",
    fg="black",
    command=load_image
)
insert_bt.grid(column=0, row=2)

process_bt = tk.Button(
    text="Process",
    width=15,
    height=1,
    bg="grey",
    fg="black",
    command=run
)
process_bt.grid(column=0, row=4)

window.mainloop()
