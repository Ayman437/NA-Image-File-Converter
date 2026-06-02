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
from PIL import Image
from PyPDF2 import PdfMerger
import fitz
import json
import psutil

pygame.mixer.init()
conv_running = False
isConsoleOpen = False
isVariablesObserverOpen = False
isSettingsOpen = False
isClosed = False
isResetingSettingsNow = False
isOpeningSettingsNow = False
isDeletingrightNow = False
isShowingSpaceErrorAlert = False
isShowingHisErrorAlertStage1 = False
isShowingHisErrorAlertStage2 = False
isShowingHisErrorAlertStage3 = False
cancelFiles = []
supportedFilesFormatFound = []

def get_memory_usage():
    while isConsoleOpen:
        memSize = psutil.Process(os.getpid()).memory_info().rss
        memSize2 = memSize
        memType = "Bytes"

        if str(round(memSize / 1024, 2)).replace("0.", "").__len__() > 2:
            memSize2 = round(memSize / 1024, 2)
            memType = "KB"
            if str(round(memSize / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                memSize2 = round(memSize / 1024 / 1024, 2)
                memType = "MB"
                if str(round(memSize / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                    memSize2 = round(memSize / 1024 / 1024 / 1024, 2)
                    memType = "GB"
                    if str(round(memSize / 1024 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                        memSize2 = round(memSize / 1024 / 1024 / 1024 / 1024, 2)
                        memType = "TB"

        memSize2 = str(memSize2)

        if memSize2.endswith("0") and memSize2.__len__() > 1:
            memSize2 = memSize2[:-1]
            memSize2 = memSize2.replace(".0", "")

        if memSize2.endswith("."):
            memSize2 = memSize2[:-1]

        if float(memSize2) < 2:
            if memType == "Bytes":
                memType = "Byte"

        if float(memSize) < 0.01 and float(memSize) != 0:
            if memType == "Byte":
                memSize2 = "Less than 0.01 Byte"

        consoleWindow.title(f"Image/File Converter | Console | Memory usage: {memSize2} {memType}")
        time.sleep(1)

def update_console_text(*args):
    global consoleEntryBox
    global consoleText
    global lastConsoleText

    if consoleEntryBox and consoleText:
        timeConsoleHour = str(time.localtime().tm_hour)
        timeConsoleMin = str(time.localtime().tm_min)
        timeConsoleSec = str(time.localtime().tm_sec)
        if timeConsoleHour.__len__() == 1:
            timeConsoleHour = "0" + timeConsoleHour
        if timeConsoleMin.__len__() == 1:
            timeConsoleMin = "0" + timeConsoleMin
        if timeConsoleSec.__len__() == 1:
            timeConsoleSec = "0" + timeConsoleSec
        timeConsole = timeConsoleHour + ":" + timeConsoleMin + ":" + timeConsoleSec
        consoleEntryBox.config(state=tkinter.NORMAL)
        consoleEntryBox.insert(tkinter.END, "\n" + timeConsole + " " + consoleText.get())
        consoleEntryBox.config(state=tkinter.DISABLED)
        consoleEntryBox.yview(tkinter.END)

def console_log(text):
    global consoleText
    global isConsoleOpen
    global consoleText
    global isShowingSpaceErrorAlert

    if isConsoleOpen == True:
        consoleText.set(text)

def conver_files():
    console_log("Preparing data for conversion process...")
    global conv_running
    global cancelFiles
    global supportedFilesFormatFound
    global isSavingInHistory
    global isCancilingFilesNow
    global isShowingSpaceErrorAlert
    global isShowingHisErrorAlertStage1
    global isShowingHisErrorAlertStage2
    global isShowingHisErrorAlertStage3

    sortingType = None
    gwf = os.getcwd().replace("\\", "/")
    if os.path.exists(gwf + "/data/settings.json"):
        console_log("Fetching settings.json file data...")
        data = json.loads(open(gwf + '/data/settings.json', 'r').read())

        sortingType = data["SPP"]

    pdfMerger = PdfMerger()
    Image.MAX_IMAGE_PIXELS = None

    conv_running = True
    firstTime = time.time()

    segType = senV.get().replace(" ", "")
    input_folder = imagesFolderPath.get()
    seg = senV.get().replace(" ", "").lower().replace(".", "")

    console_log("Gathering supported files formats found in the input folder...")

    if os.path.exists(input_folder):
        for file in os.listdir(input_folder):
            if file.lower().endswith(".pdf"):
                if not seg == "pdf":
                    supportedFilesFormatFound.append("PDF")
                    break
        for file in os.listdir(input_folder):
            if file.lower().endswith(".png"):
                if not seg == "png":
                    supportedFilesFormatFound.append("PNG")
                    break
        for file in os.listdir(input_folder):
            if file.lower().endswith(".jpg"):
                if not seg == "jpg":
                    supportedFilesFormatFound.append("JPG")
                    break
        for file in os.listdir(input_folder):
            if file.lower().endswith(".jpeg"):
                if not seg == "jpeg":
                    supportedFilesFormatFound.append("JPEG")
                    break

    console_log(f"supported files formats found is: {supportedFilesFormatFound.__str__()}")
    output_folder = outputFolderPath.get()

    if mpf.get() == "OFF" and seg == "pdf":
        seg = "pdf-o"


    input_folder = input_folder.replace("\\", "/")
    output_folder = output_folder.replace("\\", "/")

    numberOfFiles = 0

    if seg == "png":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.jpg', '.jpeg', '.pdf')):
                numberOfFiles += 1
    if seg == "jpeg":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.jpg', '.png', '.pdf')):
                numberOfFiles += 1
    if seg == "jpg":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.png', '.jpeg', '.pdf')):
                numberOfFiles += 1
    if seg == "pdf":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.png', '.jpeg', '.jpg')):
                numberOfFiles += 1
    if seg == "pdf-o":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.png', '.jpeg', '.jpg')):
                numberOfFiles += 1

    if numberOfFiles == 1:
        console_log(f"There is a 1 file with supported format in images/files folder")
    else:
        console_log(f"There is a {numberOfFiles} files with supported format in images/files folder")


    numberOfFilers2 = 0
    if seg == "png":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.jpg', '.jpeg')):
                numberOfFilers2 += 1
    if seg == "jpeg":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.jpg', '.png')):
                numberOfFilers2 += 1
    if seg == "jpg":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.png', '.jpeg')):
                numberOfFilers2 += 1
    if seg == "pdf":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.png', '.jpeg', '.jpg')):
                numberOfFilers2 += 1
    if seg == "pdf-o":
        for fileS in os.listdir(input_folder):
            if fileS.lower().endswith(('.png', '.jpeg', '.jpg')):
                numberOfFilers2 += 1
    if isShowingSpaceErrorAlert == False:
        numSuce.set(f"      Successfully converted 0/{numberOfFiles} Files | 0%")

    if output_folder.endswith('/'):
        output_folder = output_folder[:-1]
    if input_folder.endswith('/'):
        input_folder = input_folder[:-1]
    if output_folder.endswith('/'):
        output_folder = output_folder[:-1]
    if input_folder.endswith('/'):
        input_folder = input_folder[:-1]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    console_log("Preparing images/files for conversion process...")
    image_files = ""
    if seg == "png":
        image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.jpg', '.jpeg'))]
    if seg == "jpg":
        image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpeg'))]
    if seg == "jpeg":
        image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpg'))]
    if seg == "pdf" or seg == "pdf-o":
        image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    image_files2 = ""
    if seg == "png":
        image_files2 = [file for file in os.listdir(input_folder) if file.lower().endswith(('.jpg', '.jpeg', '.pdf'))]
    if seg == "jpg":
        image_files2 = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpeg', '.pdf'))]
    if seg == "jpeg":
        image_files2 = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpg', '.pdf'))]
    if seg == "pdf" or seg == "pdf-o":
        image_files2 = [file for file in os.listdir(input_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    fromconver = ""

    for fileS in os.listdir(input_folder):
        if conv_running == True:
            if fileS.lower().endswith('.pdf'):
                fromconver = "pdf"

    successNumber = 1
    filesToMerge = []

    console_log("Getting the image quality")

    quaNum = 100
    gwf323525 = os.getcwd().replace("\\", "/")
    if os.path.exists(gwf323525 + "/data/settings.json"):
        data = json.loads(open(gwf323525 + '/data/settings.json', 'r').read())
        if data["IGQ"] <= 100 and data["IGQ"] >= 1:
            quaNum = data["IGQ"]
            console_log(f"The image quality is: {quaNum}%")
        else:
            console_log("Error in image quality value: Invalid value")
    else:
        console_log("Error in fetching settings.json file: Not exists")

    console_log("Converting images/files...")
    for image_file in image_files:
        if conv_running == True:
            image_path = os.path.join(input_folder, image_file)
            image = Image.open(image_path)
            image_rgb = image.convert('RGB')
            output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + f"_{random.randint(1, 100000)}.{seg}")
            pdf_output_path = ""
            if seg == "pdf-o":
                pdf_output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + f"_{random.randint(1, 100000)}.pdf")
                cancelFiles.append(pdf_output_path)
            else:
                pdf_output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + f"_{random.randint(1, 100000)}.{seg}")
                cancelFiles.append(pdf_output_path)

            if seg == "png" and image.format != "PDF":
                temp_output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + f"_{random.randint(1, 100000)}.{image.format.lower()}")
                try:
                    image_rgb.save(temp_output_path, quality=quaNum)
                except OSError as e:
                    if e.errno == 28:
                        if isShowingSpaceErrorAlert == False:
                            isShowingSpaceErrorAlert = True
                            conv_running = False
                            console_log("Error: There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                            messagebox.showwarning("Not enough space", "There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                    else:
                        conv_running = False
                        console_log(f"Unexpected error: {e}")
                        messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")

                if os.path.exists(temp_output_path):
                    image_rgb = Image.open(temp_output_path)

                try:
                    image_rgb.save(output_path, format="PNG", quality=100)
                except OSError as e:
                    if e.errno == 28:
                        if isShowingSpaceErrorAlert == False:
                             isShowingSpaceErrorAlert = True
                             conv_running = False
                             console_log("Error: There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                             messagebox.showwarning("Not enough space", "There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                    else:
                        conv_running = False
                        console_log(f"Unexpected error: {e}")
                        messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")
                if os.path.exists(temp_output_path):
                    os.remove(temp_output_path)
                cancelFiles.append(output_path)
                if isShowingSpaceErrorAlert == False:
                    console_log(f"Successfully converted {image_file} to {seg.upper()} {successNumber}/{numberOfFiles} {str(round(successNumber * 100 / numberOfFiles, 1)).replace('.0', '')}%")
            else:
                try:
                    image_rgb.save(pdf_output_path, quality=quaNum)
                    if seg == "pdf":
                        console_log("Copying dates...")
                        stat = os.stat(image_path)
                        os.utime(pdf_output_path, (stat.st_atime, stat.st_mtime))
                except OSError as e:
                    if e.errno == 28:
                        if isShowingSpaceErrorAlert == False:
                            isShowingSpaceErrorAlert = True
                            conv_running = False
                            console_log("Error: There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                            messagebox.showwarning("Not enough space", "There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                    else:
                        conv_running = False
                        console_log(f"Unexpected error: {e}")
                        messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")

                if isShowingSpaceErrorAlert == False:
                    console_log(f"Successfully converted {image_file} to {seg.upper()} {successNumber}/{numberOfFiles} {str(round(successNumber * 100 / numberOfFiles, 1)).replace('.0', '')}%")

            if seg == "pdf":
                filesToMerge.append(pdf_output_path)
                if isShowingSpaceErrorAlert == False:
                    numSuce.set(f"      Successfully converted {successNumber}/{numberOfFiles} Files | {str(round(successNumber * 100 / numberOfFiles, 1)).replace('.0', '')}%")
            successNumber += 1

    fileNamePdfMerg = ""
    pdfsToDelete = []
    meref = 0

    if seg == "pdf":
        console_log("Sorting PDF files...")

        def extract_page_number(filename):
            match = re.search(r'_page_(\d+)', filename, re.IGNORECASE)
            return int(match.group(1)) if match else float('inf')

        def natural_sort_key(text):
            return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', text)]

        sorted_files_to_merge = filesToMerge

        console_log(f"Sorting type: {sortingType.__str__()}")
        if sortingType == "By _PNUM_ [Asce]":
            sorted_files_to_merge = sorted(filesToMerge, key=extract_page_number)
        elif sortingType == "By name [Asce]":
            sorted_files_to_merge = sorted(filesToMerge, key=natural_sort_key)
        elif sortingType == "By date [Asce]":
            sorted_files_to_merge = sorted(filesToMerge, key=lambda file: os.path.getmtime((file)))
        elif sortingType == "By _PNUM_ [Desc]":
            sorted_files_to_merge = sorted(filesToMerge, key=extract_page_number, reverse=True)
        elif sortingType == "By name [Desc]":
            sorted_files_to_merge = sorted(filesToMerge, key=natural_sort_key, reverse=True)
        elif sortingType == "By date [Desc]":
            sorted_files_to_merge = sorted(filesToMerge, key=lambda file: os.path.getmtime((file)), reverse=True)

        console_log("Merging PDF files...")

        for file in sorted_files_to_merge:
            if conv_running == True:
                if file.lower().endswith(".pdf"):
                    pdfMerger.append(file)
                    meref += 1
                    pdfsToDelete.append(file)
                    cancelFiles.append(file)
                    fileNamePdfMerg = file
                    if isShowingSpaceErrorAlert == False:
                        numSuce.set(f"      Successfully converted {meref}/{numberOfFiles} Files | {str(round(meref * 100 / numberOfFiles, 1)).replace('.0', '')}% | PDF Operation")
                    if round(meref * 100 / numberOfFiles) == 100:
                        if isShowingSpaceErrorAlert == False:
                            numSuce.set(f"      Successfully converted {meref}/{numberOfFiles} Files | {str(round(meref * 100 / numberOfFiles, 1)).replace('.0', '')}% | Please wait...")

                    if isShowingSpaceErrorAlert == False:
                        console_log(f"Successfully Merged {file.split('/')[file.split('/').__len__() - 1]} {meref}/{numberOfFiles} {str(round(meref * 100 / numberOfFiles, 1)).replace('.0', '')}%")

        newNamePdf = f"{fileNamePdfMerg.replace('.pdf', '')}_merged_{random.randint(1, 100000)}.pdf"
        try:
            pdfMerger.write(newNamePdf)
        except OSError as e:
            if e.errno == 28:
                if isShowingSpaceErrorAlert == False:
                    isShowingSpaceErrorAlert = True
                    conv_running = False
                    console_log("Error: There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                    messagebox.showwarning("Not enough space", "There is not enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
            else:
                conv_running = False
                console_log(f"Unexpected error: {e}")
                messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")

        cancelFiles.append(newNamePdf)
        pdfMerger.close()
        if isShowingSpaceErrorAlert == False:
            console_log(f"Successfully Merged all PDF files {meref}")

        console_log(f"Removing Unmerged PDF files...")
        for fileDele in pdfsToDelete:
            if conv_running == True:
                os.remove(fileDele)
                fileDele2 = fileDele.replace("\\", "")
                console_log(f"{fileDele2.split('/')[fileDele2.split('/').__len__() - 1]} has been removed successfully")
        console_log(f"Successfully deleted all Unmerged PDF files")

    if seg == "pdf-o":
        seg = "pdf"

    if fromconver == "pdf" and seg != "pdf":

        if successNumber == 1:
            successNumber = 0

        total_pages = 0

        for filename in os.listdir(input_folder):
            if conv_running:
                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(input_folder, filename)
                    pdf_document = fitz.open(pdf_path)
                    num_pages = len(pdf_document)
                    total_pages += num_pages

        numPdfOperation34 = 0

        console_log("Getting the DPI value...")

        dpiNum = 500
        gwf249080 = os.getcwd().replace("\\", "/")
        if os.path.exists(gwf249080 + "/data/settings.json"):
            data = json.loads(open(gwf249080 + '/data/settings.json', 'r').read())
            if data["DPI"] <= 2000 and data["DPI"] >= 1:
                dpiNum = data["DPI"]
                console_log(f"The DPI value is: {dpiNum}")
            else:
                console_log("Error in DPI value: Invalid value")
        else:
            console_log("Error in fetching settings.json file: Not exists")

        console_log(f"Converting PDF to {seg.upper()}...")
        for filename in os.listdir(input_folder):
            if conv_running:
                if filename.lower().endswith(".pdf"):
                    if seg != "pdf" and seg != "pdf-o":
                        pdf_path = os.path.join(input_folder, filename)
                        pdf_document = fitz.open(pdf_path)
                        for i in range(len(pdf_document)):
                            if conv_running:
                                page = pdf_document.load_page(i)
                                pix = page.get_pixmap(dpi=dpiNum)
                                temp_output_filename = f"{filename.replace('.pdf', '')}_page_{i + 1}_{random.randint(1, 100000)}.jpg"
                                temp_output_path = os.path.join(output_folder, temp_output_filename)
                                try:
                                    pix.save(temp_output_path)
                                except OSError as e:
                                    if e.errno == 28:
                                        if isShowingSpaceErrorAlert == False:
                                            isShowingSpaceErrorAlert = True
                                        conv_running = False
                                        console_log("Error: There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                        messagebox.showwarning("No enough space", "There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                    else:
                                        conv_running = False
                                        console_log(f"Unexpected error: {e}")
                                        messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")

                                if seg != "png":
                                    image = Image.open(temp_output_path)
                                    final_output_filename = f"{filename.replace('.pdf', '')}_page_{i + 1}_{random.randint(1, 100000)}.{seg}"
                                    final_output_path = os.path.join(output_folder, final_output_filename)
                                    cancelFiles.append(final_output_path)
                                    try:
                                        image.save(final_output_path, quality=quaNum)
                                    except OSError as e:
                                        if e.errno == 28:
                                            if isShowingSpaceErrorAlert == False:
                                                isShowingSpaceErrorAlert = True
                                            conv_running = False
                                            console_log("Error: There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                            messagebox.showwarning("No enough space", "There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                        else:
                                            conv_running = False
                                            console_log(f"Unexpected error: {e}")
                                            messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")

                                    if isShowingSpaceErrorAlert == False:
                                        console_log(f"successfully converted {filename} page_{i + 1} to {seg.upper()} {numPdfOperation34 + 1}/{total_pages} {str(round((numPdfOperation34 + 1) * 100 / total_pages, 1)).replace('.0', '')}%")
                                else:
                                    image = Image.open(temp_output_path)
                                    final_output_filename2 = f"{filename.replace('.pdf', '')}_page_{i + 1}_{random.randint(1, 100000)}.jpg"
                                    final_output_path2 = os.path.join(output_folder, final_output_filename2)
                                    try:
                                        image.save(final_output_path2, quality=quaNum)
                                    except OSError as e:
                                        if e.errno == 28:
                                            if isShowingSpaceErrorAlert == False:
                                                isShowingSpaceErrorAlert = True
                                            conv_running = False
                                            console_log("Error: There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                            messagebox.showwarning("No enough space", "There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                        else:
                                            conv_running = False
                                            console_log(f"Unexpected error: {e}")
                                            messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")

                                    image = Image.open(final_output_path2)
                                    final_output_filename23 = f"{filename.replace('.pdf', '')}_page_{i + 1}_{random.randint(1, 100000)}.png"
                                    final_output_path23 = os.path.join(output_folder, final_output_filename23)
                                    try:
                                        image.save(final_output_path23, quality=100)
                                    except OSError as e:
                                        if e.errno == 28:
                                            if isShowingSpaceErrorAlert == False:
                                                isShowingSpaceErrorAlert = True
                                            conv_running = False
                                            console_log("Error: There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                            messagebox.showwarning("No enough space", "There is no enough space in the device to convert, so the conversion process will be cancelled, you should free up some space and then convert again")
                                        else:
                                            conv_running = False
                                            console_log(f"Unexpected error: {e}")
                                            messagebox.showwarning("Error", "Unexpected error, the conversion process will be cancelled")
                                    if isShowingSpaceErrorAlert == False:
                                        console_log(f"successfully converted {filename} page_{i + 1} to {seg.upper()} {numPdfOperation34 + 1}/{total_pages} {str(round((numPdfOperation34 + 1) * 100 / total_pages, 1)).replace('.0', '')}%")
                                    cancelFiles.append(final_output_path23)
                                    os.remove(final_output_path2)

                                os.remove(temp_output_path)

                                numPdfOperation34 += 1
                                if isShowingSpaceErrorAlert == False:
                                    numSuce.set(f"      Successfully converted {numPdfOperation34}/{total_pages} Files | {str(round(numPdfOperation34 * 100 / total_pages, 1)).replace('.0', '')}% | PDF Operation")
                                successNumber += 1
                                if successNumber > numberOfFiles:
                                    numberOfFiles = successNumber

        if fromconver == "pdf" and seg != "pdf" and seg != "pdf-o":
            if isShowingSpaceErrorAlert == False:
                numSuce.set(f"      Successfully converted {successNumber}/{successNumber} Files | 100% Please wait...")

        numberOfFiles = total_pages + numberOfFilers2

    if successNumber == 1:
        if conv_running == True:
            if isShowingSpaceErrorAlert == False:
                numSuce.set(f"      Successfully converted 1 file | 100%")
                console_log("Successfully converted 1 file 100%")
            connVNum.config(fg="#056305")
            convertButton.config(state="write")
            constate.set("Convert more")
            canselButton.config(state=tkinter.DISABLED)
            errorText.set("")
        else:
            if isCancilingFilesNow == False:
                console_log("Canceling the operation...")
                isCancilingFilesNow = True
                for fileDelet in cancelFiles:
                    if os.path.exists(fileDelet):
                        os.remove(fileDelet)
                        fileDelet2 = fileDelet.replace("\\", "/")
                        console_log(f"{fileDelet2.split('/')[fileDelet2.split('/').__len__() - 1]} has been removed successfully")
                cancelFiles = []
                isCancilingFilesNow = False

            numSuce.set(f"      Successfully canceled the operation")
            console_log("Successfully canceled the operation")
            connVNum.config(fg="black")
            convertButton.config(state="write")
            constate.set("Convert more")
            canselButton.config(state=tkinter.DISABLED)
            errorText.set("")
            canselButton.config(text="Cancel")
    else:
        if conv_running == True:
            if isShowingSpaceErrorAlert == False:
                numSuce.set(f"      Successfully converted {numberOfFiles}/{numberOfFiles} Files | 100%")
                console_log(f"Successfully converted {numberOfFiles}/{numberOfFiles} Files 100%")
            connVNum.config(fg="#056305")
            convertButton.config(state="write")
            constate.set("Convert more")
            canselButton.config(state=tkinter.DISABLED)
            errorText.set("")
        else:
            if isCancilingFilesNow == False:
                console_log("Canceling the operation...")
                isCancilingFilesNow = True
                for fileDelet in cancelFiles:
                    if os.path.exists(fileDelet):
                        os.remove(fileDelet)
                        fileDelet2 = fileDelet.replace("\\", "/")
                        console_log(f"{fileDelet2.split('/')[fileDelet2.split('/').__len__() - 1]} has been removed successfully")
                cancelFiles = []
                isCancilingFilesNow = False

            numSuce.set(f"      Successfully canceled the operation")
            console_log("Successfully canceled the operation")
            connVNum.config(fg="black")
            convertButton.config(state="write")
            constate.set("Convert more")
            canselButton.config(state=tkinter.DISABLED)
            errorText.set("")
            canselButton.config(text="Cancel")

    if conv_running == True:
        sizeOfFilesInB28 = 0
        for file8 in cancelFiles:
            if os.path.exists(file8):
                sizeOfFilesInB28 += os.stat(file8).st_size

        oSize658 = sizeOfFilesInB28
        oType658 = "Bytes"
        oSize6528 = sizeOfFilesInB28

        if str(round(oSize658 / 1024, 2)).replace("0.", "").__len__() > 2:
            oSize6528 = round(oSize658 / 1024, 2)
            oType658 = "KB"
            if str(round(oSize658 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                oSize6528 = round(oSize658 / 1024 / 1024, 2)
                oType658 = "MB"
                if str(round(oSize658 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                    oSize6528 = round(oSize658 / 1024 / 1024 / 1024, 2)
                    oType658 = "GB"
                    if str(round(oSize658 / 1024 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                        oSize6528 = round(oSize658 / 1024 / 1024 / 1024 / 1024, 2)
                        oType658 = "TB"

        oSize6528 = str(oSize6528)

        if oSize6528.endswith("0") and oSize6528.__len__() > 1:
            oSize6528 = oSize6528[:-1]
            oSize6528 = oSize6528.replace(".0", "")

        if oSize6528.endswith("."):
            oSize6528 = oSize6528[:-1]

        if float(oSize6528) < 2:
            if oType658 == "Bytes":
                oType658 = "Byte"

        if float(oSize658) < 0.01 and float(oSize658) != 0:
            if oType658 == "Byte":
                oType658 = "0.01 Byte"
                oSize6528 = "Less than"

        console_log(f"The output files size is: {oSize6528} {oType658}")


        mainsTime = time.time() - firstTime
        seconds = mainsTime

        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        result = []
        if days > 0:
            if days >= 2:
                days = str(round(days, 2))
                if days.endswith("0"):
                    days = days[:-1]
                    days = days.replace(".0", "")
                if days.endswith("."):
                    days = days[:-1]
                result.append(f"{days} Days")
            else:
                days = str(round(days, 2))
                if days.endswith("0"):
                    days = days[:-1]
                    days = days.replace(".0", "")
                if days.endswith("."):
                    days = days[:-1]
                result.append(f"{days} Day")
        if hours > 0:
            if hours >= 2:
                hours = str(round(hours, 2))
                if hours.endswith("0"):
                    hours = hours[:-1]
                    hours = hours.replace(".0", "")
                if hours.endswith("."):
                    hours = hours[:-1]
                result.append(f"{hours} Hours")
            else:
                hours = str(round(hours, 2))
                if hours.endswith("0"):
                    hours = hours[:-1]
                    hours = hours.replace(".0", "")
                if hours.endswith("."):
                    hours = hours[:-1]
                result.append(f"{hours} Hour")
        if minutes > 0:
            if minutes >= 2:
                minutes = str(round(minutes, 2))
                if minutes.endswith("0"):
                    minutes = minutes[:-1]
                    minutes = minutes.replace(".0", "")
                if minutes.endswith("."):
                    minutes = minutes[:-1]
                result.append(f"{minutes} Minutes")
            else:
                minutes = str(round(minutes, 2))
                if minutes.endswith("0"):
                    minutes = minutes[:-1]
                    minutes = minutes.replace(".0", "")
                if minutes.endswith("."):
                    minutes = minutes[:-1]
                result.append(f"{minutes} Minute")
        if seconds > 0:
            if seconds >= 2:
                seconds = str(round(seconds, 2))
                if seconds.endswith("0"):
                    seconds = seconds[:-1]
                    seconds = seconds.replace(".0", "")
                if seconds.endswith("."):
                    seconds = seconds[:-1]
                result.append(f"{seconds} Seconds")
            else:
                seconds = str(round(seconds, 2))
                if seconds.endswith("0"):
                    seconds = seconds[:-1]
                    seconds = seconds.replace(".0", "")
                if seconds.endswith("."):
                    seconds = seconds[:-1]
                result.append(f"{seconds} Second")

        prossessTakes = " and ".join(result)

        if mainsTime < 0.01:
            prossessTakes = "Less than 0.01 Second"

        console_log(f"The Conversion process took about: {str(prossessTakes).replace('.0', '')}")

        settengsButton.config(state=tkinter.DISABLED)
        gwf4 = os.getcwd().replace("\\", "/")
        console_log("Getting some settings values...")
        if os.path.exists(gwf4 + "/data/settings.json"):
            dataS = json.loads(open(gwf4 + '/data/settings.json', 'r').read())
            console_log(f"Successfully converted notification sound is: {dataS['SCAN']}")
            console_log(f"Automatically open output location after converting is: {dataS['AOFL']}")
            console_log(f"Save converting operations in history folder is: {dataS['SFIH']}")

            if dataS["SCAN"] == "ON":
                threading.Thread(target=playDoneSound).start()

            if dataS["AOFL"] == "ON":
                console_log("Opening output folder in explorer...")
                os.startfile(output_folder)

            if dataS["SFIH"] == "ON":
                isThereSpace = True
                console_log("Updating history folder data...")
                conv_running = False
                isSavingInHistory = True
                settengsButton.config(state="write")
                convertButton.config(state=tkinter.DISABLED)
                constate.set("Updating history folder data...")

                if not os.path.exists(gwf4 + '/history'):
                    os.makedirs(gwf4 + '/history')
                    console_log("Making history folder...")

                console_log("Renaming history folders...")
                for folder in os.listdir(gwf4 + '/history/'):
                    oldName1 = gwf4 + '/history/' + folder
                    oldName2 = oldName1.split("/")[oldName1.split("/").__len__() - 1]
                    newName = oldName2.replace("_last", "_last_temporarily")
                    os.rename(gwf4 + "/history/" + folder, gwf4 + "/history/" + newName)

                console_log("Preparing new history folder...")
                localTime = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}"
                localTime2 = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + " " + str(time.localtime().tm_zone)
                randomNum = random.randint(1, 100000)
                dirName = f"{localTime}_{randomNum}_last"
                dirPath = gwf4 + '/history/' + dirName
                os.makedirs(dirPath)
                console_log("Making files folder...")
                dirNameInput = "files"
                dirPathInput = f"{dirPath}/{dirNameInput}"
                os.makedirs(dirPathInput)
                for file in image_files2:
                    if os.path.exists(input_folder + '/' + file):
                        try:
                            shutil.copy(input_folder + '/' + file, dirPathInput)
                        except OSError as e:
                            if isShowingHisErrorAlertStage1 == False:
                                isShowingHisErrorAlertStage1 = True
                                if e.errno == 28:
                                    isThereSpace = False
                                    console_log(
                                        "Error: There is not enough space in the device to save the new history folder data - stage 1, so the new history folder data will not be saved")
                                    messagebox.showwarning("Not enough space",
                                                           "There is not enough space in the device to save the new history folder data - stage 1, so the new history folder data will not be saved")
                                else:
                                    isThereSpace = False
                                    console_log(f"Unexpected error: {e}")
                                    messagebox.showwarning("Error",
                                                           "Unexpected error, the new history folder data will not be saved")
                                if os.path.exists(dirPath):
                                    shutil.rmtree(dirPath)
                                isSavingInHistory = False
                                constate.set("Convert more")
                                convertButton.config(state="write")

                if isThereSpace == True:
                    console_log("Making output folder...")
                    dirNameOutput = "output"
                    dirPathOutput = f"{dirPath}/{dirNameOutput}"
                    os.makedirs(dirPathOutput)
                    for file in cancelFiles:
                        if os.path.exists(file.replace("\\", "/")):
                            try:
                                shutil.copy(file.replace("\\", "/"), dirPathOutput)
                            except OSError as e:
                                if isShowingHisErrorAlertStage2 == False:
                                    isShowingHisErrorAlertStage2 = True
                                    if e.errno == 28:
                                        isThereSpace = False
                                        console_log("Error: There is not enough space in the device to save the new history folder data - stage 2, so the new history folder data will not be saved")
                                        messagebox.showwarning("Not enough space","There is not enough space in the device to save the new history folder data - stage 2, so the new history folder data will not be saved")
                                    else:
                                        isThereSpace = False
                                        console_log(f"Unexpected error: {e}")
                                        messagebox.showwarning("Error","Unexpected error, the new history folder data will not be saved")
                                    if os.path.exists(dirPath):
                                        shutil.rmtree(dirPath)
                                    isSavingInHistory = False
                                    constate.set("Convert more")
                                    convertButton.config(state="write")

                    if isThereSpace == True:
                        console_log("Preparing Data.txt file...")
                        oSize = 0
                        oSize2 = 0
                        oType = "Bytes"
                        for file in os.listdir(dirPathOutput):
                            oSize += os.stat(dirPathOutput + '/' + file).st_size
                            oSize2 += oSize
                        fSize = 0
                        fSize2 = 0
                        ftype = "Bytes"
                        for file in os.listdir(dirPathInput):
                            fSize += os.stat(dirPathInput + '/' + file).st_size
                            fSize2 += fSize
                        if str(round(oSize / 1024, 2)).replace("0.", "").__len__() > 2:
                            oSize2 = round(oSize / 1024, 2)
                            oType = "KB"
                            if str(round(oSize / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                oSize2 = round(oSize / 1024 / 1024, 2)
                                oType = "MB"
                                if str(round(oSize / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                    oSize2 = round(oSize / 1024 / 1024 / 1024, 2)
                                    oType = "GB"
                                    if str(round(oSize / 1024 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                        oSize2 = round(oSize / 1024 / 1024 / 1024 / 1024, 2)
                                        oType = "TB"
                        if str(round(fSize / 1024, 2)).replace("0.", "").__len__() > 2:
                            fSize2 = round(fSize / 1024, 2)
                            ftype = "KB"
                            if str(round(fSize / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                fSize2 = round(fSize / 1024 / 1024, 2)
                                ftype = "MB"
                                if str(round(fSize / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                    fSize2 = round(fSize / 1024 / 1024 / 1024, 2)
                                    ftype = "GB"
                                    if str(round(fSize / 1024 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                        fSize2 = round(fSize / 1024 / 1024 / 1024 / 1024, 2)
                                        ftype = "TB"

                        fSize2 = str(fSize2)
                        oSize2 = str(oSize2)

                        if fSize2.endswith("0") and fSize2.__len__() > 1:
                            fSize2 = fSize2[:-1]
                            fSize2 = fSize2.replace(".0", "")

                        if oSize2.endswith("0") and oSize2.__len__() > 1:
                            oSize2 = oSize2[:-1]
                            oSize2 = oSize2.replace(".0", "")

                        if float(fSize2) < 2:
                            if ftype == "Bytes":
                                ftype = "Byte"

                        if float(oSize2) < 2:
                            if oType == "Bytes":
                                oType = "Byte"

                        if fSize2.endswith("."):
                            fSize2 = fSize2[:-1]
                        if oSize2.endswith("."):
                            oSize2 = oSize2[:-1]

                        if float(fSize) < 0.01 and float(fSize) != 0:
                            if ftype == "Byte":
                                ftype = "0.01 Byte"
                                fSize2 = "Less than"

                        if float(oSize) < 0.01 and float(oSize) != 0:
                            if oType == "Byte":
                                oType = "0.01 Byte"
                                oSize2 = "Less than"

                        numberOfOutputFiles = 0
                        for file in os.listdir(dirPathOutput):
                            numberOfOutputFiles += 1
                        historyOption = "ON"
                        audioOption = "OFF"
                        sizeOption = "OFF"
                        openFolder = "OFF"
                        dpiOption = 500
                        qualityOption = 100
                        mergeOption = mpf.get()

                        if dataS["AOFL"] == "ON":
                            openFolder = "ON"
                        if dataS["ASF"] == "ON":
                            sizeOption = "ON"
                        if dataS["SCAN"] == "ON":
                            audioOption = "ON"
                        if dataS["DPI"] <= 2000 and dataS["DPI"] >= 1:
                            dpiOption = dataS["DPI"]
                        if dataS["IGQ"] <= 100 and dataS["IGQ"] >= 1:
                            qualityOption = dataS["IGQ"]

                        dataFile = open(dirPath + "/Data.txt", "w")

                        fileOrfilesOutput = "file"
                        fileOrfilesInput = "file"

                        if cancelFiles.__len__() > 1:
                            fileOrfilesOutput = "files"
                        if image_files2.__len__() > 1:
                            fileOrfilesInput = "files"

                        cancelFiles = []

                        try:
                            clmn = "'"
                            dataFile.write(f"{fileOrfilesInput.capitalize()} folder name: {input_folder.split('/')[input_folder.split('/').__len__() - 1]}\nOutput folder name: {output_folder.split('/')[output_folder.split('/').__len__() - 1]}\n\n{fileOrfilesInput.capitalize()} folder path: {input_folder}\nOutput folder path: {output_folder}\n\n{fileOrfilesInput.capitalize()} size: {fSize2} {ftype}\nOutput {fileOrfilesOutput} size: {oSize2} {oType}\n\nNumber of {fileOrfilesInput}: {numberOfFiles}\nNumber of output {fileOrfilesOutput}: {numberOfOutputFiles}\n\nFiles formats before converting: {supportedFilesFormatFound.__str__().replace('[', '').replace(']', '').replace(clmn, '')}\n\nNew {fileOrfilesOutput} format: {segType.replace('.', ' ').upper()}\n\nDate: {localTime} {localTime2}\nConversion process took about: {str(prossessTakes).replace('.0', '')}\n-----------------------------------------------------\n\nSuccessfully converted notification sound: {audioOption}\nAutomatically open output location after converting: {openFolder}\nSave converting operations in history folder: {historyOption}\nAllow converting file(s) with more than 500 MB of size: {sizeOption}\nDPI for PDF to Image Conversion: {dpiOption}\nImage quality percentage: {qualityOption}%\nPDF Sorting type: {sortingType.__str__()}\n\nMerge PDF files: {mergeOption}")
                        except OSError as e:
                            if isShowingHisErrorAlertStage3 == False:
                                isShowingHisErrorAlertStage3 = True
                                if e.errno == 28:
                                    isThereSpace = False
                                    console_log("Error: There is not enough space in the device to save the new history folder data - stage 3, so the new history folder data will not be saved")
                                    messagebox.showwarning("Not enough space","There is not enough space in the device to save the new history folder data - stage 3, so the new history folder data will not be saved")
                                else:
                                    isThereSpace = False
                                    console_log(f"Unexpected error: {e}")
                                    messagebox.showwarning("Error","Unexpected error, the new history folder data will not be saved")
                                if os.path.exists(dirPath):
                                    dataFile.close()
                                    shutil.rmtree(dirPath)
                                isSavingInHistory = False
                                constate.set("Convert more")
                                convertButton.config(state="write")

                        if isThereSpace == True:
                            dataFile.close()

                            console_log("Renaming history folders...")
                            for folder in os.listdir(gwf4 + '/history/'):
                                oldName1 = gwf4 + '/history/' + folder
                                oldName2 = oldName1.split("/")[oldName1.split("/").__len__() - 1]
                                newName = oldName2.replace("_last_temporarily", "")
                                os.rename(gwf4 + "/history/" + folder, gwf4 + "/history/" + newName)

                            console_log("Successfully updated history folder data")

                            isSavingInHistory = False
                            constate.set("Convert more")
                            convertButton.config(state="write")
                        else:
                            console_log("Renaming history folders...")
                            for folder in os.listdir(gwf4 + '/history/'):
                                oldName1 = gwf4 + '/history/' + folder
                                oldName2 = oldName1.split("/")[oldName1.split("/").__len__() - 1]
                                newName = oldName2.replace("_last_temporarily", "_last")
                                os.rename(gwf4 + "/history/" + folder, gwf4 + "/history/" + newName)

        else:
            threading.Thread(target=playDoneSound).start()
            console_log("Opening output folder in explorer...")
            os.startfile(output_folder)
        settengsButton.config(state="write")

        cancelFiles = []
        conv_running = False
        numberOfFiles = 0
        image_files = 0
        fromconver = 0
        successNumber = 0
        filesToMerge = 0
        meref = 0
        isShowingSpaceErrorAlert = False

isSavingInHistory = False
isCancilingFilesNow = False

def browse_button():
    console_log("Asking directory for images/files folder path...")
    fileName = filedialog.askdirectory()
    imagesFolderPath.set(fileName)

    if fileName != "":
        imagesPathEntry.config(state="write")
        console_log(f"Images/Files folder path has set to: {fileName}")
    else:
        imagesPathEntry.config(state="readonly")
        console_log(f"Images/Files folder path has set to: None")

def browse_button2():
    console_log("Asking directory for output folder path...")
    fileName = filedialog.askdirectory()
    outputFolderPath.set(fileName)
    if fileName != "":
        outputPathEntry.config(state="write")
        console_log(f"Output folder path has set to: {fileName}")
    else:
        outputPathEntry.config(state="readonly")
        console_log(f"Output folder path has set to: None")

def mergOnOf():
    if mpf.get() == "OFF":
        mpf.set("ON")
        console_log("Merge PDF files: ON")
    else:
        mpf.set("OFF")
        console_log("Merge PDF files: OFF")

def convertB():
    global isShowingSpaceErrorAlert
    global isShowingHisErrorAlertStage1
    global isShowingHisErrorAlertStage2
    global isShowingHisErrorAlertStage3

    if constate.get() == "Convert more":
        console_log("Resetting values...")
        isShowingSpaceErrorAlert = False
        isShowingHisErrorAlertStage1 = False
        isShowingHisErrorAlertStage2 = False
        isShowingHisErrorAlertStage3 = False
        imagesFolderPath.set("")
        outputFolderPath.set("")
        sen.config(state=tkinter.WRITABLE)
        senV.set("Select")
        numSuce.set("")
        connVNum.config(fg="black")
        sen.config(state="write")
        mpf.set("ON")
        errorText.set("")
        button1.config(state="write")
        button2.config(state="write")
        buttonOffOn.config(state="write")
        constate.set("Convert")
        canselButton.config(state="write")
        canselButton.grid_forget()
        attenchan2.place_forget()
        attenchan.place_forget()
    else:

        if outputFolderPath.get().endswith('/'):
            outputFolderPath.set(outputFolderPath.get()[:-1])
            console_log("The final slash tag in the output folder path has been deleted")
        if imagesFolderPath.get().endswith('/'):
            imagesFolderPath.set(imagesFolderPath.get()[:-1])
            console_log("The final slash tag in the images/files folder path has been deleted")
        if outputFolderPath.get().endswith('/'):
            outputFolderPath.set(outputFolderPath.get()[:-1])
            console_log("The final slash tag in the output folder path has been deleted")
        if imagesFolderPath.get().endswith('/'):
            imagesFolderPath.set(imagesFolderPath.get()[:-1])
            console_log("The final slash tag in the images/files folder path has been deleted")

        console_log("Verifying inputs...")
        if not imagesFolderPath.get().endswith('/'):
            console_log("The last slash tag in images/files folder path has been verified")
            if not outputFolderPath.get().endswith('/'):
                console_log("The last slash tag in output folder path has been verified")
                if imagesFolderPath.get().replace(" ", "") != outputFolderPath.get().replace(" ", ""):
                    console_log("The images/files folder path and output folder path are not equal to each other has been verified")
                    if imagesFolderPath.get().replace(" ", "") != "":
                        console_log("The images/files folder path is not empty has been verified")
                        if outputFolderPath.get().replace(" ", "") != "":
                            console_log("The output folder path is not empty has been verified")
                            if senV.get().replace(" ", "") != "":
                                console_log("The new image/file format has been verified | 1 | Selected")
                                if senV.get() == ".pdf" or senV.get() == ".jpg" or senV.get() == ".jpeg" or senV.get() == ".png":
                                    console_log("The new image/file format has been verified | 2 | The format is supported")
                                    if os.path.exists(imagesFolderPath.get().replace("\\", "/")):
                                        console_log("The existence of the images/files folder path has been verified")
                                        if os.path.exists(outputFolderPath.get().replace("\\", "/")):
                                            console_log("The existence of the output folder path has been verified")

                                            filesType = ()
                                            if senV.get() == ".pdf":
                                                filesType = ('.jpg', '.png', '.jpeg')
                                            if senV.get() == ".jpg":
                                                filesType = ('.pdf', '.png', '.jpeg')
                                            if senV.get() == ".jpeg":
                                                filesType = ('.pdf', '.jpg', '.png')
                                            if senV.get() == ".png":
                                                filesType = ('.pdf', '.jpg', '.jpeg')
                                            numberOfFiles2 = 0
                                            for fileS2 in os.listdir(imagesFolderPath.get().replace("\\", "/")):
                                                if fileS2.lower().endswith(filesType):
                                                    numberOfFiles2 += 1
                                            if numberOfFiles2 > 0:
                                                console_log("Verified for files of supported format in output folder")
                                                console_log("Calculating files size...")
                                                sizeOfFilesInMB = 0
                                                sizeOfFilesInB2 = 0
                                                for fileS3 in os.listdir(imagesFolderPath.get().replace("\\", "/")):
                                                    if fileS3.lower().endswith(filesType):
                                                        sizeOfFilesInMB += round(os.stat(imagesFolderPath.get().replace("\\", "/") + '/' + fileS3).st_size / 1024 / 1024, 1)
                                                        sizeOfFilesInB2 += os.stat(imagesFolderPath.get().replace("\\", "/") + '/' + fileS3).st_size

                                                oSize65 = sizeOfFilesInB2
                                                oType65 = "Bytes"
                                                oSize652 = sizeOfFilesInB2

                                                if str(round(oSize65 / 1024, 2)).replace("0.", "").__len__() > 2:
                                                    oSize652 = round(oSize65 / 1024, 2)
                                                    oType65 = "KB"
                                                    if str(round(oSize65 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                                        oSize652 = round(oSize65 / 1024 / 1024, 2)
                                                        oType65 = "MB"
                                                        if str(round(oSize65 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                                            oSize652 = round(oSize65 / 1024 / 1024 / 1024, 2)
                                                            oType65 = "GB"
                                                            if str(round(oSize65 / 1024 / 1024 / 1024 / 1024, 2)).replace("0.", "").__len__() > 2:
                                                                oSize652 = round(oSize65 / 1024 / 1024 / 1024 / 1024, 2)
                                                                oType65 = "TB"

                                                oSize652 = str(oSize652)

                                                if oSize652.endswith("0") and oSize652.__len__() > 1:
                                                    oSize652 = oSize652[:-1]
                                                    oSize652 = oSize652.replace(".0", "")

                                                if oSize652.endswith("."):
                                                    oSize652 = oSize652[:-1]

                                                if float(oSize652) < 2:
                                                    if oType65 == "Bytes":
                                                        oType65 = "Byte"

                                                if float(oSize65) < 0.01 and float(oSize65) != 0:
                                                    if oType65 == "Byte":
                                                        oType65 = "0.01 Byte"
                                                        oSize652 = "Less than"

                                                console_log(f"The images/files size is: {oSize652} {oType65}")
                                                maxSizeInMB = 500
                                                gwf6 = os.getcwd().replace("\\", "/")
                                                settings = json.loads(open(gwf6 + '/data/settings.json', 'r').read())
                                                if settings["ASF"] == "ON":
                                                    console_log("Allow converting file(s) with more than 500 MB of size option is enabled")
                                                    sizeOfFilesInMB = 0
                                                if sizeOfFilesInMB <= maxSizeInMB:
                                                    console_log("The files size has been verified")
                                                    console_log("Successfully verified inputs")

                                                    console_log("Setting values...")
                                                    convertButton.config(state=tkinter.DISABLED)
                                                    imagesPathEntry.config(state="readonly")
                                                    outputPathEntry.config(state="readonly")
                                                    sen.config(state=tkinter.DISABLED)
                                                    buttonOffOn.config(state=tkinter.DISABLED)
                                                    button1.config(state=tkinter.DISABLED)
                                                    button2.config(state=tkinter.DISABLED)
                                                    constate.set("Converting...")
                                                    errorText.set("")
                                                    canselButton.config(state="write", text="Cancel")
                                                    canselButton.grid(row=5, column=2, sticky=W, columnspan=4, pady=15, padx=4)
                                                    attenchan.place(rely=0.8)
                                                    attenchan2.place(rely=0.87)
                                                    console_log("The values have been set successfully")

                                                    console_log("Starting the conversion process...")
                                                    thread1 = threading.Thread(target=conver_files)
                                                    thread1.start()
                                                else:
                                                    console_log(f"Input error: The maximum size of the files before converting is {maxSizeInMB} MB")
                                                    errorShow(f"The maximum size of the files before converting is {maxSizeInMB} MB")
                                            else:
                                                console_log("Input error: The images/files folder has no any file with supported format")
                                                errorShow("The images/files folder has no any file with supported format")
                                        else:
                                            console_log("Input error: Please enter an exist output folder path")
                                            errorShow("Please enter an exist output folder path")
                                    else:
                                        console_log("Input error: Please enter an exist images/files folder path")
                                        errorShow("Please enter an exist images/files folder path")
                                else:
                                    console_log("Input error: Please select a supported file format")
                                    errorShow("Please select a supported file format")
                            else:
                                console_log("Input error: Please enter the new file format")
                                errorShow("Please enter the new file format")
                        else:
                            console_log("Input error: Please enter the output folder path")
                            errorShow("Please enter the output folder path")
                    else:
                        console_log("Input error: Please enter the images/files folder path")
                        errorShow("Please enter the images/files folder path")
                else:
                    console_log("Input error: Please enter a different images/files folder path & Output folder path")
                    errorShow("Please enter a different images/files folder path & Output folder path")
            else:
                console_log("Input error: Please enter a valid output folder path")
                errorShow("Please enter a valid output folder path")
        else:
            console_log("Input error: Please enter a valid images/files folder path")
            errorShow("Please enter a valid images/files folder path")

def errorShow(text):
    errorText.set("      "+text)

def close_settings(window):
    global isSettingsOpen
    global isClosed
    global consoleText
    global isConsoleOpen

    if isClosed == False:
        if isConsoleOpen == True:
            if consoleText.get() != "Closing settings...":
                console_log("Closing settings...")
        settengsButton.config(state="write")

    isSettingsOpen = False

def audioOptionClick():
    console_log("Updating settings...")
    if audioB.get() == "OFF":
        console_log("Preparing new settings.json file data...")
        audioB.set("ON")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + 'ON' + '", "ASF": "'+ sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        file = open("data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Successfully converted notification sound option has set to: ON")
    else:
        console_log("Preparing new settings.json file data...")
        audioB.set("OFF")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + 'OFF' + '", "ASF": "'+ sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf + "/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Successfully converted notification sound option has set to: OFF")

def openFileCo():
    console_log("Updating settings...")
    if openFileB.get() == "OFF":
        console_log("Preparing new settings.json file data...")
        openFileB.set("ON")
        data = json.loads('{"AOFL": "' + "ON" + '", "SCAN": "' + audioB.get() + '", "ASF": "'+ sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf+"/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Automatically open output location after converting option has set to: ON")
    else:
        console_log("Preparing new settings.json file data...")
        openFileB.set("OFF")
        data = json.loads('{"AOFL": "' + "OFF" + '", "SCAN": "' + audioB.get() + '", "ASF": "'+ sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf + "/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Automatically open output location after converting option has set to: OFF")

def sizeFileCo():
    console_log("Updating settings...")
    if sizeFile.get() == "OFF":
        console_log("Preparing new settings.json file data...")
        sizeFile.set("ON")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "ON", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf + "/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Allow converting file(s) with more than 500 MB of size option has set to: ON")
    else:
        console_log("Preparing new settings.json file data...")
        sizeFile.set("OFF")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "OFF", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf + "/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Allow converting file(s) with more than 500 MB of size option has set to: OFF")


def orderPagesCo(option):
    console_log("Updating settings...")

    console_log("Preparing new settings.json file data...")
    data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "' + sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
    gwf = os.getcwd().replace("\\", "/")
    file = open(gwf + "/data/settings.json", "w")
    console_log("Writing settings.json file...")
    file.write(str(data).replace("'", '"'))
    file.close()

    console_log("Sort PDF option has set to: " + orderPages.get())

def historyCo():
    console_log("Updating settings...")
    if history.get() == "OFF":
        console_log("Preparing new settings.json file data...")
        history.set("ON")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "' + sizeFile.get() + '", ' + '"SFIH": "ON", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf + "/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Save converting operations in history folder option has set to: ON")
    else:
        console_log("Preparing new settings.json file data...")
        history.set("OFF")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "' + sizeFile.get() + '", ' + '"SFIH": "OFF", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        gwf = os.getcwd().replace("\\", "/")
        file = open(gwf + "/data/settings.json", "w")
        console_log("Writing settings.json file...")
        file.write(str(data).replace("'", '"'))
        file.close()
        console_log("Save converting operations in history folder option has set to: OFF")

def openHistory():
    console_log("Opening history folder in explorer...")
    gwf94 = os.getcwd().replace("\\", "/")
    if os.path.exists(gwf94 + '/history'):
        os.startfile(gwf94 + '/history')
    else:
        os.makedirs(gwf94 + '/history')
        os.startfile(gwf94 + '/history')

def resetSettings():
    global isResetingSettingsNow

    isResetingSettingsNow = True

    console_log("Preparing new settings.json file data...")
    data = json.loads('{"AOFL": "ON", "SCAN": "ON", "ASF": "OFF", "SFIH": "ON", "IGQ": 100, "DPI": 500, "SPP": "By name [Asce]"}')
    file3 = open(gwf3 + "/data/settings.json", "w")
    console_log("Writing settings.json file...")
    file3.write(str(data).replace("'", '"'))
    file3.close()

    console_log("The settings have been reset successfully")

    audioB.set("ON")
    openFileB.set("ON")
    history.set("ON")
    sizeFile.set("OFF")
    orderPages.set("By name [Asce]")
    dpi.set(500)
    quality.set(100)

    isResetingSettingsNow = False


def clearHisThr():
    global isDeletingrightNow
    global isSettingsOpen

    console_log("Clearing history folder data...")

    if conv_running == False:
        gwf48 = os.getcwd().replace("\\", "/")
        if os.path.exists(gwf48 + '/history'):
            shutil.rmtree(gwf48 + '/history')
            os.makedirs(gwf48 + '/history')
        else:
            os.makedirs(gwf48 + '/history')
        if historyClearButton:
            historyClearButton.config(state="write")
        isDeletingrightNow = False

        console_log("The history data has been cleared successfully")
    else:
        isDeletingrightNow = False
        console_log("Clear history: You can't clear history folder data when you converting files")
        messagebox.showwarning("Clear history", "You can't clear history folder data when you converting files")
        if isSettingsOpen == False:
            settengsButton.config(state="write")
        historyClearButton.config(state="write")

def clearHis():
    global isDeletingrightNow
    global isSettingsOpen

    if isSavingInHistory == False:
        if isDeletingrightNow == False:
            historyClearButton.config(state=tkinter.DISABLED)
            isDeletingrightNow = True
            threading.Thread(target=clearHisThr).start()
        else:
            historyClearButton.config(state=tkinter.DISABLED)
            console_log("Clear history: Please wait until clearing history folder data")
            messagebox.showwarning("Clear history", "Please wait until clearing history folder data")
            if isSettingsOpen == False:
                settengsButton.config(state="write")
            historyClearButton.config(state="write")
    else:
        historyClearButton.config(state=tkinter.DISABLED)
        console_log("Clear history: Please wait until updating history folder data")
        messagebox.showwarning("Clear history", "Please wait until updating history folder data")
        if isSettingsOpen == False:
            settengsButton.config(state="write")
        historyClearButton.config(state="write")

def validate_input(new_value):
    global isResetingSettingsNow
    global isOpeningSettingsNow

    if new_value.isdigit():
        value = int(new_value)
        if value < 1:
            return False
        else:
            if value > 2000:
                return False
            else:
                if isResetingSettingsNow == False and isOpeningSettingsNow == False:
                    console_log("Preparing new settings.json file data...")
                data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "' + sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(quality.get()) + ', "DPI": ' + str(value) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
                gwf242408 = os.getcwd().replace("\\", "/")
                file = open(gwf242408 + "/data/settings.json", "w")
                if isResetingSettingsNow == False and isOpeningSettingsNow == False:
                    console_log("Writing settings.json file...")
                file.write(str(data).replace("'", '"'))
                file.close()
                if isResetingSettingsNow == False and isOpeningSettingsNow == False:
                    console_log(f"The new DPI value is: {value}")
                return value
    elif new_value == "":
        return 1
    else:
        return False

def validate_input_100(new_value):
    global isResetingSettingsNow
    global isOpeningSettingsNow

    if new_value.isdigit():
        value = int(new_value)
        if value < 1:
            return False
        else:
            if value > 100:
                return False
            else:
                if isResetingSettingsNow == False and isOpeningSettingsNow == False:
                    console_log("Preparing new settings.json file data...")
                data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "' + sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", ' + '"IGQ": ' + str(value) + ', "DPI": ' + str(dpi.get()) + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
                gwf43535 = os.getcwd().replace("\\", "/")
                file = open(gwf43535 + "/data/settings.json", "w")
                if isResetingSettingsNow == False and isOpeningSettingsNow == False:
                    console_log("Writing settings.json file...")
                file.write(str(data).replace("'", '"'))
                file.close()
                if isResetingSettingsNow == False and isOpeningSettingsNow == False:
                    console_log(f"The new image quality value is: {value}%")
                return value
    elif new_value == "":
        return 1
    else:
        return False

def close_console(window):
    global openConsoleButton
    global isConsoleOpen
    global isSettingsOpen

    console_log("Closing console... Bye!")

    if openConsoleButton and isSettingsOpen == True:
        openConsoleButton.config(state="write")

    isConsoleOpen = False

def close_variablesObserver(window):
    global openVariablesObserverButton
    global isVariablesObserverOpen
    global isSettingsOpen

    if isVariablesObserverOpen == True:
        console_log("Closing variables observer... Bye!")

    if openVariablesObserverButton and isSettingsOpen == True:
        openVariablesObserverButton.config(state="write")

    isVariablesObserverOpen = False

def openConsole():
    global isConsoleOpen
    global consoleWindow
    global openConsoleButton
    global consoleEntryBox
    global consoleText

    consoleText = StringVar()
    consoleText.trace_add("write", update_console_text)

    consoleWindow = Toplevel(root)
    if os.path.exists(os.getcwd().replace("\\", "/") + "/data/icon.ico"):
        consoleWindow.iconbitmap(os.getcwd().replace("\\", "/") + "/data/icon.ico")
    consoleWindow.title("NA-Image&File Converter | Console | Memory usage: Calculating...")

    consoleWindow.geometry("700x350")
    consoleWindow.minsize(580, 250)

    if openConsoleButton:
        openConsoleButton.config(state=tkinter.DISABLED)

    consoleEntryBox = scrolledtext.ScrolledText(consoleWindow)
    consoleEntryBox.pack(expand=True, fill='both')

    timeConsoleHour2 = str(time.localtime().tm_hour)
    timeConsoleMin2 = str(time.localtime().tm_min)
    timeConsoleSec2 = str(time.localtime().tm_sec)
    if timeConsoleHour2.__len__() == 1:
        timeConsoleHour2 = "0" + timeConsoleHour2
    if timeConsoleMin2.__len__() == 1:
        timeConsoleMin2 = "0" + timeConsoleMin2
    if timeConsoleSec2.__len__() == 1:
        timeConsoleSec2 = "0" + timeConsoleSec2
    timeConsole2 = timeConsoleHour2 + ":" + timeConsoleMin2 + ":" + timeConsoleSec2

    consoleEntryBox.insert(tkinter.END, timeConsole2 + " Welcome to the console, You can see here the output messages\n-------------------------------------------------------")
    consoleEntryBox.config(state=tkinter.DISABLED)

    isConsoleOpen = True

    getMmoryUsageFun = threading.Thread(target=get_memory_usage)
    getMmoryUsageFun.start()

    consoleWindow.bind("<Destroy>", close_console)


def openVariablesObserver():
    global isVariablesObserverOpen
    global VariablesObserverWindow
    global openVariablesObserverButton
    global VariablesObserverEntryBox

    console_log("Opening variables observer...")

    VariablesObserverWindow = Toplevel(root)
    if os.path.exists(os.getcwd().replace("\\", "/") + "/data/icon.ico"):
        VariablesObserverWindow.iconbitmap(os.getcwd().replace("\\", "/") + "/data/icon.ico")
    VariablesObserverWindow.title("NA-Image&File Converter | Variables Observer")

    VariablesObserverWindow.geometry("700x350")
    VariablesObserverWindow.minsize(580, 250)

    if openVariablesObserverButton:
        openVariablesObserverButton.config(state=tkinter.DISABLED)

    VariablesObserverEntryBox = scrolledtext.ScrolledText(VariablesObserverWindow)
    VariablesObserverEntryBox.pack(expand=True, fill='both')

    VariablesObserverEntryBox.config(state=tkinter.DISABLED)

    isVariablesObserverOpen = True

    threading.Thread(target=printingVariables).start()

    VariablesObserverWindow.bind("<Destroy>", close_variablesObserver)

def printingVariables():
    global VariablesObserverEntryBox

    while True:
        if isVariablesObserverOpen and VariablesObserverEntryBox and not isClosed:
            time.sleep(0.2)

            variavlesAndValues = "None"
            timeVOHour2 = "None"

            for name, value in globals().items():
                timeVOHour2 = str(time.localtime().tm_hour)
                timeVOMin2 = str(time.localtime().tm_min)
                timeVOSec2 = str(time.localtime().tm_sec)
                if timeVOHour2.__len__() == 1:
                    timeVOHour2 = "0" + timeVOHour2
                if timeVOMin2.__len__() == 1:
                    timeVOMin2 = "0" + timeVOMin2
                if timeVOSec2.__len__() == 1:
                    timeVOSec2 = "0" + timeVOSec2
                timeVOHour2 = timeVOHour2 + ":" + timeVOMin2 + ":" + timeVOSec2

                variavlesAndValues += f"{timeVOHour2} {name} => {value}\n"

            yview = VariablesObserverEntryBox.yview()
            VariablesObserverEntryBox.config(state=tkinter.NORMAL)
            VariablesObserverEntryBox.delete(1.0, "end")
            VariablesObserverEntryBox.insert(tkinter.END, timeVOHour2 + f" Welcome to the variables observer, You can see here the current variables and their values\n-------------------------------------------------------\n{variavlesAndValues}")
            VariablesObserverEntryBox.yview_moveto(yview[0])
            VariablesObserverEntryBox.config(state=tkinter.DISABLED)
        else:
            break
def openSettings():
    global settingsWindow
    global audioB
    global openFileB
    global sizeFile
    global openVariablesObserverButton
    global history
    global historyClearButton
    global dpi
    global quality
    global openConsoleButton
    global isSettingsOpen
    global isConsoleOpen
    global isVariablesObserverOpen
    global isOpeningSettingsNow
    global orderPages

    isOpeningSettingsNow = True

    console_log("Opening settings...")

    audioB = StringVar()
    audioB.set("ON")
    openFileB = StringVar()
    openFileB.set("ON")
    history = StringVar()
    history.set("ON")
    sizeFile = StringVar()
    sizeFile.set("OFF")
    orderPages = StringVar()
    orderPages.set("By name [Asce]")
    dpi = tkinter.IntVar()
    dpi.set(500)
    quality = tkinter.IntVar()
    quality.set(100)

    gwf = os.getcwd().replace("\\", "/")
    if os.path.exists(gwf+"/data/settings.json"):
        console_log("Fetching settings.json file data...")
        data = json.loads(open(gwf+'/data/settings.json', 'r').read())
        console_log("Setting values...")
        openFileB.set(data["AOFL"])
        audioB.set(data["SCAN"])
        sizeFile.set(data["ASF"])
        history.set(data["SFIH"])
        dpi.set(data["DPI"])
        quality.set(data["IGQ"])
        orderPages.set(data["SPP"])
    else:
        console_log("Creating settings.json file...")
        data = json.loads('{"AOFL": "' + openFileB.get() + '", "SCAN": "' + audioB.get() + '", "ASF": "' + sizeFile.get() + '", ' + '"SFIH": "' + history.get() + '", "IGQ": ' + str(quality.get()) + ', "DPI": ' + ', "SPP": ' + '"' + orderPages.get() + '"' + '}')
        file = open(gwf+"/data/settings.json", "w")
        file.write(str(data).replace("'", '"'))
        file.close()

    settingsWindow = Toplevel(root)
    if os.path.exists(os.getcwd().replace("\\", "/") + "/data/icon.ico"):
        settingsWindow.iconbitmap(os.getcwd().replace("\\", "/") + "/data/icon.ico")
    settingsWindow.title("NA-Image&File Converter | Settings")
    settingsWindow.maxsize(width=540, height=245)
    settingsWindow.minsize(width=540, height=245)
    settengsButton.config(state=tkinter.DISABLED)

    slbl1 = Label(settingsWindow, text="  Successfully converted notification sound: ")
    slbl1.grid(row=0, column=0, sticky=W, pady=2)
    audioOption = Button(settingsWindow, textvariable=audioB, command=audioOptionClick)
    audioOption.grid(row=0, column=1, sticky=W, pady=2, padx=163.5)

    slbl2 = Label(settingsWindow, text="  Automatically open output location after converting: ")
    slbl2.grid(row=1, column=0, sticky=W, pady=2)
    openFileOption = Button(settingsWindow, textvariable=openFileB, command=openFileCo)
    openFileOption.grid(row=1, column=1, sticky=W, pady=2, padx=163.5)

    slbl3 = Label(settingsWindow, text="  Save converting operations in history folder: ")
    slbl3.grid(row=2, column=0, columnspan=4, sticky=W, pady=2)
    ssveOption = Button(settingsWindow, textvariable=history, command=historyCo)
    ssveOption.grid(row=2, column=1, sticky=W, pady=2, padx=163.5)

    slbl4 = Label(settingsWindow, text="  Allow converting file(s) with more than 500 MB of size: ")
    slbl4.grid(row=3, column=0, columnspan=4, sticky=W, pady=2)
    sizeFileOption = Button(settingsWindow, textvariable=sizeFile, command=sizeFileCo)
    sizeFileOption.grid(row=3, column=1, sticky=W, pady=2, padx=163.5)

    vcmd = (root.register(validate_input), '%P')

    slbl8 = Label(settingsWindow, text="  Sort PDF pages: ")
    slbl8.grid(row=4, column=0, columnspan=4, sticky=W, pady=2)

    suppOptions = ['Select', 'By name [Asce]', 'By date [Asce]', 'By _PNUM_ [Asce]', 'By name [Desc]', 'By date [Desc]', 'By _PNUM_ [Desc]']

    slbl8 = OptionMenu(settingsWindow, orderPages, *suppOptions, command=orderPagesCo)
    slbl8.grid(row=4, column=1, sticky=W, padx=120)

    if os.path.exists(gwf+"/data/settings.json"):
        orderPages.set(data["SPP"])

    slbl5 = Label(settingsWindow, text="  DPI for PDF to Image Conversion - Max=2000, Min=1: ")
    slbl5.grid(row=5, column=0, columnspan=4, sticky=W, pady=2)
    dpiButtton = tkinter.Entry(settingsWindow, textvariable=dpi, width=5, validate='key', validatecommand=vcmd)
    dpiButtton.grid(row=5, column=1, sticky=W, pady=2, padx=190)

    vcmd2 = (root.register(validate_input_100), '%P')

    slbl6 = Label(settingsWindow, text="  Image quality percentage - Max=100%, Min=1%: ")
    slbl6.grid(row=6, column=0, columnspan=4, sticky=W, pady=2)
    qualityButtton = tkinter.Entry(settingsWindow, textvariable=quality, width=5, validate='key', validatecommand=vcmd2)
    qualityButtton.grid(row=6, column=1, sticky=W, pady=2, padx=190)

    slbl7 = Label(settingsWindow, text="%")
    slbl7.grid(row=6, column=1, columnspan=4, sticky=W, pady=2, padx=225)

    historyButton = Button(settingsWindow, text="Open history folder", command=openHistory)
    historyButton.place(rely=0.82, relx=0.02)

    historyClearButton = Button(settingsWindow, text="Clear history", command=clearHis)
    historyClearButton.place(rely=0.82, relx=0.24)

    openConsoleButton = Button(settingsWindow, text="Open console", command=openConsole)
    openConsoleButton.place(rely=0.82, relx=0.39)

    openVariablesObserverButton = Button(settingsWindow, text="Open variables observer", command=openVariablesObserver)
    openVariablesObserverButton.place(rely=0.82, relx=0.555)

    if isConsoleOpen == True:
        openConsoleButton.config(state=tkinter.DISABLED)

    if isVariablesObserverOpen == True:
        openVariablesObserverButton.config(state=tkinter.DISABLED)

    resetButton = Button(settingsWindow, text="Reset settings", command=resetSettings)
    resetButton.place(rely=0.82, relx=0.83)

    isSettingsOpen = True
    isOpeningSettingsNow = False

    settingsWindow.bind("<Destroy>", close_settings)

def playDoneSound():
    console_log("Playing done sound...")
    soundPath = "data/done.wav"
    if os.path.exists(soundPath):
        pygame.mixer.music.load(soundPath)
        pygame.mixer.music.play()
    else:
        console_log("Error in getting sound: The sound does not exist")

def console_log_selected_format(format):
    console_log(f"New file/image format has set to: {format}")

def stopConvirtingRun():
    global conv_running
    conv_running = False
    canselButton.config(text="Canceling...", state=tkinter.DISABLED)

gwf3 = os.getcwd().replace("\\", "/")
if not os.path.exists(gwf3+"/data/settings.json"):
    console_log("Creating settings.json file...")
    data = json.loads('{"AOFL": "ON", "SCAN": "ON", "ASF": "OFF", "SFIH": "ON", "IGQ": 100, "DPI": 500, "SPP": "By name [Asce]"}')
    file2 = open(gwf3+"/data/settings.json", "w")
    file2.write(str(data).replace("'", '"'))
    file2.close()

if not os.path.exists(gwf3+"/history"):
    os.makedirs(gwf3+"/history")

root = Tk()
if os.path.exists(os.getcwd().replace("\\", "/")+"/data/icon.ico"):
    root.iconbitmap(os.getcwd().replace("\\", "/")+"/data/icon.ico")
root.title("NA-Image&File Converter")
root.maxsize(width=469, height=240)
root.minsize(width=469, height=240)

imagesFolderPath = StringVar()
outputFolderPath = StringVar()
senV = StringVar()
mpf = StringVar()
mpf.set("ON")
errorText = StringVar()
errorText.set("")
numSuce = StringVar()
constate = StringVar()
constate.set("Convert")

lbl1 = Label(root, text="      Images/Files folder path: ")
lbl1.grid(row=0, column=0, sticky=W, pady=2)
imagesPathEntry = Entry(root, width=35, textvariable=imagesFolderPath, state="readonly")
imagesPathEntry.grid(row=0, column=1, sticky=W, pady=2)
button1 = Button(root, text="Browse", command=browse_button)
button1.grid(row=0, column=2, sticky=W, pady=2, padx=4)

lbl2 = Label(root, text="      Output folder path:")
lbl2.grid(row=1, column=0, sticky=W, pady=2)
outputPathEntry = Entry(root, width=35, textvariable=outputFolderPath, state="readonly")
outputPathEntry.grid(row=1, column=1, sticky=W, pady=2)
button2 = Button(root, text="Browse", command=browse_button2)
button2.grid(row=1, column=2, sticky=W, pady=2, padx=4)

lbl3 = Label(root, text="      New image/file format: ")
lbl3.grid(row=2, column=0, sticky=W, pady=2)

suppFormats = ['Select', '.jpg', '.jpeg', '.png', '.pdf']

labd = tkinter.Label(root, text="            ", bg="Black")
labd.grid(row=2, column=1, sticky=W, pady=2)
sen = OptionMenu(root, senV, *suppFormats, command=console_log_selected_format)
sen.grid(row=2, column=1, sticky=W, pady=2)

lbl4 = Label(root, text="      Merge PDF files: ")
lbl4.grid(row=3, column=0, sticky=W, pady=2)
buttonOffOn = Button(root, textvariable=mpf, command=mergOnOf)
buttonOffOn.grid(row=3, column=2, sticky=W, pady=2, padx=4)

convertButton = Button(root, text="Convert", width=25, command=convertB, textvariable=constate)
convertButton.place(relx=0.5, rely=0.5)
convertButton.grid(row=4, column=1, sticky=W)

connVNum = tkinter.Label(root, text="", textvariable=numSuce)
connVNum.grid(row=5, column=0, columnspan=4, sticky=W, pady=15)

canselButton = Button(root, text="Cansel", command=stopConvirtingRun)
canselButton.grid(row=5, column=1, sticky=W, columnspan=4, pady=15, padx=4)
canselButton.grid_forget()

attenchan = Label(root, text="      If there is any file in output folder has this format or unsupported format,")
attenchan.place_forget()
attenchan2 = Label(root, text="      It will be exscluded")
attenchan2.place_forget()

errorMesseg = tkinter.Label(root, fg="red", textvariable=errorText)
errorMesseg.place(rely=0.9)

settengsButton = Button(root, text="Settings", command=openSettings)
settengsButton.place(rely=0.88, relx=0.794)

def close_root():
    global cancelFiles
    global conv_running
    global isSavingInHistory
    global isDeletingrightNow
    global isCancilingFilesNow
    global isClosed

    if conv_running == False:
        if isCancilingFilesNow == False:
            isCancilingFilesNow = True
            console_log("Canceling the convertion process...")
            for fileDelet in cancelFiles:
                if os.path.exists(fileDelet.replace("\\", "/")):
                    os.remove(fileDelet.replace("\\", "/"))
                    fileDelet2 = fileDelet.replace("\\", "/")
                    console_log(f"{fileDelet2.split('/')[fileDelet2.split('/').__len__() - 1]} has been removed successfully")
            console_log("Closing the program [Exit]...")
            isCancilingFilesNow = False
            if isSavingInHistory == False:
                if isDeletingrightNow == False:
                    isClosed = True
                    root.destroy()
                else:
                    console_log("Exit: Please wait until clearing history folder data")
                    messagebox.showwarning("Exit", "Please wait until clearing history folder data")
                    settengsButton.config(state="write")
            else:
                console_log("Exit: Please wait until updating history folder data")
                messagebox.showwarning("Exit", "Please wait until updating history folder data")
                settengsButton.config(state="write")
        else:
            console_log("Exit: Please wait until canceling the process")
            messagebox.showwarning("Exit", "Please wait until canceling the process")
            settengsButton.config(state="write")
    else:
        console_log("Exit: You can't close the app while you are converting files")
        messagebox.showwarning("Exit", "You can't close the app while you are converting files")
        settengsButton.config(state="write")

root.protocol("WM_DELETE_WINDOW", close_root)
root.mainloop()