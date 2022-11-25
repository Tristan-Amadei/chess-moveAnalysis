import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.ticker import PercentFormatter
from tqdm import tqdm
import pandas as pd
import pickle

import chess
from chess import *
import chess.engine
import chess.svg

import svglib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from pdf2jpg import pdf2jpg

moves_df = pd.read_csv("../Data/moves_df.csv", dtype={"fen": str, 'zobrist_key': str})
# functions to evaluate a given chess position

def stockfish_evaluation(engine, board, time_limit=0.5):
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    return result['score'].white()


def position_eval(engine, board, time_limit=0.5, return_wdl=False):
    score = stockfish_evaluation(engine, board, time_limit)
    if not score.is_mate():
        if return_wdl:
            return score.score(), score.wdl()
        return score.score()
    # the engine has found a way to mate in a certain number of moves
    if return_wdl:
        return mateScore(score), score.wdl()
    return mateScore(score)


def findNumberOfMovesBeforeMate(score):
    str_nb_moves_before_mate = ''
    s = str(score)
    i = len(s) - 1
    while i >= 0 and s[i].isnumeric():
        str_nb_moves_before_mate = s[i] + str_nb_moves_before_mate
        i -= 1
    return int(str_nb_moves_before_mate)


def mateScore(score):
    nb_moves_before_mate = findNumberOfMovesBeforeMate(score)
    white_is_winning = (str(score.wdl())[9] == '1')
    # score.wdl() gives the probability of winning for white
    # if the 9th character is equal to 1, then white will deliver mate shortly
    # otherwise, white will lose soon and black is winning
    score_for_mate = 10000 - nb_moves_before_mate * 100
    if not white_is_winning:
        score_for_mate = (-1) * score_for_mate
    return score_for_mate


def get_eval_after_move(move_played_from_df, best_move, best_move_eval, engine, board, time_limit=0.5):
    eval_, win_proba = position_eval(engine, board, time_limit, return_wdl=True)

    if move_played_from_df.from_square == best_move.from_square and move_played_from_df.to_square == best_move.to_square:
        eval_ = best_move_eval

    return eval_, win_proba


# functions to play moves on a chess board

def getSquareNumber(square):
    col = square[0].lower()
    row = int(square[1])
    row_number = ord(col) - 97
    square_number = 8 * (row - 1) + row_number
    return square_number


def getMoveToPlay(startSquare, endSquare, promotion_piece=None):
    startSquare_num = getSquareNumber(startSquare)
    endStart_num = getSquareNumber(endSquare)
    move = chess.Move(startSquare_num, endStart_num, promotion=promotion_piece)
    return move


def getPieceToPromoteTo(move):
    # pieces : Pawn=1, Knight=2, Bishop=3, Rook=4, Queen=5, King=6
    if len(move) == 4:
        # we check again that there is indeed a promotion on this move
        return None
    promotion_piece = move[-1]
    if promotion_piece == 'q':
        return 5
    if promotion_piece == 'r':
        return 4
    if promotion_piece == 'b':
        return 3
    if promotion_piece == 'n':
        return 2


def getMove(move):
    startSquare = move[:2]
    endSquare = move[2:4]
    if len(move) == 4:
        return getMoveToPlay(startSquare, endSquare)
    promotion_piece = getPieceToPromoteTo(move[-1])
    return getMoveToPlay(startSquare, endSquare, promotion_piece)

def save_board(board, last_move, best_move_from, best_move_to):
    im_svg = chess.svg.board(board, lastmove=last_move,
                             arrows=[chess.svg.Arrow(best_move_from, best_move_to, color="#cc0000cc")])
    outputfile = open('board.svg', "w")
    outputfile.write(im_svg)
    outputfile.close()

    drawing = svg2rlg('board.svg')
    renderPDF.drawToFile(drawing, "board.pdf")

    inputpath = "./board.pdf"
    outputpath = "./"
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages="ALL")

def line_0(nb_moves):
    x = 0
    white_playing = True
    for x in range(nb_moves-1):
        if white_playing:
            plt.plot([x, x+1], [0, 0], color='green', linewidth=3)
            white_playing = False
        else:
            plt.plot([x, x+1], [0, 0], color='red', linewidth=3)
            white_playing = True

