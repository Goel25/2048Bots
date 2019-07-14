import random
import pygame
import simulation as sim

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
    (255, 0, 0),  # 512 FIGURE OUT CORRECT COLOR
    (255, 255, 0),  # 1024 FIGURE OUT CORRECT COLOR
    (255, 255, 255)]  # 2048 FIGURE OUT CORRECT COLOR
DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Roboto", 75)
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
fps = 60
fps_clock = pygame.time.Clock()
running = True
tile_width = width/4
tile_height = height/4
game = sim.Game()


def main():
    global running

    while running:
        screen.fill((51, 51, 51))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_DOWN:
                    game.move(DOWN)
                if event.key == pygame.K_UP:
                    game.move(UP)
                if event.key == pygame.K_RIGHT:
                    game.move(RIGHT)
                if event.key == pygame.K_LEFT:
                    game.move(LEFT)
        # Update

        # Draw
        render_board(game.board)

        pygame.display.flip()
        fps_clock.tick(fps)


def render_board(board):
    w = len(board)
    h = len(board[0])
    for i in range(w):
        for j in range(h):
            x = (i/w) * width
            y = (j/h) * height
            r = pygame.Rect(x + 5, y + 5, tile_width - 10, tile_height - 10)
            pygame.draw.rect(screen, get_color(board[i][j]), r)
            if (board[i][j] > 0):
                str_amt = str(2**board[i][j])
                surface = font.render(str_amt, False, (0, 0, 0))
                text_rect = surface.get_rect(
                    center=(x + tile_width/2, y + tile_height/2))
                screen.blit(surface, text_rect)


def get_color(val):
    return colors[min(len(colors)-1, val)]


if __name__ == '__main__':
    main()
    pygame.quit()
