import speech_recognition as QT_sr
from gtts import gTTS as QT_gTTS
import os as QT_os
from googletrans import Translator as QT_Translator

target_language = None 

def listen_to_voice():
    global target_language 

    recognizer = QT_sr.Recognizer()
    with QT_sr.Microphone() as source:
        print("Chọn ngôn ngữ cho giọng nói (nói 'Tiếng Việt' cho tiếng Việt, 'Tiếng Anh' for English):")
        language_choice = recognizer.listen(source)

    try:
        language_choice = recognizer.recognize_google(language_choice, language="vi-VN")
        if "tiếng việt" in language_choice.lower():
            target_language = "vi"
        elif "tiếng anh" in language_choice.lower():
            target_language = "en-US"
        else:
            print("Không hiểu lựa chọn ngôn ngữ. Hãy nói 'Tiếng Việt' hoặc 'Tiếng Anh'.") 
            return None
    except QT_sr.UnknownValueError:
        print("Không nghe được lựa chọn ngôn ngữ.")
        return None

    print(f"Ngôn ngữ đã chọn: {target_language}")
    
    with QT_sr.Microphone() as source:
        print("Vui lòng nói điều gì đó")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language=target_language)
        return user_input
    except QT_sr.UnknownValueError:
        return "Xin lỗi, tôi không hiểu bạn nói gì." 


def speak_response(QT_response_text, QT_target_language):
    tts = QT_gTTS(text=QT_response_text, lang=QT_target_language)
    tts.save("response.mp3")
  

def main():
    global target_language 
    print("Chào mừng bạn đến với trợ lý ảo!") 

    while True:
        user_input = listen_to_voice()
        
        if user_input is None:
            continue

        if user_input.lower() == "exit":
            print("Tạm biệt!") 
            break

        print(f"Bạn nói: {user_input}") 
        speak_response(user_input, target_language)

if __name__ == "__main__":
    main()
