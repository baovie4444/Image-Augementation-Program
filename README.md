# Image-Augementation-Program
This Python program is for a graphical user interface (GUI) application named "Image Augmentation App", which is designed to perform various image augmentation techniques on selected images. This application is built using the `tkinter` library for the GUI components, `PIL` (Python Imaging Library) for image processing, and other standard Python libraries. Here's an overview of its functionality:

### Features

1. **Image Augmentation Functions:**
   - `random_rotation`: Rotates the image by a random angle.
   - `random_translation`: Shifts the image by a random x and y amount.
   - `random_zoom`: Zooms in or out of the image.
   - `change_brightness`: Alters the brightness of the image.
   - `random_flip`: Randomly flips the image horizontally, vertically, or both.
   - `change_color`: Adjusts the color intensity of the image.

2. **GUI Components:**
   - Image selection and preview.
   - Choice of augmentation methods through checkboxes.
   - Input field for the number of augmented images per input.
   - Progress bar to indicate processing status.
   - Output directory specification and change option.

3. **Additional Functionalities:**
   - `clear_output_directory`: Clears the specified output directory.
   - `choose_images`: Opens a file dialog to select images.
   - `remove_images`: Clears selected images.
   - `generate_images`: Processes the images with the selected augmentations and saves them in the output directory.
   - `change_output_folder`: Changes the output directory.

4. **Application Setup:**
   - Title: "Image Augmentation App V5"
   - Window Icon: Specified (path to a `.ico` file).
   - Window Size: 1920x1080.

### Running the Application

To run this application:
1. Ensure Python is installed along with the `tkinter` and `PIL` libraries.
2. Run the script. This will open the GUI where you can choose images and apply the augmentation techniques.

### Customization and Extension

The application can be customized by modifying the augmentation functions or adding new ones. Additionally, the GUI layout and styles can be changed as per requirements.

### Note

- The icon and output directory paths are hardcoded, which might need modification based on your system setup.
- The script handles various error scenarios, like missing images or processing errors, and provides appropriate user feedback.
