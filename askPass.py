#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import *
import os


class AskPass(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        # Builder Glade
        builder = Gtk.Builder()
        builder.add_from_file('layout/askPass.glade')

        # Try passwords
        self.cont = 0

        # Widgets
        """ Entry """
        self.entry_senha = Gtk.Entry()
        self.entry_senha = builder.get_object('entry_senha')
        """ Label """
        self.lbl_informe_senha = Gtk.Label()
        self.lbl_informe_senha = builder.get_object('lbl_informe_senha')
        self.lbl_try_passwd = builder.get_object('lbl_try_passwd')

        # Signals
        builder.connect_signals(self)

        # Show Window Main
        self.window = builder.get_object('win_askpass')
        self.window.show()

    # Methods
    def on_btn_confirmar_clicked(self, *args):
        # usermod –aG wheel {getpass.getuser()} # Add user sudores CentOS
        os.environ['ENTRY_PASS'] = self.entry_senha.get_text()
        cmd_pass = run(f'echo {os.environ["ENTRY_PASS"]} | sudo -k -S touch /root/sybase.log > /dev/null 2>&1', shell=True)
        if cmd_pass.returncode == 0:
            self.window.hide()
        if cmd_pass.returncode == 1:
            self.cont += 1
            self.lbl_try_passwd.set_text(f'Senha incorreta! 0{self.cont}/03')
            self.entry_senha.set_text('')
            if self.cont == 3:
                Gtk.main_quit()
        if cmd_pass.returncode == 126:
            self.lbl_try_passwd.set_text('Usuário sem permissão para execução')
            self.entry_senha.set_text('')

    def on_entry_senha_activate(self, *args):
        self.on_btn_confirmar_clicked()

    def on_win_askpass_delete_event(self, *args):
        self.window.hide()

    def on_btn_cancelar_clicked(self, *args):
        Gtk.main_quit()


if __name__ == '__main__':
    AskPass()
    Gtk.main()