def set_grid(nb_moves):
    # Major ticks every 5, minor ticks every 1
    major_ticks = np.arange(0, nb_moves, 5)
    minor_ticks = np.arange(0, nb_moves, 1)

    plt.gca().set_xticks(major_ticks)
    plt.gca().set_xticks(minor_ticks, minor=True)

    # And a corresponding grid
    plt.gca().grid(axis='x')
    plt.gca().grid(which='minor', alpha=0.2)
    plt.gca().grid(which='major', alpha=0.5)

def saving_graph(filename):
    if filename[-3:] == 'png' or filename[-3:] == 'jpg' or filename[-3:] == 'pdf':
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.savefig(filename+".png", bbox_inches='tight')


def eval_graph_global(nb_moves, move_evals, show_graph=False, save_graph=None):
    plt.figure(figsize=(15, 10))
    plt.plot(move_evals, marker='x')

    # line_0(nb_moves)
    plt.plot([0] * nb_moves, linestyle='dotted', color='black')
    set_grid(nb_moves)

    plt.title("Evaluation dynamique de l'évaluation de la partie", fontsize=18, color='red')
    plt.xlabel("Coups joués", fontsize=14)
    plt.ylabel("Evaluation", fontsize=14)

    plt.xlim([-1, nb_moves])

    absolute_max_eval = max(max(move_evals), min(move_evals))
    if absolute_max_eval <= 100:
        plt.ylim([-100, 100])
    else:
        lim_y = absolute_max_eval + 50 - (absolute_max_eval % 50)
        plt.ylim([-lim_y, lim_y])

    if save_graph != None:
        saving_graph(save_graph)

    if show_graph:
        plt.show()

    plt.close()


def eval_graph_zoom(nb_moves, move_evals, best_move_evals, show_graph=False, save_graph=None):
    plt.figure(figsize=(10, 7))
    plt.plot(move_evals[:-1], marker='x')
    plt.scatter(len(move_evals) - 1, move_evals[-1], color='black', s=200)
    plt.scatter(len(move_evals) - 1, best_move_evals[-1], color='red', s=200)

    line_0(nb_moves)
    set_grid(nb_moves)
    plt.gca().xaxis.set_ticks(range(nb_moves))

    if len(move_evals) >= 2:
        arrow_move = mpatches.FancyArrowPatch((len(move_evals) - 2, move_evals[-2]),
                                              (len(move_evals) - 1, move_evals[-1]),
                                              arrowstyle='-|>',
                                              mutation_scale=20.0,
                                              linewidth=4,
                                              linestyle='solid',
                                              color='black',
                                              # label = 'Evaluation for the move played'
                                              )

        arrow_best_move = mpatches.FancyArrowPatch((len(move_evals) - 2, move_evals[-2]),
                                                   (len(move_evals) - 1, best_move_evals[-1]),
                                                   arrowstyle='-|>',
                                                   mutation_scale=20.0,
                                                   linewidth=4,
                                                   linestyle='solid',
                                                   color='red',
                                                   # label = 'Evaluation for the best move'
                                                   )

        plt.gca().add_patch(arrow_move)
        plt.gca().add_patch(arrow_best_move)

    min_frame = max(len(move_evals) - 5, 0)
    plt.xlim([min_frame, len(move_evals) + 1])

    plt.title("Evaluation dynamique de l'évaluation de la partie", fontsize=18, color='red')
    plt.xlabel("Coups joués", fontsize=14)
    plt.ylabel("Evaluation", fontsize=14)

    if save_graph != None:
        saving_graph(save_graph)

    if show_graph:
        plt.show()

    plt.close()


def win_proba_graph_global(nb_moves, win_probas, show_graph=False, save_graph=None):
    plt.figure(figsize=(15, 10))
    plt.plot(win_probas, marker='x')

    plt.plot([0.5] * nb_moves, linestyle='dotted', color='black')
    set_grid(nb_moves)

    plt.title("Probabilité de victoire des blancs", fontsize=18, color='red')
    plt.xlabel("Coups joués", fontsize=14)
    plt.ylabel("Probabilité", fontsize=14)

    plt.xlim([-1, nb_moves])
    plt.ylim([0, 1])

    if save_graph != None:
        saving_graph(save_graph)

    if show_graph:
        plt.show()

    plt.close()


