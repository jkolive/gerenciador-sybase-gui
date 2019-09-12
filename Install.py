#!/usr/bin/env python3

import sys
if 'linux' not in sys.platform:
    raise Exception('Somente Linux')

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from subprocess import *


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
        cmd = run('./App.py&', shell=True)
        if cmd.returncode == 0:
            raise SystemExit()

    def on_btn_instalar_clicked(self, *args):
        self.install()

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

    def on_btn_instalar_button_press_event(self, *args):
        self.btn_instalar.set_label('Instalando...')

    def install(self):
        run('./AskPass.py; chmod +x ./Install.sh', shell=True)
        cmd_pass = run('cat /tmp/pass | sudo -S ./Install.sh > /dev/null 2>&1', shell=True)
        print(cmd_pass.returncode)
        while cmd_pass.returncode != 0:
            run('./AskPass.py', shell=True)
            cmd_pass = run('cat /tmp/pass | sudo -S ./Install.sh > /dev/null 2>&1', shell=True)
            if cmd_pass.returncode == 1:
                print('Senha incorreta, tente novamente')
            elif cmd_pass.returncode == 0:
                print('Parabéns')
        raise SystemExit
        cmd_permissao = run('pkexec install -o $USER -d /opt/sybase', shell=True)
        # sudo -A /usr/bin/ssh-askpass
        if cmd_permissao.returncode == 0:
            cmd_down = run(
                'cd /tmp; wget -c http://download.dominiosistemas.com.br/instalacao/diversos/sybase16_linux_64/'
                'ASA-1600-2747-Linux-64.tar.gz > /dev/null 2>&1', shell=True)

            if cmd_down.returncode == 0:
                run('tar -xvf /tmp/ASA-1600-2747-Linux-64.tar.gz -C /opt/sybase --strip-components=1 > /dev/null 2>&1',
                    shell=True)
                self.btn_instalar.set_label('Concluído')
                self.btn_instalar.set_sensitive(False)
                self.btn_abrir.set_visible(True)
            elif cmd_permissao.returncode == 126:
                print('Usuário sem permissão para execução')
                self.btn_instalar.set_label('Instalar')

        elif cmd_permissao.returncode != 0:
            print('Não foi possível realizar a instalação, verifique sua conexão com a internet')
            self.btn_instalar.set_label('Instalar')

    def on_window_setup_destroy(self, widget):
        Gtk.main_quit(self)


if __name__ == '__main__':
    Install()
    Gtk.main()
