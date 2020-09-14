import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from itertools import product
import random
from Fenotipo import Fenotipo


class Main:
    def __init__(self):
        #cargar glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Main.glade")
        self.builder.connect_signals(self)

        #objeto ventanda
        self.window = self.builder.get_object("Window")

        #objeto spin button para cambiar cuantas caracteristicas hay
        self.spin = self.builder.get_object("spinButton")

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

    caract_genotipos = {}
    def on_btn_generar_prog_clicked(self, button):

        #borrar genotipos de la lista
        while True:
            if self.grid.get_child_at(0,1)!=None:
                self.grid.remove_row(1)
            else:
                break

        for columna in self.treeview.get_columns():
            self.treeview.remove_column(columna)


        self.label_cruce.set_visible(False)



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
        dict = {}
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
                 dict["rb{0}".format(index)] = Gtk.RadioButton(label=genotipos_combinacion[index])
                 dict["rb{0}".format(index)].connect("toggled", self.seleccion_grupo1)
                 self.grid.attach_next_to(dict["rb{0}".format(index)], self.progenitor_1, Gtk.PositionType.BOTTOM, 1, 1)
                 dict["rb2{0}".format(index)] = Gtk.RadioButton(label=genotipos_combinacion[index])
                 dict["rb2{0}".format(index)].connect("toggled", self.seleccion_grupo2)
                 self.grid.attach_next_to(dict["rb2{0}".format(index)], self.progenitor_2, Gtk.PositionType.BOTTOM, 1, 1)
                 dict["rb{0}".format(index)].set_tooltip_text(caracteristica)
                 dict["rb2{0}".format(index)].set_tooltip_text(caracteristica)
                 self.genotipo1 = [(dict["rb{0}".format(index)].get_label()[i:i+2]) for i in range(0, len(dict["rb{0}".format(index)].get_label()), 2)]
                 self.genotipo2 = [(dict["rb2{0}".format(index)].get_label()[i:i+2]) for i in range(0, len(dict["rb2{0}".format(index)].get_label()), 2)]
                 self.label_genotipo1 = dict["rb{0}".format(index)].get_label()
                 self.label_genotipo2 = dict["rb2{0}".format(index)].get_label()
            else:
                 dict["rb{0}".format(index)] = Gtk.RadioButton.new_with_mnemonic_from_widget(
                     dict["rb0"], genotipos_combinacion[index])
                 dict["rb{0}".format(index)].connect("toggled", self.seleccion_grupo1)
                 self.grid.attach_next_to(dict["rb{0}".format(index)], dict["rb{0}".format(index-1)],
                                          Gtk.PositionType.BOTTOM, 1, 1)
                 dict["rb2{0}".format(index)] = Gtk.RadioButton.new_with_mnemonic_from_widget(
                     dict["rb20"], genotipos_combinacion[index])
                 dict["rb2{0}".format(index)].connect("toggled", self.seleccion_grupo2)
                 self.grid.attach_next_to(dict["rb2{0}".format(index)], dict["rb2{0}".format(index - 1)],
                                          Gtk.PositionType.BOTTOM, 1, 1)

                 dict["rb{0}".format(index)].set_tooltip_text(caracteristica)
                 dict["rb2{0}".format(index)].set_tooltip_text(caracteristica)
            dict["rb{0}".format(index)].show()
            dict["rb2{0}".format(index)].show()

    #variables para almacenar seleccion de radio buttons
    genotipo1 = ""
    genotipo2 = ""
    label_genotipo1 = ""
    label_genotipo2 = ""

    #obtener string de seleccion de radiobutton progenitor 1
    def seleccion_grupo1(self, widget):
        if widget.get_active():
          self.label_genotipo1 = widget.get_label()
          self.genotipo1 = [(widget.get_label()[i:i+2]) for i in range(0, len(widget.get_label()), 2)]

    # obtener string de seleccion de radiobutton progenitor 2
    def seleccion_grupo2(self, widget):
        if widget.get_active():
            self.label_genotipo2 = widget.get_label()
            self.genotipo2 = [(widget.get_label()[i:i+2]) for i in range(0, len(widget.get_label()), 2)]

    color_por_genotipo = True
        # saber si se elige color por fenotipo
    def on_rb_colorear_fenotipo_toggled(self, widget):
       for columna in self.treeview.get_columns():
            self.treeview.remove_column(columna)
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

    #boton de cruce, genera cruce de los genotipos de progenitores seleccionados
    def on_cruce_btn_clicked(self, widget):


        for columna in self.treeview.get_columns():
            self.treeview.remove_column(columna)

        if self.label_genotipo1 == "":
            self.error("Debe seleccionar dos genotipos para cruzar")
            return

        self.label_cruce.set_text("Cruce de "+self.label_genotipo1 + "   x   "+ self.label_genotipo2)
        self.label_cruce.set_visible(True)

        # obtiene combinaciones para hacer los cruces
        genotipos_cruce1 = list(map("".join, product(*self.genotipo1)))
        genotipos_cruce2 = list(map("".join, product(*self.genotipo2)))

        #hace el cruce
        resultado_cruce = list(map("".join, product(genotipos_cruce2, genotipos_cruce1)))

        set_individuales = set(resultado_cruce)

        coloresGenotipo = {}
        for elemento in set_individuales:
            coloresGenotipo[elemento] = self.generar_color()

        fenotipos = list()
        set_fenotipos = set()
        for index, val in enumerate(resultado_cruce):
            for key, val in self.caract_genotipos.items():
                caracteristica = ""
                if key in resultado_cruce[index]:
                    if key.isupper():
                        caracteristica += "  " + val
                        fenotipo = Fenotipo()
                        fenotipo.fenotipo = caracteristica
                        set_fenotipos.add(caracteristica)
                        fenotipo.genotipo = resultado_cruce[index]
                        fenotipos.append(fenotipo)
                        break
                    else:
                        caracteristica += "  " + val
                        fenotipo = Fenotipo()
                        fenotipo.fenotipo = caracteristica
                        set_fenotipos.add(caracteristica)
                        fenotipo.genotipo = resultado_cruce[index]
                        fenotipos.append(fenotipo)


        coloresFenotipo={}
        for elemento in set_fenotipos:
            coloresFenotipo[elemento] = self.generar_color()
            for element in fenotipos:
                if element.fenotipo == elemento:
                    element.color = coloresFenotipo.get(elemento)

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

        resultado_cruce = list(resultado_cruce[i: i+ (len(genotipos_cruce1) + (len(genotipos_cruce1)*2))]
                               for i in range(0, len(resultado_cruce), (len(genotipos_cruce1) + (len(genotipos_cruce1)*2))))
        tamanio = 0
        for i in resultado_cruce:
            i.insert(0, genotipos_cruce2[tamanio])
            tamanio += 1


        #prepara datos para ingresarlos al treeview
        tam = 3 * len(genotipos_cruce1) + 1
        liststore = Gtk.ListStore(*[str]*tam)
        for row in resultado_cruce:
            liststore.append(row)

        #agrega el modelo al treeview
        self.treeview.set_model(liststore)

        #agrega columnas al treeview
        renderer = Gtk.CellRendererText()
        renderer.set_property("cell-background", "#E0E0E0")
        columna = Gtk.TreeViewColumn("", renderer, text=0)
        self.treeview.append_column(columna)
        texto = 1
        if self.color_por_genotipo:
            color = 2
        else:
            color = 3
        for i in range(0, (len(genotipos_cruce1))):
            renderer2 = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(genotipos_cruce1[i], renderer2, text=texto, background=color)
            self.treeview.append_column(columna)
            texto += 3
            color += 3







main = Main()
Gtk.main()
