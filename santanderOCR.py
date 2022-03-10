def extrairTextoSantander(textFile):
    #print(textFile)
    listaTexto = textFile.split("\n")
    #print(listaTexto)

    for iterator in listaTexto:
        if "03399." in iterator:
            boleto = iterator

    posBoleto = boleto.find("03399")

    boleto = boleto[posBoleto:74]
    print(boleto)

    return boleto