def win_proba_graph_zoom(nb_moves, win_probas, win_probas_best_move, show_graph=False, save_graph=None):
    plt.figure(figsize=(10, 7))
    plt.plot(win_probas[:-1], marker='x')
    plt.scatter(len(win_probas) - 1, win_probas[-1], color='black', s=200)
    plt.scatter(len(win_probas) - 1, win_probas_best_move[-1], color='red', s=200)

    # plt.plot([0.5]*nb_moves, linestyle = 'dotted', color='black')
    line_0(nb_moves)
    set_grid(nb_moves)
    plt.gca().xaxis.set_ticks(range(nb_moves))

    if len(win_probas) >= 2:
        arrow_proba = mpatches.FancyArrowPatch((len(win_probas) - 2, win_probas[-2]),
                                               (len(win_probas) - 1, win_probas[-1]),
                                               arrowstyle='-|>',
                                               mutation_scale=20.0,
                                               linewidth=4,
                                               linestyle='solid',
                                               color='black',
                                               # label = 'Evaluation for the move played'
                                               )

        arrow_proba_best_move = mpatches.FancyArrowPatch((len(win_probas) - 2, win_probas[-2]),
                                                         (len(win_probas) - 1, win_probas_best_move[-1]),
                                                         arrowstyle='-|>',
                                                         mutation_scale=20.0,
                                                         linewidth=4,
                                                         linestyle='solid',
                                                         color='red',
                                                         # label = 'Evaluation for the best move'
                                                         )

        plt.gca().add_patch(arrow_proba)
        plt.gca().add_patch(arrow_proba_best_move)

    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

    plt.title("Probabilité de victoire des blancs", fontsize=18, color='red')
    plt.ylabel("Probabilité")
    plt.xlabel("Coups joués")

    min_ = max(-1, len(win_probas) - 5)
    max_ = len(win_probas) + 1
    plt.xlim([min_, max_])

    if save_graph != None:
        saving_graph(save_graph)

    if show_graph:
        plt.show()

    plt.close()

def getNbMoves(game_index, moves_df=moves_df):
    i = 0
    nb = 0
    while moves_df.iloc[i].game_index != game_index:
        i += 1
    while moves_df.iloc[i].game_index == game_index:
        i += 1
        nb += 1
    return nb

def dictCorrespondanceIndex_gameIndex(moves_df):
    dict_corres = {}
    index = 0
    for index in tqdm(range(len(moves_df))):
        game_index = moves_df.iloc[index]['game_index']
        if dict_corres.get(game_index) == None:
            dict_corres[game_index] = index
    return dict_corres

# we first check whether the dictionary has already been calculated
try:
    with open('../Data/Metric_creation/dict_correspondance.pkl', 'rb') as f:
        dict_corres = pickle.load(f)
except:
    dict_corres = dictCorrespondanceIndex_gameIndex(moves_df)
    if not os.path.isdir('../Data/Metric_creation'):
        os.mkdir('../Data/Metric_creation')
    with open('../Data/Metric_creation/dict_correspondance.pkl', 'wb') as f:
        pickle.dump(dict_corres, f)


def playMove(i, board, move_evals, best_move_evals, win_probas, win_probas_best_move):
    engine = chess.engine.SimpleEngine.popen_uci("../Stockfish/stockfish_15_x64_avx2")

    # we get the move to play, following the games in our database
    move = moves_df.iloc[i]['moves']
    move_to_play_on_board = getMove(move)

    # we leverage the chess engine to analyse the current position, before playing our move, to find the best move
    # current_board_analysis = engine.analyse(board, chess.engine.Limit(time=0.5))
    # best_move = current_board_analysis['pv'][0]
    best_move = (engine.play(board, chess.engine.Limit(time=0.5))).move
    best_move_from = best_move.from_square
    best_move_to = best_move.to_square

    # we play the best move on the board, usr the engine to get the evaluation of the position
    # then we'll undo this move and play our move
    board.push(best_move)
    best_move_eval, win_proba_best_move = position_eval(engine, board, time_limit=0.5, return_wdl=True)
    best_move_evals.append(best_move_eval)
    win_probas_best_move.append(win_proba_best_move.expectation())
    board.pop()  # undo the last move

    # we now play our move on the board and get the evaluation
    board.push(move_to_play_on_board)
    eval_, win_proba = get_eval_after_move(move_to_play_on_board, best_move,
                                           best_move_eval, engine, board, time_limit=0.5)
    move_evals.append(eval_)
    win_probas.append(win_proba.expectation())

    engine.close()
    return move_to_play_on_board, best_move_from, best_move_to