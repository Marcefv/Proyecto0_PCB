class Io:

    def guardar(self, name, listaCaracteristicas, spin):
        file = open(name, "w+")
        file.write(spin+"\r\n")
        for i in range(0, len(listaCaracteristicas)):
            file.write(listaCaracteristicas[i]+"\r\n")



    def load(self, name):
        file = open(name, "r")
        leer = file.readlines()
        listaChar = list()
        listaFinal= list()
        listita = list()
        listita.append(leer[0])
        for line in range(1, len(leer)):
            listaChar.append(leer[line])
        listaFinal.append(listita)
        listaFinal.append(listaChar)
        return listaFinal

