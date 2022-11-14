import tkinter as tk
import tkinter.filedialog as dir
from PIL import ImageTk, Image
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
    global img
    path = dir.askopenfilename(initialdir="/", title="Select image",
                               filetypes=(("png files", "*.jpg"), ("all file", "*.*")))
    img = ImageTk.PhotoImage(Image.open(path))
    label = tk.Label(frame, image=img)
    label.pack()


btn = tk.Button(window, text='Click me !', command=load_image)
btn.place(x=25, y=100)

newLabel = tk.Label(text=" This is the starting point of our project ")
newLabel.grid(column=0, row=0)

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
    width=20,
    height=1,
    bg="grey",
    fg="black",
    command=onclick
)
insert_bt.grid(column=0, row=2)

process_bt = tk.Button(
    text="Process",
    width=20,
    height=1,
    bg="grey",
    fg="black"
)
process_bt.grid(column=0, row=4)

window.mainloop()
