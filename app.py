import tkinter as tk
from tkinter import filedialog, messagebox, IntVar, ttk
from PIL import Image,  ImageOps, ImageEnhance, ImageTk
import random
import os


# Augmentation functions

def random_rotation(image):
    return image.rotate(random.randint(-25, 25))

def random_translation(image):
    x_shift = random.randint(-10, 10)
    y_shift = random.randint(-10, 10)
    return image.transform(image.size, Image.AFFINE, (1, 0, x_shift, 0, 1, y_shift))

def random_zoom(image):
    zoom_factor = random.uniform(0.8, 1.2)
    new_width = int(image.width * zoom_factor)
    new_height = int(image.height * zoom_factor)
    if zoom_factor > 1:
        return image.resize((new_width, new_height)).crop(((new_width - image.width) // 2, (new_height - image.height) // 2,
                                                          (new_width + image.width) // 2, (new_height + image.height) // 2))
    else:
        temp = Image.new("RGB", (image.width, image.height), color="white")
        temp.paste(image.resize((new_width, new_height)), ((image.width - new_width) // 2, (image.height - new_height) // 2))
        return temp

def change_brightness(image):
    enhancer = ImageEnhance.Brightness(image)
    factor = random.uniform(0.5, 1.5)
    return enhancer.enhance(factor)

def random_flip(image):
    """Randomly apply horizontal and/or vertical flip."""
    actions = ["none", "horizontal", "vertical", "both"]
    action = random.choice(actions)
    
    if action == "horizontal":
        return ImageOps.mirror(image)
    elif action == "vertical":
        return ImageOps.flip(image)
    elif action == "both":
        return ImageOps.flip(ImageOps.mirror(image))
    else:
        return image

def change_color(image):
    enhancer = ImageEnhance.Color(image)
    factor = random.uniform(0, 3)  # Adjust the factor as needed
    return enhancer.enhance(factor)


# Available image processing methods
available_methods = {
    "Rotation": random_rotation,
    "Translation": random_translation,
    "Zoom": random_zoom,
    "Change Brightness": change_brightness,
    "Random Flip": random_flip,
    "Change Color": change_color
}


def clear_output_directory(directory):
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
# GUI Application with Multi-Image support and additional functions

class ImageAugmentationAppV5:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image Augmentation App V5")
        self.root.iconbitmap(r'C:\Users\Bao Viet\Desktop\FPT University\PFP191\Assignment 2\icon.ico') # Set the window icon
        self.root.geometry("1920x1080")
        
        self.image_paths = []
        self.num_images = IntVar(value=10)
        self.selected_methods = []
        self.image_previews = []
        
        # Styling
        style = ttk.Style()
        style.configure("TButton", font=('Arial', 12))
        style.configure("TLabel", font=('Arial', 12))
        style.configure("TCheckbutton", font=('Arial', 12))
        
        self.output_dir = r"C:\Users\Bao Viet\Desktop\FPT University\PFP191\Assignment 2\output"
        self.create_widgets()
        
        
        
    def create_widgets(self):
        # Top frame for choosing and previewing images
        top_frame = ttk.LabelFrame(self.root, text="Image Selection", padding=(10, 5))
        top_frame.pack(pady=20, fill="x", padx=10)

        self.btn_choose_image = ttk.Button(top_frame, text="Choose Images", command=self.choose_images)
        self.btn_choose_image.pack(side="left", padx=10)
        
        self.btn_remove_images = ttk.Button(top_frame, text="Remove Selected Images", command=self.remove_images)
        self.btn_remove_images.pack(side="left", padx=10)
        
        # Frame to hold image previews
        self.preview_frame = ttk.Frame(self.root)
        self.preview_frame.pack(pady=20, fill="x", padx=10)
        
        # Augmentation methods frame
        methods_frame = ttk.LabelFrame(self.root, text="Augmentation Methods", padding=(10, 5))
        methods_frame.pack(pady=20, fill="x", padx=10)
        
        for method in available_methods:
            var = IntVar()
            chk = ttk.Checkbutton(methods_frame, text=method, variable=var)
            chk.pack(anchor='w', padx=20)
            self.selected_methods.append((method, var))
        
        # Number of images frame
        num_images_frame = ttk.Frame(self.root)
        num_images_frame.pack(pady=20, fill="x", padx=10)
        
        ttk.Label(num_images_frame, text="Number of augmented images per input:").pack(side="left", padx=10)
        ttk.Entry(num_images_frame, textvariable=self.num_images, width=5).pack(side="left")
        
        # Generate images button
        self.btn_generate = ttk.Button(self.root, text="Generate Augmented Images", command=self.generate_images)
        self.btn_generate.pack(pady=20)
        
        # Progress Bar
        self.progress_label = ttk.Label(self.root, text="Progress:")
        self.progress_label.pack(pady=10, anchor="w", padx=10)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=1300, mode="determinate")
        self.progress.pack(pady=20, padx=10)

        # Output directory frame
        output_dir_frame = ttk.LabelFrame(self.root, text="Output Directory", padding=(10, 5))
        output_dir_frame.pack(pady=20, fill="x", padx=10)
        
        # Label to display current output directory
        self.output_dir_label = ttk.Label(output_dir_frame, text=self.output_dir)
        self.output_dir_label.pack(side="left", padx=10)
        
        # Button to change output directory
        self.btn_change_dir = ttk.Button(output_dir_frame, text="Change Output Folder", command=self.change_output_folder)
        self.btn_change_dir.pack(side="left", padx=10)
    
    
            
    def choose_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_paths:
            # Clear previous selections and previews
            self.image_paths.clear()
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
            
            self.image_paths.extend(file_paths)
            # Preview all selected images
            for path in file_paths:
                preview = Image.open(path)
                if preview.size[0] > 100:  # Resize for preview if too large
                    preview = preview.resize((100, int(100 * preview.size[1] / preview.size[0])))
                img = ImageTk.PhotoImage(preview)
                self.image_previews.append(img)
                label = tk.Label(self.preview_frame, image=img)
                label.pack(side=tk.LEFT, padx=5)
                
    def remove_images(self):
        # Clear image paths and previews
        self.image_paths.clear()
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
    def generate_images(self):
    
        if not self.image_paths:
            messagebox.showerror("Error", "Please choose images.")
            return
    
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        else:
        # Clear the output directory
            clear_output_directory(self.output_dir)
        
        total_images = len(self.image_paths) * self.num_images.get()
        self.progress["maximum"] = total_images
        self.progress["value"] = 0
    
        for path in self.image_paths:
            try:
                image = Image.open(path)
                # Convert the image mode to 'RGB' if it isn't already 'RGB' or 'RGBA'
                if image.mode not in ['RGB', 'RGBA']:
                    image = image.convert('RGB')
                for i in range(self.num_images.get()):
                    augmented_image = image.copy()
                    # Randomize order of selected augmentations
                    random_order = [method for method, var in self.selected_methods if var.get()]
                    random.shuffle(random_order)
                    for method in random_order:
                        augmented_image = available_methods[method](augmented_image)
                    if augmented_image.mode == 'RGBA':
                        augmented_image = augmented_image.convert('RGB')
                    base_name = os.path.basename(path).split('.')[0]
                    # Ensure unique filenames
                    counter = 1
                    save_path = os.path.join(self.output_dir, f"{base_name}_augmented_{i+1}.jpg")
                    while os.path.exists(save_path):
                        save_path = os.path.join(self.output_dir, f"{base_name}_augmented_{i+1}_{counter}.jpg")
                        counter += 1
                    augmented_image.save(save_path)
                    self.progress["value"] += 1
                    self.root.update_idletasks()
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {path}. {str(e)}")
                continue
        messagebox.showinfo("Success", f"Augmented images saved in {self.output_dir}.")
        self.progress["value"] = 0
        # Open the output directory
        os.startfile(self.output_dir)

        
    def change_output_folder(self):       
        new_dir = filedialog.askdirectory()
        if new_dir:  # If user selects a folder
            self.output_dir = new_dir
            self.output_dir_label.config(text=self.output_dir)  # Update the displayed path


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAugmentationAppV5(root)
    root.mainloop()
