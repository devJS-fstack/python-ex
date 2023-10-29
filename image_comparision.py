import tkinter as tk
from tkinter import filedialog
import cv2 as nvt_cv2


class ImageComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Comparison")

        self.label1 = tk.Label(root, text="Image 1:")
        self.label2 = tk.Label(root, text="Image 2:")
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0)

        self.button1 = tk.Button(root, text="Browse", command=self.load_image1)
        self.button2 = tk.Button(root, text="Browse", command=self.load_image2)
        self.button1.grid(row=0, column=1)
        self.button2.grid(row=1, column=1)

        self.comparison_method_label = tk.Label(
            root, text="Select Comparison Method:")
        self.comparison_method_label.grid(row=2, column=0, columnspan=2)

        self.comparison_methods = [
            "Histogram Comparison"
        ]
        self.method_var = tk.StringVar()
        self.method_var.set(self.comparison_methods[0])

        for i, method in enumerate(self.comparison_methods):
            tk.Radiobutton(root, text=method, variable=self.method_var, value=method).grid(
                row=3+i, column=0, columnspan=2)

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

        hist1 = nvt_cv2.calcHist([self.image1], [0], None, [256], [0, 256])
        hist2 = nvt_cv2.calcHist([self.image2], [0], None, [256], [0, 256])
        hist_diff = nvt_cv2.compareHist(hist1, hist2, nvt_cv2.HISTCMP_CORREL)
        color_comparison_result = f"Color Comparison (Histogram): {hist_diff:.2f}"

        size1 = self.image1.shape[0] * self.image1.shape[1]  # Rows x Columns
        size2 = self.image2.shape[0] * self.image2.shape[1]
        size_diff = abs(size1 - size2)
        size_comparison_result = f"Size Comparison: {size_diff} pixels"

        self.result_label.config(
            text=f"{color_comparison_result}\n{size_comparison_result}")

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
    app = ImageComparisonApp(root)
    root.mainloop()
