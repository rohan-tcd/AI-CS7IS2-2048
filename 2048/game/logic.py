
import random

def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix

def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while(mat[a][b] != 0):
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat

def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    for i in range(len(mat) - 1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0]) - 1):
            if mat[i][j] == mat[i + 1][j] or mat[i][j + 1] == mat[i][j]:
                return 'not over'
    for i in range(len(mat)):  # check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    for k in range(len(mat) - 1):  # to check the left/right entries on the last row
        if mat[len(mat) - 1][k] == mat[len(mat) - 1][k + 1]:
            return 'not over'
    for j in range(len(mat) - 1):  # check up/down entries on last column
        if mat[j][len(mat) - 1] == mat[j + 1][len(mat) - 1]:
            return 'not over'
    return 'lose'

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0]) - j - 1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    done = False
    for i in range(4):
        count = 0
        for j in range(4):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def get_empty_cells(mat):
    count = 0
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 0:
                count += 1

    return count


def get_weighted_cell_score(mat):
    weighted_score = 0
    weight_matrix = [[7, 6, 5, 4], [6, 5, 4, 3], [5, 4, 3, 2], [4, 3, 2, 1]]
    for i in range(4):
        for j in range(4):
                weighted_score += mat[i][j]*weight_matrix[i][j]
    return weighted_score

def merge(mat):
    done = False
    local_score = 0
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                local_score += mat[i][j]
                mat[i][j + 1] = 0
                done = True
    empty_cells_count = get_empty_cells(mat)
    weighted_cell_score = get_weighted_cell_score(mat)
    return mat, done, local_score, empty_cells_count, weighted_cell_score


def up(game):
    # return matrix after shifting up
    game = transpose(game)
    game, d = cover_up(game)
    mat, done, local_score, empty_cells_count, weighted_cell_score = merge(game)
    game = mat
    done = d or done
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done, local_score, empty_cells_count, weighted_cell_score


def down(game):
    game = reverse(transpose(game))
    game, d = cover_up(game)
    mat, done, local_score, empty_cells_count, weighted_cell_score = merge(game)
    game = mat
    done = done or d
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done, local_score, empty_cells_count, weighted_cell_score


def left(game):
    # return matrix after shifting left
    game, d = cover_up(game)
    mat, done, local_score, empty_cells_count, weighted_cell_score = merge(game)
    game = mat
    done = done or d
    game = cover_up(game)[0]
    return game, done, local_score, empty_cells_count, weighted_cell_score


def right(game):
    # return matrix after shifting right
    game = reverse(game)
    game, d = cover_up(game)
    game, done, local_score, empty_cells_count, weighted_cell_score = merge(game)
    game = game
    done = done or d
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done, local_score, empty_cells_count, weighted_cell_score
