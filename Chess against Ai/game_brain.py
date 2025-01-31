from render_game_prep import *
class Game:
    def __init__(self, screen, pygame, screen_size, color, **type_chess):

        if type_chess:
            print("customize type")
        else:
            self.current_game = ConventionalChessSetUp(screen, pygame, screen_size, color)
        self.current_turn = ""

    def dynamic_attributes(self):
        team = [piece for piece in self.current_game.pieces if piece.side == self.current_turn]

        all_team_moves = [(x, x.move_outline(self.current_game.quadrant_current_occupancy)) for x in team]

        moves_ = []
        for x in all_team_moves:
            moves = x[1]
            original_spot = x[0].current_quadrant
            for move in moves:
                moves_.append((original_spot, move[2]))

        enemies = [piece for piece in self.current_game.pieces if piece.side != self.current_turn]


        all_enemy_moves = [x.move_outline(self.current_game.quadrant_current_occupancy) for x in enemies]


        targeted_quadrants = []
        for x in all_enemy_moves:
            for move in x:
                targeted_quadrants.append(move[2])

        king = [piece for piece in self.current_game.pieces if piece.side == self.current_turn and piece.name.lower() == "king"][0]

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

        cord = (first_click[0]-60, first_click[1]-60)
        cord = self.get_requested_quadrant(cord)
        requested_spot = str(cord)

        selected_piece = [x for x in self.current_game.pieces if str(x.current_quadrant) == str(requested_spot) and str(x.side) == str(self.current_turn)]

        if len(selected_piece) == 1:
            piece = selected_piece[0]

            second_click = self.wait_click()
            if not second_click:
                print("end game")
                return "END"
            cord1 = (second_click[0] - 60, second_click[1] - 60)
            cord1 = self.get_requested_quadrant(cord1)
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

    def test_move(self, initial, final):
        v_pieces = self.current_game.create_virtual_pieces_stats()

        piece = [x for x in v_pieces if x.current_quadrant == initial][0]


        if piece.name == "king" or "rook":
            piece.change_spot(final, piece.move_outline(self.current_game.quadrant_current_occupancy), self.current_game.quadrant_current_occupancy, v_pieces)
        else:
            piece.change_spot(final, piece.move_outline(self.current_game.quadrant_current_occupancy), self.current_game.quadrant_current_occupancy)
        #piece.x = final[0]
        #piece.y = final[1]
        #piece.current_quadrant = final

        for x in v_pieces:
            if x.current_quadrant == final and x.side != piece.side:
                v_pieces.remove(x)

        v_occupancy = [[x.current_quadrant, x.side, x.name] for x in v_pieces]

        all_enemy_moves = [x.move_outline(v_occupancy) for x in v_pieces if x.side != self.current_turn]
        targeted_quadrants = []
        for x in all_enemy_moves:
            for move in x:
                targeted_quadrants.append(move[2])

        v_king = [x for x in v_pieces if x.name == "king" and x.side == self.current_turn][0]
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

        color = [x[1] for x in [self.current_game.black, self.current_game.white] if x[0] == side][0]
        images = self.current_game.images[color]
        image = [x[1] for x in images if x[0].lower() == "queen"][0]
        new_queen.image = image



        self.current_game.pieces.append(new_queen)

    def all_eligible(self, team_moves):
        eligible_moves = []
        for move in team_moves:
            info = (self.test_move(move[0], move[1]))
            targeted_quadrants= info[0]
            king = info[1]
            check = self.check(targeted_quadrants, king)

            if not check:
                eligible_moves.append(move)
        return eligible_moves

    def draw_(self, team_moves, king, targeted_quadrants):

        king_move_outline = king.move_outline(self.current_game.quadrant_current_occupancy)
        king_moves = [(king.current_quadrant, move[2]) for move in king_move_outline]

        total_moves = int(len(team_moves))
        total_king_moves = int(len(king_moves))

        safe_moves = 0
        for x in king_moves:
            if x[1] not in targeted_quadrants:
                safe_moves +=1

        if total_moves == total_king_moves and safe_moves == 0:
            return True
        else:
            return False

    def base_game(self):
        game = True
        generation = 0

        while game:
            side = self.current_game.white[0] if generation % 2 == 0 else self.current_game.black[0]
            moving_color = self.current_game.white[1] if generation % 2 == 0 else self.current_game.black[1]
            self.current_turn = side
            king_team_enemy_info = self.dynamic_attributes()

            targeted_quadrants = king_team_enemy_info[2][1]

            team_moves = king_team_enemy_info[1][1]
            king = king_team_enemy_info[0]

            check = self.check(targeted_quadrants, king)
            draw = self.draw_(team_moves, king, targeted_quadrants)
            eligible_moves = self.all_eligible(team_moves)

            if check:
                print("check")
            else:
                if draw:
                    print("draw")
                    return "draw"
            if check and eligible_moves == []:
                print("check_mate")
                return f"check_mated, loss for {moving_color} "

            print(f"TURN FOR {side}")

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















