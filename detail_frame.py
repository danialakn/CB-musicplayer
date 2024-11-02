import customtkinter
from PIL import Image
from customtkinter import *
import pygame


pygame.mixer.init()

class Frame1(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # ta ghable inja frame drost shode

        self.grid_columnconfigure((0, 2), weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # album image
        self.albom_image = CTkImage(Image.open('assets/album.jpg'), size=(480, 480))
        self.image_label = CTkLabel(self, image=self.albom_image, text='')
        self.image_label.grid(row=1, column=1, sticky='nsew', pady=35, padx=35)

        # slider seda
        self.volume_bar_state_var =DoubleVar(value=0.1)
        self.volume_bar = CTkSlider(self, orientation='vertical', height=100 ,from_=0, to=1 , variable=self.volume_bar_state_var)
        self.volume_bar.grid(row=1, column=2)
