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

        btn_file = Gtk.Button()
        btn_file.connect("clicked", self.on_btn_file_clicked)

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

    def on_btn_file_clicked(self, button):
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

    def on_about_activate(self, button):
        self.dialog.show()

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

    def on_btn_fechar_clicked(self, button):
        Gtk.main_quit(self)

    def on_window_main_destroy(self, widget):
        Gtk.main_quit(self)


if __name__ == "__main__":
    Main()
    Gtk.main()
