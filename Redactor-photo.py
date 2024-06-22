import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime, timedelta


# Function to add text to image
def add_text_to_image(image_path, text, additional_text, font_size, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Use ArialMT font
    font_path = "arial.ttf"  # Ensure this path is correct and ArialMT is available
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size
    lines = text.split('\n') + additional_text.split('\n')
    max_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
    total_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)

    # Position text at the top-right corner with increased padding
    padding = 10 * 1.75
    x_position = image.width - max_width - padding
    y_position = padding

    # Draw each line of text right-aligned
    for line in lines:
        text_width = draw.textbbox((0, 0), line, font=font)[2]
        draw.text((x_position + max_width - text_width, y_position), line, font=font, fill="white")
        y_position += draw.textbbox((0, 0), line, font=font)[3]

    image.save(output_path)


# Function to process images
def process_images():
    start_date = datetime.strptime(start_date_entry.get(), "%d/%m/%Y").date()
    end_date = datetime.strptime(end_date_entry.get(), "%d/%m/%Y").date()
    start_time = datetime.strptime(start_time_entry.get(), "%H:%M").time()
    end_time = datetime.strptime(end_time_entry.get(), "%H:%M").time()
    place_name = place_name_entry.get()
    city_name = city_name_entry.get()
    coordinates = coordinates_entry.get()
    additional_text = additional_text_entry.get()
    font_size = int(font_size_entry.get())
    time_coefficient = int(time_coefficient_entry.get())

    images = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    output_folder = filedialog.askdirectory(title="Select Output Folder")

    current_date = start_date

    for index, image_path in enumerate(images):
        if current_date > end_date:
            print("Reached end of date range. Stopping.")
            break

        if time_coefficient == 0:
            current_time = start_time
        elif time_coefficient == 1:
            random_seconds = random.randint(0, (
                        datetime.combine(current_date, end_time) - datetime.combine(current_date, start_time)).seconds)
            current_time = (datetime.combine(current_date, start_time) + timedelta(seconds=random_seconds)).time()
        else:
            current_time = start_time

        current_datetime = datetime.combine(current_date, current_time)
        date_str = current_datetime.strftime("%d.%m.%Y, %H:%M")
        text = f"{date_str}\n{place_name}\n{city_name}\n{coordinates}"
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        add_text_to_image(image_path, text, additional_text, font_size, output_path)
        print(f"Processed {image_path}")

        # Increment the current date by one day for each new image
        current_date += timedelta(days=1)


# GUI setup
root = tk.Tk()
root.title("Redactor photo")
root.geometry("400x450")
root.configure(bg="lightblue")



style = ttk.Style()
style.configure("TLabel", background="lightblue", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=10)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(frame, text="Start Date (dd/mm/yyyy):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
start_date_entry = ttk.Entry(frame)
start_date_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="End Date (dd/mm/yyyy):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
end_date_entry = ttk.Entry(frame)
end_date_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Start Time (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
start_time_entry = ttk.Entry(frame)
start_time_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="End Time (HH:MM):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
end_time_entry = ttk.Entry(frame)
end_time_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame, text="Text_1:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
place_name_entry = ttk.Entry(frame)
place_name_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(frame, text="Text_2:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
city_name_entry = ttk.Entry(frame)
city_name_entry.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(frame, text="Text_3:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
coordinates_entry = ttk.Entry(frame)
coordinates_entry.grid(row=6, column=1, padx=5, pady=5)

ttk.Label(frame, text="Text_4:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
additional_text_entry = ttk.Entry(frame)
additional_text_entry.grid(row=7, column=1, padx=5, pady=5)

ttk.Label(frame, text="Font Size:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
font_size_entry = ttk.Entry(frame)
font_size_entry.grid(row=8, column=1, padx=5, pady=5)

ttk.Label(frame, text="Time Coefficient (0 or 1):").grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)
time_coefficient_entry = ttk.Entry(frame)
time_coefficient_entry.grid(row=9, column=1, padx=5, pady=5)

process_button = ttk.Button(frame, text="OK!", command=process_images)
process_button.grid(row=11, column=0, columnspan=2, pady=20)


# Adding description of the program
description_label = ttk.Label(frame, text="T_C == 0 >>> FixTime. "
                                          " T_C == 1 >>> RandomTime.",
                             wraplength=400, justify=tk.LEFT)
description_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()