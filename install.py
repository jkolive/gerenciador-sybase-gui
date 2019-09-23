#!/usr/bin/env python3
import os
import sys
if 'linux' not in sys.platform:
    raise Exception('Somente Linux')

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import App
import AskPass


class Install(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        builder = Gtk.Builder()
        builder.add_from_file('layout/Install.glade')
        self.progressbar = builder.get_object('pgb_install')
        self.btn_instalar = builder.get_object('btn_instalar')
        self.btn_abrir = builder.get_object('btn_abrir')
        self.btn_abrir.set_visible(False)

        self.window = builder.get_object('window_install')
        builder.connect_signals(self)
        self.window.show()

    def on_btn_abrir_clicked(self, *args):
        self.window.hide()
        App.Main()

    def on_btn_instalar_clicked(self, *args):
        AskPass.AskPass()

    def on_btn_instalar_enter_notify_event(self, button, event):
        hand1 = Gdk.Cursor(Gdk.CursorType.HAND1)
        button.get_window().set_cursor(hand1)

    def on_btn_abrir_enter_notify_event(self, button, event):
        hand1 = Gdk.Cursor(Gdk.CursorType.HAND1)
        button.get_window().set_cursor(hand1)

    def on_btn_instalar_leave_notify_event(self, button, event):
        arrow = Gdk.Cursor(Gdk.CursorType.ARROW)
        button.get_window().set_cursor(arrow)

    def on_btn_abrir_leave_notify_event(self, button, event):
        arrow = Gdk.Cursor(Gdk.CursorType.ARROW)
        button.get_window().set_cursor(arrow)

    def on_window_install_focus_in_event(self, widget, event):
        if os.path.isdir('/opt/sybase'):
            self.btn_instalar.set_label('Concluido')
            self.btn_instalar.set_sensitive(False)
            self.btn_abrir.set_visible(True)

    def on_btn_instalar_button_press_event(self, *args):
        self.btn_instalar.set_label('Instalando...')

    def on_window_setup_destroy(self, widget):
        Gtk.main_quit(self)


if __name__ == '__main__':
    Install()
    Gtk.main()
