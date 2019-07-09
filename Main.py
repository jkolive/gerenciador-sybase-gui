import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


builder = Gtk.Builder()
builder.add_from_file("App.glade")

handlers = {
    "on_btn_fechar_clicked": Gtk.main_quit,

}
builder.connect_signals(handlers)
window = builder.get_object("window_main")
window.show_all()

Gtk.main()
