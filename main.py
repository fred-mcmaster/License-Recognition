import base64
import csv
import io
import os
import tkinter as tk
import tkinter.filedialog as dir
from pathlib import Path

import customtkinter as ctk
from PIL import ImageTk, Image

import plate_recognition_api

# Initialize empty report
with open("report.csv", "w", newline='') as report_csv:
    data = ["filename", "plate", "accuracy", "region", "type"]
    writer = csv.writer(report_csv)
    writer.writerow(data)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title(" Licence Recognition App ")
window.geometry("1000x600")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=7)


# Left frame
frame_left = ctk.CTkFrame(master=window, corner_radius=0)
frame_left.grid(row=0, column=0, columnspan=1, sticky="nswe")

frame_left.columnconfigure(0, weight=1)
frame_left

entry = ctk.CTkEntry(master=frame_left,
                     width=60,
                     height=40,
                     justify="center",
                     text_font=("Roboto", -20),
                     placeholder_text="Plate Number:")
entry.grid(row=5, column=0, columnspan=2, pady=(10, 5), padx=20, sticky="we")

label_scoreText = ctk.CTkLabel(master=frame_left,
                               text="Accuracy:",
                               text_font=("Roboto", -20),
                               anchor='w')
label_scoreText.grid(row=6, column=0, pady=0, padx=20, sticky="we")
label_score = ctk.CTkLabel(master=frame_left,
                           text="",
                           height=40,
                           text_font=("Roboto", -20),
                           fg_color=("white", "gray38"))
label_score.grid(row=7, column=0, columnspan=2, pady=(0, 5), padx=20, sticky="we")

label_moret = ctk.CTkLabel(master=frame_left,
                           text="More Vehicle Info:",
                           text_font=("Roboto", -20),
                           anchor='w')
label_moret.grid(row=8, column=0, pady=0, padx=20, sticky="we")
label_more = ctk.CTkLabel(master=frame_left,
                          text="",
                          height=40,
                          fg_color=("white", "gray38"))
label_more.grid(row=9, column=0, columnspan=2, pady=(0, 5), padx=20, sticky="we")

# Right Frame
frame_right = ctk.CTkFrame(master=window)
frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

frame_right.rowconfigure(3, weight=1)
frame_right.columnconfigure(0, weight=1)

frame_img = ctk.CTkFrame(master=frame_right)

frame_img.pack(fill=tk.BOTH, expand=True)
frame_img.rowconfigure(0, weight=1)
frame_img.columnconfigure(0, weight=1)

frame_crop = ctk.CTkFrame(master=frame_right)
frame_crop.pack(fill=tk.BOTH, expand=True)
frame_crop.rowconfigure(0, weight=1)
frame_crop.columnconfigure(0, weight=1)

label_img = ctk.CTkLabel(master=frame_img,
                         text="",
                         height=200,
                         corner_radius=6,
                         fg_color=("white", "gray38"),
                         justify=tk.LEFT)
label_img.grid(column=0, row=0, sticky="nwe")
label_img.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

label_crop = ctk.CTkLabel(master=frame_crop,
                          text="",
                          height=150,
                          corner_radius=6,
                          fg_color=("white", "gray38"),
                          justify=tk.LEFT)
label_crop.grid(column=0, row=0, sticky="nwe")
label_crop.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# GLOBAL VARIABLES
img_base64 = None


