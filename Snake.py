import pygame
import pygame_menu
import sys
import random
from pygame.math import Vector2


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        xPos = int(self.pos.x * cellSize)
        yPos = int(self.pos.y * cellSize)
        fruit_rect = pygame.Rect(xPos, yPos, cellSize, cellSize)
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self, startPos):
        self.body = startPos
        self.direction = Vector2(0, 0)
        self.newBlock = False
        # Head positions
        self.headUp = pygame.image.load('Pictures/head_up.png').convert_alpha()
        self.headDown = pygame.image.load(
            'Pictures/head_down.png').convert_alpha()
        self.headRight = pygame.image.load(
            'Pictures/head_right.png').convert_alpha()
        self.headLeft = pygame.image.load(
            'Pictures/head_left.png').convert_alpha()
        # Tail positions
        self.tailUp = pygame.image.load('Pictures/tail_up.png').convert_alpha()
        self.tailDown = pygame.image.load(
            'Pictures/tail_down.png').convert_alpha()
        self.tailRight = pygame.image.load(
            'Pictures/tail_right.png').convert_alpha()
        self.tailLeft = pygame.image.load(
            'Pictures/tail_left.png').convert_alpha()
        # Turns
        self.rTurn = pygame.image.load('Pictures/body_bl.png').convert_alpha()
        self.rrTurn = pygame.image.load('Pictures/body_tl.png').convert_alpha()
        self.rrrTurn = pygame.image.load(
            'Pictures/body_tr.png').convert_alpha()
        self.rrrrTurn = pygame.image.load(
            'Pictures/body_br.png').convert_alpha()
        # Straight
        self.bodyVertical = pygame.image.load(
            'Pictures/body_vertical.png').convert_alpha()
        self.bodyHorizontal = pygame.image.load(
            'Pictures/body_horizontal.png').convert_alpha()

        self.chrunchSound = pygame.mixer.Sound("Sound/ChrunchSound.wav")

    def draw_snake(self):
        self.update_snake_head_graphics()
        self.update_snake_tail_graphics()

        for index, block in enumerate(self.body):
            xPos = int(block.x * cellSize)
            yPos = int(block.y * cellSize)
            block_rect = pygame.Rect(xPos, yPos, cellSize, cellSize)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previousBlock = self.body[index + 1] - block
                nextBlock = self.body[index - 1] - block
                if previousBlock.x == nextBlock.x:
                    screen.blit(self.bodyVertical, block_rect)
                elif previousBlock.y == nextBlock.y:
                    screen.blit(self.bodyHorizontal, block_rect)
                else:
                    if previousBlock.x == -1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == -1:
                        screen.blit(self.rTurn, block_rect)
                    elif previousBlock.x == -1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == -1:
                        screen.blit(self.rrTurn, block_rect)
                    elif previousBlock.x == 1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == 1:
                        screen.blit(self.rrrTurn, block_rect)
                    else:
                        screen.blit(self.rrrrTurn, block_rect)

    def update_snake_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.headLeft
        elif head_relation == Vector2(-1, 0):
            self.head = self.headRight
        elif head_relation == Vector2(0, 1):
            self.head = self.headUp
        elif head_relation == Vector2(0, -1):
            self.head = self.headDown

    def update_snake_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tailLeft
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tailRight
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tailUp
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tailDown

    def move_snake(self):
        if self.newBlock:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newBlock = False
        else:
            if self.direction != Vector2(0, 0):
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]

    def add_block(self):
        self.newBlock = True

    def play_crunch_sound(self):
        self.chrunchSound.play()

    def reset(self):
        self.direction = Vector2(0, 0)
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]


class MAIN:
    def __init__(self):
        self.highScore = 0
        self.menu = pygame_menu.Menu('Welcome', gameSize, gameSize,
                                     theme=pygame_menu.themes.THEME_GREEN)
        self.score = self.menu.add.label("")
        self.snake = SNAKE([Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        currentScore = int(len(self.snake.body) - 3)
        if currentScore > self.highScore:
            self.highScore = currentScore
        self.snake.reset()
        self.game_menu(False)

    def draw_grass(self):
        grassColor = (167, 209, 61)
        for row in range(cellNumber):
            if row % 2 == 0:
                for col in range(cellNumber):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grass_rect)
            else:
                for col in range(cellNumber):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grass_rect)

    def draw_score(self):
        scoreText = str(len(self.snake.body) - 3)
        scoreSurface = gameFont.render(scoreText, True, (56, 26, 12))
        scoreX = int(gameSize - 60)
        scoreY = int(gameSize - 40)
        scoreRect = scoreSurface.get_rect(center=(scoreX, scoreY))
        appleRect = apple.get_rect(
            midright=(scoreRect.left, scoreRect.centery))
        backgroudRect = pygame.Rect(
            appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 6, appleRect.height)
        pygame.draw.rect(screen, (167, 209, 61), backgroudRect)
        screen.blit(scoreSurface, scoreRect)
        screen.blit(apple, appleRect)
        pygame.draw.rect(screen, (56, 74, 12), backgroudRect, 2)

    def game_menu(self, starting):
        if starting:
            pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
            pygame_menu.font.FONT_8BIT
            pygame_menu.widgets.LeftArrowSelection
            self.menu.add.text_input('Name: ', default='Markus VGJ')
            self.menu.add.button('Play', play_game)
            self.menu.add.button('Quit', pygame_menu.events.EXIT)
            self.menu.mainloop(screen)
        self.menu.remove_widget(self.score)
        self.score = self.menu.add.label(
            "Latest highscore: " + str(self.highScore))
        self.menu.mainloop(screen)


# Pygame settings
pygame.init()  # Initialisation
pygame.display.set_mode()  # Pictures
pygame.mixer.pre_init(44100, -16, 2, 512)  # Sound

# Variables
cellSize = 40
cellNumber = 20
gameSize = cellNumber * cellSize
framerate = 60
backgroudColour = (175, 215, 70)
gameFont = pygame.font.Font("Font/Wigglye.ttf", 30)
apple = pygame.image.load('Pictures/Apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (cellSize, cellSize))
screen = pygame.display.set_mode((gameSize, gameSize))
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
mainGame = MAIN()


def play_game():
    while True:
        for event in pygame.event.get():  # Looking for events from user
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                mainGame.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if mainGame.snake.direction.y != 1:
                        mainGame.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if mainGame.snake.direction.y != -1:
                        mainGame.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if mainGame.snake.direction.x != -1:
                        mainGame.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if mainGame.snake.direction.x != 1:
                        mainGame.snake.direction = Vector2(-1, 0)
        # Updating
        screen.fill(backgroudColour)
        mainGame.draw_elements()
        pygame.display.update()
        clock.tick(framerate)


mainGame.game_menu(True)
