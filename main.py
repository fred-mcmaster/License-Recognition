import tkinter as tk
import tkinter.filedialog as dir
from PIL import ImageTk, Image
import matplotlib.pyplot as plt

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
window.mainloop()
