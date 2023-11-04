import tkinter as nvt_tk
from tkinter import ttk as nvt_ttk
from tkinter import filedialog as nvt_filedialog
import cv2 as nvt_cv2
from PIL import Image, ImageTk
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "07_VanTinh_D19CQPT01_PTITHCM: ĐỒ ÁN HP: LẬP TRÌNH MULTI-APP")

        self.image_label = None
        self.image = None
        self.is_sliding = False


        self.create_widgets()

    def stop_slide(self):
        self.is_sliding = False


    def create_widgets(self):

        button_frame = nvt_ttk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        open_button = nvt_ttk.Button(
            button_frame, text="Open Image", command=self.open_image)
        open_button.grid(row=0, column=0, pady=5, sticky="w")

        row = 1
        grayscale_button = nvt_ttk.Button(
            button_frame, text="Grayscale", command=self.grayscale)
        grayscale_button.grid(row=row, column=0, pady=5, sticky="w")
        row += 1

        rotate_button = nvt_ttk.Button(
            button_frame, text="Rotate 90°", command=self.rotate)
        rotate_button.grid(row=row, column=0, pady=5, sticky="w")
        row += 1

        slide_button = nvt_ttk.Button(
            button_frame, text="Strart Slide Image", command=self.apply_sliding_window_on_3_channels)
        slide_button.grid(row=row, column=0, pady=5, sticky="w")
        slide_button = nvt_ttk.Button(
            button_frame, text="Stop Slide Image", command=self.stop_slide)
        slide_button.grid(row=row, column=1, pady=5, sticky="w",  padx=5)
        row += 1

        self.window_slide_size = nvt_ttk.Label(
            button_frame, text="Window Slide Size (Width x Height):", font=("Helvetica", 14))
        self.window_slide_size.grid(row=row, column=0, pady=5, sticky="w")

        self.window_slide_entry = nvt_ttk.Entry(button_frame, font=("Helvetica", 14))
        self.window_slide_entry.grid(row=row, column=1, pady=5, sticky="w")
        row += 1

        show_size_button = nvt_ttk.Button(
            button_frame, text="Show Size", command=self.show_size)
        show_size_button.grid(row=row, column=0, pady=5, sticky="w")
        row += 1

        self.size_label = nvt_ttk.Label(
            button_frame, text="", font=("Helvetica", 14))
        self.size_label.grid(row=row, column=0, pady=10, sticky="w")
        row += 1

        self.rgb_label = nvt_ttk.Label(
            button_frame, text="", font=("Helvetica", 14))
        self.rgb_label.grid(row=row, column=0, pady=10, sticky="w")
        row += 1

        self.resize_label = nvt_ttk.Label(
            button_frame, text="Resize (Width x Height):", font=("Helvetica", 14))
        self.resize_label.grid(row=row, column=0, pady=5, sticky="w")
        row += 1

        self.resize_entry = nvt_ttk.Entry(button_frame, font=("Helvetica", 14))
        self.resize_entry.grid(row=row, column=0, pady=5, sticky="w")
        row += 1

        resize_button = nvt_ttk.Button(
            button_frame, text="Resize", command=self.resize_image)
        resize_button.grid(row=row, column=0, pady=5, sticky="w")
        row += 1

        self.keep_aspect_ratio_var = nvt_tk.BooleanVar()
        self.keep_aspect_ratio_var.set(False)

        image_frame = nvt_ttk.Frame(self.root)
        image_frame.grid(row=0, column=1, padx=10, pady=10)

        self.image_label = nvt_ttk.Label(image_frame)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        crop_frame = nvt_ttk.Frame(button_frame)
        crop_frame.grid(row=11, column=0, pady=10, sticky="w")


    def open_image(self):
        file_path = nvt_filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.png *.gif *.bmp")])

        if file_path:
            self.image = nvt_cv2.imread(file_path)
            self.image = nvt_cv2.cvtColor(self.image, nvt_cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, img):
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

    def grayscale(self):
        if self.image is not None:
            gray_image = nvt_cv2.cvtColor(self.image, nvt_cv2.COLOR_RGB2GRAY)
            self.display_image(gray_image)

    def rotate(self):
        if self.image is not None:
            self.image = nvt_cv2.rotate(
                self.image, nvt_cv2.ROTATE_90_CLOCKWISE)
            self.display_image(self.image)

    def show_size(self):
        if self.image is not None:
            height, width, channels = self.image.shape
            size_info = f"Width: {width}, Height: {height}, Channels: {channels}"
            self.size_label.config(text=size_info)

    def resize_image(self):
        if self.image is not None:
            dimensions = self.resize_entry.get()
            try:
                width, height = map(int, dimensions.split("x"))

                if self.keep_aspect_ratio_var.get():

                    current_height, current_width, _ = self.image.shape
                    aspect_ratio = current_width / current_height
                    if width / height > aspect_ratio:
                        width = int(aspect_ratio * height)
                    else:
                        height = int(width / aspect_ratio)

                resized_image = nvt_cv2.resize(self.image, (width, height))
                self.display_image(resized_image)
            except ValueError:

                pass

    def crop_image(self):
        if self.image is not None:
            try:
                from_width = int(self.from_width_entry.get())
                to_width = int(self.to_width_entry.get())
                from_height = int(self.from_height_entry.get())
                to_height = int(self.to_height_entry.get())

                cropped_image = self.image[from_height:to_height,
                                           from_width:to_width]
                self.display_image(cropped_image)
            except ValueError:
                pass

    def apply_sliding_window_on_3_channels(self, padding=0, stride=1):
        self.is_sliding = True
        if self.image is not None:
            try:
                measure = self.window_slide_entry.get().split("x")
                w = int(measure[0])
                h = int(measure[1])
            except:
                w = 156
                h = 156

            for (x, y, window) in self.sliding_window(step_size=40, window_size=(w, h)):
                if not self.is_sliding:
                    break
                clone = self.image.copy()
                nvt_cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
                self.display_image(clone)
                self.root.update()
                self.root.after(100)

    def sliding_window(self, step_size, window_size):
        h, w = window_size
        image_h, image_w = self.image.shape[:2]
        for y in range(0, image_h, step_size):
            for x in range(0, image_w, step_size):
                window = self.image[y:y + h, x:x + w]
                if window.shape[:2] != window_size:
                    continue
                yield (x, y, window)


if __name__ == "__main__":
    root = nvt_tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
