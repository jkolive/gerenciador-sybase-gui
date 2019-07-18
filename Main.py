import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Main(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        builder = Gtk.Builder()
        builder.add_from_file('App.glade')
        self.dialog = builder.get_object('about_dialog')

        self.name_file = ''
        self.name_dir = ''

        self.list_store = builder.get_object('list_store')
        self.list_store.append([False, self.name_dir, self.name_file])
        self.treeview = builder.get_object('treeView')

        self.txt_nome_servidor = builder.get_object('txt_nome_servidor')
        self.txt_nome_servidor.set_placeholder_text('Ex. srvlinux, srvcontabil')

        self.txt_mem_cache = builder.get_object('txt_mem_cache')
        self.txt_mem_cache.set_placeholder_text('Informe em MB')

        self.txt_param_rede = builder.get_object('txt_param_rede')
        self.txt_param_servidor = builder.get_object('txt_param_servidor')
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

        builder.connect_signals(self)
        self.window = builder.get_object("window_main")
        self.window.show_all()

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
            print("Cancel clicked")

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

        if count > 1:
            pass
        else:
            self.list_store.set_value(self.list_store[0].iter, 0, False)
            self.list_store.set_value(self.list_store[0].iter, 1, '')
            self.list_store.set_value(self.list_store[0].iter, 2, '')

            self.txt_nome_servidor.set_sensitive(True)
            self.txt_mem_cache.set_sensitive(True)
            self.btn_incluir.set_sensitive(True)
            self.btn_gravar.set_sensitive(True)

    def on_btn_iniciar_clicked(self, button):
        if not self.btn_gravar.get_sensitive():
            self.btn_parar.set_sensitive(True)
            self.btn_iniciar.set_sensitive(False)
        else:
            pass

    def on_btn_parar_clicked(self, buttoon):
        self.btn_iniciar.set_sensitive(True)
        self.btn_parar.set_sensitive(False)
        self.txt_nome_servidor.set_sensitive(True)
        self.txt_mem_cache.set_sensitive(True)
        self.btn_gravar.set_sensitive(True)

    def on_btn_gravar_clicked(self, button):
        if self.txt_nome_servidor.get_text() == '' \
                or self.txt_mem_cache.get_text() == '' \
                or self.list_store[self.list_store[0].iter][1] == '' \
                or self.list_store[self.list_store[0].iter][2] == '':

            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, 'INFORMAÇÃO IMPORTANTE')
            dialog.format_secondary_text(
                'Campos necessários ainda não preenchidos!')
            dialog.run()

            dialog.destroy()
        else:
            self.txt_nome_servidor.set_sensitive(False)
            self.txt_mem_cache.set_sensitive(False)
            self.btn_gravar.set_sensitive(False)

    def on_btn_fechar_clicked(self, button):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "INFORMAÇÃO IMPORTANTE")
        dialog.format_secondary_text("O sistema ficará executando em segundo plano.")
        dialog.run()

        dialog.destroy()

    def on_window_main_destroy(self, widget):
        Gtk.main_quit(self)


if __name__ == "__main__":
    Main()
    Gtk.main()
