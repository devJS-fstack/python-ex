import tkinter as tk
from tkinter import filedialog
import cv2
import os

# Get the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output_frames")

def browse_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if video_path:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, video_path)

def cut_video():
    input_video = entry_video.get()

    if not input_video:
        return

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the input video file
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    frame_rate = 24  # Frames per second
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        output_filename = os.path.join(output_dir, f"image{frame_count}.jpg")

            # Display the frame on the GUI
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF

            # Save the frame
        cv2.imwrite(output_filename, frame)

            # Allow the user to stop by pressing 'Q'
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Video frames have been saved to the 'output_frames' folder.")

app = tk.Tk()
app.title("Video to Frames Converter")

# Create GUI elements
label_video = tk.Label(app, text="Input Video:")
label_video.pack()

entry_video = tk.Entry(app, width=50)
entry_video.pack()

button_browse_video = tk.Button(app, text="Browse", command=browse_video)
button_browse_video.pack()

button_convert = tk.Button(app, text="Convert Video to Frames", command=cut_video)
button_convert.pack()

# Run the Tkinter main loop
app.mainloop()
