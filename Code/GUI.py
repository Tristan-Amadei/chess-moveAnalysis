import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
from Fonction_GUI import *

#On met un thème par défaut
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
#Initialisation des variables globales
global game_index
game_index = 10
#L'indice du coup
global i
i = dict_corres[game_index]
#Nombre de coups dans la partie
global Nb_moves
Nb_moves=getNbMoves(game_index)
#Liste des évaluations des meilleurs coups
global best_move_evals
best_move_evals = []
#Liste des évaluations des coups joués
global move_evals
move_evals = []
#Liste des probabilités de gagner si le coup joué est le meilleur
global win_probas_best_move
win_probas_best_move = []
#Liste des probabilités de gagner avec le coup joué
global win_probas
win_probas = []
global board
board = chess.Board()
#Temps laissé à Stockfish
global time
time=0.01

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mon interface de jeu Python.py")
        self.WIDTH=self.winfo_screenwidth()
        self.HEIGHT=self.winfo_screenheight()
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{0}+{0}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        self.frame_left.grid_rowconfigure(0, minsize=5)
        self.frame_left.grid_rowconfigure(11, minsize=2)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Mes options",
                                              text_font=("Roboto Medium", -16),
                                              fg_color="#D3CFCF",
                                              height=40,
                                              width=180,
                                              text_color="#9B221C",
                                              corner_radius=5)
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

        self.button_7 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Revenir d'un coup",
                                                fg_color='#3447A6',
                                                command=self.button_event6)
        self.button_7.grid(row=5, column=0, pady=3, padx=0)

        self.label_time = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Temps laissé à Stockfish (en s)",
                                              fg_color="#D3CFCF",
                                              text_color="#9B221C",
                                                corner_radius=20)
        self.label_time.grid(row=6, column=0, pady=3, padx=0, columnspan =2)

        self.list_time = customtkinter.CTkComboBox(master=self.frame_left,
                                                   values=["0.01","0.05","0.1","0.5","1","5","10"],
                                                   command=self.get_time,
                                                   fg_color="#D3CFCF",
                                                   text_color="#9B221C")
        self.list_time.grid(row=6, column=2, pady=3, padx=0, sticky="we")

        #Initialisation avec les images par défaut
        image2 = Image.open("Images/T_m.png")
        w_im_2, h_im_2 = image2.size
        image2 = image2.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
        self.bg_image2 = ImageTk.PhotoImage(image2)

        self.image_label2 = tkinter.Label(master=self.frame_left, image=self.bg_image2,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label2.grid(row=7, column=0, sticky="nw", padx=50, pady=15, columnspan=3)

        image3 = Image.open("Images/T_m.png")
        w_im_3, h_im_3 = image3.size
        image3 = image3.resize((int(w_im_3 / 2), int(h_im_3 / 2)))
        self.bg_image3 = ImageTk.PhotoImage(image3)

        self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                          height=int(h_im_3 / 2),
                                          width=int(w_im_3 / 2))
        self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)

        #Changement de thème par un menu d'option
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=10, column=0, pady=0, padx=2, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=11, column=0, pady=0, padx=2, sticky="w")

        image = Image.open("Images/board_init.png")
        w_im, h_im =image.size
        image=image.resize((int(w_im/2),int(h_im/2)))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                                   height=int(h_im/2),
                                                    width=int(w_im/2))
        self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2, rowspan=2)

        #Initialisation de la progressbar sous le board
        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_right,
                                                        width=int(w_im/2.5))
        self.progressbar.grid(row=3, column=0, sticky="nw", padx=0, pady=10, columnspan=2)

        image4 = Image.open("Images/T_zoom_m.png")
        w_im_4, h_im_4 = image4.size
        image4 = image4.resize((int(w_im_4 /1.3), int(h_im_4 / 1.3)))
        self.bg_image4 = ImageTk.PhotoImage(image4)

        self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                          height=int(h_im_4 / 1.3),
                                          width=int(w_im_4 / 1.3))
        self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

        image5 = Image.open("Images/T_zoom_m.png")
        w_im_5, h_im_5 = image5.size
        image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        self.bg_image5 = ImageTk.PhotoImage(image5)

        self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)

        #Configuration des raccourcis clavier
        # --> pour prochain coup
        self.bind_all('<Right>', lambda event:self.button_event2())
        # <-- pour prochain revenir en arrière
        self.bind_all('<Left>', lambda event: self.button_event6())
        # Entrée pour revenir au début de la partie
        self.bind_all('<Return>', lambda event: self.button_event3())

        # set default values
        self.optionmenu_1.set("Dark")
        self.progressbar.set(0)


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

    def initialisation(self):
        global i
        i=dict_corres[game_index]
        image2 = Image.open("Images/T_m.png")
        w_im_2, h_im_2 = image2.size
        image2 = image2.resize((int(w_im_2 / 2), int(h_im_2 / 2)))
        self.bg_image2 = ImageTk.PhotoImage(image2)

        self.image_label2 = tkinter.Label(master=self.frame_left, image=self.bg_image2,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label2.grid(row=7, column=0, sticky="nw", padx=50, pady=15, columnspan=3)

        image3 = Image.open("Images/T_m.png")
        w_im_3, h_im_3 = image3.size
        image3 = image3.resize((int(w_im_3 / 2), int(h_im_3 / 2)))
        self.bg_image3 = ImageTk.PhotoImage(image3)

        self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                          height=int(h_im_3 / 2),
                                          width=int(w_im_3 / 2))
        self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)
        image = Image.open("Images/board_init.png")
        w_im, h_im = image.size
        image = image.resize((int(w_im / 2), int(h_im / 2)))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=self.frame_right, image=self.bg_image,
                                         height=int(h_im / 2),
                                         width=int(w_im / 2))
        self.image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=15, columnspan=2, rowspan=2)
        image4 = Image.open("Images/T_zoom_m.png")
        w_im_4, h_im_4 = image4.size
        image4 = image4.resize((int(w_im_4 / 1.3), int(h_im_4 / 1.3)))
        self.bg_image4 = ImageTk.PhotoImage(image4)

        self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                          height=int(h_im_4 / 1.3),
                                          width=int(w_im_4 / 1.3))
        self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

        image5 = Image.open("Images/T_zoom_m.png")
        w_im_5, h_im_5 = image5.size
        image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        self.bg_image5 = ImageTk.PhotoImage(image5)

        self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)

    def button_event2(self):
        global i
        global time
        image2 = Image.open("Images/T_m.png")
        w_im_2, h_im_2 = image2.size
        image5 = Image.open("Images/T_zoom_m.png")
        w_im_5, h_im_5 = image5.size
        nb_moves = getNbMoves(game_index)
        move_to_play_on_board, best_move_from, best_move_to = playMove(i, board,
                                                                       move_evals, best_move_evals,
                                                                       win_probas, win_probas_best_move,time)
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

        image = Image.open("Images/board.png")
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
        self.bg_image3 = ImageTk.PhotoImage(image3)
        self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                          height=int(h_im_2 / 2),
                                          width=int(w_im_2 / 2))
        self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)

        image4 = Image.open("Images/eval_zoom.png")
        image4 = image4.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        self.bg_image4 = ImageTk.PhotoImage(image4)

        self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

        image5 = Image.open("Images/probas_zoom.png")
        image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
        self.bg_image5 = ImageTk.PhotoImage(image5)

        self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                          height=int(h_im_5 / 1.3),
                                          width=int(w_im_5 / 1.3))
        self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)
        self.progressbar.set(len(win_probas)/Nb_moves)
        i+=1

    #Début de partie
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
        self.initialisation()

    #Partie suivante
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
        self.initialisation()

    # Partie précédente
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
        self.initialisation()

    #Revenir un coup en arrière
    def button_event6(self):
        global best_move_evals
        global move_evals
        global win_probas_best_move
        global win_probas
        global board
        global time
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
            image2 = Image.open("Images/T_m.png")
            w_im_2, h_im_2 = image2.size
            image5 = Image.open("Images/T_zoom_m.png")
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
                                                                           win_probas, win_probas_best_move,time)
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

            image = Image.open("Images/board.png")
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
            self.bg_image3 = ImageTk.PhotoImage(image3)
            self.image_label3 = tkinter.Label(master=self.frame_left, image=self.bg_image3,
                                              height=int(h_im_2 / 2),
                                              width=int(w_im_2 / 2))
            self.image_label3.grid(row=8, column=0, sticky="nw", padx=50, pady=2, columnspan=3)

            image4 = Image.open("Images/eval_zoom.png")
            image4 = image4.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
            self.bg_image4 = ImageTk.PhotoImage(image4)

            self.image_label4 = tkinter.Label(master=self.frame_right, image=self.bg_image4,
                                              height=int(h_im_5 / 1.3),
                                              width=int(w_im_5 / 1.3))
            self.image_label4.grid(row=0, column=3, sticky="nw", padx=0, pady=15)

            image5 = Image.open("Images/probas_zoom.png")
            image5 = image5.resize((int(w_im_5 / 1.3), int(h_im_5 / 1.3)))
            self.bg_image5 = ImageTk.PhotoImage(image5)

            self.image_label5 = tkinter.Label(master=self.frame_right, image=self.bg_image5,
                                              height=int(h_im_5 / 1.3),
                                              width=int(w_im_5 / 1.3))
            self.image_label5.grid(row=1, column=3, sticky="nw", padx=0, pady=15)
            self.progressbar.set(len(win_probas)/Nb_moves)
            i+=1

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
    def progress_bar(self,value):
        print(value)
        self.progressbar.set(value/Nb_moves)

    def get_time(self,choice):
        global time
        time=float(choice)

if __name__ == "__main__":
    app = App()
    app.mainloop()

