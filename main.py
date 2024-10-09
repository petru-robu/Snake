import pygame, time, random

WHITE = (255, 255, 255)
WHITE_ALT = (235, 235, 235)
BLACK = (0, 0, 0)
BLUE1 = (129, 195, 211)
YELLOW1 = (255, 192, 58)

GRAY1 = (51, 51, 51)
GRAY2 = (58, 58, 58)

#window constants
WIDTH = 1160
HEIGHT = 640
SCREEN_SIZE = WIDTH, HEIGHT
CENTER = WIDTH/2, HEIGHT/2
CENTERX, CENTERY = CENTER

#grid constants
CELL_SIZE = 40
N = 16
M = 29

FPS = 120

DEF_FONT = "monospace"

pygame.init()
clock = pygame.time.Clock()    
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption("Snake")
pygame.mouse.set_visible(1)


def contains_mouse(x_mouse, y_mouse, x1, y1, x2, y2):
    return x_mouse > x1 and y_mouse > y1 and x_mouse < x2 and y_mouse <y2

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/music.wav")
        pygame.mixer.music.play(-1)
        self.music_vol = pygame.mixer.music.get_volume()

        self.button_click_sound = pygame.mixer.Sound("sounds/button_click.wav")
        self.food_pickup_sound = pygame.mixer.Sound("sounds/pickupCoin.wav")

    def play_music(self):
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def change_music_state(self):
        if pygame.mixer.music.get_volume() == 0:
            pygame.mixer.music.set_volume(self.music_vol)
        else:
            pygame.mixer.music.set_volume(0)
    
    def button_click(self):
        pygame.mixer.Sound.play(self.button_click_sound)
    
    def food_pickup(self):
        pygame.mixer.Sound.play(self.food_pickup_sound)

class Text:
    def __init__(self, label, text_size=2, posx=0, posy=0, color=WHITE,  font=DEF_FONT, bold=False, italic=False):
        self.label, self.color = label, color
        self.posx, self.posy = posx, posy
        self.font = pygame.font.SysFont(font, text_size, bold, italic)
        self.writeable = self.font.render(label, True, color)

    def display(self):
        screen.blit(self.writeable, (self.posx, self.posy))

    def get_rect(self):
        return self.writeable.get_rect()
    
    def center_at(self, x=0, y=0):
        width, height = self.get_rect().size
        self.posx = x - width/2
        self.posy = y - height/2
    
    def change_label(self, new_label):
        self.label = new_label
        self.writeable = self.font.render(new_label, True, self.color)

class Button:
    def __init__(self, label, text_size, posx=0, posy=0, back_color=WHITE, text_color=BLACK):
        self.label = label
        self.color = back_color
        self.back_color = back_color
        self.text = Text(label, text_size, posx, posy, text_color)
        text_width, text_height = self.text.get_rect().size
        self.box = pygame.Rect(posx, posy, text_width+15, text_height+5)
        
    def display(self):
        pygame.draw.rect(screen, self.color, self.box, 0, 17)
        self.text.display()

    def center_at(self, x=0, y=0):
        self.text.center_at(x, y)
        self.box.center = (x, y)
    
    def change_color(self, color):
        self.color = color

    def hover(self):
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if contains_mouse(x_mouse, y_mouse, self.box.left, self.box.top, self.box.right, self.box.bottom):
            r, g, b = self.back_color
            r, g, b = r*0.74, g*0.74, b*0.74
            self.change_color((r,g,b))
            return True
        else:
            self.change_color(self.back_color)
            return False

