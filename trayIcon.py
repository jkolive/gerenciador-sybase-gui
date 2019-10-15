#!/usr/bin/env python3

import main
import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import run
from time import time


class TrayIcon(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.APPIND = 1
        try:
            gi.require_version('AppIndicator3', '0.1')
            from gi.repository import AppIndicator3
        except ImportError:
            self.APPIND = 0
        if self.APPIND == 1:
            timestamp = time()
            self.indicator = AppIndicator3.Indicator.new(f"_id_{timestamp}", sys.path[0] + '/images/app-gerenciador.png',
                                                         AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.active = AppIndicator3.IndicatorStatus.ACTIVE
            self.passive = AppIndicator3.IndicatorStatus.PASSIVE
            self.indicator.set_status(self.active)
            self.indicator.set_title('Gerencidor Sybase')
            self.indicator.set_menu(self.add_menu_indicator())
            Gtk.main()

        else:
            self.statusIcon = Gtk.StatusIcon()
            self.statusIcon.set_from_file(sys.path[0] + '/images/trayicon/app-gerenciador.png')
            self.statusIcon.set_tooltip_text('Gerenciador Sybase')
            self.statusIcon.connect('popup-menu', self.on_right_click)

    def add_menu_indicator(self):
        menu = Gtk.Menu()
        miApp = Gtk.MenuItem()
        miApp.set_label('Abri Gerenciador')
        miApp.connect('activate', self.show_app)
        menu.append(miApp)

        miExit = Gtk.MenuItem()
        miExit.set_label('Sair')
        miExit.connect('activate', self.close_app)
        menu.append(miExit)

        menu.show_all()
        return menu

    def on_right_click(self, icon, button, time_active):
        menu = Gtk.Menu()
        miApp = Gtk.MenuItem()
        miApp.set_label('Abri Gerenciador')
        miApp.connect('activate', self.show_app)
        menu.append(miApp)

        miExit = Gtk.MenuItem()
        miExit.set_label('Sair')
        miExit.connect('activate', self.close_app)
        menu.append(miExit)

        menu.show_all()
        menu.popup(None, None, None, self.statusIcon, button, time_active)

    def show_app(self, *args):
        if self.APPIND == 0:
            self.statusIcon.set_visible(False)
        self.indicator.set_status(self.passive)
        main.Main()

    def close_app(self, *args):
        cmd = run('pidof -s dbsrv16', shell=True)
        if cmd.returncode == 0:
            dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                       buttons=Gtk.ButtonsType.YES_NO, text='ATENÇÃO!')
            dialog.format_secondary_text('Banco de Dados ainda em execução! Deseja parar o Banco de dados?')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.YES:
                run('killall -w -s 15 dbsrv16', shell=True)
                raise SystemExit()

            if response == Gtk.ResponseType.NO:
                dialog.destroy()

        raise SystemExit()


if __name__ == '__main__':
    TryIcon()
