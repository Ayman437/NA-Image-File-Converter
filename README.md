# NA-Image&File Convertor

--> I want to note that if you are on GitHub and you want to use the software like any normal program on your computer `Windows 10+ 64-bit`, just download `exe_program.rar` and extract it and then use it as an ordinary exe program.

<img width="612" height="138" alt="Exe program files" src="https://github.com/user-attachments/assets/dd9d7cc7-6cff-44e3-8d6e-58f2c66c405b" />

## Architecture

```text
NA-Image&File Converter/
│
├── data/
│   ├── done.wav              # Notification sound played after conversion
│   ├── icon.ico              # Application icon
|   ├── README.md             # Data's folder README.txt
│   └── settings.json         # User settings and application configuration
│
├── history/                  # Conversion history
│   └── README.txt            # History's folder README.txt
│
├── app_version.txt           # Current application version
├── exe_program.rar           # Compiled Windows executable package
├── README.md                 # Project documentation
└── source_code.py            # Main application source code
```

## Instructions for normal user

## Format Converter Tool

## Overview
This program is a format converter that can convert between the following formats:
- PNG
- JPG
- JPEG
- PDF

<img width="76" height="108" alt="Formats GUI" src="https://github.com/user-attachments/assets/3531ba85-b0fc-4c35-a07e-58aae1336d0d" />

## How to use?
1. Put the path of the folder containing the files to be converted in the File Folder field.
2. In the output Folder field, put the path of the folder where you want to put the output files after conversion.
3. Select the format you want to convert to from the format selection box.
4. If you are converting from images to PDF and do not want to collect all the images in one PDF file, you can disable the Merge PDF files option.
5. Click on the convert button.
6. Now it should start the file conversion process, and you should wait until the conversion process is finished. If you want to cancel the process, click on the cancel button.

<img width="473" height="271" alt="Program GUI 2" src="https://github.com/user-attachments/assets/8382c87b-7812-4804-b931-b34a983e1b56" />
<img width="470" height="271" alt="Program GUI 3" src="https://github.com/user-attachments/assets/1f8b9a0b-91fb-48d0-b4f2-5a262d4dce07" />
<img width="471" height="271" alt="Program GUI 4" src="https://github.com/user-attachments/assets/e1fea77b-5ae4-4c9b-bb56-3e109fdb6656" />

## Version
- Current version: 1.4.2

## Features
- Completely free.
- Does not require an internet connection.
- Can convert multiple different formats to a single format in the same operation.
- Can resize images flexibly.

## Usage Instructions
1. **Slow Conversion from PDF to Image**: If the conversion process from a PDF to an image is extremely slow or lead to high memory usage, you can reduce the DPI value in the settings.
2. **Image Quality**: The default value of image quality in the program is 100%, meaning the full original quality of the image before conversion. If you want to reduce the image size or image quality, then you can reduce this value. Know that you can also reduce the image size without affecting the image quality after conversion by reducing the value of the image quality slightly, for example, to 95%, 90%, 85%, or even 80%. These values reduce the quality in a very small, unnoticeable way, while reducing the image size significantly. However, reducing the image quality value will decrease the image size. The max image quality value in the program is 100%, min is 1%, I think you know that already :)
3. **DPI Settings**: Be cautious when increasing the DPI value in the settings. Higher DPI values can significantly slow down the conversion process from an image to a PDF, cause unexpected errors, or lead to extremely high memory usage, depending on your device's performance. However, the default value of DPI in the program is 500, it's good and produces high resolution images.

## Settings
- There is a settings in this program, that allows you to control the following:
1. Successfully converted notification sound.
2. Automatically open output location after converting.
3. Save converting operations in history folder.
4. Allow converting file(s) with more than 500 MB of size.
5. Open resize images window before every convertion.
6. Sort PDF pages method.
7. DPI for PDF to Image Conversion.
8. Image quality percentage.
9. Open history folder.
10. Clear history.
11. Open console.
12. Open variables observer.
13. Reset settings.

<img width="541" height="276" alt="Program settings GUI 2" src="https://github.com/user-attachments/assets/299bf92b-4744-450b-844d-520a5730ceff" />

## PDF sorting methods

1. By name.
2. By date.
3. By _PNUM_.
- You can choose whether you want the sorting be ascending or descending, in the options [Asce] means ascending while [Desc] means descending.

<img width="557" height="156" alt="pdf sorting method" src="https://github.com/user-attachments/assets/7e6a6753-86c2-4ef0-a0de-820d2a45841a" />

## Resizing images
- The program has a built-in resizing images feature, which is pretty useful for some users.
- If you want to resize images after convertion process, go to the settings and set the option "Open resize images window before every convertion" to ON.

<img width="405" height="174" alt="Resize images 1" src="https://github.com/user-attachments/assets/9b8df5e1-8ee8-4651-beed-dec4355c70d7" />

