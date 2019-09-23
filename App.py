#!/usr/bin/env python3

import sys
if 'linux' not in sys.platform:
    raise Exception('Somente Linux')

import os
import json
import time
import signal
import subprocess
from subprocess import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import TryIcon


class Main(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        builder = Gtk.Builder()
        builder.add_from_file('layout/App.glade')
        self.dialog = builder.get_object('about_dialog')

        self.name_file = ''
        self.name_dir = ''

        self.list_store = builder.get_object('list_store')
        self.txt_nome_servidor = builder.get_object('txt_nome_servidor')
        self.txt_nome_servidor.set_placeholder_text('Ex. srvlinux, srvcontabil')
        self.txt_mem_cache = builder.get_object('txt_mem_cache')
        self.txt_mem_cache.set_placeholder_text('Informe em MB')
        self.txt_param_rede = builder.get_object('txt_param_rede')
        self.txtbuffer_param_rede = self.txt_param_rede.get_buffer()
        self.txt_param_servidor = builder.get_object('txt_param_servidor')
        self.txtbuffer_param_servidor = self.txt_param_servidor.get_buffer()
        self.rbtn_automatico = builder.get_object('rbtn_automatico')
        self.rbtn_desativado = builder.get_object('rbtn_desativado')

        if os.path.isfile('./.data.json'):
            with open('.data.json') as json_file:
                self.data = json.load(json_file)
                self.txt_nome_servidor.set_text(self.data['banco'][0]['nome_servidor'])
                self.txt_mem_cache.set_text(self.data['banco'][0]['mem_cache'])
                self.txtbuffer_param_rede.set_text(self.data['banco'][0]['param_redes'])
                self.txtbuffer_param_servidor.set_text(self.data['banco'][0]['param_servidor'])
                self.rbtn_automatico.set_active(self.data['banco'][0]['automatico'])
                self.rbtn_desativado.set_active(self.data['banco'][0]['desativado'])
                self.list_store.append([True, self.data['banco'][0]['caminho'], self.data['banco'][0]['nome_arquivo']])
        else:
            self.list_store.append([False, self.name_dir, self.name_file])

        self.treeview = builder.get_object('treeView')

        self.btn_gravar = builder.get_object('btn_gravar')
        self.btn_incluir = builder.get_object('btn_incluir')
        self.btn_iniciar = builder.get_object('btn_iniciar')
        self.btn_parar = builder.get_object('btn_parar')
        self.btn_parar.set_sensitive(False)

        self.btn_iniciar.connect('clicked', self.on_btn_iniciar_clicked)
        self.btn_parar.connect('clicked', self.on_btn_parar_clicked)
        btn_incluir = Gtk.Button()
        btn_incluir.connect("clicked", self.on_btn_incluir_clicked)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cbox_db_toggled)

        column_toggle = Gtk.TreeViewColumn("#", renderer_toggle, active=0)
        self.treeview.append_column(column_toggle)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Caminho", renderer_text, text=1)
        self.treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Nome", renderer_text, text=2)
        self.treeview.append_column(column_text)

        init_cmd = run('pidof -s dbsrv16', shell=True)
        if init_cmd.returncode == 0:
            self.txt_nome_servidor.set_sensitive(False)
            self.txt_mem_cache.set_sensitive(False)
            self.btn_gravar.set_sensitive(False)
            self.btn_parar.set_sensitive(True)
            self.btn_iniciar.set_sensitive(False)

        builder.connect_signals(self)
        self.window = builder.get_object("window_main")
        self.window.show_all()

    def on_txt_mem_cache_changed(self, button):
        if self.txt_mem_cache.get_text().isalpha():
            self.txt_mem_cache.set_text('')

    def on_cbox_db_toggled(self, widget, path):
        self.list_store[path][0] = not self.list_store[path][0]

    def on_btn_incluir_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Localize o banco de dados", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)
        dialog.set_transient_for(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.name_file = os.path.basename(path)
            self.name_dir = os.path.dirname(path)

            self.list_store.set_value(self.list_store[0].iter, 0, True)
            self.list_store.set_value(self.list_store[0].iter, 1, self.name_dir)
            self.list_store.set_value(self.list_store[0].iter, 2, self.name_file)

        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def add_filters(self, dialog):
        filter_file = Gtk.FileFilter()
        filter_file.set_name("Arquivos *.db")
        filter_file.add_pattern("*.db")
        dialog.add_filter(filter_file)

    def on_about_activate(self, *args):
        self.dialog.run()

    def on_about_dialog_response(self, *args):
        self.dialog.hide()

    def on_btn_excluir_clicked(self, button):
        count = len(self.list_store)
        if not self.btn_iniciar.get_sensitive():
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO')
            dialog.format_secondary_text('Necessário parar o banco de dados!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            return True

        elif count > 1:
            pass
        else:
            try:
                os.remove('.data.json')

                self.txt_nome_servidor.set_text('')
                self.txt_mem_cache.set_text('')
                self.txtbuffer_param_rede.set_text('')
                self.txtbuffer_param_servidor.set_text('')
                self.list_store.set_value(self.list_store[0].iter, 0, False)
                self.list_store.set_value(self.list_store[0].iter, 1, '')
                self.list_store.set_value(self.list_store[0].iter, 2, '')

                self.txt_nome_servidor.set_sensitive(True)
                self.txt_mem_cache.set_sensitive(True)
                self.btn_incluir.set_sensitive(True)
                self.btn_gravar.set_sensitive(True)

            except Exception as erro:
                print(f'Banco não encontrado!', erro)

    def on_btn_iniciar_clicked(self, button):
        if self.btn_gravar.get_sensitive():
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO')
            dialog.format_secondary_text('Necessário gravar as informações antes de inicializar o banco!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            return True
        else:
            try:
                self.cmd_iniciar()

            except Exception as erro:
                print(erro)

    def cmd_iniciar(self):
        caminho = self.data['banco'][0]['caminho']
        nome_arquivo = self.data['banco'][0]['nome_arquivo']
        run([f"mkdir -p '{caminho}'/log"], shell=True)
        run([f"touch '{caminho}/log/logservidor.txt'"], shell=True)
        os.environ['SYBHOME'] = "/opt/sybase/SYBSsa16"
        os.environ['PATH'] = os.environ['PATH'] + ":" + os.environ['SYBHOME'] + "/bin64"
        os.environ['LD_LIBRARY_PATH'] = os.environ['SYBHOME'] + "/lib64"
        cmd = f"dbsrv16 -c {self.txt_mem_cache.get_text()}M -n {self.txt_nome_servidor.get_text()} " \
            f"-ud -o '{caminho}/log/logservidor.txt' '{caminho}/{nome_arquivo}'"
        process = run([cmd], shell=True, executable='/bin/bash')

        if process.returncode == 0:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO')
            dialog.format_secondary_text('Banco de dados inicializado com sucesso!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()
            self.btn_parar.set_sensitive(True)
            self.btn_iniciar.set_sensitive(False)
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            return True

        elif process.returncode == 21:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO')
            dialog.format_secondary_text('Banco de Dados já inicializado!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            return True

        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.OK, 'ATENÇÃO')
            dialog.format_secondary_text('Não foi possível iniciar o Banco de dados!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            return True

    def get_pid(self, name):
        return int(check_output(['pidof', '-s', name]))

    def on_btn_parar_clicked(self, buttoon):
        pid = self.get_pid('dbsrv16')
        cmd_final = run(f'kill {pid}', shell=True)
        time.sleep(3)
        if cmd_final.returncode == 0:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO')
            dialog.format_secondary_text('Banco de dados parado com sucesso!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
                self.btn_iniciar.set_sensitive(True)
                self.btn_parar.set_sensitive(False)
                self.txt_nome_servidor.set_sensitive(True)
                self.txt_mem_cache.set_sensitive(True)
                self.btn_gravar.set_sensitive(True)
            return True
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                       Gtk.ButtonsType.OK, 'ATENÇÃO')
            dialog.format_secondary_text('Não foi possível parar o banco de dados!')
            dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            return True

    def on_btn_gravar_clicked(self, button):
        if self.txt_nome_servidor.get_text() == '' \
                or self.txt_mem_cache.get_text() == '' \
                or self.list_store[self.list_store[0].iter][1] == '' \
                or self.list_store[self.list_store[0].iter][2] == '':

            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO')
            dialog.format_secondary_text(
                'Campos necessários ainda não preenchidos!')
            dialog.run()

            dialog.destroy()
        else:
            self.save_data()
            self.txt_nome_servidor.set_sensitive(False)
            self.txt_mem_cache.set_sensitive(False)
            self.btn_gravar.set_sensitive(False)

    def save_data(self):
        data = {'banco': []}
        data['banco'].append({
            'nome_servidor': self.txt_nome_servidor.get_text(),
            'mem_cache': self.txt_mem_cache.get_text(),
            'param_redes': self.txtbuffer_param_rede.get_text(self.txtbuffer_param_rede.get_start_iter(),
                                                              self.txtbuffer_param_rede.get_end_iter(),
                                                              False),
            'param_servidor': self.txtbuffer_param_servidor.get_text(self.txtbuffer_param_servidor.get_start_iter(),
                                                                     self.txtbuffer_param_servidor.get_end_iter(),
                                                                     False),
            'automatico': self.rbtn_automatico.get_active(),
            'desativado': self.rbtn_desativado.get_active(),
            'caminho': self.list_store[self.list_store[0].iter][1],
            'nome_arquivo': self.list_store[self.list_store[0].iter][2]
        })
        with open('.data.json', 'w') as outfile:
            json.dump(data, outfile)

    def on_btn_fechar_clicked(self, button):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK_CANCEL, "Fechar Aplicativo")
        dialog.format_secondary_text("O sistema ficará minimizado na área de notificação.")
        dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            # raise SystemExit()
            self.window.hide()
            TryIcon.TryIcon()
        if response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def on_window_main_delete_event(self, *args):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO, 'Fechar Aplicativo')
        dialog.format_secondary_text("O sistema ficará minimizado na área de notificação.")
        dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            self.window.hide()
            TryIcon.TryIcon()

        return True


if __name__ == "__main__":
    Main()
    Gtk.main()
