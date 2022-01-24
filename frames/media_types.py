#!/usr/bin/python3
#-----------------------------------------------------------------------------
# project:  chinook
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   hiems MMXXI
#-----------------------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox
import frames.media_type as ui

SQL = "SELECT * FROM media_types ORDER BY media_type ASC;"

class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="media_types")

        self.parent = parent
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.table = "media_types"
        self.primary_key = "media_type_id"
        self.obj = None
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        f = self.master.engine.get_frame(self, 2)
        self.lstItems = self.master.engine.get_listbox(f,)
        self.lstItems.bind("<<ListboxSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-Button-1>", self.on_item_activated)
        f.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=5, pady=5)

        f = self.master.engine.get_frame(self, 2)
        self.master.engine.get_add_edit_cancel(self, f)
        f.pack(fill=tk.BOTH, expand=1)

    def on_open(self,):

        msg = "Media Type"
        self.title(msg)
        self.set_values()

    def set_values(self):

        self.lstItems.delete(0, tk.END)
        index = 0
        self.dict_items = {}

        rs = self.master.engine.read(True, SQL, ())

        if rs:
            self.lstItems.delete(0, tk.END)

            for i in rs:
                s = "{0}".format(i[1])
                self.lstItems.insert(tk.END, s)
                if i[2] != 1:
                    self.lstItems.itemconfig(index, {"bg":"light gray"})
                self.dict_items[index] = i[0]
                index += 1

    def on_add(self, evt):

        self.obj = ui.UI(self)
        self.obj.on_open()

    def on_edit(self, evt):
        self.on_item_activated()

    def on_item_selected(self, evt):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            pk = self.dict_items.get(index)
            self.selected_item = self.master.engine.get_selected(self.table, self.primary_key, pk)
            
    def on_item_activated(self, evt=None):

        if self.lstItems.curselection():
            index = self.lstItems.curselection()[0]
            self.obj = ui.UI(self, index)
            self.obj.on_open(self.selected_item,)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.master.engine.no_selected,
                                   parent=self)

    def on_cancel(self, evt=None):
        if self.obj is not None:
            self.obj.destroy()
        self.destroy()
