import io
import os
import re
from PIL import Image, ExifTags
from rembg import remove
from PIL import Image as PILImage, ImageDraw, ImageFont
from PIL import ImageFilter
import cv2
import numpy as np
import piexif
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random
from colorama import Fore, Style, init


# ─────────────────────────────────────────────
# IMG-M : Image Multi-tool Framework (v0.1)
# ─────────────────────────────────────────────

def print_banner():
    # Color variations for "IMG-M" (you can customize these)
    title_colors = [
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX
    ]
    
    chosen_color = random.choice(title_colors)
    
    banner = f"""
{chosen_color}{Style.BRIGHT}
    ██╗███╗   ███╗ ██████╗        ███╗   ███╗
    ██║████╗ ████║██╔════╝        ████╗ ████║
    ██║██╔████╔██║██║  ███╗       ██╔████╔██║
    ██║██║╚██╔╝██║██║   ██║ ████║ ██║╚██╔╝██║
    ██║██║ ╚═╝ ██║╚██████╔╝       ██║  ╚═╝██║
    ╚═╝╚═╝     ╚═╝ ╚═════╝        ╚═╝     ╚═╝
{Fore.RESET}
        {Fore.YELLOW}⚡ Image Multi-Tool Framework (v0.1){Style.RESET_ALL}
        {Fore.LIGHTBLACK_EX}───────────────────────────────────{Style.RESET_ALL}
"""
    print(banner)

def main_menu():
    # Get the same random color used in the banner
    title_colors = [
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.LIGHTBLUE_EX,
        Fore.LIGHTMAGENTA_EX,
        Fore.LIGHTCYAN_EX
    ]
    chosen_color = random.choice(title_colors)
    
    print(f"""{chosen_color}{Style.BRIGHT}Available Commands:{Style.RESET_ALL}
  {Fore.GREEN}1. Resize images
  {Fore.BLUE}2. Convert image format
  {Fore.YELLOW}3. Apply image filters
  {Fore.MAGENTA}4. Remove background
  {Fore.CYAN}5. Show image metadata
  {Fore.LIGHTRED_EX}6. Download images from URL
  {Fore.LIGHTMAGENTA_EX}7. Add watermark to image
  {Fore.RED}8. Exit{Style.RESET_ALL}
""")

# Resize images
def resize_images():
    directory = input("Enter the full path of the image directory: ").strip()
    if not os.path.isdir(directory):
        print(f"Invalid directory: {directory}")
        return

    try:
        width = int(input("Enter new width (X): "))
        height = int(input("Enter new height (Y): "))
        extension = input("Enter the new image format (png, jpg, jpeg, bmp, etc.): ").strip().lower()

        valid_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'}
        if extension not in valid_extensions:
            print(f"Invalid extension: {extension}")
            return

        output_dir = os.path.join(directory, 'resized')
        os.makedirs(output_dir, exist_ok=True)

        # Ask if user wants to resize one image or more images
        choice = input("Do you want to resize one image or multiple images? (1 for one, 2 for multiple): ").strip()

        if choice == '1':  # Resize one image
            image_path = input("Enter the full path of the image to resize: ").strip()
            if not os.path.isfile(image_path):
                print(f"Invalid image path: {image_path}")
                return

            try:
                img = Image.open(image_path)
                resized_img = img.resize((width, height))
                base_name, _ = os.path.splitext(os.path.basename(image_path))
                new_file = os.path.join(output_dir, f"{base_name}_resized.{extension}")
                resized_img.save(new_file)
                print(f"Resized: {image_path} → {new_file}")
            except Exception as e:
                print(f"Error with {image_path}: {e}")

        elif choice == '2':  # Resize multiple images
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(tuple(valid_extensions)):
                    try:
                        img = Image.open(file_path)
                        resized_img = img.resize((width, height))
                        base_name, _ = os.path.splitext(filename)
                        new_file = os.path.join(output_dir, f"{base_name}_resized.{extension}")
                        resized_img.save(new_file)
                        print(f"Resized: {filename} → {new_file}")
                    except Exception as e:
                        print(f"Error with {filename}: {e}")

        else:
            print("Invalid choice. Please enter '1' for one image or '2' for multiple images.")
    except Exception as e:
        print(f"Error: {e}")

