# programa jogador de Othello
#classe para definição de atributos e funções do player
class Othelleiro:
    def __init__(self, color, depth=4):
        from models.board import Board
        self.color = color
        self.depth = depth
        self.opponent_color = Board.BLACK if color is Board.WHITE else Board.WHITE

    def evaluate_board(self, board):
        return (self.corner_evaluation(board) * 10) + (self.score_evaluation(board) / 100) + self.mobility_evaluation(board)

    def corner_evaluation(self, board):
        count = 0
        opp_count = 0
        if board.get_square_color(1, 1) == self.color:
            count += 1
        elif board.get_square_color(1, 1) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(1, 8) == self.color:
            count += 1
        elif board.get_square_color(1, 8) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(8, 1) == self.color:
            count += 1
        elif board.get_square_color(8, 1) == self.opponent_color:
            opp_count += 1
        if board.get_square_color(8, 8) == self.color:
            count += 1
        elif board.get_square_color(8, 8) == self.opponent_color:
            opp_count += 1

        return count - opp_count

    def score_evaluation(self, board):
        from models.board import Board

        score = board.score()

        if self.color == Board.WHITE:
            return score[0] - score[1]
        else:
            return score[1] - score[0]

    def mobility_evaluation(self, board):
        return len(board.valid_moves(self.color)) - len(board.valid_moves(self.opponent_color))

    def play(self, board):

        depth = self.depth if not self.game_is_ending(board) else 8
        value, move = self.evaluate(
            board, 1, depth, -float("inf"), float("inf"))

        return move

    def game_is_ending(self, board):
        score = board.score()
        return (64 - score[1] - score[0]) <= 10

    def endgame(self, board):
        return len(board.valid_moves(self.color)) == 0 and len(board.valid_moves(self.opponent_color)) == 0

    def evaluate_endgame_board(self, board):
        from models.board import Board

        score = board.score()
        if score[0] > score[1]:
            if self.color == Board.WHITE:
                return 10000 + score[0]
            else:
                return -10000
        elif score[1] > score[0]:
            if self.color == Board.BLACK:
                return 10000 + score[1]
            else:
                return -10000
        else:
            return -10000

    # Função para encontrar o melhor movimento naquele momento dentro de um tabuleiro
    # board = tabuleiro da partida
    # nodeType = 1 para MAX
    # nodeType = -1 caso seja MIN
    # depth = profundidade que a busca percorreu
    def evaluate(self, board, node_type, depth, alpha, beta):
        # se ainda nao chegou no final
        endgame = self.endgame(board)
        if depth > 0 and not endgame:
            if node_type == 1:
                cur_value = alpha
                comp = max
                color = self.color
            else:
                cur_value = beta
                comp = min
                color = self.opponent_color
            cur_move = None
            # caso não haja movimento, passar a vez
            if len(board.valid_moves(color)) == 0:
                value, move = self.evaluate(
                    board, -node_type, depth - 1, alpha, beta)
                return value, move
            # para cada movimento possivel
            for move in board.valid_moves(color):
                # faz um clone do board, em que o movimento foi feito
                child = board.get_clone()
                child.play(move, color)
                # pega o valor do nó filho, ignorando o movimento
                # na chamada recursiva, inverte o tipo e reduz a profundidade
                if node_type == 1:
                    value, ignore = self.evaluate(
                        child, -node_type, depth - 1, cur_value, beta)
                else:
                    value, ignore = self.evaluate(
                        child, -node_type, depth - 1, alpha, cur_value)

                if comp([cur_value, value]) == value:
                    cur_value = value
                    cur_move = move
                if node_type == 1:
                    if cur_value >= beta:
                        return cur_value, cur_move
                else:
                    if cur_value <= alpha:
                        return cur_value, cur_move
            # Melhor valor e melhor movimento
            return cur_value, cur_move
        else:
            if endgame:
                return self.evaluate_endgame_board(board), None
            else:
                return self.evaluate_board(board), None
