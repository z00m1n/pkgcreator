import gtk

def main():
    win = gtk.Window()
    win.props.title = 'pkgcreator-gtk'
    win.connect('delete-event', lambda *_: gtk.main_quit())
    win.show()
    gtk.main()

if __name__ == '__main__':
    main()

