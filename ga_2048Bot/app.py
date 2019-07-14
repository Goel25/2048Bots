import random
import pygame
# import simulation as sim
import ga as genetic_alg

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
smaller_font = pygame.font.SysFont("Roboto", 45)
width, height = 900, 850
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")
fps = 60
fps_clock = pygame.time.Clock()
running = True
simulating = False
avg, alive = -1, -1
ga = genetic_alg.GA(75 + 1)
speed = 1
amt_to_show = 1


def main():
    global running, simulating, avg, alive, width, speed, amt_to_show

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
                    avg, alive = ga.step()
                if event.key == pygame.K_p:
                    print("Begin debugging!")

                if event.key == pygame.K_EQUALS:
                    speed += 5
                if event.key == pygame.K_MINUS and speed > 1:
                    speed -= 5

                if event.key == pygame.K_0:
                    # if (amt_to_show + 1) * (amt_to_show + 1) <= len(
                    #         ga.population[0].boards):
                    amt_to_show += 1
                if event.key == pygame.K_9 and amt_to_show > 1:
                    amt_to_show -= 1

                if event.key == pygame.K_s:
                    ga.save_best()
                if event.key == pygame.K_l:
                    ga.load()

                # if event.key == pygame.K_DOWN:
                #     game.move(DOWN)
                # if event.key == pygame.K_UP:
                #     game.move(UP)
                # if event.key == pygame.K_RIGHT:
                #     game.move(RIGHT)
                # if event.key == pygame.K_LEFT:
                #     game.move(LEFT)
        # Update
        if simulating:
            for i in range(speed):
                avg, alive = ga.step()

        # Draw
        boards = ga.population[ga.current_member].alive_boards
        # alive_boards = [curr_member.boards[i] for i in range(
        #     len(curr_member.boards)) if curr_member.boards[i].alive]
        index = -1
        amt_w = width/amt_to_show
        amt_h = height/amt_to_show
        top_buffer = 50
        amt_buffer = top_buffer / 4
        index = 0
        done = False

        for x in range(amt_to_show):
            for y in range(amt_to_show):
                if not done:
                    if y == 0:
                        offset = top_buffer
                    else:
                        offset = top_buffer - (amt_buffer * y)
                    index += 1
                    if index > len(boards) - 1:
                        done = True
                        break
                    render_board(boards[index].board,
                                 boards[index].moves_survived, x *
                                 amt_w, y * amt_h + offset,
                                 amt_w*.95, (amt_h-12.5) * .95)

        gen = ga.generation
        # avg = "{0:.2f}".format(avg)
        show_text(f"Gen: {gen}", 10, 10)
        show_text(f"Avg Score: {format(avg, '.2f')}", width/4 - 50, 10)
        show_text(f"Still Alive: {alive}", width/4 * 2, 10)
        show_text(f"Speed: {speed}", width/4 * 3, 10)

        pygame.display.flip()
        fps_clock.tick(fps)


def render_board(board, f, start_x=0, start_y=0, new_w=width, new_h=height):
    global amt_to_show
    tile_width = new_w/4
    tile_height = new_h/4
    w = len(board)
    h = len(board[0])
    font = pygame.font.SysFont("Roboto", round(150/amt_to_show))
    score_font = pygame.font.SysFont("Roboto", round(100/amt_to_show))
    r = pygame.Rect(start_x + 5, start_y + 5,  # MAKE OUTLINE!
                    new_w - 10, new_h - 10)
    pygame.draw.rect(screen, (51, 51, 51), r)
    for i in range(w):
        for j in range(h):
            x = (i/w) * new_w
            y = (j/h) * new_h
            r = pygame.Rect(x + 2.5 + start_x, y + 2.5 + start_y,
                            tile_width - 5, tile_height - 5)
            pygame.draw.rect(screen, get_color(board[i][j]), r)
            if (board[i][j] > 0):
                str_amt = str(2**board[i][j])
                surface = font.render(str_amt, False, (0, 0, 0))
                text_rect = surface.get_rect(
                    center=(x + tile_width/2 + start_x,
                            y + tile_height/2 + start_y))
                screen.blit(surface, text_rect)

    surface = score_font.render(f"Score: {f}", False, (150, 50, 50))
    text_rect = pygame.Rect(start_x+10, start_y+15, 100, 50)
    screen.blit(surface, text_rect)


def show_text(txt, x, y):
    surface = smaller_font.render(txt, False, (255, 255, 255))
    text_rect = pygame.Rect(x, y, 50, 50)
    screen.blit(surface, text_rect)


def get_color(val):
    return colors[min(len(colors)-1, val)]


if __name__ == '__main__':
    main()
    pygame.quit()
