using WebKitGUI;

void button_clicked(string widget, string event) {
    stdout.printf("button was clicked");
}

void main(string[] args) {
    var gui = new WebKitGtkGUI();
    gui.init("doesntmatter.html");
    gui.connect_signal("button_clicked", button_clicked);
    gui.show();
}
