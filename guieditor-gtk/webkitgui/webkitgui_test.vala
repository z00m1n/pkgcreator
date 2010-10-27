using WebKit;
using WebKitGUI;

void myhandler(WebFrame wf, string title) {
    stdout.printf(title);
}

void main(string[] args) {
    var gui = new WebKitGtkGUI();
    gui.init("Test Application", 300, 300, ref args);
    gui.load_from_path("../../example/gui.html");
    gui.webkit.title_changed.connect(myhandler);
    gui.show();
}
