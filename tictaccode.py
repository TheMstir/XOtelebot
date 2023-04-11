import random

class Board:
    def __init__(self):
        self.board = [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']]

    def in_action(self, place, do):
        self.board[place].append(do)

        return board

    def step(self):
        count = 0
        for i in self.board:
            print(i, end='')
            count += 1
            if count == 3:
                print('')
                count = 0

    def brake_system(self, player):
        bord = ''
        for i in self.board:
            for j in i:
                bord += j
        if bord[0:3] == player.xo * 3 or bord[3:6] == player.xo * 3 or bord[6:] == player.xo * 3 or bord[0::4] == player.xo * 3 or bord[2:7:2] == player.xo or bord[0:8:3] == player.xo * 3 or bord[1:9:3] == player.xo * 3 or bord[2::3] == player.xo * 3:
            return True
        elif '1' and '2' and '3' and '4' and '5' and '6' and '7' and '8' and '9' not in bord:
            print('Ничья!\n')
            self.board = [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']]


class Player:
    def __init__(self, xo):
        self.name = 'Игрок'
        self.xo = xo
        self.board = Board()

    def do(self, doit, board, name):
        board[doit - 1] = [name]
        #board.board[]

class Ai:
    def __init__(self, player):
        self.name = 'Компьютер'
        self.xo = 'o'
        self.enemy = player

    def doai(self, board):
        rand = random.randint(0, 8)
        while True:
            if board[rand] != ['x'] and board[rand] != ['o']:
                board[rand] = ['o']
                break
            else:
                rand = random.randint(0, 8)


def play(player_1, player_2, board):
    board.step()
    while True:
        print(f'Ходит игрок рисующий {player_1.xo}')
        try:
            player_1.do(int(input('Куда ставим крестик?: ')), board.board, player_1.xo)
        except ValueError:
            print('Пропуск хода. Да именно так')
        board.step()

        if board.brake_system(player_1):
            print(f'Победил {player_1.name} {player_1.xo}\n')
            break

        if player_2.name == 'Игрок':
            print(f'Ходит игрок рисующий {player_2.xo}')
            try:
                player_2.do(int(input('Куда ставим нолик?: ')), board.board, player_2.xo)
            except ValueError:
                print('Пропуск хода. Да именно так')
        elif player_2.name == 'Компьютер':
            print('Ходит Суперкомпьютер')
            player_2.doai(board.board)
        if board.brake_system(player_2):
            print(f'Победил {player_2.name} {player_2.xo}\n')
            break
        board.step()



board = Board()
player_1 = Player('x')
player_2 = Player('o')
comp = Ai(player_1)

print('Игра крестики-нолики\n(клетки слева направо-сверху вниз), для хода нужно ввести цифру')
ask = input('Будем играть вдвоем или с компьютером? (2/1): ')
if ask == '1':
    play(player_1, comp, board)
elif ask == '2':
    play(player_1, player_2, board)
