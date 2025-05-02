# 🖼️ Image Framework Tool

A versatile and interactive image processing framework for developers, designers, and automation workflows. This tool allows you to perform advanced image operations such as resizing, format conversion, metadata extraction, filtering, watermarking, background removal, and image downloading—all through a user-friendly CLI.

---

## 🚀 Features

- 📐 **Resize Images**  
  Resize images by specifying dimensions or scaling percentage.

- 🔄 **Convert Image Format**  
  Easily convert images to popular formats like PNG, JPG, WEBP, etc.

- 🎨 **Apply Image Filters**  
  Apply filters including blur, sharpen, grayscale, and more using Pillow and OpenCV.

- ✂️ **Remove Image Background**  
  Automatically remove backgrounds using `rembg`, powered by ML.

- 🧾 **Show Image Metadata**  
  View basic info and EXIF metadata using `piexif` and `Pillow`.

- 🌐 **Download Image from URL**  
  Download images from public URLs using `requests` and `BeautifulSoup`.

- 💧 **Add Watermark to Image**  
  Add text-based watermarks using custom fonts and positioning.

- 🧭 **Interactive CLI Menu**  
  Simple, colorful terminal interface with options to choose tasks.

---

## 📂 Usage

Start the tool via terminal:

```bash
python3 pip install pillow opencv-python rembg piexif requests beautifulsoup4 numpy colorama
python3 IMG-M.py