def load_image():
    global img, path, img_base64

    path = dir.askopenfilename(initialdir=os.getcwd(), title="Select image",
                               filetypes=(("png files", "*.jpg"), ("all file", "*.*")))

    # Keep aspect ratio of the loaded image consistent
    fixed_width = 400
    loaded_image = Image.open(path)
    width_percent = (fixed_width / float(loaded_image.size[0]))
    dynamic_height = int((float(loaded_image.size[1]) * float(width_percent)))
    loaded_image = loaded_image.resize((fixed_width, dynamic_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(loaded_image)

    # Read image file as base64 encoded string
    with open(path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    label_img.configure(image=img)


def get_image_dynamic_width_fixed_height(img_path, height):
    image = Image.open(img_path)
    height_percent = (height / float(image.size[1]))
    dynamic_width = int((float(image.size[0]) * float(height_percent)))
    resized_image = image.resize((dynamic_width, height), Image.ANTIALIAS)
    return dynamic_width


def set_cropped_image(box):

    global path, img_cropped, label_crop

    # Crop params (pixels)
    left = box.xmin
    top = box.ymin
    right = box.xmax
    bottom = box.ymax

    # Crop original image
    fixed_width = 250
    original_image = Image.open(path)
    img_cropped = original_image.crop((left, top, right, bottom))

    # Maintain aspect ratio
    width_percent = (fixed_width / float(img_cropped.size[0]))
    dynamic_height = int((float(img_cropped.size[1]) * float(width_percent)))
    img_cropped = img_cropped.resize((fixed_width, dynamic_height), Image.ANTIALIAS)
    # img_cropped.show()

    # Save cropped image to buffer
    buffer = io.BytesIO()
    img_cropped.save(buffer, format="png")
    original_image.close()

    # Set cropped image buffer in UI
    if img_cropped:
        img_cropped = ImageTk.PhotoImage(data=buffer.getvalue())
        label_crop.configure(image=img_cropped)


def write_csv_report():
    global path, resultData

    file_name = Path(path).name
    plate = resultData.results[0].plate.upper()
    plate_score = resultData.results[0].score
    region = resultData.results[0].region
    vehicle = resultData.results[0].vehicle

    with open("report.csv", "a", newline='') as report_csv:
        # data = ["filename", "plate", "accuracy", "region", "type"]
        writer = csv.writer(report_csv)
        writer.writerow([file_name, plate, percent(plate_score), region.code.upper(), vehicle.type])


def percent(val):
    conv_ = round(float(val) * 100)
    return str(conv_) + '%'


def run():
    global path, img_cropped, label_crop, resultData

    resultData = plate_recognition_api.identify_license_plate_from_image(img_base64)
    print(resultData.results)
    print("Plate found: ", resultData.is_plate_found())

    # Reset UI contents
    entry.delete(0, tk.END)
    entry.insert(0, "")
    label_score.configure(text="")
    label_more.configure(text="")
    label_crop.configure(text="")

    # Here we need to do the null check. the result list may be empty.
    if resultData.is_plate_found():
        plate = resultData.results[0].plate.upper()
        plate_score = resultData.results[0].score
        region = resultData.results[0].region
        vehicle = resultData.results[0].vehicle
        entry.delete(0, tk.END)
        entry.insert(0, plate)
        label_score.configure(text=percent(plate_score), font=('Times New Roman', 15, 'bold'))

        box = resultData.results[0].box
        set_cropped_image(box)

        if region:
            label_more.configure(text=region.code.upper() + " , " + vehicle.type,
                                 font=('Times New Roman', 15, 'bold'))
            write_csv_report()
        else:
            label_more.configure(text="No Vehicle Info")

    # alert message to user.
    else:
        label_crop.configure(text="License Plate Not Found !", font=('Times New Roman', 17, 'bold'), image='')


app_label = ctk.CTkLabel(
    master=frame_left,
    text=" Licence Plate Recognition ",
    text_font=("Roboto Medium", -20)
)
app_label.grid(row=1, column=0, pady=10, padx=10)

insert_bt = ctk.CTkButton(
    master=frame_left,
    text="Insert",
    text_font=("Roboto", -15),
    height=32,
    command=load_image
)

insert_bt.grid(row=2, column=0, pady=10, padx=20)

process_bt = ctk.CTkButton(
    master=frame_left,
    text="Process",
    text_font=("Roboto", -15),
    height=32,
    command=run
)
process_bt.grid(row=3, column=0, pady=10, padx=20)

window.mainloop()
