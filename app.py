#!/usr/bin/env python3

import sys
import gi
from main import Main
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id='br.com.opensourcesolution.app_gerenciador',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.main()

    def main(self):
        Gtk.ApplicationWindow(application=self)
        Main()


if __name__ == '__main__':
    app = App()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
