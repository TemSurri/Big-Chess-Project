import random
import os

addresses = str(__file__).split("/")
addresses.pop()
addresses.append("chess_pieces_imgs")
pieces_folder = "/".join(addresses)
pieces_paths = []
for file in os.listdir(pieces_folder):
    filename = os.fsdecode(file)
    if str(filename[-3]+filename[-2]+filename[-1]) == "png":
        pieces_paths.append("/".join([pieces_folder, file]))

def classify_images(paths):
    pieces = {}

    white_organized_pieces = []
    black_organized_pieces = []

    for path in paths:

        if path[-8] == "l":
            if path[-9] == "b":
                white_organized_pieces.append(["bishop", path])
            if path[-9] == "p":
                white_organized_pieces.append(["pawn", path])
            if path[-9] == "r":
                white_organized_pieces.append(["rook", path])
            if path[-9] == "q":
                white_organized_pieces.append(["queen", path])
            if path[-9] == "k":
                white_organized_pieces.append(["king", path])
            if path[-9] == "n":
                white_organized_pieces.append(["knight", path])
        if path[-8] == "d":
            if path[-9] == "b":
                black_organized_pieces.append(["bishop", path])
            if path[-9] == "p":
                black_organized_pieces.append(["pawn", path])
            if path[-9] == "r":
                black_organized_pieces.append(["rook", path])
            if path[-9] == "q":
                black_organized_pieces.append(["queen", path])
            if path[-9] == "k":
                black_organized_pieces.append(["king", path])
            if path[-9] == "n":
                black_organized_pieces.append(["knight", path])
    pieces["white"] = white_organized_pieces
    pieces["black"] = black_organized_pieces
    return pieces

classified_images = classify_images(pieces_paths)

class BoardBackgroundPieces:

    def __init__(self, screen, pygame, size):
        self.domain = [1,2,3,4,5,6,7,8]
        self.range = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.screen =  screen
        self.screen_size = size
        self.quadrant_size = self.screen_size/10
        self.locations = [(self.screen_size/10)* i for i in range(0,10)]
        self.pygame = pygame
        self.screen.fill("white")
        self.pygame.display.flip()
        self.board_dimensions = [x for i, x in enumerate(self.locations) if i != 0 and i != 9]
        self.quadrants = []
        self.keys = [str(i+1)+y for i, y in enumerate(self.range)]
        self.occupied_quadrants = []
        self.classified_images = classified_images


        for i, x in enumerate(self.board_dimensions):
            for iy, y in enumerate(self.board_dimensions):
                self.quadrants.append([str(self.domain[i])+str(self.range[iy]), (x,y),(i+1,iy+1)])
    def write_list(self,x,y, i, list_, c):
        self.pygame.display.set_caption("Chess InterFace")
        font = self.pygame.font.Font('freesansbold.ttf', int(self.quadrant_size))
        text = font.render(str(list_[i]), True, c)
        text_rect = text.get_rect()
        text_rect.center = (int(x)+int(self.quadrant_size/2.4), int(y)+int(self.quadrant_size/2))
        self.screen.blit(text, text_rect)

    def render_params(self):
        locations_numbers = [(x, self.locations[0]) for x in self.board_dimensions]
        locations_numbers_2 = [(x, self.locations[9]) for x in self.board_dimensions]
        locations_letters = [(self.locations[0], y) for y in self.board_dimensions]
        locations_letters_2 = [(self.locations[9], y) for y in self.board_dimensions]
        for i, x in enumerate(locations_letters):
            self.pygame.draw.rect(self.screen, "grey", (x[0], x[1], self.quadrant_size, self.quadrant_size))
            self.write_list(x[0], x[1], i, self.range, "black")
        for i, x in enumerate(locations_letters_2):
            self.pygame.draw.rect(self.screen, "grey", (x[0], x[1], self.quadrant_size, self.quadrant_size))
            self.write_list(x[0], x[1], i, self.range, "black")
        for i, x in enumerate(locations_numbers):
            self.pygame.draw.rect(self.screen, "black", (x[0], x[1], self.quadrant_size, self.quadrant_size))
            self.write_list(x[0], x[1], i, self.domain, "grey")
        for i, x in enumerate(locations_numbers_2):
            self.pygame.draw.rect(self.screen, "black", (x[0], x[1], self.quadrant_size, self.quadrant_size))
            self.write_list(x[0], x[1], i, self.domain, "grey")
    def fill_board(self, color):
        for i, y in enumerate(self.board_dimensions):
            if i % 2 == 0:
                for ix, x in enumerate(self.board_dimensions):
                    if ix % 2 == 0:
                       self.pygame.draw.rect(self.screen, color , (x, y, self.quadrant_size, self.quadrant_size))
            if i % 2 != 0:
                for ix, x in enumerate(self.board_dimensions):
                    if (ix+1) % 2 == 0:
                       self.pygame.draw.rect(self.screen, color , (x, y, self.quadrant_size, self.quadrant_size))
    def render_pieces(self, organized_images, positions):
        scale = self.quadrant_size

        images = []

        for item in positions:
            team = organized_images[item[1]]
            for x in team:
                if item[0] == x[0]:
                    image = x[1]
                    location = item[2]

                    piece = self.pygame.image.load(image)
                    piece = self.pygame.transform.scale(piece, (scale, scale))
                    self.screen.blit(piece, location)
                    self.pygame.display.update()

                    images.append((item[0], item[1], image))
        self.pygame.display.update()
        return images
    def update_pieces(self, pieces_list):
        scale = self.quadrant_size
        for piece in pieces_list:
            image = piece.image
            quadrant = piece.current_quadrant
            location = [x[1] for x in self.quadrants if x[2] == quadrant][0]

            piece = self.pygame.image.load(image)
            piece = self.pygame.transform.scale(piece, (scale, scale))
            self.screen.blit(piece, location)
            self.pygame.display.update()
    def create(self, color):
        self.screen.fill("white")
        self.render_params()
        self.fill_board(color)
        self.pygame.display.flip()

