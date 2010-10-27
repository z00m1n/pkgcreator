using Gee;

namespace WebKitGUI {
    //Delegate Callback not yet supported as generic type argument
    //delegate void Callback(string widget, string event);
    internal abstract class WebKitGUI : Object {
        //protected Gee.HashMap<string, pointer p> callbacks;
        public WebKitGUI() {
            //callbacks = new Gee.HashMap<string, pointer p> ();
        }
        public abstract bool init(string title, int width, int height, ref unowned string[] args);
        public abstract void load_from_path(string path);
        /*public void connect_signal(string signal_name, Callback c) {
            callbacks[signal_name] = c;
        }*/
        public abstract void show();
        //public abstract void set_var(string varname, string varproperty, string varvalue);
        /*protected void handle_signal(WebFrame wf, string info) {
            string signal_name, widget, event;
            string template = "signal: '%s' , widget: '%s', event: '%s'";
            template.scanf(out signal_name, out widget, out event);
            if(signal_name in callbacks) {
                stdout.printf(signal_name + " found. Dispatching...");
                callbacks[signal_name] ();
            }
            else
                stdout.printf("Warning: signal '%s' not connected", signal_name);
        }*/
    }
}