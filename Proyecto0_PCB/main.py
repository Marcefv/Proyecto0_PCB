import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from itertools import product
import random
from Fenotipo import Fenotipo
from IO import Io


class Main:
    def __init__(self):
        #cargar glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Main.glade")
        self.builder.connect_signals(self)

        #objeto ventanda
        self.window = self.builder.get_object("Window")

        #objeto spin button para cambiar cuantas caracteristicas hay
        self.spin = self.builder.get_object("spin_cantidad")

        #boton para generar posibles genotipos de progenitores
        self.btn_generar_prog = self.builder.get_object("btn_generar_prog")

        #boton para generar tabla con cruce
        self.btn_cruce = self.builder.get_object("cruce_btn")

        #lista con los campos para las caracteristicas y sus descripciones
        self.lista_caracteristicas = list()
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_1"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_1"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_2"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_2"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_3"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_3"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_4"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_4"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_5"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_5"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_6"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_6"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_7"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_7"))
        self.lista_caracteristicas.append(self.builder.get_object("lab_car_8"))
        self.lista_caracteristicas.append(self.builder.get_object("txt_car_8"))

        #grid con genotipos lista
        self.grid = self.builder.get_object("grid")

        #label de progenitores
        self.progenitor_1 = self.builder.get_object("progenitor_1")
        self.progenitor_2 = self.builder.get_object("progenitor_2")

        #Treeview con cruce
        self.treeview = self.builder.get_object("treeView")

        #label cruce
        self.label_cruce = self.builder.get_object("label_cruce")

        #botonoes colores
        self.rb_genotipo = self.builder.get_object("rb_colorear_genotipo")
        self.rb_fenotipo = self.builder.get_object("rb_colorear_fenotipo")

        #boton guardar y generar archivo y cargar archivo
        self.btn_save = self.builder.get_object("btn_save")
        self.btn_load = self.builder.get_object("btn_load")

        #boton para mostrar porcentajes
        self.btn_porcentajes = self.builder.get_object("btn_porcentajes")
        self.text_view1 = self.builder.get_object("text_view1")
        self.text_view2 = self.builder.get_object("text_view2")

        #mostrar elementos
        self.window.show()

    # Cerrar ventana con boton x de ventana
    def on_Window_destroy(self, window):
        Gtk.main_quit()

    # Cuando cambia valor de cantidad de caracteristicas se muestran u ocultan espacios
    def on_spin_cantidad_value_changed(self, spin):
        if spin.get_value_as_int() == 1:
            for widget in self.lista_caracteristicas:
                if "1" in Gtk.Buildable.get_name(widget) or "2" in Gtk.Buildable.get_name(widget):
                    widget.set_visible(True)
                else:
                    widget.set_visible(False)

        elif spin.get_value_as_int() == 2:
            for widget in self.lista_caracteristicas:
                if ("1" in Gtk.Buildable.get_name(widget) or "2" in Gtk.Buildable.get_name(widget) or "3"
                        in Gtk.Buildable.get_name(widget) or "4" in Gtk.Buildable.get_name(widget)):
                    widget.set_visible(True)
                else:
                    widget.set_visible(False)

        elif spin.get_value_as_int() == 3:
            for widget in self.lista_caracteristicas:
                if "7" in Gtk.Buildable.get_name(widget) or "8" in Gtk.Buildable.get_name(widget):
                    widget.set_visible(False)
                else:
                    widget.set_visible(True)

        elif spin.get_value_as_int() == 4:
            for widget in self.lista_caracteristicas:
                widget.set_visible(True)

    # Metodo para generar ventana con mensaje de error
    def error(self, message):
        error_message = Gtk.MessageDialog(parent=None, flags=0, message_type=Gtk.MessageType.WARNING,
                                          buttons=Gtk.ButtonsType.OK,
                                          text=message)
        error_message.set_title("Error")
        error_message.run()
        error_message.destroy()

    # poner nombres de caracteristicas por defecto
    def caracteristicas_por_defecto(self):
        self.lista_caracteristicas[0].set_text("A")
        self.lista_caracteristicas[2].set_text("a")
        self.lista_caracteristicas[4].set_text("B")
        self.lista_caracteristicas[6].set_text("b")
        self.lista_caracteristicas[8].set_text("C")
        self.lista_caracteristicas[10].set_text("c")
        self.lista_caracteristicas[12].set_text("D")
        self.lista_caracteristicas[14].set_text("d")
        self.lista_caracteristicas[1].set_text("")
        self.lista_caracteristicas[3].set_text("")
        self.lista_caracteristicas[5].set_text("")
        self.lista_caracteristicas[7].set_text("")
        self.lista_caracteristicas[9].set_text("")
        self.lista_caracteristicas[11].set_text("")
        self.lista_caracteristicas[13].set_text("")
        self.lista_caracteristicas[15].set_text("")
        self.genotipo1 = ""
        self.genotipo2 = ""
        self.label_genotipo1 = ""
        self.label_genotipo2 = ""


    #cuando cambia la letra de una caracteristica, se cambia la de la otra pareja automaticamente
    def on_entry_change(self, widget):
        #determina cual etiqueta esta cambiando para saber la etiqueta que debe elegir
        if int(Gtk.Buildable.get_name(widget)[-1]) % 2 == 0:
            obj = self.builder.get_object("lab_car_" + str(int(Gtk.Buildable.get_name(widget)[-1]) - 1))
            #si el texto del cambioes mayuscula entonces cambia la otra etiqueta a minuscula y viceversa
            if widget.get_text().isupper():
                obj.set_text(widget.get_text().lower())
            else:
                obj.set_text(widget.get_text().upper())
        else:
            obj = self.builder.get_object("lab_car_" + str(int(Gtk.Buildable.get_name(widget)[-1]) + 1))
            if widget.get_text().isupper():
                obj.set_text(widget.get_text().lower())
            else:
                obj.set_text(widget.get_text().upper())

    #almacena las caracteristicas de los genotipos
    caract_genotipos = {}
    dict = {}
    #genera los posibles gentoipos de los progenitores
    def on_btn_generar_prog_clicked(self, button):
        self.caract_genotipos = {}
        self.dict = {}
        #borrar genotipos de la lista
        while True:
            if self.grid.get_child_at(0,1)!=None:
                self.grid.remove_row(1)
            else:
                break
        #borrar resultados de cruce
        for columna in self.treeview.get_columns():
            self.treeview.remove_column(columna)

        #oculta label de cruce
        self.label_cruce.set_visible(False)

        self.porcentaje_fenotipos = "Fenotipos:\n\n"
        self.porcentajes_genotipos = "Genotipos:\n\n"
        self.borrar_text_view()

        #guarda la lista con genotipos
        list_genotipos =list()
        inicial = ""

        #validaciones de los campos y generar lista de caracteristicas
        for index, widget in enumerate(self.lista_caracteristicas):

            # determinar cual informacion validadr dependiendo de si es visible o no
            if widget.get_visible():
                if index == 0:
                    inicial = widget.get_text()

                # para las etiquetas o nombres de caracteristica
                if "lab" in Gtk.Buildable.get_name(widget):

                    self.caract_genotipos[widget.get_text()] = self.builder.get_object("txt_car_" + str(int(Gtk.Buildable.get_name(widget)[-1]))).get_text()

                    # determina si es solo texto y si no manda un mensaje de error y devuelve las etiquetas a los valores por defecto
                    # esto tambien valida si el campo esta vacio
                    if not widget.get_text().isalpha():
                        self.error("Solo puede colocar Caracteres alfabeticos\n\nNo puede dejar espacios vacios")
                        self.caracteristicas_por_defecto()
                        self.caract_genotipos.clear()
                        return
                    # valida si hay nombres repetidos, si es asi muestra mensaje de advertencia y vuelve a valores por defecto
                    elif not index == 0:
                        if widget.get_text() == inicial:
                            self.error("No puede colocar caracteres iguales")
                            self.caracteristicas_por_defecto()
                            self.caract_genotipos.clear()
                            return
                        else:
                            inicial == widget.get_text()

                # si es una descripcion, se valida si esta vacio, si esta vacio se muestra un mensaje de error
                else:
                    if widget.get_text().strip() == "":
                        self.error("No puede dejar espacios vacios")
                        self.caract_genotipos.clear()
                        return

        #lista con combinaciones por caracteristica
        set_caract_genotipos = {key.upper(): value for key, value in self.caract_genotipos.items()}
        set_caract_genotipos = set(set_caract_genotipos.keys())
        for value in set_caract_genotipos:
            list_genotipos.append(value + value)
            list_genotipos.append(value + value.lower())
            list_genotipos.append(value.lower() + value.lower())

        #lista de combinaciones entre caracteristicas
        genotipos_combinacion = list_genotipos
        if len(set_caract_genotipos) == 2:
            genotipos_combinacion = list(map("".join, product(list_genotipos[0:3], list_genotipos[3:6])))
        elif len(set_caract_genotipos) == 3:
            genotipos_combinacion = list(map("".join, product(list_genotipos[0:3], list_genotipos[3:6], list_genotipos[6:9])))
        elif len(set_caract_genotipos) == 4:
            genotipos_combinacion = list(map("".join, product(list_genotipos[0:3], list_genotipos[3:6], list_genotipos[6:9], list_genotipos[9:13])))

        #agregar los genotipos a la pantalla de genotipos

        for index, value in enumerate(genotipos_combinacion):
            #varaibale que va a contener el string con caracteristicas del genotipo
            caracteristica = ""

            #Se asigna al string las caracteristicas del genotipo usando un diccionario creado anteriormente
            # y validando si las llaves estan o no presentes en el genotipo
            for key, val in self.caract_genotipos.items():
                if key in genotipos_combinacion[index]:
                    if key.isupper():
                            caracteristica += "  " + val
                    elif (key + key) in genotipos_combinacion[index]:
                            caracteristica += "  " + val

            #si es el primer elemento se crea un radio button y luego los demas van a pertenecer a ese grupo
            if index == 0:
                 self.dict["rb{0}".format(index)] = Gtk.RadioButton(label=genotipos_combinacion[index])
                 self.dict["rb{0}".format(index)].connect("toggled", self.seleccion_grupo1)
                 self.grid.attach_next_to(self.dict["rb{0}".format(index)], self.progenitor_1, Gtk.PositionType.BOTTOM, 1, 1)
                 self.dict["rb20{0}".format(index)] = Gtk.RadioButton(label=genotipos_combinacion[index])
                 self.dict["rb20{0}".format(index)].connect("toggled", self.seleccion_grupo2)
                 self.grid.attach_next_to(self.dict["rb20{0}".format(index)], self.progenitor_2, Gtk.PositionType.BOTTOM, 1, 1)
                 self.dict["rb{0}".format(index)].set_tooltip_text(caracteristica)
                 self.dict["rb20{0}".format(index)].set_tooltip_text(caracteristica)
                 self.genotipo1 = [(self.dict["rb{0}".format(index)].get_label()[i:i+2]) for i in range(0, len(self.dict["rb{0}".format(index)].get_label()), 2)]
                 self.genotipo2 = [(self.dict["rb20{0}".format(index)].get_label()[i:i+2]) for i in range(0, len(self.dict["rb20{0}".format(index)].get_label()), 2)]
                 self.label_genotipo1 = self.dict["rb{0}".format(index)].get_label()
                 self.label_genotipo2 = self.dict["rb20{0}".format(index)].get_label()
                 self.nombre_rb1 ="rb{0}".format(index)
                 self.nombre_rb2 = "rb20{0}".format(index)
                 self.dict["rb20{0}".format(index)].set_property("name", "rb20{0}".format(index))
                 self.dict["rb{0}".format(index)].set_property("name", "rb{0}".format(index))
            else:
                 self.dict["rb{0}".format(index)] = Gtk.RadioButton.new_with_mnemonic_from_widget(
                     self.dict["rb0"], genotipos_combinacion[index])
                 self.dict["rb{0}".format(index)].connect("toggled", self.seleccion_grupo1)
                 self.grid.attach_next_to(self.dict["rb{0}".format(index)], self.dict["rb{0}".format(index-1)],
                                          Gtk.PositionType.BOTTOM, 1, 1)
                 self.dict["rb20{0}".format(index)] = Gtk.RadioButton.new_with_mnemonic_from_widget(
                     self.dict["rb200"], genotipos_combinacion[index])
                 self.dict["rb20{0}".format(index)].connect("toggled", self.seleccion_grupo2)
                 self.grid.attach_next_to(self.dict["rb20{0}".format(index)], self.dict["rb20{0}".format(index - 1)],
                                          Gtk.PositionType.BOTTOM, 1, 1)
                 self.dict["rb20{0}".format(index)].set_property("name", "rb20{0}".format(index))
                 self.dict["rb{0}".format(index)].set_property("name", "rb{0}".format(index))
                #agrega variable caracteristica que tiene el fenotipo escrito como tooltip
                 self.dict["rb{0}".format(index)].set_tooltip_text(caracteristica)
                 self.dict["rb20{0}".format(index)].set_tooltip_text(caracteristica)
           #muestra los radio buttons con los genotipos
            self.dict["rb{0}".format(index)].show()
            self.dict["rb20{0}".format(index)].show()

    #variables para almacenar seleccion de radio buttons con genotipos
    genotipo1 = ""
    genotipo2 = ""
    label_genotipo1 = ""
    label_genotipo2 = ""

    nombre_rb1 = ""
    nombre_rb2 = ""
    #obtener string de seleccion de radiobutton progenitor 1
    def seleccion_grupo1(self, widget):
        if widget.get_active():
          self.label_genotipo1 = widget.get_label()
          self.genotipo1 = [(widget.get_label()[i:i+2]) for i in range(0, len(widget.get_label()), 2)]
          self.nombre_rb1 = widget.get_property("name")

    # obtener string de seleccion de radiobutton progenitor 2
    def seleccion_grupo2(self, widget):
        if widget.get_active():
            self.label_genotipo2 = widget.get_label()
            self.genotipo2 = [(widget.get_label()[i:i+2]) for i in range(0, len(widget.get_label()), 2)]
            self.nombre_rb2 = widget.get_property("name")

    #variable que indica si se debe colorear cruce por genotipo o no
    color_por_genotipo = True

    # saber si se elige color por fenotipo
    def on_rb_colorear_fenotipo_toggled(self, widget):
       if widget.get_active():
            self.color_por_genotipo = False
            self.on_cruce_btn_clicked(self.btn_cruce)


     # saber si se elige color por genotipo
    def on_rb_colorear_genotipo_toggled(self, widget):
        if widget.get_active():
            self.color_por_genotipo = True
            self.on_cruce_btn_clicked(self.btn_cruce)

    #genera colores al azar
    def generar_color(self):
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        return color

    porcentaje_fenotipos = "Fenotipos:\n\n"
    porcentajes_genotipos = "Genotipos:\n\n"
    #boton de cruce, genera cruce de los genotipos de progenitores seleccionados
    def on_cruce_btn_clicked(self, widget):

        #remueve el treeview
        for columna in self.treeview.get_columns():
            self.treeview.remove_column(columna)

        #valida que haya genotipos seleccionados
        if self.label_genotipo1 == "":
            self.error("Debe seleccionar dos genotipos para cruzar")
            return

        self.borrar_text_view()

        #pone una etiqueta que muestra los genotipos que se estan cruzando
        self.label_cruce.set_text("Cruce de "+self.label_genotipo1 + "   x   "+ self.label_genotipo2)
        self.label_cruce.set_visible(True)

        self.porcentaje_fenotipos ="Fenotipos:\n\n"
        self.porcentajes_genotipos ="Genotipos:\n\n"

        # obtiene combinaciones para hacer los cruces
        genotipos_cruce1 = list(map("".join, product(*self.genotipo1)))
        genotipos_cruce2 = list(map("".join, product(*self.genotipo2)))

        #hace el cruce
        resultado_cruce = list(map("".join, product(genotipos_cruce2, genotipos_cruce1)))

        #obtiene todos los resultados unicos del cruce
        set_individuales = set(resultado_cruce)

        #porcentaje de elementos
        diccionarioGeno = {}
        for genot in set_individuales:
            diccionarioGeno[genot]= (resultado_cruce.count(genot)/len(resultado_cruce))*100
        diccionarioGeno = {k: v for k, v in sorted(diccionarioGeno.items(), key=lambda item: item[1], reverse=True)}

        #ordenado de mayor a menor
        for key, value in diccionarioGeno.items():
            self.porcentajes_genotipos = self.porcentajes_genotipos + key + " :" \
                                        + str(round(value,2)) + "%\n"

        #asinga un color a cada genotipo unico del cruce y lo coloca en un diccionario asociando color a genotipo
        coloresGenotipo = {}
        for elemento in set_individuales:
            coloresGenotipo[elemento] = self.generar_color()

        #obtiene los fenotipos
        fenotipos = list()
        set_fenotipos = set()
        for index, val in enumerate(resultado_cruce):
            #con el diccionario que contenia las descripciones de los fenotipos se va a determinar el fenotipo de cada elemnto del cruce
            caracteristica = ""
            for key, val in self.caract_genotipos.items():
                #si tiene mayuscula una letra se agrega ese fenotipo a esa caracteristica,
                if key in resultado_cruce[index]:
                    if key.isupper():
                        caracteristica += "  " + val
                        #se crea un objeto de tipo fenotipo que va a guardar el genotipo asociado al fenotipo y el fenotipo,
                        # tambien se agregan cracteristicas el set de fenotipos para tener fenotipos unicos
                        fenotipo = Fenotipo()
                        fenotipo.genotipo = resultado_cruce[index]
                    elif resultado_cruce[index].count(key)==2:
                        caracteristica += "  " + val
                        fenotipo = Fenotipo()
                        fenotipo.genotipo = resultado_cruce[index]
            set_fenotipos.add(caracteristica)
            fenotipo.fenotipo = caracteristica
            fenotipos.append(fenotipo)
        #se asocian colores a cada fenotipo unico con un diccionario
        coloresFenotipo={}
        totalFenotipos = list()
        for elemento in set_fenotipos:
            coloresFenotipo[elemento] = self.generar_color()
            # a cada objeto fenotipo se le agrega el color dependiendo del color del fenotipo
            for element in fenotipos:
                totalFenotipos.append(element.fenotipo)
                if element.fenotipo == elemento:
                    element.color = coloresFenotipo.get(elemento)


        #porcentaje de fentotipos
        diccionario={}
        for fenot in set_fenotipos:
            diccionario[fenot]= (totalFenotipos.count(fenot) / len(totalFenotipos))*100
        diccionario = {k: v for k, v in sorted(diccionario.items(), key=lambda item: item[1], reverse=True)}

        #ordenado de mayor a menor
        for key, value in diccionario.items():
            self.porcentaje_fenotipos = self.porcentaje_fenotipos + key + " :" \
                                        + str(round(value,2)) + "%\n"

        #se agregan los colores de genotipo y fenotipo a cada resultado del cruce
        i = 1
        colores = 0
        while i <len(resultado_cruce):
            resultado_cruce.insert(i, coloresGenotipo[resultado_cruce[colores]])
            for elemento in fenotipos:
                if (elemento.genotipo == resultado_cruce[colores]):
                    resultado_cruce.insert(i+1, elemento.color)
                    break
            i += 3
            colores=colores+3
        resultado_cruce.append(coloresGenotipo[resultado_cruce[-1]])
        for elemento in fenotipos:
            if (elemento.genotipo == resultado_cruce[-2]):
                resultado_cruce.append(elemento.color)
                break

        #divide el resultado del cruce en las filas que van en el treeview
        resultado_cruce = list(resultado_cruce[i: i+ (len(genotipos_cruce1) + (len(genotipos_cruce1)*2))]
                               for i in range(0, len(resultado_cruce), (len(genotipos_cruce1) + (len(genotipos_cruce1)*2))))

        #agrega las etiquetas que van en la parte izquierda del treeview
        tamanio = 0
        for i in resultado_cruce:
            i.insert(0, genotipos_cruce2[tamanio])
            tamanio += 1


        #prepara datos para ingresarlos al treeview creando una liststore
        tam = 3 * len(genotipos_cruce1) + 1
        liststore = Gtk.ListStore(*[str]*tam)
        for row in resultado_cruce:
            liststore.append(row)

        #agrega el modelo al treeview
        self.treeview.set_model(liststore)

        #agrega primera columna al treeview que tiene las etiquetas de la parte izquierda
        renderer = Gtk.CellRendererText()
        renderer.set_property("cell-background", "#E0E0E0")
        columna = Gtk.TreeViewColumn("", renderer, text=0)
        self.treeview.append_column(columna)
        texto = 1

        #dependiendo de si se elige colorear por genotipo o fenotipo, el valor de color va a cambiar para elegir el color asociado
        if self.color_por_genotipo:
            color = 2
        else:
            color = 3

        #agrega el resto de columnas al treeview
        for i in range(0, (len(genotipos_cruce1))):
            renderer2 = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(genotipos_cruce1[i], renderer2, text=texto, background=color)
            self.treeview.append_column(columna)
            texto += 3
            color += 3

    file = None
    #guardar los datos en archivo de texto, abre un dialogo filechooser para elegir donde guardar
    def on_btn_save_clicked(self, widget):
        choose = Gtk.FileChooserDialog("Elija la ubicacion para guardar el archivo", parent=None, action=Gtk.FileChooserAction.SAVE )
        choose.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        choose.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT)
        choose.set_do_overwrite_confirmation(True)
        choose.set_modal(True)
        if self.file is not None:
            try:
                choose.set_filename(self.file)
            except:
                ""
        choose.connect("response", self.save_response_cb)
        choose.show()


    def save_response_cb(self, dialog, response_id):
        save_dialog = dialog
        document = Io()
        if response_id == Gtk.ResponseType.ACCEPT:
            self.file = save_dialog.get_current_folder()
            self.file= self.file+"/"+save_dialog.get_current_name()
            lista = list()
            for i in  self.lista_caracteristicas:
                lista.append(i.get_text())
            document.guardar(self.file, lista, str(self.spin.get_value()), str(self.nombre_rb1), str(self.nombre_rb2))
        dialog.destroy()

    def on_btn_load_clicked(self, widget):
        choose = Gtk.FileChooserDialog("Elija el archivo a abrir", parent=None, action=Gtk.FileChooserAction.OPEN )
        choose.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        choose.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT)
        choose.set_local_only(False)
        choose.set_modal(True)
        choose.connect("response", self.load_response_cb)
        choose.show()

    inicio_datos = list()
    def load_response_cb(self, dialog, response_id):
        open_dialog = dialog
        document = Io()
        if response_id == Gtk.ResponseType.ACCEPT:
            self.file = open_dialog.get_filename()
            try:
             self.inicio_datos = document.load(self.file)
             self.cargar_datos(self.inicio_datos)
            except:
               ""
        dialog.destroy()

    def cargar_datos(self, lista):
        i = 0

        self.caracteristicas_por_defecto()
        # borrar genotipos de la lista
        while True:
            if self.grid.get_child_at(0, 1) != None:
                self.grid.remove_row(1)
            else:
                break
        # borrar resultados de cruce
        for columna in self.treeview.get_columns():
            self.treeview.remove_column(columna)

        # oculta label de cruce
        self.label_cruce.set_visible(False)

        #crea valores de caracteristicas guardados en el documento
        for i , value in enumerate(self.lista_caracteristicas):
            if(lista[2][i]=='\n'):
                value.set_text("")
            else:
                value.set_text(lista[2][i].rstrip('\n'))
        #asigna valor del spin para ver cuantas caracteristicas son visiles
        self.spin.set_value(int(float(lista[0][0].strip('\n'))))

        #ejecuta el boton para generar cruces
        self.btn_generar_prog.emit("clicked")

        if(lista[1][0].rstrip('\n')!= ""):
            for row in self.grid.get_children():
                if row.get_name() == lista[1][0].rstrip('\n'):
                    radio_b1 = row
                if row.get_name() == lista[1][1].rstrip('\n'):
                    radio_b2 = row
            radio_b1.set_active(True)
            radio_b2.set_active(True)
            radio_b1.emit("toggled")
            radio_b2.emit("toggled")
            self.btn_cruce.emit("clicked")



    #texto que muestra porcentajes de genotipos y fenotipos en textview
    def on_btn_porcentajes_clicked(self,widget):
        self.borrar_text_view()
        buffer = self.text_view1.get_buffer()
        buffer2 = self.text_view2.get_buffer()
        self.text_view1.get_buffer().insert(buffer.get_start_iter(),self.porcentajes_genotipos)
        self.text_view2.get_buffer().insert(buffer2.get_start_iter(),self.porcentaje_fenotipos)


    def borrar_text_view(self):
        buffer = self.text_view1.get_buffer()
        buffer2 = self.text_view2.get_buffer()
        buffer.delete(
            buffer.get_start_iter(),
            buffer.get_end_iter())
        buffer2.delete(
            buffer2.get_start_iter(),
            buffer2.get_end_iter())

main = Main()
Gtk.main()
