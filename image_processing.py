import tkinter as qt_tk
from tkinter import ttk as qt_ttk
from tkinter import filedialog as qt_filedialog
import cv2 as qt_cv2
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor By QT")

        self.image_label = None
        self.image = None

        self.create_widgets()

    def create_widgets(self):
        
        button_frame = qt_ttk.Frame(self.root)
        button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

      
        open_button = qt_ttk.Button(button_frame, text="Open Image", command=self.open_image)
        open_button.grid(row=0, column=0, pady=5, sticky="w")

        grayscale_button = qt_ttk.Button(button_frame, text="Grayscale", command=self.grayscale)
        grayscale_button.grid(row=1, column=0, pady=5, sticky="w")

        rotate_button = qt_ttk.Button(button_frame, text="Rotate 90°", command=self.rotate)
        rotate_button.grid(row=2, column=0, pady=5, sticky="w")

        show_size_button = qt_ttk.Button(button_frame, text="Show Size", command=self.show_size)
        show_size_button.grid(row=3, column=0, pady=5, sticky="w")

        show_rgb_button = qt_ttk.Button(button_frame, text="Show RGB Value", command=self.show_rgb_value)
        show_rgb_button.grid(row=4, column=0, pady=5, sticky="w")

        self.size_label = qt_ttk.Label(button_frame, text="", font=("Helvetica", 14))
        self.size_label.grid(row=5, column=0, pady=10, sticky="w")

        self.rgb_label = qt_ttk.Label(button_frame, text="", font=("Helvetica", 14))
        self.rgb_label.grid(row=6, column=0, pady=10, sticky="w")

        self.resize_label = qt_ttk.Label(button_frame, text="Resize (Width x Height):", font=("Helvetica", 14))
        self.resize_label.grid(row=7, column=0, pady=5, sticky="w")

        self.resize_entry = qt_ttk.Entry(button_frame, font=("Helvetica", 14))
        self.resize_entry.grid(row=8, column=0, pady=5, sticky="w")

        resize_button = qt_ttk.Button(button_frame, text="Resize", command=self.resize_image)
        resize_button.grid(row=9, column=0, pady=5, sticky="w")

        self.keep_aspect_ratio_var = qt_tk.BooleanVar()
        self.keep_aspect_ratio_var.set(True)

        keep_aspect_ratio_checkbox = qt_ttk.Checkbutton(button_frame, text="Keep Aspect Ratio", variable=self.keep_aspect_ratio_var)
        keep_aspect_ratio_checkbox.grid(row=10, column=0, pady=5, sticky="w")


        image_frame = qt_ttk.Frame(self.root)
        image_frame.grid(row=0, column=1, padx=10, pady=10)

        self.image_label = qt_ttk.Label(image_frame)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        
        crop_frame = qt_ttk.Frame(button_frame)
        crop_frame.grid(row=11, column=0, pady=10, sticky="w")

        label_width = 15  
        entry_width = 5 
        entry_pady = 5    

        self.from_width_label = qt_ttk.Label(crop_frame, text="From Width:", font=("Helvetica", 14), width=label_width)
        self.from_width_label.grid(row=0, column=0, pady=entry_pady, sticky="w")

        self.from_width_entry = qt_ttk.Entry(crop_frame, font=("Helvetica", 14), width=entry_width)
        self.from_width_entry.grid(row=1, column=0, pady=entry_pady, sticky="w")

        self.to_width_label = qt_ttk.Label(crop_frame, text="To Width:", font=("Helvetica", 14), width=label_width)
        self.to_width_label.grid(row=0, column=1, pady=entry_pady, sticky="w")

        self.to_width_entry = qt_ttk.Entry(crop_frame, font=("Helvetica", 14), width=entry_width)
        self.to_width_entry.grid(row=1, column=1, pady=entry_pady, sticky="w")

        self.from_height_label = qt_ttk.Label(crop_frame, text="From Height:", font=("Helvetica", 14), width=label_width)
        self.from_height_label.grid(row=0, column=2, pady=entry_pady, sticky="w")

        self.from_height_entry = qt_ttk.Entry(crop_frame, font=("Helvetica", 14), width=entry_width)
        self.from_height_entry.grid(row=1, column=2, pady=entry_pady, sticky="w")

        self.to_height_label = qt_ttk.Label(crop_frame, text="To Height:", font=("Helvetica", 14), width=label_width)
        self.to_height_label.grid(row=0, column=3, pady=entry_pady, sticky="w")

        self.to_height_entry = qt_ttk.Entry(crop_frame, font=("Helvetica", 14), width=entry_width)
        self.to_height_entry.grid(row=1, column=3, pady=entry_pady, sticky="w")

        crop_button = qt_ttk.Button(button_frame, text="Crop", command=self.crop_image)
        crop_button.grid(row=12, column=0, pady=5, sticky="w")
        
        sliding_window_frame = qt_ttk.Frame(button_frame)
        sliding_window_frame.grid(row=12, column=0, pady=10, sticky="w")

        self.window_size_h_label = qt_ttk.Label(sliding_window_frame, text="Window size H:", font=("Helvetica", 14), width=label_width)
        self.window_size_h_label.grid(row=0, column=0, pady=entry_pady, sticky="w")

        self.window_size_w_label = qt_ttk.Label(sliding_window_frame, text="Window size W:", font=("Helvetica", 14), width=label_width)
        self.window_size_w_label.grid(row=0, column=1, pady=entry_pady, sticky="w")

        self.step_size_label = qt_ttk.Label(sliding_window_frame, text="Step size:", font=("Helvetica", 14), width=label_width)
        self.step_size_label.grid(row=0, column=2, pady=entry_pady, sticky="w")

        self.window_size_h_entry = qt_ttk.Entry(sliding_window_frame, font=("Helvetica", 14), width=entry_width)
        self.window_size_h_entry.grid(row=1, column=0, pady=entry_pady, sticky="w")
        
        self.window_size_w_entry = qt_ttk.Entry(sliding_window_frame, font=("Helvetica", 14), width=entry_width)
        self.window_size_w_entry.grid(row=1, column=1, pady=entry_pady, sticky="w")

        self.step_size_entry = qt_ttk.Entry(sliding_window_frame, font=("Helvetica", 14), width=entry_width)
        self.step_size_entry.grid(row=1, column=2, pady=entry_pady, sticky="w")

        show_value_button = qt_ttk.Button(button_frame, text="Show Value", command=self.process_image_with_sliding_window)
        show_value_button.grid(row=13, column=0, pady=5, sticky="w")

    def open_image(self):
        file_path = qt_filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.gif *.bmp")])

        if file_path:
            self.image = qt_cv2.imread(file_path)
            self.image = qt_cv2.cvtColor(self.image, qt_cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, img):
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

    def grayscale(self):
        if self.image is not None:
            gray_image = qt_cv2.cvtColor(self.image, qt_cv2.COLOR_RGB2GRAY)
            self.display_image(gray_image)

    def rotate(self):
        if self.image is not None:
            self.image = qt_cv2.rotate(self.image, qt_cv2.ROTATE_90_CLOCKWISE)
            self.display_image(self.image)

    def show_size(self):
        if self.image is not None:
            height, width, channels = self.image.shape
            size_info = f"Width: {width}, Height: {height}, Channels: {channels}"
            self.size_label.config(text=size_info)

    def show_rgb_value(self):
        if self.image is not None:
           
            pixel_value = self.image[100, 100]
            rgb_info = f"RGB Value at (100, 100): {pixel_value}"
            self.rgb_label.config(text=rgb_info)

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

                resized_image = qt_cv2.resize(self.image, (width, height))
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

                cropped_image = self.image[from_height:to_height, from_width:to_width]
                self.display_image(cropped_image)
            except ValueError:
                pass

    def sliding_window(self,image, step_size, window_size):
            for y in range(0, image.shape[0], step_size):
                for x in range(0, image.shape[1], step_size):
                    yield x, y, image[y:y + window_size[1], x:x + window_size[0]]
    
    def process_image_with_sliding_window(self):
         
         if self.image is not None:    
             window_size = (int(self.window_size_h_entry.get()),int(self.window_size_w_entry.get()))
             step_size = int(self.step_size_entry.get())
             print("Window size value", window_size)
             print("Step size value", step_size)
             
             image = qt_cv2.cvtColor(self.image, qt_cv2.COLOR_BGR2GRAY)
             for (x, y, window) in self.sliding_window(image, step_size, window_size):
                if window.shape[0] != window_size[1] or window.shape[1] != window_size[0]:
                    continue
                value = int(window.mean())
                qt_cv2.rectangle(image, (x, y), (x + window_size[0], y + window_size[1]), (0, 255, 0), 2)
                qt_cv2.putText(image, str(value), (x, y + 30), qt_cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 2)
                
             self.display_image(image)    
             
if __name__ == "__main__":
    root = qt_tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
