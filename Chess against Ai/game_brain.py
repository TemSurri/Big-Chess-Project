
from render_game_prep import *
import time

class Node:
    def __init__(self,i,pieces, c, v):
        self.imm = i
        self.pieces = pieces
        self.value = v
        #c = [(move, child_node)...]
        self.children = c
        self.defining_move = None

class Game:
    def __init__(self, screen, pygame, screen_size, color, **type_chess):

        self.maximizing_agent = "black"
        self.minimizing_agent = "white"
        if type_chess:
            print("customize type")
        else:
            self.current_game = ConventionalChessSetUp(screen, pygame, screen_size, color)
        self.current_turn = ""
        self.current_color = ''

    def dynamic_attributes(self, pieces, occupancy, color):
        self.current_game = self.current_game
        team = [piece for piece in pieces if piece.color == color]

        all_team_moves = [(x, x.move_outline(occupancy)) for x in team]

        moves_ = []
        for x in all_team_moves:
            moves = x[1]
            original_spot = x[0].current_quadrant
            for move in moves:
                moves_.append((original_spot, move[2]))

        enemies = [piece for piece in pieces if piece.color != color]


        all_enemy_moves = [x.move_outline(occupancy) for x in enemies]


        targeted_quadrants = []
        for x in all_enemy_moves:
            for move in x:
                targeted_quadrants.append(move[2])

        king = [piece for piece in pieces if piece.color == color and piece.name.lower() == "king"][0]

        return [king, [team, moves_], [enemies, targeted_quadrants]]

    def move(self, piece, spot):

        possible_spots = piece.move_outline(self.current_game.quadrant_current_occupancy)
        print(piece.name, possible_spots)

        if piece.name == "king" or "rook":
            attempt = piece.change_spot(spot, possible_spots, self.current_game.quadrant_current_occupancy,
                                        self.current_game.pieces)
        else:
            attempt = piece.change_spot(spot, possible_spots, self.current_game.quadrant_current_occupancy)

        if attempt[1] == "error":
            return False
        if attempt[0] != 0:
            for x in self.current_game.pieces:
                if x.current_quadrant == spot and x.side != piece.side:
                    self.current_game.pieces.remove(x)
        if piece.name.lower() == "pawn":
            if piece.side == "upper" and spot[1] == 8:
                self.pawn_promotion(piece)
            if piece.side == "lower" and spot[1] == 1:
                self.pawn_promotion(piece)

        self.current_game.update_occupancy()
        return True

    def get_requested_quadrant(self, cord):
        x_i = float(cord[0])
        y_i = float(cord[1])

        all_quadrants = self.current_game.board_info.quadrants
        quadrant_range = float(self.current_game.board_info.quadrant_size)

        x_f = [x[2][0] for x in all_quadrants if float(x[1][0]) > x_i > (float(x[1][0]) - quadrant_range )]
        y_f = [x[2][1] for x in all_quadrants if float(x[1][1]) > y_i > (float(x[1][1]) - quadrant_range)]
        if len(x_f) == 0 or len(y_f) == 0:
            return False
        cord = (x_f[0], y_f[0])
        return cord

    def wait_click(self):
        click = False
        pygame = self.current_game.board_info.pygame
        while not click:

            events = pygame.event.get()

            for event in events:
                if str(event) == "<Event(256-Quit {})>":
                    return False
                if event.type == pygame.MOUSEBUTTONUP:

                    pos = pygame.mouse.get_pos()
                    return pos

    def move_process(self, eligible_moves):

        first_click = self.wait_click()

        if not first_click:
            print("end game")
            return "END"

        #don't worry if first_click not slice-able list it won't get here
        cord = (first_click[0]-60, first_click[1]-60)

        cord = self.get_requested_quadrant(cord)
        requested_spot = str(cord)

        selected_piece = [x for x in self.current_game.pieces if str(x.current_quadrant) == str(requested_spot) and str(x.side) == str(self.current_turn)]

        if len(selected_piece) == 1:
            piece = selected_piece[0]

            second_click = self.wait_click()



            cord1 = (second_click[0] - 60, second_click[1] - 60)
            cord1 = self.get_requested_quadrant(cord1)


            if not second_click:
                print("end game")
                return "END"

            requested_move = cord1

            move = (eval(requested_spot), requested_move)


            if move not in eligible_moves:
                print("move not eligible")
                return False

            attempt_move = self.move(piece, requested_move)
            if not attempt_move:
                return False
            return True
        else:
            print("No pieces found")
            return False

    def test_move(self, initial, final, pieces):
        v_pieces = self.current_game.create_virtual_pieces_stats(pieces)
        occ = self.current_game.create_occupancy(pieces)

        piece = [x for x in v_pieces if x.current_quadrant == initial][0]

        if piece.name == "king" or "rook":
            piece.change_spot(final, piece.move_outline(occ), occ, v_pieces)
        else:
            piece.change_spot(final, piece.move_outline(occ), occ)

        for x in v_pieces:
            if x.current_quadrant == final and x.side != piece.side:
                v_pieces.remove(x)

        v_occupancy = [[x.current_quadrant, x.side, x.name, x.color, x.times_moved] for x in v_pieces]

        all_enemy_moves = [x.move_outline(v_occupancy) for x in v_pieces if x.side != piece.side]
        targeted_quadrants = []
        for x in all_enemy_moves:
            for move in x:
                targeted_quadrants.append(move[2])

        v_king = [x for x in v_pieces if x.name == "king" and x.side == piece.side][0]

        return [targeted_quadrants, v_king]

    def check(self, targeted_quadrants, king):
        self.current_game = self.current_game
        king_quadrant = king.current_quadrant
        if king_quadrant in targeted_quadrants:
            return True
        else:
            return False

    def pawn_promotion(self, pawn):
        side = pawn.side
        quadrant = pawn.current_quadrant
        all_quadrants = self.current_game.quadrant_classifications
        self.current_game.pieces.remove(pawn)
        new_queen = Queen(quadrant, "queen", all_quadrants, side)
        new_queen.color = pawn.color

        images = self.current_game.images[new_queen.color]
        image = [x[1] for x in images if x[0].lower() == "queen"][0]
        new_queen.image = image



        self.current_game.pieces.append(new_queen)

    def all_eligible(self, team_moves, pieces):
        eligible_moves = []
        for move in team_moves:

            info = (self.test_move(move[0], move[1], pieces))
            targeted_quadrants = info[0]
            king = info[1]

            check = self.check(targeted_quadrants, king)

            if not check:
                eligible_moves.append(move)
        return eligible_moves

    def evaluate_board(self, pieces):
        values = {"pawn":1, "bishop":3, "rook":4.5, "knight": 3, "queen" : 9, "king" : 5}

        max_pieces = [x.name for x in pieces if x.color == self.maximizing_agent]
        min_pieces = [x.name for x in pieces if x.color == self.minimizing_agent]
        state_value = 0

        for x in max_pieces:
            state_value += values[x]
        for x in min_pieces:
            state_value -= values[x]

        return state_value

    def evaluate_threats(self, pieces, **min_move):
        values = {"pawn": 1, "bishop": 3, "rook": 3.5, "knight": 3, "queen": 9, "king": 5}
        state_value = 0

        occ = self.current_game.create_occupancy(pieces)
        all_maximizing_moves = []
        all_minimizing_moves = []

        max_moves = []
        min_moves = []

        for x in pieces:
            if x.color == self.maximizing_agent:
                moves = x.move_outline(occ)
                for move in moves:
                    max_moves.append((x.current_quadrant,move[2]))
                    all_maximizing_moves.append(move[2])
            if x.color == self.minimizing_agent:
                moves = x.move_outline(occ)
                for move in moves:
                    min_moves.append((x.current_quadrant, move[2]))
                    all_minimizing_moves.append(move[2])

        spots_for_min = all_minimizing_moves
        spots_for_max = all_maximizing_moves

        for x in pieces:
            if x.color == self.maximizing_agent:
                if x.current_quadrant in spots_for_min:
                    if x.name.lower() == "king":
                        escapes = self.all_eligible(max_moves, pieces)

                        if not escapes:
                            state_value -= 10000
                    else:

                        if min_move:
                            state_value -= values[x.name]/3

                        else:
                            state_value -= values[x.name]

            if x.color == self.minimizing_agent:

                if x.current_quadrant in spots_for_max:
                    if x.name.lower() == "king":

                        escapes = self.all_eligible(min_moves, pieces)
                        if not escapes:
                            state_value += 10000
                    else:
                        if min_move:
                            state_value += values[x.name]
                        else:
                            state_value += values[x.name]/3
        return state_value

    def evaluate_state(self, pieces, **min_move):
        if min_move:
            return(self.evaluate_board(pieces)*2) +(self.evaluate_threats(pieces)/2)
        return (self.evaluate_board(pieces)*2)+(self.evaluate_threats(pieces, min_move = True)/2)

    def shallow_heuristic_search(self, pieces, all_moves, **mini):

        valued_moves = []

        for move in all_moves:
            new_pieces = self.current_game.create_virtual_pieces_stats(pieces)
            piece = [x for x in new_pieces if x.current_quadrant == move[0]][0]
            piece.current_quadrant = move[1]

            for x in new_pieces:
                if piece.side != x.side:
                    if x.current_quadrant == piece.current_quadrant:
                        new_pieces.remove(x)

            if mini:
                value = self.evaluate_state(new_pieces, mini = True)
            else:
                value = self.evaluate_state(new_pieces)

            valued_moves.append([piece, move[1], value, move[0]])
        #for x in valued_moves:
         #   print(x[2], (x[3], x[1]))
        largest = ["f", "f",-1000000]
        if mini:
            largest = ["f", "f", 10000000]

        for x in valued_moves:
            if mini:
                if x[2] < largest[2]:
                    largest = x
            else:
                if x[2] > largest[2]:
                    largest = x

        piece = [x for x in pieces if x.current_quadrant == largest[3]][0]
        move = largest[1]
        value = largest[2]

        return piece, move, value

    def base_game(self, **ai):
        game = True
        generation = 0
        ai_moves = []
        while game:
            side = self.current_game.white[0] if generation % 2 == 0 else self.current_game.black[0]
            moving_color = self.current_game.white[1] if generation % 2 == 0 else self.current_game.black[1]
            self.current_turn = side
            self.current_color = moving_color

            king_team_enemy_info = self.dynamic_attributes(self.current_game.pieces, self.current_game.quadrant_current_occupancy, self.current_color)

            targeted_quadrants = king_team_enemy_info[2][1]

            team_moves = king_team_enemy_info[1][1]
            king = king_team_enemy_info[0]

            check = self.check(targeted_quadrants, king)

            eligible_moves = self.all_eligible(team_moves, self.current_game.pieces)

            if check:
                print("check")
            if check and eligible_moves == []:
                print("check_mate")
                return f"check_mated, loss for {moving_color}"
            if not eligible_moves:
                print("draw")
                time.sleep(2)
                return "draw"

            print(f"TURN FOR {self.current_color}")
            if ai:


                if generation % 2 != 0:
                    piece, move = self.mini_max_algorithm(self.current_game.pieces, eligible_moves, self.current_color)

                    #piece, move, value = self.shallow_heuristic_search(self.current_game.pieces, eligible_moves)
                    #return top 3 moves with values, the more times already moved                     
                    ai_moves.append(move)

                    self.move(piece, move)

                else:

                    turn = self.move_process(eligible_moves)
                    if turn == "END":
                        return "END"
                    while not turn:
                        turn = self.move_process(eligible_moves)
                        if turn == "END":
                            return "END"
                    else:
                        print(self.current_game.quadrant_current_occupancy)

            else:

                turn = self.move_process(eligible_moves)
                if turn == "END":
                    return "END"
                while not turn:
                    turn = self.move_process(eligible_moves)
                    if turn == "END":
                        return "END"
                else:
                    print(self.current_game.quadrant_current_occupancy)

            generation += 1

    def get_moves(self, pieces, color):
        info = self.dynamic_attributes(pieces, self.current_game.create_occupancy(pieces), color)
        team_moves = info[1][1]
        all_moves = self.all_eligible(team_moves, pieces)
        return all_moves

    def virtual_move(self, move, pieces):
        new_pieces = self.current_game.create_virtual_pieces_stats(pieces)
        piece = [piece for piece in new_pieces if move[0] == piece.current_quadrant][0]

        occ = self.current_game.create_occupancy(new_pieces)
        for x in new_pieces:
            if x.current_quadrant == move[1] and x.color != piece.color:
                new_pieces.remove(x)

        piece.change_spot(move[1], piece.move_outline(occ), occ)
        return new_pieces

    def create_nodes(self, pieces, moves, f_m):

        #static creation of 2 depths of nodes, due to time constraints

        if f_m == self.maximizing_agent:
            s_m = self.minimizing_agent
        else:
            s_m = self.maximizing_agent

        gen1 = Node(0, pieces, None, self.evaluate_state(pieces))
        children1 = []
        for move in moves:
            new_pieces = self.virtual_move(move, pieces)
            state = Node(1, new_pieces, None, self.evaluate_state(new_pieces, min_move = True))
            state.defining_move = move

            new_moves = self.get_moves(new_pieces, s_m)
            children2 = []
            for mo in new_moves:
                newer_pieces = self.virtual_move(mo, new_pieces)
                state2 = Node(2, newer_pieces, None, self.evaluate_state(newer_pieces))
                state2.defining_move = mo
                children2.append(state2)
            state.children = children2
            children1.append(state)
        gen1.children = children1

        for x in gen1.children:
            print(x.defining_move, x.value)
            for f in x.children:
                print("          ", f.defining_move, f.value)

        return gen1

    def mini_max_algorithm(self, pieces, moves, f_m):
        mother_node = self.create_nodes(pieces, moves, f_m)
        #move = self.non_recursive_minimax(mother_node)
        move = self.recursive_mini_max(2, mother_node, True).defining_move

        piece = [piece for piece in pieces if piece.current_quadrant == move[0]][0]
        spot = move[1]
        print(move)
        return piece, spot

    def recursive_mini_max(self, depth, node, maximum):
        if depth == 0:
            return node

        if maximum:
            max_val = -10000
            ideal_node = None
            for child in node.children:
                val = self.recursive_mini_max(depth-1, child, False).value
                if val > max_val:

                    node.value = max_val
                    max_val = val
                    ideal_node = child

            if not ideal_node:
                return node

            return ideal_node

        else:
            min_val = 10000
            ideal_node = None
            for child in node.children:
                val = self.recursive_mini_max(depth - 1, child, True).value
                if val < min_val:

                    min_val = val
                    node.value = min_val
                    ideal_node = child

            if not ideal_node:
                return node

            return ideal_node
