import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def select_txt_file():
    txt_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    txt_file_entry.delete(0, tk.END)
    txt_file_entry.insert(tk.END, txt_file_path)

def select_font_file():
    font_file_path = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf")])
    font_file_entry.delete(0, tk.END)
    font_file_entry.insert(tk.END, font_file_path)

def create_images():
    # Get the path of the text file
    txt_file_path = txt_file_entry.get()

    # Check if the text file exists
    if not os.path.exists(txt_file_path):
        status_label.config(text="Text file not found.", fg="red")
        return

    # Get the path of the font file
    font_file_path = font_file_entry.get()

    # Check if the font file exists
    if not os.path.exists(font_file_path):
        status_label.config(text="Font file not found.", fg="red")
        return

    # Define the background color and text color
    background_color = (255, 255, 255)  # White (255, 255, 255)
    text_color = (0, 0, 0)  # Black (0, 0, 0)

    # Define the font and font size
    font_size = 37
    font = ImageFont.truetype(font_file_path, font_size)

    # Define the textbox dimensions and alignment
    textbox_width = 500
    textbox_height = 600
    textbox_padding = 30  # Padding around the textbox
    textbox_position = ((500 - textbox_width) // 2, (600 - textbox_height) // 2)

    # Read the file and get the lines
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

    # Create the output folder
    current_directory = os.getcwd()
    output_folder_path = os.path.join(current_directory, 'Output')
    os.makedirs(output_folder_path, exist_ok=True)

    # Create an image for each line
    for i, line in enumerate(lines):
        # Create the image
        image = Image.new('RGB', (500, 700), background_color)
        draw = ImageDraw.Draw(image)

        # Wrap the text and write line by line
        wrapped_lines = textwrap.wrap(line, width=15)
        y = textbox_position[1] + textbox_padding

        for wrapped_line in wrapped_lines:
            # Place the text on the image
            text_bbox = draw.textbbox((textbox_position[0] + textbox_padding, y),
                                      wrapped_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = textbox_position[0] + textbox_padding + (textbox_width - text_width) // 2
            draw.text((x, y), wrapped_line, font=font, fill=text_color)

            # Leave a 5-pixel gap between lines
            y += text_height + 5

        # Save the image
        output_file_path = os.path.join(output_folder_path, f'{i + 1}.png')
        cropped_image = image.crop((textbox_position[0], textbox_position[1],
                                    textbox_position[0] + textbox_width,
                                    textbox_position[1] + textbox_height))
        cropped_image.save(output_file_path)

        status_label.config(text=f'{output_file_path} saved.', fg="green")

    status_label.config(text='Process completed.', fg="green")

# Create the Tkinter application
root = tk.Tk()
root.title("Image Creator")
root.geometry("600x250")
root.resizable(False, False)

# Top frame
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Text file selection
txt_file_label = tk.Label(top_frame, text="Text File:")
txt_file_label.grid(row=0, column=0, padx=10, sticky="w")
txt_file_entry = tk.Entry(top_frame, width=40)
txt_file_entry.grid(row=0, column=1, padx=10, sticky="w")
txt_file_button = tk.Button(top_frame, text="Browse", command=select_txt_file)
txt_file_button.grid(row=0, column=2, padx=10)

# Font file selection
font_file_label = tk.Label(top_frame, text="Font File:")
font_file_label.grid(row=1, column=0, padx=10, sticky="w")
font_file_entry = tk.Entry(top_frame, width=40)
font_file_entry.grid(row=1, column=1, padx=10, sticky="w")
font_file_button = tk.Button(top_frame, text="Browse", command=select_font_file)
font_file_button.grid(row=1, column=2, padx=10)

# Middle frame
middle_frame = tk.Frame(root)
middle_frame.pack(pady=10)

# Process button
create_button = tk.Button(middle_frame, text="Create Images", command=create_images)
create_button.pack()

# Status label
status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=10)

# Run the application
root.mainloop()