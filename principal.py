import os
from time import sleep, time
from multiprocessing.pool import ThreadPool
from util import readPDF
import xlsxwriter

# Listar os pdfs #

workbook = xlsxwriter.Workbook('codigoBoletos.xlsx')

start = time()

def multiprocessamento(banco, path):

    worksheet = workbook.add_worksheet(banco)
    threads = []
    pool = ThreadPool(processes=4)
    linhaAtual = 0
    col = 0
    worksheet.write(0, 0, 'boleto') 

    for foldername,subfolders,files in os.walk(path):
        for file in files:
            async_result = pool.map_async(readPDF,(file +";"+ banco,))
            threads.append(async_result)
    letters_list = [result.get() for result in threads]

    for lista1 in letters_list:
        for lista2 in lista1:
            linhaAtual +=1
            worksheet.write(linhaAtual, col, lista2)
    
listaBancos = [('Santander','pdf/')]

for banco,path in listaBancos:
    multiprocessamento(banco,path)

workbook.close()

end = time()
print('tempo de execução : {}'.format(end - start))


