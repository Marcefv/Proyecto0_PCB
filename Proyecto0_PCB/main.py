import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from itertools import combinations, product


class Main:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Main.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Window")
        self.spin = self.builder.get_object("spinButton")
        self.btn_generar_prog = self.builder.get_object("btn_generar_prog")
        self.lista_caracteristicas = list()
        self.box_progenitores = self.builder.get_object("progFrame")
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
        self.grid = self.builder.get_object("grid")
        self.progenitor_1 = self.builder.get_object("progenitor_1")
        self.progenitor_2 = self.builder.get_object("progenitor_2")
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


    def on_btn_generar_prog_clicked(self, button):

        #borrar genotipos de la lista
        while True:
            if self.grid.get_child_at(0,1)!=None:
                self.grid.remove_row(1)
            else:
                break

        caract_genotipos = set()
        list_genotipos =list()
        genotipos_combinacion = set()

        #validaciones de los campos y generar lista de caracteristicas
        for index, widget in enumerate(self.lista_caracteristicas):
            # determinar cual informacion validadr dependiendo de si es visible o no
            if widget.get_visible():
                # para las etiquetas o nombres de caracteristica
                if "lab" in Gtk.Buildable.get_name(widget):
                    caract_genotipos.add(widget.get_text().upper())
                    # determina si es solo texto y si no manda un mensaje de error y devuelve las etiquetas a los valores por defecto
                    # esto tambien valida si el campo esta vacio
                    if not widget.get_text().isalpha():
                        self.error("Solo puede colocar Caracteres alfabeticos\n\nNo puede dejar espacios vacios")
                        self.caracteristicas_por_defecto()
                        caract_genotipos.clear()
                        break
                    # valida si hay nombres repetidos, si es asi muestra mensaje de advertencia y vuelve a valores por defecto
                    elif len(set(self.lista_caracteristicas)) != len(self.lista_caracteristicas):
                        self.error("No puede haber nombres de caracteristicas repetidos")
                        self.caracteristicas_por_defecto()
                        caract_genotipos.clear()
                        break

                # si es una descripcion, se valida si esta vacio, si esta vacio se muestra un mensaje de error
                else:
                    if widget.get_text().strip() == "":
                        self.error("No puede dejar espacios vacios")
                        caract_genotipos.clear()
                        break

        for v in caract_genotipos:
            print(v)
        #lista con combinaciones por caracteristica
        for value in caract_genotipos:
            list_genotipos.append(value + value)
            list_genotipos.append(value + value.lower())
            list_genotipos.append(value.lower() + value.lower())

        #lista de combinaciones entre caracteristicas
        genotipos_combinacion = list_genotipos
        if len(caract_genotipos) == 2:
            genotipos_combinacion = list(map("".join, product(list_genotipos[0:3], list_genotipos[3:6])))
        elif len(caract_genotipos) == 3:
            genotipos_combinacion = list(map("".join, product(list_genotipos[0:3], list_genotipos[3:6], list_genotipos[6:9])))
        elif len(caract_genotipos) == 4:
            genotipos_combinacion = list(map("".join, product(list_genotipos[0:3], list_genotipos[3:6], list_genotipos[6:9], list_genotipos[9:13])))

        #agregar los genotipos a la pantalla de genotipos
        dict = {}
        for index, value in enumerate(genotipos_combinacion):
             if index == 0:
                 dict["rb{0}".format(index)] = Gtk.RadioButton(label=genotipos_combinacion[index])
                 dict["rb{0}".format(index)].connect("toggled", self.toggled_cb)
                 self.grid.attach_next_to(dict["rb{0}".format(index)], self.progenitor_1, Gtk.PositionType.BOTTOM, 1, 1)
                 dict["rb2{0}".format(index)] = Gtk.RadioButton(label=genotipos_combinacion[index])
                 dict["rb2{0}".format(index)].connect("toggled", self.toggled_cb)
                 self.grid.attach_next_to(dict["rb2{0}".format(index)], self.progenitor_2, Gtk.PositionType.BOTTOM, 1, 1)
             else:
                 dict["rb{0}".format(index)] = Gtk.RadioButton.new_with_mnemonic_from_widget(
                     dict["rb0"], genotipos_combinacion[index])
                 dict["rb{0}".format(index)].connect("toggled", self.toggled_cb)
                 self.grid.attach_next_to(dict["rb{0}".format(index)], dict["rb{0}".format(index-1)],
                                          Gtk.PositionType.BOTTOM, 1, 1)
                 dict["rb2{0}".format(index)] = Gtk.RadioButton.new_with_mnemonic_from_widget(
                     dict["rb20"], genotipos_combinacion[index])
                 dict["rb2{0}".format(index)].connect("toggled", self.toggled_cb)
                 self.grid.attach_next_to(dict["rb2{0}".format(index)], dict["rb2{0}".format(index - 1)],
                                          Gtk.PositionType.BOTTOM, 1, 1)
             dict["rb{0}".format(index)].show()
             dict["rb2{0}".format(index)].show()

    def toggled_cb(self, button):
        state = ""
        if button.get_active():
            state = "on"
main = Main()
Gtk.main()
