import tkinter as nvt_tk
from tkinter import scrolledtext, Label
from tkinter import messagebox
from tkinter import ttk, filedialog
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment as AudioSegment_07_dev
import os

recognizer = None
nvt_wav_file = "temp.wav"


def listen(filepath=None):
    global recognizer
    recognizer = sr.Recognizer()

    if filepath == None:
        with sr.Microphone() as source:
            listen_label.config(text="Đang nghe...")
            app.update()
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            listen_label.config(text="")
    else:
        audio = AudioSegment_07_dev.from_mp3(filepath)
        audio.export(nvt_wav_file, format="wav")
        with sr.AudioFile(nvt_wav_file) as source:
            listen_label.config(text="Đang nghe...")
            app.update()
            audio = recognizer.record(source)
            listen_label.config(text="")

    try:
        recognize_label.config(text="Đang nhận diện...")
        app.update()
        selected_language = language_combo.get()
        language_code = language_options[selected_language]
        text = recognizer.recognize_google(audio, language=language_code)
        text_box.insert(nvt_tk.END, text + "\n")
        tts = gTTS(text=text, lang=language_code)
        tts.save("output.mp3")
        recognize_label.config(text="Nhận diện thành công!")
        play_audio()
    except sr.UnknownValueError:
        recognize_label.config(text="Xin lỗi, tôi không hiểu bạn đang nói gì.")
    except sr.RequestError as e:
        recognize_label.config(text=f"Error: {e}")
    finally:
        if os.path.exists(nvt_wav_file):
            os.remove(nvt_wav_file)


def open_file():
    filepath = filedialog.askopenfilename(title="File to translate",
                                          filetypes=(("Audio file (*.mp3)", "*.mp3"),))
    f1 = open(filepath, "r", encoding="utf-8")
    print("filepath", filepath)
    f1.close()
    listen(filepath)


def play_audio():
    playsound("output.mp3")


def close_app():
    result = messagebox.askyesno(
        "Đóng ứng dụng", "Bạn thật sự muốn đóng ứng dụng?")
    if result:
        app.destroy()


def show_ok_message_lang_combobox(event):
    selected_option = language_combo.get()
    messagebox.showinfo("Selection", f"Bạn chọn: {selected_option}")


app = nvt_tk.Tk()
app.title("07 VanTinh_D19CQPT01_PTITHCM: ĐỒ ÁN HP: LẬP TRÌNH MULTI-APP")
app.geometry('500x400')
app.resizable(nvt_tk.FALSE, nvt_tk.FALSE)

app.protocol("WM_DELETE_WINDOW", close_app)

language_options = {"English": "en", "Vietnamese": "vi"}
language_combo = ttk.Combobox(app, values=list(language_options.keys()))
language_combo.set("English")
language_combo_label = Label(app, text="Chọn ngôn ngữ:")
language_combo_label.pack()
language_combo.pack()
language_combo.bind("<<ComboboxSelected>>", show_ok_message_lang_combobox)


button_frame = nvt_tk.Frame(app)
button_frame.pack()

listen_button = ttk.Button(button_frame, text="Lắng nghe", command=listen)
listen_button.grid(row=0, column=0,  pady=2)

open_file_button = ttk.Button(
    button_frame, text="Chọn file", command=open_file)
open_file_button.grid(row=1, column=0, pady=2)

listen_label = Label(app, text="", fg="blue")
listen_label.pack()

recognize_label = Label(app, text="", fg="green")
recognize_label.pack()

text_box = scrolledtext.ScrolledText(app, width=40, height=10)
text_box.pack()

app.mainloop()