class PieceFoundational:
    def __init__(self, start_quadrant, name, quadrants, side, *times_moved):
        self.all_cords = quadrants
        self.name = name
        self.side = side
        self.color = ""

        self.starting_quadrant = start_quadrant
        self.current_quadrant = start_quadrant
        self.image = ""
        if times_moved:
            self.times_moved = times_moved[0]
        else:
            self.times_moved = 0

        self.pawn_direction = ""

        if self.side == "lower":
            self.pawn_direction = "up"
        if self.side == "upper":
            self.pawn_direction = "down"

    def castling(self, occupancy):

        if self.times_moved != 0:
            return []

        king_spot = [x[0] for x in occupancy if x[2] == "king" and x[1] == self.side and x[4]==0]
        if len(king_spot) == 0:
            return []
        else:
            king_spot = king_spot[0]
        closer_rook_ = [[x[0], x[4]] for x in occupancy if x[2] == "rook" and x[1] == self.side and abs(x[0][0] - king_spot[0]) == 3]
        further_rook_ = [[x[0], x[4]] for x in occupancy if x[2] == "rook" and x[1] == self.side and abs(x[0][0] - king_spot[0]) == 4]


        king_moves = []
        further_rook_moves = []
        closer_rook_moves = []

        if len(closer_rook_) == 1:

            closer_rook = closer_rook_[0][0]
            c_moved = closer_rook_[0][1]

            larger_num = closer_rook[0] if closer_rook[0] > king_spot[0] else king_spot[0]
            smaller_num = closer_rook[0] if king_spot[0] > closer_rook[0] else king_spot[0]

            blockage = [x for x in occupancy if larger_num > x[0][0] > smaller_num and x[0][1] == king_spot[1]]

            if not blockage and c_moved == 0:

                king_moves.append(closer_rook)
                closer_rook_moves.append(king_spot)

        else:
            closer_rook = False

        if len(further_rook_) == 1:
            further_rook = further_rook_[0][0]
            f_moved = further_rook_[0][1]
            larger_num = further_rook[0] if further_rook[0] > king_spot[0] else king_spot[0]
            smaller_num = further_rook[0] if king_spot[0] > further_rook[0] else king_spot[0]
            blockage = [x for x in occupancy if larger_num > x[0][0] > smaller_num and x[0][1] == king_spot[1]]

            if not blockage and f_moved == 0:

                king_moves.append(further_rook)
                further_rook_moves.append(king_spot)

        else:
            further_rook = False

        king_moves = [x for x in self.all_cords if x[2] in king_moves]
        further_rook_moves = [x for x in self.all_cords if x[2] in further_rook_moves]
        closer_rook_moves = [x for x in self.all_cords if x[2] in closer_rook_moves]

        if self.name == "king":
            return king_moves


        elif self.name.lower() == "rook":

            if str(self.current_quadrant) == str(closer_rook):
                return closer_rook_moves
            elif str(self.current_quadrant) == str(further_rook):
                return further_rook_moves
            else:
                return []
        else:
            return []

    def change_spot(self, cord, move_outline, occupancy, *pieces, **no_castle):

        enemies = [x[0] for x in occupancy if x[1] != self.side]
        spots = [x[2] for x in move_outline]

        if cord in spots:
            if no_castle:
                self.times_moved =+ 1
                self.current_quadrant = cord

                if cord in enemies:
                    return [cord, "remove enemy at this location this turn"]
                else:
                    return [0, "moved"]

            if pieces:

                castle_able_king = [king for king in pieces[0] if king.name == "king" and self.side == king.side and king.times_moved == 0]
                castle_able_rooks = [rook for rook in pieces[0] if rook.name == "rook" and self.side == rook.side and rook.times_moved == 0]

                if len(castle_able_king) == 0:
                    pass

                else:
                    king_spot = castle_able_king[0].current_quadrant
                    further_rook = [x for x in castle_able_rooks if abs(x.current_quadrant[0] - king_spot[0]) == 4]
                    closer_rook = [x for x in castle_able_rooks if abs(x.current_quadrant[0] - king_spot[0]) == 3]

                    move_able = [king_spot]
                    for x in further_rook+closer_rook:
                        move_able.append(x.current_quadrant)

                    if cord in move_able:
                        print("castle")

                        further_swap = []
                        closer_swap = []

                        if len(closer_rook) == 1:
                            closer_rook_ = closer_rook[0].current_quadrant

                            larger_num = closer_rook_[0] if closer_rook_[0] > king_spot[0] else king_spot[0]


                            if closer_rook_[0] == larger_num:
                                x_cord = king_spot[0] + 2
                                x_r_cord = closer_rook_[0] - 2
                            else:
                                x_cord = king_spot[0] - 2
                                x_r_cord = closer_rook_[0] + 2

                            king_move = (x_cord, king_spot[1])
                            rook_move = (x_r_cord, king_spot[1])
                            closer_swap.append(("king", king_move))
                            closer_swap.append(("rook", rook_move))

                        if len(further_rook) == 1:
                            further_rook_ = further_rook[0].current_quadrant

                            larger_num = further_rook_[0] if further_rook_[0] > king_spot[0] else king_spot[0]

                            if further_rook_[0] == larger_num:
                                x_cord = king_spot[0] + 3
                                x_r_cord = further_rook_[0] - 2
                            else:
                                x_cord = king_spot[0] - 3
                                x_r_cord = further_rook_[0] + 2

                            king_move = (x_cord, king_spot[1])
                            rook_move = (x_r_cord, king_spot[1])

                            further_swap.append(("king", king_move))
                            further_swap.append(("rook", rook_move))

                        closer_rook_spot = []
                        further_rook_spot = []

                        if closer_rook:
                            closer_rook_spot = closer_rook[0].current_quadrant

                        if further_rook:
                            further_rook_spot = further_rook[0].current_quadrant

                        if self.current_quadrant == king_spot or self.current_quadrant == closer_rook_spot:
                            if closer_rook_spot == cord or king_spot == cord:

                                rook_move = [x[1] for x in closer_swap if x[0] == "rook"][0]
                                king_move = [x[1] for x in closer_swap if x[0] == "king"][0]

                                closer_rook[0].change_spot(rook_move, [x for x in self.all_cords if x[2] ==rook_move], occupancy, no_castle = True)

                                castle_able_king[0].change_spot(king_move,[x for x in self.all_cords if x[2] == king_move], occupancy, no_caslte = True)

                                return [0, "moved"]
                            else:
                                pass

                        if self.current_quadrant == king_spot or self.current_quadrant == further_rook_spot:
                            if further_rook_spot == cord or king_spot == cord:
                                rook_move = [x[1] for x in further_swap if x[0] == "rook"][0]
                                king_move = [x[1] for x in further_swap if x[0] == "king"][0]

                                further_rook[0].change_spot(rook_move, [x for x in self.all_cords if x[2] == rook_move],
                                                           occupancy, no_castle=True)
                                castle_able_king[0].change_spot(king_move,
                                                                [x for x in self.all_cords if x[2] == king_move],
                                                            occupancy, no_caslte=True)
                                return [0, "moved"]
                            else:
                                pass

            self.times_moved =+ 1
            self.current_quadrant = cord

            if cord in enemies:
                return [cord, "remove enemy at this location this turn"]
            else:

                return [0, "moved"]

        else:
            print(occupancy)
            print("spot not possible")
            return [0, "error"]

    def occupancies_acknowledged(self, possible_spots, occupancy):
        side = self.side

        possible_spots_cord = [x[2] for x in possible_spots]

        ally_pieces = [x[0] for x in occupancy if x[1] == side]
        for x in ally_pieces:
            if x == self.current_quadrant:
                ally_pieces.remove(x)
        enemy_pieces = [x[0] for x in occupancy if x[1] != side]

        conflicting_allies = [piece for piece in ally_pieces if piece in possible_spots_cord]
        conflicting_enemies = [piece for piece in enemy_pieces if piece in possible_spots_cord]

        closest_ally = (100,100)
        for cord in conflicting_allies:

            if abs(cord[0] - self.current_quadrant[0])< abs(closest_ally[0]- self.current_quadrant[0]):
                closest_ally = cord
            elif abs(cord[1] - self.current_quadrant[1]) < abs(closest_ally[1] - self.current_quadrant[1]):
                closest_ally = cord
            else:
                pass

        closest_enemy = (100, 100)
        for cord in conflicting_enemies:
            if abs(cord[0] - self.current_quadrant[0]) < abs(closest_enemy[0] - self.current_quadrant[0]):
                closest_enemy = cord
            elif abs(cord[1] - self.current_quadrant[1]) < abs(closest_enemy[1] - self.current_quadrant[1]):
                closest_enemy = cord
            else:
                pass

        ally_factor = (abs(closest_ally[0] - self.current_quadrant[0])+abs(closest_ally[1] - self.current_quadrant[1]))
        enemy_factor = (abs(closest_enemy[0] - self.current_quadrant[0])+abs(closest_enemy[1] - self.current_quadrant[1]))

        if ally_factor < enemy_factor:
            closest_piece = (closest_ally, "ally")
            closest_factor = ally_factor
        else:
            closest_piece = (closest_enemy, "enemy")
            closest_factor = enemy_factor

        remove = []
        for x in possible_spots_cord:

            factor = (abs(x[0] - self.current_quadrant[0]) + abs(x[1] - self.current_quadrant[1]))
            if closest_piece[1] == "ally":
                if factor > closest_factor or factor == closest_factor:
                    remove.append(x)
            elif closest_piece[1] == "enemy":
                if factor > closest_factor:
                    remove.append(x)
            else:
                pass

        possible_final = [x for x in possible_spots_cord if x not in remove]
        return possible_final

    def one_step_pos_foundational(self, direction, occupancy, **pawn):
        x = self.current_quadrant[0]
        y = self.current_quadrant[1]

        cord = (x, y)

        if direction == "up":
            cord = (x,y-1)
        if direction == "down":
            cord = (x,y+1)
        if direction == "right":
            cord = (x+1,y)
        if direction == "left":
            cord = (x-1,y)
        if direction == "up-right":
            cord = (x+1, y-1)
        if direction == "up-left":
            cord = (x-1, y-1)
        if direction == "down-right":
            cord = (x+1, y+1)
        if direction == "down-left":
            cord = (x-1, y+1)

        if pawn:
            additive = -1 if direction == "up" else 1
            diagonals = [(x+1,y+additive), (x-1,y+additive)]
            enemies = [x[0] for x in occupancy if x[1] != self.side]
            edibles = [x for x in diagonals if x in enemies]

            edibles = [x for x in self.all_cords if x[2] in edibles]

            if self.times_moved == 0:

                if direction == "up":
                    extra_cord = (cord[0],cord[1]-1)
                else:
                    extra_cord = (cord[0],cord[1]+1)

                cords = [extra_cord, cord]
                possible_spots = [x for x in self.all_cords if x[2] in cords]
                spots = self.occupancies_acknowledged(possible_spots, occupancy)
                for x in spots:
                    if x in enemies:
                        spots.remove(x)
                possible_spots = [x for x in self.all_cords if x[2] in spots]
                return possible_spots+edibles
            else:
                possible_spots = [x for x in self.all_cords if x[2] == cord]
                spots = self.occupancies_acknowledged(possible_spots, occupancy)
                for x in spots:
                    if x in enemies:
                        spots.remove(x)
                possible_spots = [x for x in self.all_cords if x[2] in spots]

                return possible_spots+edibles

        possible_spots = [x for x in self.all_cords if x[2] == cord]
        spots = self.occupancies_acknowledged(possible_spots, occupancy)
        possible_spots = [x for x in self.all_cords if x[2] in spots]

        return possible_spots

    def component_separation_foundational(self):
        x = self.current_quadrant[0]
        y = self.current_quadrant[1]

        hor_available = [cord[2][0] for cord in self.all_cords if cord[2][0] > x and cord[2][1] == y or cord[2][0] < x and cord[2][1] == y]
        ver_available = [cord[2][1] for cord in self.all_cords if cord[2][1] > y and cord[2][0] == x or cord[2][1] < y and cord[2][0] == x]

        right_x = [1 for x_cord in hor_available if x_cord > x]
        left_x = [1 for x_cord in hor_available if x_cord < x]
        up_y = [1 for y_cord in ver_available if y_cord < y]
        down_y = [1 for y_cord in ver_available if y_cord > y]

        return right_x, left_x, up_y, down_y

    def diagonal_foundational(self, occupancy):
        x = self.current_quadrant[0]
        y = self.current_quadrant[1]
        set_available= self.component_separation_foundational()

        x_right = set_available[0]
        x_left = set_available[1]

        y_up = set_available[2]
        y_down = set_available[3]

        def move(r_or_l, u_or_d):
            if r_or_l == "r":
                domain = x_right
            else:
                domain = x_left

            if u_or_d == "u":
                range_ = y_up
            else:
                range_ = y_down

            available = []

            if len(domain) > len(range_):
                factor = range_
            else:
                factor = domain

            for i, iterable in enumerate(factor):
                if u_or_d == "u":
                    if r_or_l == "r":
                        cord = (x + i+1, y - i-1)
                    else:
                        cord = (x - i-1, y - i-1)
                else:
                    if r_or_l == "r":
                        cord = (x + i+1, y + i+1)
                    else:
                        cord = (x - i-1, y + i+1)
                available.append(cord)
            return available

        r_u = move("r", "u")
        r_u = [x for x in self.all_cords if x[2] in r_u]
        l_u = move("l", "u")
        l_u = [x for x in self.all_cords if x[2] in l_u]
        r_d = move("r", "d")
        r_d = [x for x in self.all_cords if x[2] in r_d]
        l_d = move("l", "d")
        l_d = [x for x in self.all_cords if x[2] in l_d]

        list1 = self.occupancies_acknowledged(r_u, occupancy)
        list2 = self.occupancies_acknowledged(l_u, occupancy)
        list3 = self.occupancies_acknowledged(r_d, occupancy)
        list4 = self.occupancies_acknowledged(l_d, occupancy)

        possible_spots = [x for x in self.all_cords if x[2] in list1 + list2 + list3 + list4]
        return possible_spots

    def straight_foundational(self, occupancy):
        x = self.current_quadrant[0]
        y = self.current_quadrant[1]

        set_available = self.component_separation_foundational()

        x_right = set_available[0]
        right = [(x+i+1, y) for i, iterable in enumerate(x_right)]
        right = [x for x in self.all_cords if x[2] in right]
        right = self.occupancies_acknowledged(right, occupancy)

        x_left = set_available[1]
        left = [(x - i - 1, y) for i, iterable in enumerate(x_left)]
        left = [x for x in self.all_cords if x[2] in left]
        left = self.occupancies_acknowledged(left, occupancy)

        y_up = set_available[2]
        up = [(x, y-1-i) for i, iterable in enumerate(y_up)]
        up = [x for x in self.all_cords if x[2] in up]
        up = self.occupancies_acknowledged(up, occupancy)

        y_down = set_available[3]
        down = [(x, y + 1 + i) for i, iterable in enumerate(y_down)]
        down = [x for x in self.all_cords if x[2] in down]
        down = self.occupancies_acknowledged(down, occupancy)

        possible_spots = [x for x in self.all_cords if x[2] in right+left+up+down]

        return possible_spots

    def horse_foundational(self, occupancy):
        x = self.current_quadrant[0]
        y = self.current_quadrant[1]

        right = [(x+2,y-1), (x+2, y+1)]
        right = [x for x in self.all_cords if x[2] in right]

        if len(right) == 0:
            right1 = []
            right2 = []
        elif len(right) == 1:
            right1 = [right[0]]
            right2 = []
        else:
            right1 = [right[0]]
            right2 = [right[1]]

        right1 = self.occupancies_acknowledged(right1, occupancy)
        right2 = self.occupancies_acknowledged(right2, occupancy)

        left = [(x-2,y-1), (x-2, y+1)]
        left = [x for x in self.all_cords if x[2] in left]

        if len(left) == 0:
            left1 = []
            left2 = []
        elif len(left) == 1:
            left1 = [left[0]]
            left2 = []
        else:
            left1 = [left[0]]
            left2 = [left[1]]

        left1 = self.occupancies_acknowledged(left1, occupancy)
        left2 = self.occupancies_acknowledged(left2, occupancy)

        up = [(x-1,y-2), (x+1, y-2)]
        up = [x for x in self.all_cords if x[2] in up]

        if len(up) == 0:
            up1 = []
            up2 = []
        elif len(up) == 1:
            up1 = [up[0]]
            up2 = []
        else:
            up1 = [up[0]]
            up2 = [up[1]]

        up1 = self.occupancies_acknowledged(up1, occupancy)
        up2 = self.occupancies_acknowledged(up2, occupancy)

        down = [(x-1,y+2), (x+1, y+2)]
        down = [x for x in self.all_cords if x[2] in down]

        if len(down) == 0:
            down1 = []
            down2 = []
        elif len(down) == 1:
            down1 = [down[0]]
            down2 = []
        else:
            down1 = [down[0]]
            down2 = [down[1]]

        down1 = self.occupancies_acknowledged(down1, occupancy)
        down2 = self.occupancies_acknowledged(down2, occupancy)

        possible_spots = [x for x in self.all_cords if x[2] in right1+right2 + left1+left2 + up1+up2 + down1+down2]
        return possible_spots

