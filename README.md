--> I want to note that if you are on Github and you want to use the software like any normal program on your computer "Windows 10+ 64-bit", just download "exe_program.rar" and extract it and then use it as an ordinary exe program.

## Instructions for normal user

## Format Converter Tool

## Overview
This program is a format converter that can convert between the following formats:
- PNG
- JPG
- JPEG
- PDF

## How to use?
- 1. Put the path of the folder containing the files to be converted in the File Folder field.
- 2. In the output Folder field, put the path of the folder where you want to put the output files after conversion.
- 3. Select the format you want to convert to from the format selection box.
- 4. If you are converting from images to PDF and do not want to collect all the images in one PDF file, you can disable the Merge PDF files option.
- 5. Click on the convert button.
- 6. Now it should start the file conversion process, and you should wait until the conversion process is finished. If you want to cancel the process, click on the cancel button.

## Version
- Current version: 1.3.1

## Features
- Completely free.
- Does not require an internet connection.
- Can convert multiple different formats to a single format in the same operation.

## Usage Instructions
- 1. **Slow Conversion from PDF to Image**: If the conversion process from a PDF to an image is extremely slow or lead to high memory usage, you can reduce the DPI value in the settings.
- 2. **Image Quality**: The default value of image quality in the program is 100%, meaning the full original quality of the image before conversion. If you want to reduce the image size or image quality, then you can reduce this value. Know that you can also reduce the image size without affecting the image quality after conversion by reducing the value of the image quality slightly, for example, to 95%, 90%, 85%, or even 80%. These values reduce the quality in a very small, unnoticeable way, while reducing the image size significantly. However, reducing the image quality value will decrease the image size. The max image quality value in the program is 100%, min is 1%, I think you know that already :)
- 3. **DPI Settings**: Be cautious when increasing the DPI value in the settings. Higher DPI values can significantly slow down the conversion process from an image to a PDF, cause unexpected errors, or lead to extremely high memory usage, depending on your device's performance. However, the default value of DPI in the program is 500, it's good and produces high resolution images.

## Settings
- There is a settings in this program, that allows you to control the following:
- 1. Successfully converted notification sound.
- 2. Automatically open output location after converting.
- 3. Save converting operations in history folder.
- 4. Allow converting file(s) with more than 500 MB of size.
- 5. Sort PDF pages method.
- 6. DPI for PDF to Image Conversion.
- 7. Image quality percentage.
- 8. Open history folder.
- 9. Clear history.
- 10. Open console.
- 11. Open variables observer.
- 12. Reset settings.

## PDF sorting methods
- 1. By name.
- 2. By date.
- 3. By _PNUM_.
- You can choose whether you want the sorting be ascending or descending, in the options [Asce] means ascending while [Desc] means descending.

## What is DPI?
- DPI stands for Dots Per Inch. It is a measure of the resolution of a printed or digital image. Higher DPI values mean higher resolution and better image quality, but they also require more processing power and memory. The max DPI value in the program is 2000, min is 1.

## What is Console?
- The console shows the output messages, meaning the console shows detailed information and real-time data. It's useful for advanced users needing deeper insights and for debugging.

## What is Variables observer?
- The variables observer shows the program current variables and its values, most of these variables are created by me when I was writing the program's code (when I was programming it), meaning the variables observer shows detailed information and real-time data. It's useful for extra-advanced users needing deeper insights and for debugging.

## What is History?
- The history feature allows you to keep track of all the activities and data you have generated while using the app. It acts as a comprehensive log that records your interactions, making it easy for you to revisit and review your past conversion processes at any time, it also records the input folder name & path, output folder name & path, files size, output files size, number of files, number of output files, files formats before converting, new files format, conversion date & time, conversion process duration and also all of the values of the program settings when the user converted the files.

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

## Some information for developers on Github
- This source code of this software is written in python.
- Libraries used in the software: socket, time, datetime, requests, threading, subprocess, tkinter, urllib3, os, sys, json.
- The source code of this software is converted in an exe program using pyinstaller.
