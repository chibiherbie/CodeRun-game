import string
from random import choices, randint


class Game:
    def __init__(self):
        self.game_started = False
        self.code_game = ''
        self.maze = ''
        self.players_code = {}
        self.map_matrix = []
        self.pos_player = [1, 0]

    def create_code_game(self, len_code=4) -> str:
        self.code_game = ''.join(choices(string.ascii_uppercase + string.digits, k=len_code))
        return self.code_game

    def create_user_code(self, info):
        self.players_code[info['user']] = info['code']
        print(self.players_code)

    def choice_map(self):
        pass

    def check_code_user(self, step):
        # print(self.map_matrix)
        # print(self.map_matrix[1][0])
        # print(self.map_matrix[1][1])
        print('STEP', self.pos_player[1] + step[1])
        print(self.pos_player)
        # print(self.pos_player[0] + step[0], self.pos_player[1] + step[1])

        return False

        if self.map_matrix[self.pos_player[0] + step[0]][self.pos_player[1] + step[1]] == '0':
            self.pos_player = [self.pos_player[0] + step[0], self.pos_player[1] + step[1]]
            return True
        return False

    def open_map(self):
        with open(f'src/static/img/maze/{self.maze}.txt') as f:
            self.map_matrix = [i for i in f.readlines()]

    def start_game(self):
        self.game_started = True
        self.pos_player = [1, 0]
        self.maze = randint(1, 10)
        self.open_map()

        return self.maze

    def end_game(self):
        self.game_started = False
        return self.players_code


if __name__ == '__main__':
    game = Game()
    print(game.create_code_game())
    game.start_game()
    print(game.check_code_user((0, 1)))
