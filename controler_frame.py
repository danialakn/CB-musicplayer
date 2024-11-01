import customtkinter
from PIL import Image
from customtkinter import *
import pygame
import music_tag

pygame.mixer.init()

class Frame2(customtkinter.CTkFrame):
    def __init__(self, master,frame3,frame1, **kwargs):
        super().__init__(master, **kwargs)

        self.frame1 = frame1
        self.frame3 = frame3
        self.window = master

        self.grid_columnconfigure(tuple((i for i in range(7))), weight=1)

        self.is_paused = BooleanVar(value=False)



        self.play_image=CTkImage(Image.open('assets/play_light.png'),Image.open('assets/play_dark.png'),size=(48,48))
        self.puse_image=CTkImage(Image.open('assets/pause_light.png'),Image.open('assets/pause_dark.png'),size=(48,48))
        self.stop_image=CTkImage(Image.open('assets/stop_light.png'),Image.open('assets/stop_dark.png'),size=(48,48))
        self.next_image=CTkImage(Image.open('assets/next_light.png'),Image.open('assets/next_dark.png'),size=(48,48))
        self.previous_image=CTkImage(Image.open('assets/perevious_light.png'),Image.open('assets/previous_dark.png'),size=(48,48))

        self.play_button=CTkButton(self, image=self.play_image , text='' ,fg_color='transparent', command= self.play)
        self.pause_button=CTkButton(self, image=self.puse_image , text='' ,fg_color='transparent', command= self.pause)
        self.stop_button = CTkButton(self, image=self.stop_image , text='' ,fg_color='transparent',command=self.stop)
        self.next_button = CTkButton(self, image=self.next_image , text='' ,fg_color='transparent', command= self.next)
        self.previous_button = CTkButton(self, image=self.previous_image , text='' ,fg_color='transparent', command= self.previous)

        self.play_button.grid(row=0, column=1)
        self.pause_button.grid(row=0, column=2)
        self.stop_button.grid(row=0, column=3)
        self.next_button.grid(row=0, column=4)
        self.previous_button.grid(row=0, column=5)

        #postion slider
        self.postion_slider = CTkSlider(self,width=800)
        self.postion_slider.grid(row=1, column=1, columnspan=6)
        self.start_time =CTkLabel(self, text='00:00' )
        self.start_time.grid(row=1, column=0)
        self.stop_time =CTkLabel(self, text='00:00' )
        self.stop_time.grid(row=1, column=7)

    def play(self):
        if self.is_paused.get():
            self.is_paused.set(False)
            pygame.mixer_music.unpause()
        else:
            self.music_index = self.frame3.listbox.curselection()
            self.music_name = self.frame3.listbox.get(self.music_index)
            self.mp3 = music_tag.load_file(f'playlist/{self.music_name}')


            #musice name
            self.music_title = self.mp3['title']
            self.window.music_name_label.configure(text=self.music_title)

            if not self.music_title:
                self.window.music_name_label.configure(text=self.music_name)


            # baresi vojod artwork va khali nabodanesh
            if 'artwork' in self.mp3 and self.mp3['artwork'].first:
                self.album_art_data = self.mp3['artwork'].first.data
                with open('assets/image.jpeg', 'wb') as image:
                    image.write(self.album_art_data)
                    self.album_art_image = CTkImage(Image.open('assets/image.jpeg'), size=(480, 480))
            else:
                self.album_art_image = CTkImage(Image.open('assets/album.jpg'), size=(480, 480))
            # hala age artwork bashe mifreste be frame1 nadashte bashe tasvir pish farz
            self.frame1.image_label.configure(image=self.album_art_image)

            #inam vase play ahang
            pygame.mixer_music.load(f'playlist/{self.music_name}')
            pygame.mixer_music.play()

    def next(self):
        try:
            self.active_index = self.frame3.listbox.curselection()
            self.frame3.listbox.activate(self.active_index + 1 )
            self.play()
        except:
            self.frame3.listbox.activate(0)
            self.play()

    def previous(self):
        try:
            self.active_index = self.frame3.listbox.curselection()
            self.frame3.listbox.activate(self.active_index - 1 )
            self.play()
        except:
            self.frame3.listbox.activate('end')

    def stop(self):
        self.active_index = self.frame3.listbox.curselection()
        self.frame3.listbox.deactivate(self.active_index)
        pygame.mixer_music.stop()
        default_image = CTkImage(Image.open('assets/album.jpg'), size=(480, 480))
        self.frame1.image_label.configure(image=default_image)
        self.window.music_name_label.configure(text='music name')

    def pause(self):
        if not self.is_paused.get():
            self.is_paused.set(value=True)
            pygame.mixer_music.pause()
        else:
            self.is_paused.set(value=False)
            pygame.mixer_music.unpause()














