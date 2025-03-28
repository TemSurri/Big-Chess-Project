import pygame
from game_brain import *


class MenusAndGame:
    def __init__(self, pyg):
        self.pygame = pyg
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((500, 500))
        self.pygame.display.set_caption("Tem Chess Engine")
        self.running = True
        self.clock = self.pygame.time.Clock()
        self.page = "initial"
        self.result = ""


        self.chess_s_s = 600
        self.chess_color = "light grey"
        self.competitive = False
        self.input_activity = False

    def passive(self):
        while self.running:
            if self.page == "results":
                self.screen.fill("white")
                self.render_game_result(self.result)
                for x in pygame.event.get():
                    if str(x) == "<Event(256-Quit {})>":
                        self.running = False
                    self.box_active(x)
                    if x.type == pygame.MOUSEBUTTONUP:
                        self.page = "initial"
                        self.screen.fill("black")
            if self.page == "initial":
                self.initial_display()
                for x in pygame.event.get():
                    if str(x) == "<Event(256-Quit {})>":
                        self.running = False
                    if x.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        stat = self.check_click(pos)

                        if stat == "pvp offline":
                            self.page = "pvp options"

            if self.page == "pvp options":

                self.pvp_o_f_customization()
                for x in pygame.event.get():
                    if str(x) == "<Event(256-Quit {})>":
                        self.running = False
                    self.box_active(x)
                    if x.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        stat = self.check_click(pos)

                        if stat == "comp_on":
                            self.competitive = True
                        if stat == "comp_off":
                            self.competitive = False
                        if stat == "game_start":
                            self.start_game()

            pygame.display.flip()
            self.clock.tick(60)
        self.pygame.quit()

    def render_texts(self, texts):

        for x in texts:

            size = x[0]
            content = x[1]
            color = x[2]
            cord = x[3]

            font = self.pygame.font.Font('freesansbold.ttf', size)
            text = font.render(content, True, color)
            text_rect = text.get_rect()
            text_rect.center = cord
            self.screen.blit(text, text_rect)

    def render_game_result(self, result):

        result_info = [(25, result, "black", (240, 200))]
        self.render_texts(result_info)

    def render_regions(self, squares):

        for x in squares:
            color = x[0]
            sizing = x[1]

            self.pygame.draw.rect(self.screen, color, sizing)

    def initial_display(self):
        texts = [(50, "Tem's Chess", "white", (250, 50)),
                 (20, "click on respective squares to play", "dark grey", (250, 100)),
                 (20, "offline", "white", (85, 200))]
        squares = [("dark grey", (50, 150, 150, 150))]

        self.render_regions(squares)
        self.render_texts(texts)

    def check_click(self, click):
        x = click[0]
        y = click[1]

        if self.page == "pvp options":
            print(click)
            if y > 400:
                return "game_start"

            if 375 > y > 325:
                if 360 > x > 305:
                    return "comp_on"
                if 460 > x > 395:
                    return "comp_off"

            if 490 > x > 185:
                if 165 > y > 135:
                    self.input_activity = ["color"]
                    return "_input"
            if 490 > x > 275:
                if 265 > y > 235:
                    self.input_activity = ["sizing"]
                    return "_input"
                
        self.input_activity = False
        if 200 > x > 50:
            if 300 > y > 150:
                return "pvp offline"

    def start_game(self):

        if 499 > int(self.chess_s_s) or 5000 < int(self.chess_s_s):
            print("hi")
            self.input_activity = ["sizing", "red"]

            return
        try:
            self.pygame.display.set_mode((self.chess_s_s, self.chess_s_s))
            engine = Game(self.screen, self.pygame, self.chess_s_s, self.chess_color)
            if self.competitive:
                game_outcome = engine.base_game(ai = True)
            else:
                game_outcome = engine.base_game()

            self.result = game_outcome
            if self.result == "END":
                pass
            else:
                self.page = "results"

        except ValueError:
            self.pygame.display.set_mode((500,500))
            self.input_activity = ["color", "red"]

        self.pygame.display.set_mode((500, 500))

    def box_active(self, event):

        if self.input_activity == ["sizing"]:
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                #key has to be an integer or float turn integer once it can be without any issues
                #use try and finally raise exceptions and shii
                #if not turn the color red
                try:
                    if key == "\x08":
                        self.chess_s_s = int([str(self.chess_s_s)[:-1]][0])
                    else:
                        self.chess_s_s = int(str(self.chess_s_s) + str(key))
                except ValueError:
                    self.chess_s_s = 0

        if self.input_activity == ["color"]:
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                #key has to be a proper color
                if key == "\x08":
                    self.chess_color = [str(self.chess_color)[:-1]][0]
                else:
                    self.chess_color = str(self.chess_color) + str(key)

    def render_input_boxes(self, active, text_input):

        not_active_color = "dark grey"
        active_color = "light green"

        screen_size_box_info = [185, 135, 310, 30]
        color_box_info = [275, 235, 220, 30]

        if not active:
            squares = [(not_active_color, screen_size_box_info), (not_active_color, color_box_info)]
        elif active[0] == "sizing":
            if len(active) == 2:
                squares = [(not_active_color, screen_size_box_info), ("red", color_box_info)]
            else:
                squares = [(not_active_color, screen_size_box_info), (active_color, color_box_info)]
        elif active[0] == "color":
            if len(active) == 2:
                squares = [("red", screen_size_box_info), (not_active_color, color_box_info)]
            else:
                squares = [(active_color, screen_size_box_info), (not_active_color, color_box_info)]
        else:
            squares = [(active_color, screen_size_box_info), (active_color, color_box_info)]

        self.render_regions(squares)

        size = str(text_input[0])
        color = str(text_input[1])

        texts = [(25, color ,"dark blue", (350, 150)), (25, size, "dark blue", (390, 250))]

        self.render_texts(texts)

    def pvp_o_f_customization(self):
        size = self.chess_s_s
        color = self.chess_color
        competitive = self.competitive
        activity = self.input_activity

        regions = [(True, ("dark grey",(310, 320, 50, 50))), (False,("dark grey", (400, 320, 50, 50)))]
        regions_2 = [("light green", (0, 400, 1000, 1000))]

        self.screen.fill("grey")

        texts1 = [(50, "PVP offline Chess", "white", (250, 60)), (50, "START", "dark green", (250, 450)),(25, "Versus AI?:", "black", (140, 350)),(25, "Board Size (pixels):", "black", (145, 250)), (25, "Board Color:", "black", (100, 150))]
        texts2 = [(30, "Yes", "green", (335, 350)), (30, "No", "dark red", (425, 350))]

        self.render_regions([x[1] for x in regions if x[0] == competitive]+regions_2)
        self.render_texts(texts1+texts2)

        self.render_input_boxes(activity, [size, color])





