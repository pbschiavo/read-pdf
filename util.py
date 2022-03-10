from pdf2image import convert_from_path
import cv2
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import xlsxwriter
from multiprocessing.pool import ThreadPool
from time import sleep, time
from santanderOCR import extrairTextoSantander

row = 0
col = 0

def readPDF(fileBank):
    listaFileBank = str(fileBank).split(";")
    filePDF = listaFileBank[0]
    banco = listaFileBank[1]
    global col
    global row
    row += 1
    linhaAtual = row
    pathImage = str(filePDF).replace(".pdf","")
    pathPDF = "pdf/"+ banco + "/"
    text = ""
    saldo = ""
    conta = ""
    agencia = ""
    tripaNum = ""
    textFile = convert_from_path(pathPDF + str(filePDF), 500)

    try:
        if os.path.exists(pathImage): 
            for foldername,subfolders,files in os.walk(pathImage):
                for file in files:
                    os.remove(foldername + "/" + file) 

            os.rmdir(pathImage)
            os.mkdir(pathImage)
        else:
            os.mkdir(pathImage)
        
    except OSError as error:
        print(error)

    i = 1
    for pageTextFile in textFile:
        image_name = pathImage + "/Page_" + str(i) + ".jpg"  
        pageTextFile.save(image_name, "JPEG")
        i = i+1        

    for foldername,subfolders,files in os.walk(pathImage):
        
        for file in files:
            textImage = cv2.imread(foldername + "/" + file)
            text += pytesseract.image_to_string(textImage)

    if banco == "Santander":
        boleto = extrairTextoSantander(text)

    for foldername,subfolders,files in os.walk(pathImage):
        for file in files:
            os.remove(foldername + "/" + file)
    
    os.rmdir(pathImage)

    return boleto