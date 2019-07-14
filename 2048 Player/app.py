import random
import pygame
import numpy as np
import math
import tensorflow as tf
import simulation as sim
import decision as deci
# import json

colors = [
    (151, 151, 151),  # No color
    (235, 224, 213),  # 2
    (234, 219, 191),  # 4
    (240, 167, 111),  # 8
    (244, 138, 89),  # 16
    (255, 104, 75),  # 32
    (243, 84, 51),  # 64
    (239, 200, 85),  # 128
    (241, 195, 64),  # 256
    (244, 201, 60),  # 512
    (244, 195, 39),  # 1024
    (255, 255, 255)]  # 2048 FIGURE OUT CORRECT COLOR
DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3
# MIN_SCORE = 500

pygame.init()
pygame.font.init()
smaller_font = pygame.font.SysFont("Roboto", 45)
font = pygame.font.SysFont("Roboto", 70)
width, height = 500, 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
fps = 60
fps_clock = pygame.time.Clock()

running = True
simulating = True
speed = 1
# try:
#     path = "/Users/leo/Desktop/Python/Data_collector_2048"
# except:
#     path = "Data_collector_2048"
# data_file = open(path + "/data.json", 'r')
# try:
#     raw_data = json.load(data_file)
# except:
#     raw_data = []
#     print("No data!")
#     running = False

player = sim.Game()
decider = deci.Decider()
# decider = deci.Decider(path)

# xs = []
# ys = []
# for game in raw_data:
#     if game['score'] > MIN_SCORE:
#         for i in range(len(game['inps'])):
#             xs.append(game['inps'][i])
#             ys.append(game['outs'][i])
# # Normalize all xs according to largest value of that x
# for i in range(len(xs)):
#     largest = max(xs[i])
#     xs[i] = [(xs[i][j] / largest) for j in range(len(xs[i]))]

# three_quarters = math.floor((len(xs) / 4) * 3)
# full = len(xs)

# random.shuffle(xs)
# random.shuffle(ys)
# training = (xs[0:three_quarters], ys[0:three_quarters])
# testing = (xs[three_quarters:full], ys[three_quarters:full])
# player.brain.train(training[0], training[1], 50)
# decider.brain.train(xs, ys, 15) #TODO Perhaps uncomment this
# TODO WHY IS THE EVAL RETURNING THE SAME THING, DOES TRAINING ALSO SPLIT
# INTO TESTING?
# TODO Debug this and make sure all inps and stuff are working
# evalu = player.brain.model.evaluate([testing[0]], [testing[1]])
# print(evalu)
# print("done")


def main():
    global running, simulating, width, speed, amt_to_show

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_a:
                    simulating = not simulating
                if event.key == pygame.K_n:
                    move = decider.decide(player.board)
                    player.move(move)
                if event.key == pygame.K_q:
                    player.reset()

                if event.key == pygame.K_EQUALS:
                    speed += 1
                if event.key == pygame.K_MINUS and speed > 1:
                    speed -= 1

                # if event.key == pygame.K_DOWN:
                #     player.move(DOWN)
                # if event.key == pygame.K_UP:
                #     player.move(UP)
                # if event.key == pygame.K_RIGHT:
                #     player.move(RIGHT)
                # if event.key == pygame.K_LEFT:
                #     player.move(LEFT)
        # Update
        if simulating:
            for i in range(speed):
                move = decider.decide(player.board)
                player.move(move)

        # Draw
        render_board(player.board, player.fitness)
        pygame.display.flip()
        fps_clock.tick(fps)


def render_board(board, fit):
    w = len(board)
    h = len(board[0])
    tile_width = width/w
    tile_height = (height)/h
    for j in range(w):
        for i in range(h):
            x = ((j)/w) * width
            y = ((i)/h) * height
            r = pygame.Rect(x + 5, y + 5,
                            tile_width - 10, tile_height - 10)
            pygame.draw.rect(screen, get_color(board[i][j]), r)
            if (board[i][j] > 0):
                str_amt = str(2**board[i][j])
                surface = font.render(str_amt, False, (0, 0, 0))
                text_rect = surface.get_rect(
                    center=(x + tile_width/2, y + tile_height/2))
                screen.blit(surface, text_rect)
    surface = smaller_font.render(f"Score: {fit}", False, (150, 50, 50))
    text_rect = pygame.Rect(10, 15, 100, 50)
    screen.blit(surface, text_rect)


def show_text(txt, x, y):
    surface = smaller_font.render(txt, False, (255, 255, 255))
    text_rect = pygame.Rect(x, y, 50, 50)
    screen.blit(surface, text_rect)


def get_color(val):
    return colors[min(len(colors)-1, val)]


def get_val(col):
    return colors.index(col)


if __name__ == '__main__':
    main()
    pygame.quit()