class Queen(PieceFoundational):
    def move_outline(self, occupancy):
        possible_spots = self.straight_foundational(occupancy) + self.diagonal_foundational(occupancy)
        return possible_spots

class King(PieceFoundational):
    def move_outline(self, occupancy):
        possible_spots = self.one_step_pos_foundational("up", occupancy) + self.one_step_pos_foundational("down", occupancy) + self.one_step_pos_foundational("right", occupancy) + self.one_step_pos_foundational("left", occupancy)+self.one_step_pos_foundational("up-right", occupancy) + self.one_step_pos_foundational("up-left", occupancy) + self.one_step_pos_foundational("down-right", occupancy) + self.one_step_pos_foundational("down-left", occupancy)
        castle_spots = self.castling(occupancy)
        possible_spots = possible_spots + castle_spots
        return possible_spots

class Bishop(PieceFoundational):
    def move_outline(self, occupancy):
        possible_spots = self.diagonal_foundational(occupancy)
        return possible_spots

class Rook(PieceFoundational):
    def move_outline(self, occupancy):
        possible_spots = self.straight_foundational(occupancy)
        castle_spots = self.castling(occupancy)
        possible_spots = possible_spots + castle_spots
        return possible_spots

class Knight(PieceFoundational):
    def move_outline(self, occupancy):
        possible_spots = self.horse_foundational(occupancy)
        return possible_spots

