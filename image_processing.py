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

        self.create_widgets()

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
            button_frame, text="Slide Image", command=self.apply_sliding_window_on_3_channels)
        slide_button.grid(row=row, column=0, pady=5, sticky="w")
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

    def apply_sliding_window(self, img, padding=0, stride=1):
        h, w = img.shape[:2]

        img_p = np.zeros([h+2*padding, w+2*padding])

        img_p[padding:padding+h, padding:padding+w] = img

        kernel = np.array([[1]])

        assert len(
            kernel.shape) == 2 and kernel.shape[0] == kernel.shape[1]
        assert kernel.shape[0] % 2 != 0
        k_size = kernel.shape[0]
        k_half = int(k_size/2)

        y_pos = [v for idx, v in enumerate(
            list(range(k_half, h-k_half))) if idx % stride == 0]
        x_pos = [v for idx, v in enumerate(
            list(range(k_half, w-k_half))) if idx % stride == 0]

        new_img = np.zeros([len(y_pos), len(x_pos)])
        for new_y, y in enumerate(y_pos):
            for new_x, x in enumerate(x_pos):
                if k_half == 0:
                    pixel_val = img_p[y, x] * kernel
                else:
                    pixel_val = np.sum(
                        img_p[y-k_half:y-k_half+k_size, x-k_half:x-k_half+k_size] * kernel)
                new_img[new_y, new_x] = pixel_val

        return new_img

    def apply_sliding_window_on_3_channels(self, padding=0, stride=1):
        if self.image is not None:
            layer_blue = self.apply_sliding_window(
                self.image[:, :, 0], padding, stride)
            layer_green = self.apply_sliding_window(
                self.image[:, :, 1], padding, stride)
            layer_red = self.apply_sliding_window(
                self.image[:, :, 2], padding, stride)

            new_img = np.zeros(list(layer_blue.shape) + [3])
            new_img[:, :, 0], new_img[:, :, 1], new_img[:,
                                                        :, 2] = layer_blue, layer_green, layer_red

            nvt_cv2.imshow("Img", new_img)
            self.display_image(new_img)


if __name__ == "__main__":
    root = nvt_tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
