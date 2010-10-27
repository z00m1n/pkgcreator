namespace WebKitGUI {
    class WebKitGtkGUI : WebKitGUI {
        public override bool init(string html) {
            stdout.printf("HTML loaded.");
            return true;
        }
        public override void show() {
            stdout.printf("Waiting for events...");
        }
    }
}