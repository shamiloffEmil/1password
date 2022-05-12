# -*- coding: utf-8 -*

import json
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from zipfile import *


class Page(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Page1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = new_frame
        self._frame.pack()


class Page1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.val = StringVar()
        self.master = master
        self.message = Label(self, text='Invalid password')

        fileZIP = "data_file.zip"  # type: str

        def checkPassword(event):

            z = ZipFile('data_file.zip', 'r')
            pas = self.val.get().encode('cp850', 'replace')
            try:
                z.extract('data_file.json', None, pas)
                z.close()
                self.master.switch_frame(Page2)

            except RuntimeError:
                self.entry.delete(0, END)
                self.message.pack()

        def checkArchive(fzip):

            if not os.path.isfile(fzip):
                return False
            else:
                return True

        if checkArchive(fileZIP):
            self.lab = Label(self, text='Авторизация')
            self.butOK = Button(self, text='Ok')
            self.butOK.bind('<Button->', checkPassword)
            self.entry = Entry(self, textvariable=self.val, show="*")

            self.lab.pack()
            self.butOK.pack()
            self.entry.pack()

        else:

            self.master.switch_frame(Page2)


class Page2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        self.l = Listbox(selectmode=EXTENDED)
        self.l.bind('<<ListboxSelect>>', self.onselect)
        self.l.pack(side=TOP)
        self.site = ''
        self.login = ''
        self.password = ''
        self.data = {}
        self.FillInList()
        self.entryLogin = Entry(self, textvariable="")
        self.entryPassword = Entry(self, textvariable="")
        Label(self, text="Логин").pack()
        self.entryLogin.pack()
        Label(self, text="Пароль").pack()
        self.entryPassword.pack()
        self.bPlus = Button(text="+", command=self.newSite)
        self.bMinus = Button(text="-", command=self.deleteSite)
        self.btun = Button(text="Изменить", command=self.addSite)
        self.btun.pack()
        self.bPlus.pack()
        self.bMinus.pack()
        self.entrySite = Entry(self, textvariable="")
        self.entrySite.pack_forget()
        self.counterButtonSave = 0
        # tk.Button(self, text="Return to start page",
        #          command=lambda: master.switch_frame(Page1)).pack()
        # self.master.switch_frame(Page3)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def showPassword(self):

        selecion = self.l.curselection()
        key = self.l.get(selecion[0])
        JString = self.data.get(key)
        self.site = key
        self.login = JString.get('login')
        self.password = JString.get('password')

        self.entryLogin.delete(0, END)
        self.entryPassword.delete(0, END)
        self.entrySite.delete(0, END)
        self.entryLogin.insert(0, self.login)
        self.entryPassword.insert(0, self.password)
        self.entrySite.insert(0, self.site)

    def onselect(self, a):
        selecion = self.l.curselection()
        key = self.l.get(selecion[0])
        JString = self.data.get(key)

        self.site = key
        self.login = JString.get('login')
        self.password = JString.get('password')

        self.entryLogin.delete(0, END)
        self.entryPassword.delete(0, END)
        self.entrySite.delete(0, END)
        self.entryLogin.insert(0, self.login)
        self.entryPassword.insert(0, self.password)
        self.entrySite.insert(0, self.site)

    def deleteSite(self):
        selection = self.l.curselection()
        self.deleteInLabel()
        self.l.delete(selection[0])

    def addSite(self):
        # self.entrySite = Entry(self, textvariable="")
        # self.entrySite.pack()
        # self.entrySite.insert(0, self.site)
        self.counterButtonSave += 1;

        if self.counterButtonSave == 1:
            self.entrySite.pack()
            self.bAdd = Button(text="Сохранить", command=self.saveInLabel).pack()

        self.btun.pack_forget()

    def newSite(self):
        self.counterButtonSave += 1;
        self.site = ''

        if self.counterButtonSave == 1:
            self.entrySite.pack()
            self.bAdd = Button(text="Сохранить", command=self.saveInLabel).pack()

        self.entrySite.delete(0, END)
        self.entryLogin.delete(0, END)
        self.entryPassword.delete(0, END)

    def saveInLabel(self):
        if self.site == self.entrySite.get():
            ourDictionary = self.data[self.site]
            ourDictionary.update({
                'login': '' + self.entryLogin.get() + '', 'password': '' + self.entryPassword.get() + ''
            })
        elif self.site == '':
            self.data[self.entrySite.get()] = {'login': '' + self.entryLogin.get() + '',
                                               'password': '' + self.entryPassword.get() + ''}
        else:
            self.data[self.entrySite.get()] = self.data.pop(self.site)
            self.site = self.entrySite.get()

            ourDictionary = self.data[self.site]
            ourDictionary.update({
                'login': '' + self.entryLogin.get() + '', 'password': '' + self.entryPassword.get() + ''
            })

        self.refreshList()

        with open("data_file.json", "w") as fb:
            json.dump(self.data, fb)
            fb.close()

        with ZipFile('data_file.zip', 'w') as myzip:
            myzip.write('data_file.json')

    def deleteInLabel(self):
        self.data.pop(self.site)

        with open("data_file.json", "w") as fb:
            json.dump(self.data, fb)
            fb.close()

        with ZipFile('data_file.zip', 'w') as myzip:
            myzip.write('data_file.json')

    def on_closing(self):
        answer = mb.askyesno(title="Вопрос", message="Закрыть программу?")
        if answer == True:
            os.remove("data_file.json")
            self.master.destroy()

    def unpacking(self):
        with open("data_file.json", "r") as read_file:
            loadData = json.load(read_file)  # [0]
            self.data = loadData

    def FillInList(self):
        self.unpacking()
        for key in self.data:
            self.l.insert(END, key)

    def refreshList(self):
        self.l.delete(0, END)
        for key in self.data:
            self.l.insert(END, key)

    def getPassword(self):
        return self.password

    def getLogin(self):
        return self.login


if __name__ == "__main__":
    app = Page()
    app.mainloop()
