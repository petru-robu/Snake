import pygame
from Engine import Engine

RED = (255, 26, 26)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

MARGIN = 20
CELL_NUM = 3
GRID_SIZE = 360

BACKGROUND = WHITE
SCREEN_SIZE = 640, 400

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.en = Engine()

    def draw_grid(self):
        cellSize = int(GRID_SIZE / CELL_NUM)
        for x in range(MARGIN, MARGIN + GRID_SIZE-1, cellSize):
            for y in range(MARGIN, MARGIN + GRID_SIZE-1, cellSize):
                rect = pygame.Rect(x, y, cellSize, cellSize)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
        return True

    def init(self):
        self.screen.fill(WHITE)
        self.draw_grid()

    def type_text_at_pos(self, x, y, toType, size=20, font_name="dejavusansmono", color=BLACK):
        font = pygame.font.SysFont(font_name, size)
        label = font.render(toType, 1, color)
        self.screen.blit(label, (x, y))
    
    def type_text_in_cell(self, x1, y1, x2, y2, toType):
        x , y = int((x1+x2)/2)-20, int((y1+y2)/2-26)
        self.type_text_at_pos(x, y, toType, 62)

    def get_cell_coords(self):
        st_X, st_Y, grid_size = MARGIN, MARGIN, GRID_SIZE
        en_X, en_Y = st_X+grid_size, st_Y+grid_size

        cellSize = int(grid_size/3)

        cells = [[(0,0,0,0),(0,0,0,0),(0,0,0,0)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                stx, sty = int(st_X + j*cellSize), int(st_Y + i*cellSize)
                enx, eny = int(stx + cellSize), int(sty + cellSize)
                cells[i][j] = (stx, sty, enx, eny)
        return cells


    def contains_mouse(self, x_mouse, y_mouse, x1, y1, x2, y2):
        return x_mouse > x1 and y_mouse > y1 and x_mouse < x2 and y_mouse <y2

    def onClick(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        cells = self.get_cell_coords()

        state = self.en.get_state()
        if state == "running":
            for i in range(3):
                for j in range(3):
                    if self.contains_mouse(x_mouse, y_mouse, *cells[i][j]):
                        #print(f"S-a clickuit celula: {i+1, j+1}")
                        self.type_text_in_cell(*cells[i][j],'X')

                        i_ans, j_ans = self.en.make_move(i, j)
                        if i_ans != -1 and j_ans != -1:
                            self.type_text_in_cell(*cells[i_ans][j_ans], 'O')
    
    def onFrame(self):
        gameState = self.en.get_state()
        if gameState == "draw":
            self.type_text_at_pos(430, 200, "Este remiza!", 24)
        elif gameState == "X":
            self.type_text_at_pos(430, 200, "Ai castigat!", 24)
        elif gameState == "O": 
            self.type_text_at_pos(430, 200, "Ai pierdut!", 24)
            

    def run(self):
        self.init()
        exit = False
        while not exit:

            self.onFrame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "escape":
                        exit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.onClick()

            pygame.display.update()
        pygame.quit()

