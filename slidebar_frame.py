import customtkinter
from customtkinter import *
from CTkListbox import *
from PIL import Image
import os
from tkinter.filedialog import askopenfilename
import shutil
from tkinter.messagebox import *


class Frame3(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.playlist_lbl = CTkLabel(self, text="Playlist", font=CTkFont(size=30, weight="bold"))
        self.playlist_lbl.grid(row=0, column=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.listbox = CTkListbox(self, height=360)
        self.listbox.grid(row=1, column=0)

        #      play list btn frame
        self.bts_frame = CTkFrame(self, fg_color='transparent', )
        self.bts_frame.grid(row=3, column=0)

        self.add_to_playlist_image = CTkImage(light_image=Image.open('assets/add_light.png'),
                                              dark_image=Image.open('assets/add_dark.png'), size=(20, 20))
        self.remove_playlist_image = CTkImage(light_image=Image.open('assets/remove_light.png'),
                                              dark_image=Image.open('assets/remove_dark.png'), size=(20, 20))

        self.add_to_playlist_btn = CTkButton(master=self.bts_frame, text='', fg_color='transparent',
                                             image=self.add_to_playlist_image, command=self.add_music)
        self.remove_playlist_btn = CTkButton(master=self.bts_frame, text='', fg_color='transparent',
                                             image=self.remove_playlist_image, command=self.remove_music)

        self.add_to_playlist_btn.grid(row=0, column=0)
        self.remove_playlist_btn.grid(row=0, column=1)

        # farakhani method show
        self.show()

    def add_music(self):
        try:
            self.music_path = askopenfilename(title='chose the music: ', filetypes=(('mp3', '*.mp3'),))
            shutil.copy2(self.music_path, 'playlist')
            self.show()
        except FileNotFoundError:
            showerror('Error', 'Please select a mp3 file')

    def remove_music(self):
        try:
            self.selected = self.listbox.curselection()
            self.music_path = self.listbox.get(self.selected)
            os.remove(f'playlist/{self.music_path}')
            self.show()
        except FileNotFoundError:
            showerror('Error', 'Please select a mp3 file')

    def show(self):
        self.listbox.delete(0, END)
        self.musics = os.listdir('playlist')
        for music in self.musics:
            self.listbox.insert(END, music)

    #    vase inke az listbox to class hae dg estefae konim
    def get_listbox(self):
        return self.listbox.get(0, 'end')


