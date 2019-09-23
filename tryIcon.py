""" System Try Icon"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import App


class TryIcon:
    def __init__(self):
        self.menu = Gtk.Menu()
        self.statusIcon = Gtk.StatusIcon()
        self.statusIcon.set_from_file('images/tux.png')
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
        App.Main()

    def close_app(self, *args):
        Gtk.main_quit()


if __name__ == '__main__':
    TryIcon()
