import tkinter as tk
from tkinter import filedialog
import cv2 as nvt_cv2
import numpy as np


class ImageComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("07_VanTinh_D19CQPT01_PTITHCM: ĐỒ ÁN HP: LẬP TRÌNH MULTI-APP")

        self.label1 = tk.Label(root, text="Image 1:")
        self.label2 = tk.Label(root, text="Image 2:")
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0)

        self.button1 = tk.Button(root, text="Browse", command=self.load_image1)
        self.button2 = tk.Button(root, text="Browse", command=self.load_image2)
        self.button1.grid(row=0, column=1)
        self.button2.grid(row=1, column=1)

        self.compare_button = tk.Button(
            root, text="Compare", command=self.compare_images)
        self.compare_button.grid(row=5, column=0, columnspan=2)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=6, column=0, columnspan=2)

        self.image1 = None
        self.image2 = None

    def load_image1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image1 = nvt_cv2.imread(file_path)
            self.image1 = nvt_cv2.cvtColor(self.image1, nvt_cv2.COLOR_BGR2RGB)
            self.label1.config(text="Image 1: " + file_path)
            self.show_image(self.image1, self.label1)

    def load_image2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image2 = nvt_cv2.imread(file_path)
            self.image2 = nvt_cv2.cvtColor(self.image2, nvt_cv2.COLOR_BGR2RGB)
            self.label2.config(text="Image 2: " + file_path)
            self.show_image(self.image2, self.label2)

    def compare_images(self):
        if self.image1 is None or self.image2 is None:
            self.result_label.config(text="Please select both images.")
            return

        diff_width = self.image1.shape[0] - self.image2.shape[0]
        diff_height = self.image1.shape[1] - self.image2.shape[1]
        size_comparison_result = f"Size Comparison: {abs(diff_width)} x {abs(diff_height)}"

        is_same = False
        if diff_width == 0 and diff_height == 0:
            difference = nvt_cv2.subtract(self.image1, self.image2)
            b, g, r = nvt_cv2.split(difference)
            if nvt_cv2.countNonZero(b) == 0 and nvt_cv2.countNonZero(g) == 0 and nvt_cv2.countNonZero(r) == 0:
                is_same = True
            else:
                nvt_cv2.imshow('Difference', difference)

        self.result_label.config(
            text=f"Color Comparsion: {is_same}\n{size_comparison_result}")

    def show_image(self, image, label):
        if image is not None:
            image = nvt_cv2.cvtColor(image, nvt_cv2.COLOR_BGR2RGB)
            image = nvt_cv2.resize(image, (300, 300))
            photo = self.convert_image_to_photo(image)
            label.config(image=photo)
            label.image = photo

    def convert_image_to_photo(self, image):
        _, image_data = nvt_cv2.imencode(".png", image)
        photo = tk.PhotoImage(data=image_data.tobytes())
        return photo


if __name__ == "__main__":
    root = tk.Tk()
    root.title("07_VanTinh_D19CQPT01_PTITHCM: ĐỒ ÁN HP: LẬP TRÌNH MULTI-APP")
    app = ImageComparisonApp(root)
    root.mainloop()
