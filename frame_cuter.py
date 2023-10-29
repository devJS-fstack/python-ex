import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
from tkinter import ttk as nvt_ttk
import speech_recognition as sr
from word2number import w2n


script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output_frames")
absolute_videos = os.path.abspath("videos")


def browse_video():
    video_path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if video_path:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, video_path)


def listen():
    global recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

    try:
        text = recognizer.recognize_google(audio, language="en")
        try:
            position = w2n.word_to_num(text)
            filename = files[position-1]
            entry_video.delete(0, tk.END)
            entry_video.insert(0, f"{absolute_videos}\{filename}")

        except:
            messagebox.showerror("NotFound", "Option not found")

        print(file)
    except sr.UnknownValueError:
        print("Error unknown")
    except sr.RequestError as e:
        print("Error RequestError")


def cut_video():
    input_video = entry_video.get()

    if not input_video:
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(input_video)
    frame_count = 0
    success = True

    while success and cap.get(cv2.CAP_PROP_POS_MSEC) <= int(entry_interval.get()):
        if frame_count > int(entry_frame.get()) - 1:
            break
        output_filename = os.path.join(
            output_dir, f"{entry_filename.get()}_{frame_count}.jpg")
        success, frame = cap.read()
        cv2.imwrite(output_filename, frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF

        if key == ord("q"):
            break
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print("Video frames have been saved to the 'output_frames' folder.")


files = os.listdir("videos")
print(files)

app = tk.Tk()
app.title("07_VanTinh_D19CQPT01_PTITHCM: ĐỒ ÁN HP: LẬP TRÌNH MULTI-APP")
app.geometry("400x400")

file_frame = nvt_ttk.Frame(app)
file_frame.pack()

row = 0

for file in files:
    row += 1
    nvt_ttk.Label(file_frame, text=f"{row}. {file}", font=("Helvetica", 12)).grid(
        row=row, column=0, pady=2, sticky="w")

record_btn = tk.Button(app, text="Choose by voice", command=listen)
record_btn.pack()

input_frame = nvt_ttk.Frame(app)
input_frame.pack()

tk.Label(input_frame, text="Input Video:").grid(
    row=0, column=0, pady=2, sticky="w")

entry_video = tk.Entry(input_frame, width=30)
entry_video.grid(
    row=0, column=1, pady=2, sticky="w")

tk.Label(input_frame, text="Interval Frame:").grid(
    row=1, column=0, pady=2, sticky="w")

entry_interval = tk.Entry(input_frame, width=30)
entry_interval.grid(
    row=1, column=1, pady=2, sticky="w")

tk.Label(input_frame, text="Limit Frames:").grid(
    row=2, column=0, pady=2, sticky="w")

entry_frame = tk.Entry(input_frame, width=30)
entry_frame.grid(
    row=2, column=1, pady=2, sticky="w")

tk.Label(input_frame, text="File Name:").grid(
    row=3, column=0, pady=2, sticky="w")

entry_filename = tk.Entry(input_frame, width=30)
entry_filename.grid(
    row=3, column=1, pady=2, sticky="w")

button_browse_video = tk.Button(app, text="Browse", command=browse_video)
button_browse_video.pack()

button_convert = tk.Button(
    app, text="Convert Video to Frames", command=cut_video)
button_convert.pack()

app.mainloop()
