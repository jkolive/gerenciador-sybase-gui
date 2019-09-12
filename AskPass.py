#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import *


class AskPass(Gtk.Window):
    def __init__(self, passwd=''):
        Gtk.Window.__init__(self)

        # Builder Glade
        builder = Gtk.Builder()
        builder.add_from_file('layout/AskPass.glade')

        # Widgets
        self.entry_senha = Gtk.Entry()
        self.entry_senha = builder.get_object('entry_senha')

        self.passwd = passwd

        # Signals
        builder.connect_signals(self)

        # Show Window Main
        self.window = builder.get_object('win_askpass')
        self.window.show()

    # Metodos
    def on_btn_confirmar_clicked(self, *args):
        self.passwd = self.entry_senha.get_text()
        run(f'echo {self.passwd} > /tmp/pass', shell=True)
        Gtk.main_quit(self)

    def on_win_askpass_destroy(self, *args):
        Gtk.main_quit(self)

    def on_btn_cancelar_clicked(self, *args):
        Gtk.main_quit(self)


if __name__ == '__main__':
    AskPass()
    Gtk.main()