class Menu:
    def __init__(self):
        self.buttons = [Button("PLAY", 55, 0, 0, BLUE1), Button("CREDITS", 55, 0, 0, BLUE1), 
                        Button("MUSIC ON/OFF", 55, 0, 0, BLUE1), Button("EXIT", 55, 0, 0, BLUE1)]
        self.game_title = Text("Snake", 80, 0, 0, WHITE)
        begin = 200
        separation = 75
        for i in range(len(self.buttons)):
            self.buttons[i].center_at(CENTERX, begin + i*separation)
        self.game_title.center_at(CENTERX, 60)

    def display(self):
        for button in self.buttons:
            button.display()
        self.game_title.display()
    
    def on_hover(self):
        for button in self.buttons:
            button.hover()

    def check_button_click(self):
        clickedButton = ""
        for button in self.buttons:
            if button.hover() == True:
                clickedButton = button.label
        if clickedButton == "PLAY":
            pass
        elif clickedButton == "CREDITS":
            pass
        elif clickedButton == "MUSIC ON/OFF":
            pass
        elif clickedButton == "EXIT":
            pass    

        return clickedButton

class Gui:
    def __init__(self):
        self.score_text = Text("Length", 25, 0, 0, WHITE)
        self.score_text.center_at(CENTERX-10, 25)

        self.score_val_text = Text("0", 25, 0, 0, WHITE)
        self.score_val_text.center_at(CENTERX-10, 55)

        self.highScore_text = Text("Max Length", 19, 0, 0, WHITE)
        self.highScore_text.center_at(60, 20)

        self.highScore_val_text = Text("", 19, 0, 0, WHITE)
        self.highScore_val_text.center_at(10, 45)

        self.death_no_text = Text("Deaths", 19, 0, 0, WHITE)
        self.death_no_text.center_at(WIDTH-40, 20)
        self.death_no_val_text = Text("", 19, 0, 0, WHITE)
        self.death_no_val_text.center_at(WIDTH-40, 45)

        self.controls=[
        'Snake Game Controls:',
        'w, a, s, d - move',
        'm - music on/off',
        'esc - exit the game'
        ]

        self.info=[
        'Made By: Petru',
        '7.03.2023'
        ]

    def display_list_of_text(self, text_list, spacing, startx, starty):
        for i in range(len(text_list)):
            t = Text(text_list[i], 18, 0, 0, WHITE)
            t.center_at(startx, starty + spacing*i)
            t.display()

    def display(self):
        self.score_text.display()
        self.score_val_text.display()

        self.highScore_text.display()
        self.highScore_val_text.display()

        self.death_no_text.display()
        self.death_no_val_text.display()
        
        self.display_list_of_text(self.controls, 20, 120, 560)
        self.display_list_of_text(self.info, 20, 1070, 605)

class Scoreboard:
    def __init__(self):
        self.curr_len = 0
        self.max_len = 0
        self.death_no = 0
    
    def update(self):
        self.max_len = max(self.curr_len, self.max_len)

class Grid:
    def __init__(self):
        pass

    def display(self):
        i = 0
        for x in range(0, WIDTH, CELL_SIZE):
            i+=1
            j = 0
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                if (i+j)% 2 == 0:
                    pygame.draw.rect(screen, GRAY1, rect)
                else:
                    pygame.draw.rect(screen, GRAY2, rect)
                j+=1

    def to_idx(self, posx, posy):
        return (int(posx/CELL_SIZE), int(posy/CELL_SIZE))

class Food:
    def __init__(self):
        self.row_idx, self.col_idx = self.get_random_pos()

    def display(self):
        pygame.draw.circle(screen, WHITE_ALT, (self.row_idx*CELL_SIZE + 20, self.col_idx*CELL_SIZE + 20), 10)

    def get_random_pos(self):
        randx = random.randint(1, M-1)
        randy = random.randint(1, N-1)
        return (randx, randy)
    
    def consume(self):
        self.row_idx, self.col_idx = self.get_random_pos()