- Then, before starting the process of convertion, a resize images window will open, so you can enter some required values for resizing the images.
- The required values: 

1. New width in pixels.
2. New height in pixels.
3. Resize method.
4. Resampling.
5. Background color.

### Resize methods
- There are different methods you can choose between in order to resize your images.
1. **Exact size**, this method allows you to fix the size of every image to your specified width and height.
2. **Preserve aspect ratio (compute width)**, this method keeps the original proportions of images when resizing them, so every image does not look stretched or squashed, this particular method will ignore your specified width and compute it automatically based on your specified height.
3. **Preserve aspect ratio (compute height)**, this method does the same but this time it ignores your specified height and computes it automatically based on your specified width.
4. **Fit inside box**, this method resizes the image so that it fits completely within a specified width and height without cropping.
5. **Crop to fit**, this method resizes the image so that the entire target box is filled, even if some parts of the image have to be cut off.
6. **Add padding**, this method resizes the image to fit inside the target dimensions while preserving its aspect ratio, and then filling the remaining empty space with a background color (the color you chose in background color option). 

<img width="338" height="149" alt="resize methods" src="https://github.com/user-attachments/assets/6ab9dff1-6047-4999-a75b-6a510655a66c" />

<img width="106" height="184" alt="background colors" src="https://github.com/user-attachments/assets/54aaf045-f186-43ba-9dee-c2af8e357755" />

### Resampling
- Resampling is a method used to calculate new pixel values when an image is resized.
- Different resampling methods produce different image quality and speed.
- The methods available in the program are: LANCZOS (recommended), BICUBIC, NEAREST, BILINEAR.
- The way they work is a bit complex, you can look them up on the internet if you want to know more about them.

<img width="269" height="118" alt="resampling methods" src="https://github.com/user-attachments/assets/a3bff83b-51b2-408c-9dfd-ca0754ee75e5" />

## What is DPI?
- DPI stands for Dots Per Inch. It is a measure of the resolution of a printed or digital image. Higher DPI values mean higher resolution and better image quality, but they also require more processing power and memory. The max DPI value in the program is 2000, min is 1.

## What is Console?
- The console shows the output messages and the software's RAM usage, meaning the console shows detailed information and real-time data. It's useful for advanced users needing deeper insights and for debugging.

<img width="1920" height="1038" alt="Program console GUI 3" src="https://github.com/user-attachments/assets/3d48f4e1-21fe-497a-a9d9-a49e9ddbca83" />

## What is Variables observer?
- The variables observer shows the program current variables and its values, most of these variables are created by me when I was writing the program's code (when I was programming it), meaning the variables observer shows detailed information and real-time data. It's useful for extra-advanced users needing deeper insights and for debugging.

<img width="1920" height="1039" alt="Variables observer" src="https://github.com/user-attachments/assets/84e41291-e941-47b6-9367-cedbd5698883" />

## What is History?
- The history feature allows you to keep track of all the activities and data you have generated while using the app. It acts as a comprehensive log that records your interactions, making it easy for you to revisit and review your past conversion processes at any time, it also records the input folder name & path, output folder name & path, files size, output files size, number of files, number of output files, files formats before converting, new files format, conversion date & time, conversion process duration and also all the values of the program settings when the user converted the files.

## What is sorting by _PNUM_?
- In this program, I created a new sorting method called _PNUM_, it stands for page number, it allows you to sort the PDF pages by the pages numbers that are in the pages names, which are being added automatically by the program to the pages names when converting from PDF to Image (like "file_page_2_.jpg"), so that you can sort the images after reconverting them to a PDF pages by the same way it has been sorted befor in the PDF file, or even adding the pages numbers to the pages names yourself so you can sort it the way you like.

## Additional Notes
- If there is any file in the folder with the same format as the target format before conversion, it will be ignored.
- Be cautious when enabling the option to convert files larger than 500 MB, as this can significantly slow down the conversion process, cause unexpected errors, or lead to high memory usage if your device's capabilities are not strong enough.
- Do not modify anything in the data folder.
- Do not modify the history / data folders names, as it might break the program. 
- Do not modify anything in the files that the program generates while the converting proccess is not finished yet. 

- Developed by Ayman Saied -
- Please contact me [ clulyf88@gmail.com ] if you face any problem with the program, so I can fix it -

## Some information for developers on GitHub
- To run the program `python source_code.py`
- This source code of this software is written in python.
- Libraries used in python:

```python
import gc
import sys
import time
import shutil
import threading
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.ttk import *
from tkinter import filedialog
import pygame
import random
import re
import os
from PIL import Image, ImageOps
from PyPDF2 import PdfMerger
import fitz
import json
import psutil
```

- The source code of this software is converted into an exe program using pyinstaller.
