import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
import os
from tqdm import tqdm
import glob
from pdf2jpg import pdf2jpg
from Fonction_GUI import *

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
#Partie Data
global game_index
game_index = 10
global i
i = dict_corres[game_index]
global Nb_moves
Nb_moves=getNbMoves(game_index)
# nb_moves = getNbMoves(game_index)
global best_move_evals
best_move_evals = []
global move_evals
move_evals = []
global win_probas_best_move
win_probas_best_move = []
global win_probas
win_probas = []
global board
board = chess.Board()

class App(customtkinter.CTk):
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
        self.frame_left.grid_rowconfigure(0, minsize=5)   # empty row with minsize as spacing
        # self.frame_left.grid_rowconfigure(9, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=2)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Mes options",
                                              # width=2,
                                              # height=10,
                                              text_font=("Roboto Medium", -16),
                                              fg_color="#D3CFCF",
                                              height=40,
                                              width=180,
                                              text_color="#9B221C",
                                              corner_radius=5)  # font name and size in px
        self.label_1.grid(row=1, column=1, pady=3, padx=0)

        self.entry_id_partie = customtkinter.CTkEntry(master=self.frame_left,
                                            placeholder_text="Numéro de partie",
                                            fg_color="#D3CFCF",
                                            height=15,
                                            width=90,
                                            text_color="#9B221C",
                                            corner_radius=5)
        self.entry_id_partie.grid(row=2, column=1, pady=3, padx=0, sticky="we")

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Valider",
                                                command=self.button_validation)
        self.button_1.grid(row=3, column=1, pady=3, padx=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Partie précédente",
                                                fg_color = '#3447A6',
                                                command=self.button_event5)
        self.button_2.grid(row=4, column=0, pady=3, padx=0)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Début de la partie",
                                                fg_color='#3447A6',
                                                command=self.button_event3)
        self.button_3.grid(row=4, column=1, pady=3, padx=0)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Prochaine partie",
                                                fg_color='#3447A6',
                                                command=self.button_event4)
        self.button_4.grid(row=4, column=2, pady=3, padx=0)

        self.button_5 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Avancer d'un coup",
                                                fg_color='#3447A6',
                                                command= self.button_event2)
        self.button_5.grid(row=5, column=2, pady=3, padx=0)

        self.button_6 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Coup par coup",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_6.grid(row=5, column=1, pady=3, padx=0)

        self.button_7 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Revenir d'un coup",
                                                fg_color='#3447A6',
                                                command=self.button_event6)
        self.button_7.grid(row=5, column=0, pady=3, padx=0)

        self.button_8 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Ralentir",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_8.grid(row=6, column=0, pady=3, padx=0)

        self.button_9 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Mettre la pause",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_9.grid(row=6, column=1, pady=3, padx=0)

        self.button_10 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Accélérer",
                                                fg_color='#3447A6',
                                                command=self.button_event)
        self.button_10.grid(row=6, column=2, pady=3, padx=0)

        image2 = Image.open("T_m.png")
        w_im_2, h_im_2 = image2.size
        image2 = image2.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
        print(image2.size)
        self.bg_image2 = ImageTk.PhotoImage(image2)

        self.image_label2 = tkinter.Label(master=self.frame_left, image=self.bg_image2,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label2.grid(row=7, column=0, sticky="nw", padx=50, pady=15, columnspan=3)

        image3 = Image.open("T_m.png")
        w_im_3, h_im_3 = image3.size
        image3 = image3.resize((int(w_im_3 / 2), int(h_im_3 / 2)))
        print(image3.size)
        self.bg_image3 = ImageTk.PhotoImage(image3)

        self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                          height=int(h_im_3 / 2),
                                          width=int(w_im_3 / 2))
        self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=10, column=0, pady=0, padx=2, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=11, column=0, pady=0, padx=2, sticky="w")


        # load image with PIL and convert to PhotoImage
        # image = Image.open("Chess_image.png").resize((960, 540))
        image = Image.open("board_init.png")
        w_im, h_im =image.size
        image=image.resize((int(w_im/2),int(h_im/2)))
        print(image.size)
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                                   height=int(h_im/2),
                                                    width=int(w_im/2))
        self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2, rowspan=2)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_right,
                                                        width=int(w_im/2.5))
        self.progressbar.grid(row=3, column=0, sticky="nw", padx=0, pady=10, columnspan=2)

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=Nb_moves,
                                                number_of_steps=Nb_moves,
                                                width=int(w_im/2.5),
                                                command=self.progress_bar)
        # self.slider_1.grid(row=2, column=0, pady=10, padx=0, sticky="nw", columnspan=2)

        image4 = Image.open("T_zoom_m.png")
        w_im_4, h_im_4 = image4.size
        image4 = image4.resize((int(w_im_4 /1.3), int(h_im_4 / 1.3)))
        print(image4.size)
        self.bg_image4 = ImageTk.PhotoImage(image4)

        self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                          height=int(h_im_4 / 1.3),
                                          width=int(w_im_4 / 1.3))
        self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

        image5 = Image.open("T_zoom_m.png")
        w_im_5, h_im_5 = image5.size
        image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        print(image5.size)
        self.bg_image5 = ImageTk.PhotoImage(image5)

        self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)

        # set default values
        self.optionmenu_1.set("Dark")
        self.progressbar.set(0)
        self.slider_1.set(0)


    def button_validation(self):
        Text=self.entry_id_partie.get()
        global game_index
        game_index=int(Text)
        global i
        i = dict_corres[game_index]
        global Nb_moves
        Nb_moves = getNbMoves(game_index)
        global best_move_evals
        best_move_evals = []
        global move_evals
        move_evals = []
        global win_probas_best_move
        win_probas_best_move = []
        global win_probas
        win_probas = []
        global board
        board = chess.Board()

        self.initialisation()



    def button_event(self):
        print("Button pressed")

    def initialisation(self):
        global i
        i=dict_corres[game_index]
        image2 = Image.open("T_m.png")
        w_im_2, h_im_2 = image2.size
        image2 = image2.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
        print(image2.size)
        self.bg_image2 = ImageTk.PhotoImage(image2)

        self.image_label2 = tkinter.Label(master=self.frame_left, image=self.bg_image2,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label2.grid(row=7, column=0, sticky="nw", padx=50, pady=15, columnspan=3)

        image3 = Image.open("T_m.png")
        w_im_3, h_im_3 = image3.size
        image3 = image3.resize((int(w_im_3 / 2), int(h_im_3 / 2)))
        print(image3.size)
        self.bg_image3 = ImageTk.PhotoImage(image3)

        self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                          height=int(h_im_3 / 2),
                                          width=int(w_im_3 / 2))
        self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)
        # load image with PIL and convert to PhotoImage
        image = Image.open("board_init.png")
        w_im, h_im = image.size
        image = image.resize((int(w_im / 2), int(h_im / 2)))
        print(image.size)
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                         height=int(h_im / 2),
                                         width=int(w_im / 2))
        self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2, rowspan=2)
        image4 = Image.open("T_zoom_m.png")
        w_im_4, h_im_4 = image4.size
        image4 = image4.resize((int(w_im_4 / 1.3), int(h_im_4 / 1.3)))
        print(image4.size)
        self.bg_image4 = ImageTk.PhotoImage(image4)

        self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                          height=int(h_im_4 / 1.3),
                                          width=int(w_im_4 / 1.3))
        self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

        image5 = Image.open("T_zoom_m.png")
        w_im_5, h_im_5 = image5.size
        image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        print(image5.size)
        self.bg_image5 = ImageTk.PhotoImage(image5)

        self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)

    def button_event2(self):
        print("Bouton 2")
        # game_index = 3
        # i = dict_corres[game_index]
        global i
        image2 = Image.open("T_m.png")
        w_im_2, h_im_2 = image2.size
        image5 = Image.open("T_zoom_m.png")
        w_im_5, h_im_5 = image5.size
        nb_moves = getNbMoves(game_index)
        move_to_play_on_board, best_move_from, best_move_to = playMove(i, board,
                                                                       move_evals, best_move_evals,
                                                                       win_probas, win_probas_best_move)
        save_board(board, move_to_play_on_board, best_move_from, best_move_to)
        filename_eval_zoom = "./Images/eval_zoom"
        eval_graph_zoom(nb_moves, move_evals, best_move_evals, show_graph=False, save_graph=filename_eval_zoom)

        filename_eval_global = "./Images/eval_global"
        eval_graph_global(nb_moves, move_evals, show_graph=False, save_graph=filename_eval_global)

        filename_probas_zoom = "./Images/probas_zoom"
        win_proba_graph_zoom(nb_moves, win_probas, win_probas_best_move, show_graph=False,
                             save_graph=filename_probas_zoom)

        filename_probas_global = "./Images/probas_global"
        win_proba_graph_global(nb_moves, win_probas, show_graph=False, save_graph=filename_probas_global)

        image = Image.open("board.png")
        w_im, h_im = image.size
        image = image.resize((int(w_im/2), int(h_im/2)))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                         height=int(h_im/2),
                                         width=int(w_im/2))
        self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2, rowspan=2)

        image2 = Image.open("Images/eval_global.png")
        image2 = image2.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
        self.bg_image2 = ImageTk.PhotoImage(image2)
        self.image_label2 = tkinter.Label(master=self.frame_left, image=self.bg_image2,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label2.grid(row=7, column=0, sticky="nw", padx=50, pady=15, columnspan=3)

        image3 = Image.open("Images/probas_global.png")
        image3 = image3.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
        print(image3.size)
        self.bg_image3 = ImageTk.PhotoImage(image3)
        self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)

        image4 = Image.open("Images/eval_zoom.png")
        image4 = image4.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        print(image4.size)
        self.bg_image4 = ImageTk.PhotoImage(image4)

        self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

        image5 = Image.open("Images/probas_zoom.png")
        image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        print(image5.size)
        self.bg_image5 = ImageTk.PhotoImage(image5)

        self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)
        self.progressbar.set(len(win_probas)/Nb_moves)
        # self.slider_1.set(len(win_probas))
        i+=1

    def button_event3(self):
        global i
        i = dict_corres[game_index]
        global Nb_moves
        Nb_moves = getNbMoves(game_index)
        global best_move_evals
        best_move_evals = []
        global move_evals
        move_evals = []
        global win_probas_best_move
        win_probas_best_move = []
        global win_probas
        win_probas = []
        global board
        board = chess.Board()
        print(game_index)
        print(i)
        self.initialisation()

    def button_event4(self):
        global game_index
        game_index +=1
        global i
        i = dict_corres[game_index]
        global Nb_moves
        Nb_moves = getNbMoves(game_index)
        global best_move_evals
        best_move_evals = []
        global move_evals
        move_evals = []
        global win_probas_best_move
        win_probas_best_move = []
        global win_probas
        win_probas = []
        global board
        board = chess.Board()
        print(game_index)
        print(i)
        self.initialisation()

    def button_event5(self):
        global game_index
        game_index -=1
        global i
        i = dict_corres[game_index]
        global Nb_moves
        Nb_moves = getNbMoves(game_index)
        global best_move_evals
        best_move_evals = []
        global move_evals
        move_evals = []
        global win_probas_best_move
        win_probas_best_move = []
        global win_probas
        win_probas = []
        global board
        board = chess.Board()
        print(game_index)
        print(i)
        self.initialisation()

    def button_event6(self):
        print("Bouton 6")
        global best_move_evals
        global move_evals
        global win_probas_best_move
        global win_probas
        global board
        if len(move_evals)<=1:
            print("Impossible")
            best_move_evals.pop()
            move_evals.pop()
            win_probas_best_move.pop()
            win_probas.pop()
            board.pop()
            self.initialisation()
        else:
            global i
            image2 = Image.open("T_m.png")
            w_im_2, h_im_2 = image2.size
            image5 = Image.open("T_zoom_m.png")
            w_im_5, h_im_5 = image5.size
            nb_moves = getNbMoves(game_index)

            i-=2
            best_move_evals.pop()
            best_move_evals.pop()
            move_evals.pop()
            move_evals.pop()
            win_probas_best_move.pop()
            win_probas_best_move.pop()
            win_probas.pop()
            win_probas.pop()
            board.pop()
            board.pop()



            move_to_play_on_board, best_move_from, best_move_to = playMove(i, board,
                                                                           move_evals, best_move_evals,
                                                                           win_probas, win_probas_best_move)
            save_board(board, move_to_play_on_board, best_move_from, best_move_to)
            filename_eval_zoom = "./Images/eval_zoom"
            eval_graph_zoom(nb_moves, move_evals, best_move_evals, show_graph=False, save_graph=filename_eval_zoom)

            filename_eval_global = "./Images/eval_global"
            eval_graph_global(nb_moves, move_evals, show_graph=False, save_graph=filename_eval_global)

            filename_probas_zoom = "./Images/probas_zoom"
            win_proba_graph_zoom(nb_moves, win_probas, win_probas_best_move, show_graph=False,
                                 save_graph=filename_probas_zoom)

            filename_probas_global = "./Images/probas_global"
            win_proba_graph_global(nb_moves, win_probas, show_graph=False, save_graph=filename_probas_global)

            image = Image.open("board.png")
            w_im, h_im = image.size
            image = image.resize((int(w_im/2), int(h_im/2)))
            self.bg_image = ImageTk.PhotoImage(image)
            self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                             height=int(h_im/2),
                                             width=int(w_im/2))
            self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2, rowspan=2)

            image2 = Image.open("Images/eval_global.png")
            image2 = image2.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
            self.bg_image2 = ImageTk.PhotoImage(image2)
            self.image_label2 = tkinter.Label(master=self.frame_left, image=self.bg_image2,
                                              height=int(h_im_2 / 2),
                                              width=int(w_im_2 / 2))
            self.image_label2.grid(row=7, column=0, sticky="nw", padx=50, pady=15, columnspan=3)

            image3 = Image.open("Images/probas_global.png")
            image3 = image3.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
            print(image3.size)
            self.bg_image3 = ImageTk.PhotoImage(image3)
            self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                              height=int(h_im_2 / 2),
                                              width=int(w_im_2 / 2))
            self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)

            image4 = Image.open("Images/eval_zoom.png")
            image4 = image4.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
            print(image4.size)
            self.bg_image4 = ImageTk.PhotoImage(image4)

            self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                              height=int(h_im_5 / 1.3),
                                              width=int(w_im_5 / 1.3))
            self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

            image5 = Image.open("Images/probas_zoom.png")
            image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
            print(image5.size)
            self.bg_image5 = ImageTk.PhotoImage(image5)

            self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                              height=int(h_im_5 / 1.3),
                                              width=int(w_im_5 / 1.3))
            self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)
            self.progressbar.set(len(win_probas)/Nb_moves)
            # self.slider_1.set(len(win_probas))
            i+=1

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
    def progress_bar(self,value):
        print(value)
        self.progressbar.set(value/Nb_moves)

    # def optionmenu_callback(self,choice):
    #     print("optionmenu dropdown clicked:", choice)


if __name__ == "__main__":
    app = App()
    app.mainloop()