# Convert images
def convert_image_format():
    # Get the directory containing images
    directory = input("Enter the full path of the image directory: ").strip()
    if not os.path.isdir(directory):
        print(f"Invalid directory: {directory}")
        return

    # Ask for single or multiple images
    convert_multiple = input("Do you want to convert one image or multiple images? (1 for one, 2 for multiple): ").strip()

    # Ask for the desired output format
    output_format = input("Enter the output image format (e.g., PNG, JPEG, BMP, GIF, TIFF, WEBP, PDF): ").strip().upper()

    output_dir = os.path.join(directory, 'converted')
    os.makedirs(output_dir, exist_ok=True)

    if convert_multiple == '1':
        image_path = input("Enter the image path to convert: ").strip()
        if os.path.isfile(image_path):
            try:
                img = PILImage.open(image_path)
                base_name, _ = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(output_dir, f"{base_name}.{output_format.lower()}")
                img.save(output_path, format=output_format)
                print(f"Image converted: {image_path} → {output_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        else:
            print(f"Invalid image file: {image_path}")

    elif convert_multiple == '2':
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    img = PILImage.open(file_path)
                    base_name, _ = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, f"{base_name}.{output_format.lower()}")
                    img.save(output_path, format=output_format)
                    print(f"Image converted: {filename} → {output_path}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    else:
        print("Invalid input. Please choose either '1' for one image or '2' for multiple images.")

# Apply image filters
def apply_image_filters():
    # Get the directory containing images
    directory = input("Enter the full path of the image directory: ").strip()
    if not os.path.isdir(directory):
        print(f"Invalid directory: {directory}")
        return

    # Ask for single or multiple images
    filter_choice = input("Do you want to apply filters to one image or multiple images? (1 for one, 2 for multiple): ").strip()

    # Ask for the filter to apply
    print("\nAvailable filters:")
    print("1. BLUR")
    print("2. CONTOUR")
    print("3. DETAIL")
    print("4. EDGE_ENHANCE")
    print("5. EMBOSS")
    print("6. SHARPEN")
    filter_type = input("Choose a filter (1-6): ").strip()

    filter_dict = {
        '1': ImageFilter.BLUR,
        '2': ImageFilter.CONTOUR,
        '3': ImageFilter.DETAIL,
        '4': ImageFilter.EDGE_ENHANCE,
        '5': ImageFilter.EMBOSS,
        '6': ImageFilter.SHARPEN
    }

    selected_filter = filter_dict.get(filter_type)

    if selected_filter is None:
        print("Invalid choice of filter.")
        return

    output_dir = os.path.join(directory, 'filtered')
    os.makedirs(output_dir, exist_ok=True)

    if filter_choice == '1':
        image_path = input("Enter the image path to apply the filter: ").strip()
        if os.path.isfile(image_path):
            try:
                img = Image.open(image_path)

                # Check if image is RGBA and apply filter accordingly
                if img.mode == 'RGBA':
                    img = img.convert('RGBA')  # Ensure the image is RGBA
                else:
                    img = img.convert('RGB')  # Convert non-RGBA images to RGB for filters

                img = img.filter(selected_filter)

                # Save with the appropriate format based on the mode
                base_name, _ = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(output_dir, f"{base_name}_filtered.png" if img.mode == 'RGBA' else f"{base_name}_filtered.jpg")
                img.save(output_path)
                print(f"Filter applied: {image_path} → {output_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        else:
            print(f"Invalid image file: {image_path}")

    elif filter_choice == '2':
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    img = Image.open(file_path)

                    # Check if image is RGBA and apply filter accordingly
                    if img.mode == 'RGBA':
                        img = img.convert('RGBA')  # Ensure the image is RGBA
                    else:
                        img = img.convert('RGB')  # Convert non-RGBA images to RGB for filters

                    img = img.filter(selected_filter)

                    # Save with the appropriate format based on the mode
                    base_name, _ = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, f"{base_name}_filtered.png" if img.mode == 'RGBA' else f"{base_name}_filtered.jpg")
                    img.save(output_path)
                    print(f"Filter applied: {filename} → {output_path}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    else:
        print("Invalid input. Please choose either '1' for one image or '2' for multiple images.")

# Remove background
def remove_background():
    # Get the directory containing images
    directory = input("Enter the full path of the image directory: ").strip()
    if not os.path.isdir(directory):
        print(f"Invalid directory: {directory}")
        return

    # Ask for single or multiple images
    remove_choice = input("Do you want to remove the background from one image or multiple images? (1 for one, 2 for multiple): ").strip()

    output_dir = os.path.join(directory, 'no_background')
    os.makedirs(output_dir, exist_ok=True)

    if remove_choice == '1':
        image_path = input("Enter the image path to remove the background: ").strip()
        if os.path.isfile(image_path):
            try:
                with open(image_path, 'rb') as img_file:
                    input_image = img_file.read()
                output_image = remove(input_image)
                
                # Convert the binary output back to an image and save it
                img_output = Image.open(io.BytesIO(output_image))
                base_name, _ = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(output_dir, f"{base_name}_no_bg.png")
                img_output.save(output_path)
                print(f"Background removed: {image_path} → {output_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
        else:
            print(f"Invalid image file: {image_path}")

    elif remove_choice == '2':
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    with open(file_path, 'rb') as img_file:
                        input_image = img_file.read()
                    output_image = remove(input_image)

                    # Convert the binary output back to an image and save it
                    img_output = Image.open(io.BytesIO(output_image))
                    base_name, _ = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, f"{base_name}_no_bg.png")
                    img_output.save(output_path)
                    print(f"Background removed: {filename} → {output_path}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    else:
        print("Invalid input. Please choose either '1' for one image or '2' for multiple images.")

# Show image metadata
def show_image_metadata():
    # Get the image path from the user
    image_path = input("Enter the full path of the image file: ").strip()
    
    if not os.path.isfile(image_path):
        print(f"Invalid image file: {image_path}")
        return

    try:
        # Open the image
        with Image.open(image_path) as img:
            print(f"Image Metadata for: {image_path}")
            
            # Display basic metadata like size and format
            print(f"Format: {img.format}")
            print(f"Mode: {img.mode}")
            print(f"Size: {img.size}")
            print(f"Width: {img.width} px")
            print(f"Height: {img.height} px")
            
            # Display EXIF data if it exists (common in JPEG images)
            exif_data = img._getexif()
            if exif_data:
                print("EXIF Metadata:")
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)  # Get the tag name if possible
                    print(f"Tag: {tag_name} - Value: {value}")
            else:
                print("No EXIF metadata found.")

            # Check if the image has PNG metadata (e.g., comments)
            if img.format == 'PNG':
                png_info = img.info
                if png_info:
                    print("PNG Metadata:")
                    for key, value in png_info.items():
                        print(f"{key}: {value}")
                else:
                    print("No PNG metadata found.")

    except Exception as e:
        print(f"Error reading the image: {e}")

# Download images from URL
def download_image_from_url():
    image_url = input("Enter the image URL: ").strip()

    if not image_url.startswith('http'):
        print("Please provide a valid URL.")
        return

    try:
        # Detect file extension from the URL (fallback to jpg)
        ext_match = re.search(r'\.(jpg|jpeg|png|gif|bmp|webp|tiff)', image_url, re.IGNORECASE)
        ext = ext_match.group(1).lower() if ext_match else 'jpg'

        # Set the temp image file name
        temp_image_name = f"temp_image.{ext}"

        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(temp_image_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image successfully downloaded and saved as: {temp_image_name}")
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")

    except Exception as e:
        print(f"Error downloading the image: {e}")

# Add watermark to image
def add_watermark_to_image():
    image_path = input("Enter the full path of the image: ").strip()

    if not os.path.isfile(image_path):
        print("Invalid image file.")
        return

    watermark_type = input("Watermark type? (text/image): ").strip().lower()

    try:
        img = Image.open(image_path).convert("RGBA")
        watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        if watermark_type == 'text':
            watermark_text = input("Enter the watermark text: ").strip()
            font_path = input("Enter font path (leave blank for default): ").strip()
            font_size = int(input("Enter font size (e.g., 36): ").strip() or 36)
            color_input = input("Enter text color as R,G,B (e.g., 255,255,255): ").strip()
            opacity = int(input("Enter opacity (0–255): ").strip() or 150)
            position = input("Enter position (top-left, top-right, bottom-left, bottom-right, center): ").strip().lower()

            # Set font
            try:
                font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            # Text color and size
            color = tuple(map(int, color_input.split(","))) if color_input else (255, 255, 255)
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Position
            x, y = {
                "top-left": (20, 20),
                "top-right": (img.width - text_width - 20, 20),
                "bottom-left": (20, img.height - text_height - 20),
                "bottom-right": (img.width - text_width - 20, img.height - text_height - 20),
                "center": ((img.width - text_width) // 2, (img.height - text_height) // 2)
            }.get(position, (img.width - text_width - 20, img.height - text_height - 20))

            draw.text((x, y), watermark_text, font=font, fill=(*color, opacity))

        elif watermark_type == 'image':
            watermark_image_path = input("Enter the path to the watermark image: ").strip()
            if not os.path.isfile(watermark_image_path):
                print("Invalid watermark image file.")
                return

            wm_img = Image.open(watermark_image_path).convert("RGBA")
            scale = float(input("Enter scale for watermark image (e.g., 0.25 for 25%): ").strip() or 0.25)
            opacity = int(input("Enter opacity (0–255): ").strip() or 128)
            position = input("Enter position (top-left, top-right, bottom-left, bottom-right, center): ").strip().lower()

            # Resize watermark with correct resampling
            try:
                resample_method = Image.Resampling.LANCZOS
            except AttributeError:
                resample_method = Image.LANCZOS

            new_size = (int(wm_img.width * scale), int(wm_img.height * scale))
            wm_img = wm_img.resize(new_size, resample_method)

            # Set opacity
            alpha = wm_img.getchannel("A")
            alpha = alpha.point(lambda p: opacity)
            wm_img.putalpha(alpha)

            # Position
            x, y = {
                "top-left": (20, 20),
                "top-right": (img.width - wm_img.width - 20, 20),
                "bottom-left": (20, img.height - wm_img.height - 20),
                "bottom-right": (img.width - wm_img.width - 20, img.height - wm_img.height - 20),
                "center": ((img.width - wm_img.width) // 2, (img.height - wm_img.height) // 2)
            }.get(position, (img.width - wm_img.width - 20, img.height - wm_img.height - 20))

            watermark.paste(wm_img, (x, y), wm_img)

        else:
            print("Unsupported watermark type.")
            return

        combined = Image.alpha_composite(img, watermark)
        base_name = os.path.basename(image_path)
        output_name = f"watermarked_{base_name}"
        combined.convert("RGB").save(output_name)
        print(f"Watermarked image saved as {output_name}")

    except Exception as e:
        print(f"Error adding watermark: {e}")

if __name__ == "__main__":
    print_banner()
    while True:
        main_menu()
        choice = input("Choose an option (1-8): ").strip()
        if choice == '1':
            resize_images()
        elif choice == '2':
            convert_image_format()
        elif choice == '3':
            apply_image_filters()
        elif choice == '4':
            remove_background()
        elif choice == '5':
            show_image_metadata()
        elif choice == '6':
            download_image_from_url()
        elif choice == '7':
            add_watermark_to_image()
        elif choice == '8':
            print("\033[92mGoodbye!\033[0m")
            break
        else:
            print("Invalid choice. Please choose a valid option.")