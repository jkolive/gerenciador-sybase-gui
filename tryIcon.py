#!/usr/bin/env python3

import app
import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import run


class TryIcon(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.menu = Gtk.Menu()
        self.statusIcon = Gtk.StatusIcon()
        self.statusIcon.set_from_file(sys.path[0] + '/images/app-gerenciador.png')
        self.statusIcon.set_tooltip_text('Gerenciador Sybase')
        self.statusIcon.connect('popup-menu', self.on_right_click)
        # print(dir(self.statusIcon))

    def on_right_click(self, icon, button, time_active):
        miApp = Gtk.MenuItem()
        miApp.set_label('Abri Gerenciador')
        miApp.connect('activate', self.show_app)
        self.menu.append(miApp)

        miExit = Gtk.MenuItem()
        miExit.set_label('Sair')
        miExit.connect('activate', self.close_app)
        self.menu.append(miExit)

        self.menu.show_all()
        self.menu.popup(None, None, None, self.statusIcon, button, time_active)

    def show_app(self, *args):
        self.statusIcon.set_visible(False)
        app.Main()

    def close_app(self, *args):
        cmd = run('pidof -s dbsrv16', shell=True)
        if cmd.returncode == 0:
            dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                       buttons=Gtk.ButtonsType.YES_NO, text='ATENÇÂO!')
            dialog.format_secondary_text('Banco de Dados ainda em execução! Deseja sair e parar o Banco de dados?')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                run('killall -w -s 15 dbsrv16', shell=True)
                Gtk.main_quit()

            if response == Gtk.ResponseType.NO:
                dialog.destroy()

        Gtk.main_quit()


if __name__ == '__main__':
    TryIcon()
