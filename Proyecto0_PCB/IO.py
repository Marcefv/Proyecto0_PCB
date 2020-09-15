class Io:

    def guardar(self, name, listaCaracteristicas, spin, rb1, rb2):
        file = open(name, "w+")
        file.write(spin+"\r\n")
        file.write(rb1 + "\r\n")
        file.write(rb2 + "\r\n")
        for i in range(0, len(listaCaracteristicas)):
            file.write(listaCaracteristicas[i]+"\r\n")
        file.close()

    def load(self, name):
        file = open(name, "r")
        leer = file.readlines()
        listaChar = list()
        listaFinal= list()
        listita = list()
        listarb = list()
        listita.append(leer[0])
        listarb.append(leer[1])
        listarb.append(leer[2])
        for line in range(3, len(leer)):
            listaChar.append(leer[line])
        listaFinal.append(listita)
        listaFinal.append(listarb)
        listaFinal.append(listaChar)
        print(listaFinal)
        file.close()
        return listaFinal

