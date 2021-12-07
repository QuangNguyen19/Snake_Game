import pygame
# library contains key_event to check which key 
# when pressing key on keyboard to operate on window_surface
from pygame.locals import *

import time


import random

# size of the block
SIZE = 40

sleep_time = 0.3
class Apple:
    def __init__(self,window_surface):
        self.image = pygame.image.load("resources//apple.jpg").convert()
        self.window_surface = window_surface
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.window_surface.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    # this function to create new coordinates of apple when the head of snake match the old coordinates
    def move(self):
        self.x = random.randint(0,24) * SIZE
        self.y = random.randint(0,14) * SIZE

class Snake:
    def __init__(self,window_surface,length):
        self.length = length

        self.window_surface = window_surface
        # set block is the block_image: Each block is 1 piece on the snake body
        self.block = pygame.image.load("resources//block.jpg").convert()

        # each time the snake eat an apple, it will exponentially increasing = number of apples eaten
        self.x = [SIZE] * length
        self.y = [SIZE] * length

        self.direction = 'down'

    # increase length of the snake when eaten an apple
    def increase_length(self):
        self.length += 1
        self.x.append(1)
        self.y.append(1)

    # add_block to sanke when press key on key_board
    def add_block(self):
        # clearing window_surface when pressing a key board
        # self.window_surface.fill((3, 252, 11))
        # the block will move
        for i in range(self.length):
            self.window_surface.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()
    
    def moves_left(self):
        self.direction = 'left'

    def moves_right(self):
        self.direction = 'right'

    def moves_up(self):
        self.direction = 'up'

    def moves_down(self):
        self.direction = 'down'
       

    # this function use to make the snake auto run
    def walk(self):
        # this for loop to set the position of those block following after the head_block
        for i in range(self.length-1,0,-1):
            # the next block will equal to the coordinates of the old block 
            self.x[i] = self.x[i- 1] 
            self.y[i] = self.y[i- 1] 
    
        if self.direction == 'up':
            # when pressing up key board: the head of the snake will move up so : 
            # the coordinate x of the head block stay the same, 
            # y coordinate moves up so y will decrease 
            self.y[0] -= 40

        if self.direction == 'down':
            # when pressing down key board: the head of the snake will move down 
            # so the coordinate x of the head block stay the same, 
            # y coordinate moves down so y will increase
            self.y[0] += 40

        if self.direction == 'right':
            # when pressing right key board: he head of the snake will move right 
            # so the coordinate y of the head block stay the same, 
            # x coordinate moves left so x will increase 
            self.x[0] += 40

        if self.direction == 'left':
            # when pressing left key board: the head of the snake will move left 
            # so the coordinate y of the head block stay the same, 
            # x coordinate moves left so x will increase 
            self.x[0] -= 40

        # add new block after pressing key board
        self.add_block()

class Game:
    
    def __init__(self):
        pygame.init() 
        pygame.mixer.init()
        self.play_bg_sound()

        # generate window_surface
        self.surface = pygame.display.set_mode((1000,600))
        # set window_surface with green
        # self.surface.fill((3, 252, 11))

        self.snake = Snake(self.surface,1)
        # add first block
        self.snake.add_block()
    
        self.apple = Apple(self.surface)
        # add first apple
        self.apple.draw()

    def show_bg_image(self):
        bg = pygame.image.load("resources//grass_bg.jpg")
        self.surface.blit(bg,(0,0))

    def play_bg_sound(self):
        pygame.mixer.music.load("resources//bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self,sound_name):
        sound = pygame.mixer.Sound(f"resources//{sound_name}.mp3")
        pygame.mixer.Sound.play(sound)

    
    def score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score: {self.snake.length}",True,(0,0,0))
        self.surface.blit(score,(800,10))
        pygame.display.flip()

    def show_game_over(self):
        self.surface.fill((14, 10, 23))
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(380,200))

        mess = font.render(f"Press Enter to play again",True,(255,255,255))
        self.surface.blit(mess,(350,220))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


    '''
        x2: x coordinate of the apple
        y2: y coordinate of the apple
        x1: x coordinate of the head of the snake
        y1: y coordinate of the head of the snake
        
        This funcition to check if the head of the snake match the coordinates of the apple
    '''
    def match(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 +SIZE :
            if y1 >= y2 and y1  < y2 + SIZE:
                return True
        return False
    
    '''
        x: x coordinate of the head of the snake
        y: y coordinate of the head of the snake
        
        This funcition to check if the head of the snake hit the wall
    '''

    def hit_the_wall(self,x,y):
        if x == 1080 or x == -80:
            return True
        if y == -80 or y == 680:
            return True
        return False
        

    def play(self):
        self.show_bg_image()
        self.snake.walk()
        self.apple.draw()
        self.score()
        
        
        if self.hit_the_wall(self.snake.x[0],self.snake.y[0]):
            hit_wall_sound = pygame.mixer.Sound("resources//crash.mp3")
            pygame.mixer.Sound.play(hit_wall_sound)
            raise "You hit the wall"

        # excute apple.move when match
        if self.match(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            # play ding sound when the sanke eat an apple
            self.play_sound("ding")
            self.apple.move()
            self.snake.increase_length()

        # check the head is match hit the body of snake
        for i in range(3,self.snake.length):
            if self.match(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                if self.snake.length % 3 == 0 and sleep_time > 0.2:
                    sleep_time -= 0.05
                    
                self.play_sound("crash")
                raise "You hit the body"

    def run(self):
        running = True
        pause = False
        # using while loop to activate surface operations
        while  running:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.moves_up()

                    if event.key == K_DOWN:
                        self.snake.moves_down()

                    if event.key == K_LEFT:
                        self.snake.moves_left()
 
                    if event.key == K_RIGHT:
                        self.snake.moves_right()
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    # while playing if press escape keyboard, it will quit the window_surface
                    if event.key == K_ESCAPE:
                        running = False
                    
                # press x button will quit the window_surface
                elif event.type == QUIT:
                    running = False
            try:
                if pause == False:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            # after 0.4 second snake will active the while loop
            time.sleep(sleep_time )

if __name__ == "__main__":
    game = Game()
    game.run()
