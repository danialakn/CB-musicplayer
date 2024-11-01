import customtkinter
from customtkinter import *
from detail_frame import Frame1
from controler_frame import Frame2
from slidebar_frame import Frame3


class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x600")
        # row and coulmn configure
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=1)


        self.music_detail_frame = Frame1(self)
        self.music_detail_frame.grid(row=1, column=0, sticky='nsew', padx=5)

        # side bar frame
        self.sidebar_frame = Frame3(self)
        self.sidebar_frame.grid(row=0, column=1, sticky='nsew', rowspan=4)

        # control frame
        self.contoroler_frame = Frame2(self,self.sidebar_frame,self.music_detail_frame)
        self.contoroler_frame.grid(row=2, column=0, sticky='nsew')


        #name lable
        self.music_name_label = CTkLabel(self, text='music name',font=CTkFont(size=30,weight='bold'))
        self.music_name_label.grid(row=0, column=0, sticky='nsew')


if __name__ == '__main__':
    window = Window()
    window.mainloop()

