from time import strftime
import customtkinter
from PIL import Image
from customtkinter import *
import pygame
import music_tag
import time

pygame.mixer.init()


class Frame2(customtkinter.CTkFrame):
    def __init__(self, master, frame3, frame1, **kwargs):
        super().__init__(master, **kwargs)

        self.frame1 = frame1
        self.frame3 = frame3
        self.window = master
        self.active_index = self.frame3.listbox.curselection()
        self.realtime = IntVar(value=0)
        self.music_len = IntVar(value=0)

        self.grid_columnconfigure(tuple((i for i in range(7))), weight=1)

        self.is_paused = BooleanVar(value=False)

        self.play_image = CTkImage(Image.open('assets/play_light.png'), Image.open('assets/play_dark.png'),
                                   size=(48, 48))
        self.puse_image = CTkImage(Image.open('assets/pause_light.png'), Image.open('assets/pause_dark.png'),
                                   size=(48, 48))
        self.stop_image = CTkImage(Image.open('assets/stop_light.png'), Image.open('assets/stop_dark.png'),
                                   size=(48, 48))
        self.next_image = CTkImage(Image.open('assets/next_light.png'), Image.open('assets/next_dark.png'),
                                   size=(48, 48))
        self.previous_image = CTkImage(Image.open('assets/perevious_light.png'), Image.open('assets/previous_dark.png'),
                                       size=(48, 48))

        self.play_button = CTkButton(self, image=self.play_image, text='', fg_color='transparent', command=self.play)
        self.pause_button = CTkButton(self, image=self.puse_image, text='', fg_color='transparent', command=self.pause)
        self.stop_button = CTkButton(self, image=self.stop_image, text='', fg_color='transparent', command=self.stop)
        self.next_button = CTkButton(self, image=self.next_image, text='', fg_color='transparent', command=self.next)
        self.previous_button = CTkButton(self, image=self.previous_image, text='', fg_color='transparent',
                                         command=self.previous)

        self.play_button.grid(row=0, column=1)
        self.pause_button.grid(row=0, column=2)
        self.stop_button.grid(row=0, column=3)
        self.next_button.grid(row=0, column=4)
        self.previous_button.grid(row=0, column=5)

        # postion slider
        self.postion_slider_state_var = IntVar(value=0)
        self.postion_slider = CTkSlider(self, width=800, from_=0, to=100, variable=self.postion_slider_state_var,
                                        command=self.slid)
        self.postion_slider.grid(row=1, column=1, columnspan=6)
        self.start_time = CTkLabel(self, text='00:00')
        self.start_time.grid(row=1, column=0)
        self.stop_time = CTkLabel(self, text='00:00')
        self.stop_time.grid(row=1, column=7)

    def play(self):
        if self.is_paused.get():
            self.is_paused.set(False)
            pygame.mixer_music.unpause()
        else:
            self.music_name = self.frame3.listbox.get(self.active_index)
            self.mp3 = music_tag.load_file(f'playlist/{self.music_name}')

            # musice name
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

            # inam vase play ahang
            pygame.mixer_music.load(f'playlist/{self.music_name}')
            self.get_current_time()
            self.get_time_length()
            pygame.mixer_music.play()

    def next(self):
        try:
            self.frame3.listbox.activate(self.active_index + 1)
            self.play()
        except:
            self.frame3.listbox.activate(0)
            self.play()

    def previous(self):
        try:
            self.frame3.listbox.activate(self.active_index - 1)
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

    def get_current_time(self):
        # chon az manfi yek shoro mishe ba yek jamesh kardam va chon bar hasb mili saniye hast taghsim bar 1000
        self.current_time = self.realtime.get() + ((int(pygame.mixer_music.get_pos() + 1) / 1000))
        self.coverted_current_time = time.strftime('%M:%S', time.gmtime(self.current_time))
        self.start_time.configure(text=self.coverted_current_time)
        if self.current_time+1 == self.music_len.get():
            print('hello')
        self.stop_time.after(1000, self.get_current_time)
        self.postion_slider_state_var.set(self.current_time)

    def get_time_length(self):
        self.active_index = self.frame3.listbox.curselection()
        self.music_name = self.frame3.listbox.get(self.active_index)
        self.mp3 = music_tag.load_file(f'playlist/{self.music_name}')
        self.mp3_length = int(self.mp3['#length'])
        self.music_len.set(value=self.mp3_length)
        self.postion_slider.configure(to=self.mp3_length)
        self.convert_music_len = strftime('%M:%S', time.gmtime(self.mp3_length))
        self.stop_time.configure(text=self.convert_music_len)

    def slid(self, time):
        self.realtime.set(value=time)
        pygame.mixer_music.load(f'playlist/{self.music_name}')
        pygame.mixer_music.play(start=time)

