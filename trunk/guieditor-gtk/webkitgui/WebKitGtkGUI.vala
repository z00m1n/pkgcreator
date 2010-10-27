using Gtk;
using WebKit;

namespace WebKitGUI {
    class WebKitGtkGUI : WebKitGUI {
        private Window window;
        private ScrolledWindow scrolled_window;
        public WebView webview;
        public override bool init(string title, int width, int height, ref unowned string[] args) {
            Gtk.init (ref args);
            //Creating Gtk window
            window = new Window ();
            window.title = title;
            window.set_default_size (width, height);
            window.position = WindowPosition.CENTER;
            window.destroy.connect (Gtk.main_quit);
            //Creating scrolled window
            scrolled_window = new ScrolledWindow(null, null);
            window.add(scrolled_window);
            //Creating webview
            webview = new WebView();
            //webview.title_changed.connect(this.handle_signal);
            webview.title_changed.connect(title_changed);
            scrolled_window.add(webview);
            window.show_all();
            return true;
        }
        public override void load_from_path(string path) {
            string? abspath = Utils.get_absolute_path(path);
            var errormsg = "Warning: invalid path passed in load_from_path method";
            if (abspath != null) {
                try {
                    var uri = Filename.to_uri(abspath, null);
                    webview.load_uri(uri);
                }
                catch (GLib.ConvertError e) {
                    stdout.printf(errormsg);
                }
            }
            else
                stdout.printf(errormsg);
        }
        public override void show() {
            Gtk.main ();
        }
    }
}