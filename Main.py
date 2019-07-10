import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Main:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('App.glade')

        self.list_store = builder.get_object('list_store')
        self.list_store.append([True, " /home/jackson/Dados", "Contabil.db"])
        self.treeview = builder.get_object('treeView')

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

        builder.connect_signals(Handlers)
        window = builder.get_object("window_main")
        window.show_all()

    def on_cbox_db_toggled(self, widget, path):
        self.list_store[path][0] = not self.list_store[path][0]


def open_file(button):
    dialog = Gtk.FileChooserDialog("Localize o banco de dados", None, Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    add_filters(dialog)

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        print("Open clicked")
        # print("File selected: " + dialog.get_filename())
    elif response == Gtk.ResponseType.CANCEL:
        print("Cancel clicked")

    dialog.destroy()


def add_filters(dialog):
    filter_file = Gtk.FileFilter()
    filter_file.set_name("Arquivos *.db")
    filter_file.add_pattern("*.db")
    dialog.add_filter(filter_file)


Handlers = {
    "on_btn_fechar_clicked": Gtk.main_quit,
    "on_window_main_destroy": Gtk.main_quit,
    "on_btn_file_clicked": open_file
}

if __name__ == "__main__":
    Main()
    Gtk.main()
