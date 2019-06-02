import tkinter
import pickle
import os.path
import console_interface as console
import gui_interface as gui


def main():
    """Main method. Either calls console_interface or gui_interface.
    """
    # console.console_interface() # Commented out: Console Interface. Still functional.
    m = gui.GuiInterface()
    m.protocol("WM_DELETE_WINDOW", m.on_close)
    m.after(100, m.update)
    m.mainloop()


if __name__ == "__main__":
    main()
