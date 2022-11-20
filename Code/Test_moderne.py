import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os
from tqdm import tqdm


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    # WIDTH = 1920
    # HEIGHT = 1080

    def __init__(self):
        super().__init__()
        self.title("Mon interface de jeu Python.py")
        self.WIDTH=self.winfo_screenwidth()
        self.HEIGHT=self.winfo_screenheight()
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{0}+{0}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(9, weight=1)  # empty row as spacing
        # self.frame_left.grid_rowconfigure(9, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Mes options",
                                              # width=2,
                                              # height=10,
                                              text_font=("Roboto Medium", -16),
                                              fg_color="#D3CFCF",
                                              height=50,
                                              width=180,
                                              text_color="#9B221C",
                                              corner_radius=5)  # font name and size in px
        self.label_1.grid(row=1, column=1, pady=10, padx=0)

        self.entry_id_partie = customtkinter.CTkEntry(master=self.frame_left,
                                            placeholder_text="Numéro de partie",
                                            fg_color="#D3CFCF",
                                            height=20,
                                            width=90,
                                            text_color="#9B221C",
                                            corner_radius=5)
        self.entry_id_partie.grid(row=2, column=1, pady=10, padx=0, sticky="we")

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Valider",
                                                command=self.button_validation)
        self.button_1.grid(row=3, column=1, pady=10, padx=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Partie précédente",
                                                fg_color = '#3447A6',
                                                command=self.button_event)
        self.button_2.grid(row=4, column=0, pady=10, padx=0)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Début de la partie",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_3.grid(row=4, column=1, pady=10, padx=0)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Prochaine partie",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_4.grid(row=4, column=2, pady=10, padx=0)

        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Avancer d'un coup",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_5.grid(row=5, column=2, pady=10, padx=0)

        self.button_6 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Coup par coup",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_6.grid(row=5, column=1, pady=10, padx=0)

        self.button_7 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Revenir d'un coup",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_7.grid(row=5, column=0, pady=10, padx=0)

        self.button_8 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Ralentir",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_8.grid(row=6, column=0, pady=10, padx=0)

        self.button_9 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Mettre la pause",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_9.grid(row=6, column=1, pady=10, padx=0)

        self.button_10 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Accélérer",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_10.grid(row=6, column=2, pady=10, padx=0)



        # self.combobox = customtkinter.CTkComboBox(master=self.frame_left,
        #                                     values=["option 1", "option 2"],
        #                                     command=self.optionmenu_callback,
        #                                     variable=self.optionmenu_var)
        # self.combobox.grid(row=4,column=1,pady=10,padx=2)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=10, column=0, pady=0, padx=2, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=11, column=0, pady=10, padx=2, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        # self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        # self.frame_right.rowconfigure(7, weight=10)
        # self.frame_right.columnconfigure((0, 1), weight=10)
        # self.frame_right.columnconfigure(2, weight=0)
        # self.frame_right.columnconfigure((0,1), weight=2)

        # self.frame_info = customtkinter.CTkFrame(master=self.frame_right,width=self.WIDTH,height=self.HEIGHT)
        # self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # # configure grid layout (1x1)
        # self.frame_info.rowconfigure(0, weight=1)
        # self.frame_info.columnconfigure(0, weight=1)

        # load image with PIL and convert to PhotoImage
        # image = Image.open("Chess_image.png").resize((960, 540))
        image = Image.open("Chess_image.png")
        w_im, h_im =image.size
        image=image.resize((int(w_im/2),int(h_im/2)))
        print(image.size)
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                                   height=int(h_im/2),
                                                    width=int(w_im/2))
        self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_right,
                                                        width=int(w_im/2.5))
        self.progressbar.grid(row=2, column=0, sticky="nw", padx=0, pady=10)

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=10,
                                                number_of_steps=10,
                                                width=int(w_im/2.5),
                                                command=self.progress_bar)
        self.slider_1.grid(row=1, column=0, pady=10, padx=0, sticky="nw")

        image2 = Image.open("Chess_image.png")
        w_im, h_im = image2.size
        image2 = image2.resize((int(w_im / 4), int(h_im / 4)))
        print(image2.size)
        self.bg_image2 = ImageTk.PhotoImage(image2)

        self.image_label2 = tkinter.Label(master=self.frame_right, image=self.bg_image2,
                                         height=int(h_im / 4),
                                         width=int(w_im / 4))
        self.image_label2.grid(row=3, column=0, sticky="nw", padx=0, pady=15)

        image3 = Image.open("Chess_image.png")
        w_im, h_im = image3.size
        image3 = image3.resize((int(w_im / 8), int(h_im / 8)))
        print(image3.size)
        self.bg_image3 = ImageTk.PhotoImage(image3)

        self.image_label3 = tkinter.Label(master=self.frame_right, image=self.bg_image3,
                                          height=int(h_im / 8),
                                          width=int(w_im / 8))
        self.image_label3.grid(row=3, column=1, sticky="nw", padx=0, pady=15)


        # self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
        #                                            text="CTkLabel: Lorem ipsum dolor sit,\n" +
        #                                                 "amet consetetur sadipscing elitr,\n" +
        #                                                 "sed diam nonumy eirmod tempor" ,
        #                                            height=100,
        #                                            corner_radius=6,  # <- custom corner radius
        #                                            fg_color=("white", "gray38"),  # <- custom tuple-color
        #                                            justify=tkinter.LEFT)
        # self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        #
        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        # self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ============

        # self.radio_var = tkinter.IntVar(value=0)

        # self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
        #                                                 text="CTkRadioButton Group:")
        # self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        # self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
        #                                                    variable=self.radio_var,
        #                                                    value=0)
        # self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        #
        # self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
        #                                                    variable=self.radio_var,
        #                                                    value=1)
        # self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        #
        # self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
        #                                                    variable=self.radio_var,
        #                                                    value=2)
        # self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
        #                                         from_=0,
        #                                         to=1,
        #                                         number_of_steps=3,
        #                                         command=self.progressbar.set)
        # self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")
        #
        # self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
        #                                         command=self.progressbar.set)
        # self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        # self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,
        #                                         text="CTkSwitch")
        # self.switch_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")
        #
        # self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right,
        #                                         text="CTkSwitch")
        # self.switch_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")
        #
        # self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
        #                                             values=["Value 1", "Value 2"])
        # self.combobox_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")
        #
        # self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                              text="CTkCheckBox")
        # self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")
        #
        # self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                              text="CTkCheckBox")
        # self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")
        #
        # self.entry = customtkinter.CTkEntry(master=self.frame_right,
        #                                     width=120,
        #                                     placeholder_text="CTkEntry")
        # self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        #
        # self.button_5 = customtkinter.CTkButton(master=self.frame_right,
        #                                         text="CTkButton",
        #                                         border_width=2,  # <- custom border_width
        #                                         fg_color=None,  # <- no fg_color
        #                                         command=self.button_event)
        # self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")
        # self.combobox_1.set("CTkCombobox")
        # self.radio_button_1.select()
        # self.slider_1.set(0.2)
        # self.slider_2.set(0.7)
        self.progressbar.set(0)
        self.slider_1.set(0)
        # self.switch_2.select()
        # self.radio_button_3.configure(state=tkinter.DISABLED)
        # self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        # self.check_box_2.select()
        # self.optionmenu_var = customtkinter.StringVar(value="option 2")  # set initial value

    def button_validation(self):
        Text=self.entry_id_partie.get()
        print(Text)
    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
    def progress_bar(self,value):
        # print(value)
        self.progressbar.set(value/10)

    # def optionmenu_callback(self,choice):
    #     print("optionmenu dropdown clicked:", choice)


if __name__ == "__main__":
    app = App()
    app.mainloop()

