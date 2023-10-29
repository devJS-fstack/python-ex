import subprocess
import tkinter as nvt_tk
import sys

python_executable = sys.executable


def image_processing():
    script_path = "image_processing.py"
    subprocess.run([python_executable, script_path])


def frame_cutter():
    script_path = "frame_cuter.py"
    subprocess.run([python_executable, script_path])


def speech_to_text():
    script_path = "speech_to_text.py"
    subprocess.run([python_executable, script_path])


def image_comparison():
    script_path = "image_comparision.py"    
    subprocess.run([python_executable, script_path])


root = nvt_tk.Tk()
root.title("07_VanTinh_D19CQPT01_PTITHCM: ĐỒ ÁN HP: LẬP TRÌNH MULTI-APP")
root.geometry('500x400')
root.resizable(nvt_tk.FALSE, nvt_tk.FALSE)

title_label = nvt_tk.Label(root, text="Main Form", font=("Helvetica", 20))
title_label.pack(pady=20)


button_frame = nvt_tk.Frame(root)
button_frame.pack()

button_style = {"padx": 10, "pady": 10, "width": 20,
                "font": ("Helvetica", 12), "background": "yellow"}


open_speech_to_text_button = nvt_tk.Button(
    button_frame, text="Speech to Text", command=speech_to_text, **button_style)
open_speech_to_text_button.grid(row=0, column=0, padx=10, pady=10)

open_image_processing_button = nvt_tk.Button(
    button_frame, text="Image Processing", command=image_processing, **button_style)
open_image_processing_button.grid(row=1, column=0, padx=10, pady=10)

open_frame_cutter_button = nvt_tk.Button(
    button_frame, text="Frame Cutter", command=frame_cutter, **button_style)
open_frame_cutter_button.grid(row=2, column=0, padx=10, pady=10)

open_image_comparison = nvt_tk.Button(
    button_frame, text="Image comparison", command=image_comparison, **button_style)
open_image_comparison.grid(row=3, column=0, padx=10, pady=10)

root.mainloop()