class Pawn(PieceFoundational):
    def move_outline(self, occupancy):
        possible_spots = self.one_step_pos_foundational(self.pawn_direction, occupancy, pawn = True)
        return possible_spots

class ConventionalChessSetUp:
    def __init__(self, screen, pygame, size, board_color):

        self.board_info = BoardBackgroundPieces(screen, pygame, size)
        self.quadrant_classifications = self.board_info.quadrants
        self.board_color = board_color
        self.images = self.board_info.classified_images

        self.pawns = [("Pawn", x ,2, "upper")for x in range(1,9)] + [("Pawn", x, 7, "lower") for x in range(1,9)]
        self.rooks = [("Rook",1,1, "upper"), ("Rook",8,1, "upper"),("Rook",1,8, "lower"), ("Rook",8,8, "lower")]
        self.horses = [("Knight",2, 1, "upper"), ("Knight", 7, 1, "upper"), ("Knight",2, 8, "lower"), ("Knight",7, 8, "lower")]
        self.bishops = [("Bishop", 3, 1, "upper"), ("Bishop", 6, 1, "upper"), ("Bishop", 3, 8, "lower"), ("Bishop", 6, 8, "lower")]
        self.kings_queens = [("King",4, 1, "upper"), ("Queen",5, 1, "upper"),("King",5, 8, "lower"), ("Queen", 4, 8,"lower")]
        self.kings_queens_v2 = [("King",4, 8, "lower"), ("Queen", 5, 8, "lower"),("King", 5, 1, "upper"), ("Queen",4, 1, "upper")]

        self.setup = self.pawns+self.rooks+self.horses+self.bishops+self.kings_queens_v2
        self.pieces = [eval(x[0])((x[1],x[2]), x[0].lower(), self.quadrant_classifications, x[3]) for x in self.setup]

        sides = ["upper", "lower"]

        self.black = [random.choice(sides), "black"]
        sides.remove(self.black[0])
        self.white = [random.choice(sides), "white"]

        for x in self.pieces:
            if x.side == self.black[0]:
                x.color = self.black[1]
            else:
                x.color = self.white[1]

        self.quadrant_starting_occupancy = [[x.current_quadrant, x.side, x.name, x.color, x.times_moved] for x in self.pieces]
        self.quadrant_current_occupancy = self.quadrant_starting_occupancy

        positions = [[piece.name, piece.side, piece.starting_quadrant] for piece in self.pieces]
        positions_info = []
        for info in positions:
            side = info[1]

            if self.black[0] == side:
                color = "black"
            else:
                color = "white"

            location = info[2]
            spot = [x[1] for x in self.quadrant_classifications if str(x[2]) == str(location)][0]
            positions_info.append([info[0], color, spot] )

        self.board_info.create(self.board_color)
        image_info = self.board_info.render_pieces(classified_images, positions_info)

        for piece in self.pieces:
            for info in image_info:
                if piece.name == info[0]:
                    piece_color = [x[1] for x in [self.black, self.white] if piece.side.lower() == x[0].lower()][0]
                    if piece_color == info[1]:
                        piece.image = info[2]

    def update_occupancy(self):
        self.board_info.create(self.board_color)
        self.quadrant_current_occupancy = [[x.current_quadrant, x.side, x.name, x.color, x.times_moved] for x in self.pieces]
        self.board_info.update_pieces(self.pieces)
    def create_occupancy(self, pieces):
        self.board_info = self.board_info
        occupancy = [[x.current_quadrant, x.side, x.name, x.color, x.times_moved] for x in pieces]
        return occupancy
    def create_virtual_pieces_stats(self, *pieces):
        if pieces:
            v_pieces = [eval(x.name.capitalize())(x.current_quadrant, x.name.lower(), self.quadrant_classifications, x.side, x.times_moved) for x in pieces[0]]
        else:
            v_pieces = [eval(x.name.capitalize())(x.current_quadrant, x.name.lower(), self.quadrant_classifications, x.side, x.times_moved) for x in self.pieces]
        for x in v_pieces:
            if x.side == self.black[0]:
                x.color = self.black[1]
            else:
                x.color = self.white[1]

        return v_pieces




















































        
