class Snake:
    def __init__(self):
        self.cell_list = [(10,11), (10,10), (10,9), (10,8)]
        self.dir = "E"

    def reset(self):
        self.cell_list = [(10,11), (10,10)]
        self.dir = "V"

    def update(self):
        for i in range(len(self.cell_list)-1, 0, -1):
            self.cell_list[i] = self.cell_list[i-1]

        hx, hy = self.cell_list[0]
        if self.dir == "N":
            hy -= 1
        if self.dir == "E":
            hx += 1
        if self.dir == "S":
            hy += 1
        if self.dir == "V":
            hx -=1
        self.cell_list[0] = (hx, hy)

        if hx < 0 or hx >= M or hy < 0 or hy>= N:
            self.reset()
            return "out_of_bounds"
        
        time.sleep(0.1)
        return "updated"

    def moveRight(self):
        if self.dir != "V":
            self.dir = "E"
            return True
        return False
    
    def moveLeft(self):
        if self.dir != "E":
            self.dir = "V"
            return True
        return False
    
    def moveUp(self):
        if self.dir != "S":
            self.dir = "N"
            return True
        return False
    
    def moveDown(self):
        if self.dir != "N":
            self.dir = "S"
            return True
        return False

    def length(self):
        return len(self.cell_list)

    def append(self):
        new_x, new_y = self.cell_list[len(self.cell_list)-1]
        if self.dir == "E":
            new_x, new_y = new_x-1, new_y
        if self.dir == "V":
            new_x, new_y = new_x+1, new_y
        if self.dir == "N":
            new_x, new_y = new_x, new_y+1
        if self.dir == "S":
            new_x, new_y = new_x, new_y-1

        self.cell_list.append((new_x, new_y))

    def check_self_collide(self):
        for i in range(3, len(self.cell_list)-1, 1):
            if self.cell_list[i] == self.cell_list[0]:
                self.reset()
                return True
        return False

    def display(self):
        color = BLUE1
        for i in range(len(self.cell_list)):
            x, y = self.cell_list[i]
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            r, g, b = color
            if r>5:
                r = r-5
            if g>5:
                g = g-5
            if b>5:
                b = b-5
            color = (r,g,b)
            pygame.draw.rect(screen, color, rect)

class Main:
    def __init__(self):
        self.gameState = "Menu"
        self.running = True

        self.menu = Menu()
        self.audio = AudioManager()
        self.gui = Gui()
        self.grid = Grid()
        self.food = Food()
        self.snake = Snake()

        self.scoreboard = Scoreboard()
 
    def display(self):
        screen.fill(GRAY1)
        if self.gameState == "Menu":
            self.menu.display()

        if self.gameState == "Playing":
            self.grid.display()
            self.food.display()
            self.snake.display()
            self.gui.display()
    
    def hover(self):
        if self.gameState == "Menu":
            self.menu.on_hover()
        
    def mouse_click(self):
        if self.gameState == "Menu":
            buttonClick = self.menu.check_button_click()
            if buttonClick:
                self.audio.button_click()
                if buttonClick == "EXIT":
                    self.running = False
                if buttonClick == "MUSIC ON/OFF":
                    self.audio.change_music_state()
                if buttonClick == "CREDITS":
                    pass
                if buttonClick == "PLAY":
                    self.gameState = "Playing"


    def key_press(self, event):
        if event.key == pygame.K_m:
            self.audio.change_music_state()
            self.audio.button_click()

        if self.gameState == "Menu":
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.audio.button_click()

        if self.gameState == "Playing":
            if event.key == pygame.K_ESCAPE:
                self.gameState = "Menu"
                self.audio.button_click()
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.snake.moveUp()
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.snake.moveDown()
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.snake.moveLeft()
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.snake.moveRight()

    def update(self):
        if self.gameState == "Playing":
            self.scoreboard.curr_len = len(self.snake.cell_list)
            self.scoreboard.update()

            if self.snake.update() == "out_of_bounds":
                self.scoreboard.death_no+=1

            if self.snake.check_self_collide() == True:
                self.scoreboard.death_no+=1

            self.gui.score_val_text.change_label(str(self.scoreboard.curr_len))
            self.gui.highScore_val_text.change_label(str(self.scoreboard.max_len))
            self.gui.death_no_val_text.change_label(str(self.scoreboard.death_no))

            if self.snake.cell_list[0] == (self.food.row_idx, self.food.col_idx):
                self.food.consume()
                self.snake.append()
                self.audio.food_pickup()


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click()
                if event.type == pygame.KEYDOWN:
                    self.key_press(event)
                
            self.update()
            self.hover()

            self.display()
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()


instance = Main()
instance.run()
        