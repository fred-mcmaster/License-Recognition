import tkinter as tk
import customtkinter as ctk
import tkinter.filedialog as dir
from PIL import ImageTk, Image, ImageChops
import os
import plate_recognition_api
import base64
import json

from plate_recognition_result_ui import PlateRecognitionUiResults, Plate, Region, Vehicle

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title(" Licence Recognition App ")
window.geometry("600x400")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

frame_left = ctk.CTkFrame(master=window, width=150, corner_radius=0)
frame_left.grid(row=0, column=0, sticky="nswe")

entry = ctk.CTkEntry(master=frame_left,
                     width=60,
                     justify="center",
                     placeholder_text="Plate Number:")
entry.grid(row=5, column=0, columnspan=2, pady=(10, 5), padx=20, sticky="we")

label_scoreText = ctk.CTkLabel(master=frame_left,
                               text="Accuracy:",
                               anchor='w')
label_scoreText.grid(row=6, column=0, pady=0, padx=20, sticky="we")
label_score = ctk.CTkLabel(master=frame_left,
                           text="",
                           fg_color=("white", "gray38"))
label_score.grid(row=7, column=0, columnspan=2, pady=(0, 5), padx=20, sticky="we")

label_moret = ctk.CTkLabel(master=frame_left,
                           text="More Vehicle Info:",
                           anchor='w')
label_moret.grid(row=8, column=0, pady=0, padx=20, sticky="we")
label_more = ctk.CTkLabel(master=frame_left,
                          text="",
                          fg_color=("white", "gray38"))
label_more.grid(row=9, column=0, columnspan=2, pady=(0, 5), padx=20, sticky="we")


# Right Frame
frame_right = ctk.CTkFrame(master=window)
frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

frame_right.rowconfigure([0, 1, 2], weight=1)
frame_right.rowconfigure(3, weight=10)
frame_right.columnconfigure((0, 1), weight=1)
frame_right.columnconfigure(2, weight=0)

frame_img = ctk.CTkFrame(master=frame_right)
frame_img.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")
frame_img.rowconfigure(0, weight=1)
frame_img.columnconfigure(0, weight=1)

frame_crop = ctk.CTkFrame(master=frame_right)
frame_crop.grid(row=3, column=0, columnspan=2, rowspan=2, sticky="nsew")
frame_crop.rowconfigure(0, weight=1)
frame_crop.columnconfigure(0, weight=1)

label_img = ctk.CTkLabel(master=frame_img,
                         text="",
                         height=200,
                         corner_radius=6,  # <- custom corner radius
                         fg_color=("white", "gray38"),  # <- custom tuple-color
                         justify=tk.LEFT)
label_img.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

label_crop = ctk.CTkLabel(master=frame_crop,
                          text="",
                          height=150,
                          corner_radius=6,  # <- custom corner radius
                          fg_color=("white", "gray38"),  # <- custom tuple-color
                          justify=tk.LEFT)
label_crop.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

# GLOBAL VARIABLES
img_base64 = None
plate_results_ui = None


def load_image():
    global img, path, img_base64

    path = dir.askopenfilename(initialdir=os.getcwd(), title="Select image",
                               filetypes=(("png files", "*.jpg"), ("all file", "*.*")))
    img = ImageTk.PhotoImage(Image.open(path).resize((400, 200), Image.ANTIALIAS))

    # Read image file as base64 encoded string
    with open(path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    label_img.configure(image=img)


def crop(img_crop):
    bg = Image.new(img_crop.mode, img_crop.size, img_crop.getpixel((0, 0)))
    diff = ImageChops.difference(img_crop, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        # label_crop.configure(image=img_crop.crop(bbox))
        print(bbox)
        # return img_crop.crop(bbox)


def percent(val):
    conv_ = round(float(val) * 100)
    return str(conv_) + '%'

def run():
    global plate_results_ui

    resultData = plate_recognition_api.identify_license_plate_from_image(img_base64)
    print(resultData.results)
    print("Plate found: ", resultData.is_plate_found())

    # reset UI contents
    entry.delete(0, tk.END)
    entry.insert(0, "")
    label_score.configure(text="")
    label_more.configure(text="")
    label_crop.configure(text="")



    # here we need to do the null check. the result list may be empty.
    if resultData.is_plate_found():
        plate = resultData.results[0].plate.upper()
        plate_score = resultData.results[0].score
        region = resultData.results[0].region
        vehicle = resultData.results[0].vehicle
        entry.delete(0, tk.END)
        entry.insert(0, plate)
        label_score.configure(text=percent(plate_score), font=('Times New Roman', 10, 'bold'))

        # Map fields from API to display in UI object
        plate_results_ui = PlateRecognitionUiResults()
        plate_results_ui.plate = Plate(plate, percent(plate_score))
        # TODO: map region and vehicle to UI object
        region_obj = Region(region.code, percent(region.score))
        if region_obj:
            label_more.configure(text=region.code.upper() + " , " + vehicle.type,
                                 font=('Times New Roman', 10, 'bold'))
        else:
            label_more.configure(text="No Vehicle Info")

        print(plate_results_ui.toJSON())

    # alert message to user.
    else:
        label_crop.configure(text="License Plate Not Found !", font=('Times New Roman', 17, 'bold'))

app_label = ctk.CTkLabel(
    master=frame_left,
    text=" Licence Plate Recognition ",
    text_font=("Roboto Medium", -16)
)
app_label.grid(row=1, column=0, pady=10, padx=10)

insert_bt = ctk.CTkButton(
    master=frame_left,
    text="Insert",
    height=32,
    command=load_image
)
insert_bt.grid(row=2, column=0, pady=10, padx=20)

process_bt = ctk.CTkButton(
    master=frame_left,
    text="Process",
    height=32,
    command=run
)
process_bt.grid(row=3, column=0, pady=10, padx=20)

window.mainloop()
