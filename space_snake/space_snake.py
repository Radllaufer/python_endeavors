# -----  Setup  -----

import pygame
import random
import copy

pygame.init()

font = pygame.font.SysFont('Futura', 30)



# -----  Variables  -----

bg_colour = '#000420'
snake_colour = '#ffe000'
moon_colour = '#bfc7ff'
score_colour = '#9fabff'
highscore_colour = '#9fabff'

background = pygame.image.load('space_snake_bg.png')

screen = pygame.display.set_mode((810, 490)) # + 10px padding on both
pygame.display.set_caption('Space Snake')
clock = pygame.time.Clock()
run = True

prev_snake = None
snake = [ pygame.Rect(210, 250, 30, 30), # + 5px to centre squares inside coordinates
          pygame.Rect(170, 250, 30, 30),
          pygame.Rect(130, 250, 30, 30) ]
moon =   pygame.Rect(615, 255, 20, 20) # + 10px paddington

directions_list = ['']
moving_direction = ''
useable_keys = ['w', 's', 'd']

start_switch = True
speed = 0
interval_counter = 0

score = 0
highscore = 0
score_surface = font.render(f'{score}', True, score_colour)
highscore_surface = font.render(f'{highscore}', True, highscore_colour)
score_rect = score_surface.get_rect(topright = (715, 25))
highscore_rect = highscore_surface.get_rect(topleft = (736, 25))


# -----  General Functions  -----

def randy(min, max):
    return random.randint(min, max)


def get_list_copy(list):
    copied_list = []

    for current in list:
        copied_list.append( copy.copy(current) )

    return copied_list


def get_field_components():
    new_coords = [[], []]
    x = 5
    y = 5

    for _ in range(20):
        new_coords[0].append(x)
        x += 40
    for _ in range(12):
        new_coords[1].append(y)
        y += 40

    return new_coords


def get_available_coords():
    field_components = get_field_components()
    available_coords = []
    occupied_coords = []

    for current_x in field_components[0]:
        for current_y in field_components[1]:
            available_coords.append([current_x, current_y])

    for current_tailpiece in snake:
        if ( current_tailpiece[0] - 5 in field_components[0] and # -5 pad
             current_tailpiece[1] - 5 in field_components[1] ):
            occupied_coords.append([current_tailpiece[0] - 5, current_tailpiece[1] - 5])

    for current_coords in occupied_coords:
        if current_coords in available_coords:
            available_coords.pop( available_coords.index( current_coords ) )

    return available_coords


def behead_snake(condemned_snake):
    beheaded_snake = copy.copy(condemned_snake)
    beheaded_snake.pop(0)
    
    return beheaded_snake



# -----  Main Functions  -----

def reset_game():
    global snake, moon, directions_list, moving_direction, useable_keys, start_switch

    snake = [ pygame.Rect(210, 250, 30, 30),
              pygame.Rect(170, 250, 30, 30),
              pygame.Rect(130, 250, 30, 30) ]
    moon =   pygame.Rect(615, 255, 20, 20)

    directions_list = ['']
    moving_direction = ''
    useable_keys = ['w', 's', 'd']
    start_switch = True


def stop_game():
    global speed
    speed = 0


def set_highscore():
    global score, highscore, score_surface, highscore_surface, score_rect, highscore_rect

    if score > highscore:
        highscore = score

    score = 0
    score_surface = font.render(f'{score}', True, score_colour)
    highscore_surface = font.render(f'{highscore}', True, highscore_colour)
    score_rect = score_surface.get_rect(topright = (715, 25))
    highscore_rect = highscore_surface.get_rect(topleft = (736, 25))


def update_score():
    global score, score_surface, score_rect
    score += 1
    score_surface = font.render(f'{score}', True, score_colour)
    score_rect = score_surface.get_rect(topright = (715, 25))


def check_if_dead():
    field_components = get_field_components()
    beheaded_snake = behead_snake(snake)

    if ( snake[0][0] < field_components[0][0]  or
         snake[0][0] > field_components[0][-1] + 5 or # account for paddington
         snake[0][1] < field_components[1][0]  or
         snake[0][1] > field_components[1][-1] + 5 ):
        
        stop_game()
        set_highscore()

        return True

    if snake[0].collidelist(beheaded_snake) >= 0:
        stop_game()
        set_highscore()

        return True


def move_moon():
    global moon
    available_coords = get_available_coords()

    random_index = randy(0, len(available_coords) - 1)
    random_coords = available_coords[ random_index ]

    moon[0] = random_coords[0] + 10
    moon[1] = random_coords[1] + 10

    update_score()


def extend_tail(last_tailpiece):
    snake.append( pygame.Rect(last_tailpiece[0], last_tailpiece[1], 30, 30) )


def update_tail(initial_snake):
    global snake
    leading_tailpiece = None
    beheaded_snake = behead_snake(snake)
    

    for current_tailpiece in snake:
        i = snake.index(current_tailpiece)
        i_count = 0
        
        if leading_tailpiece:
            for comparison_tailpiece in snake:
                if comparison_tailpiece == current_tailpiece:
                    i_count += 1
            if i_count == 2:
                i = beheaded_snake.index(current_tailpiece) + 1


            if current_tailpiece[0] < leading_tailpiece[0]: # right
                current_tailpiece.move_ip(40, 0)

            elif current_tailpiece[0] > leading_tailpiece[0]: # left
                current_tailpiece.move_ip(-40, 0)

            elif current_tailpiece[1] < leading_tailpiece[1]: # down
                current_tailpiece.move_ip(0, 40)

            elif current_tailpiece[1] > leading_tailpiece[1]: # up
                current_tailpiece.move_ip(0, -40)

        leading_tailpiece = initial_snake[i]


def update_useable_keys(key):
    global useable_keys

    match key:
        case 'w':
            useable_keys = ['w', 'a', 'd']
        case 'a':
            useable_keys = ['a', 'w', 's']
        case 's':
            useable_keys = ['s', 'a', 'd']
        case 'd':
            useable_keys = ['d', 'w', 's']


def turn():
    global moving_direction, useable_keys

    match directions_list[0]:
        case 'w':
            snake[0].move_ip(0, -40)
            moving_direction = 'w'
        case 'a':
            snake[0].move_ip(-40, 0)
            moving_direction = 'a'
        case 's':
            snake[0].move_ip(0, 40)
            moving_direction = 's'
        case 'd':
            snake[0].move_ip(40, 0)
            moving_direction = 'd'
    

def update_directions_list():
    global directions_list
    
    if len(directions_list) >= 2:
        if directions_list[0] == moving_direction:
            directions_list.pop(0)
        else:
            directions_list.pop()


def change_direction(key):
    global directions_list

    if directions_list[0] == moving_direction:
        directions_list[0] = key
    else:
        directions_list.append(key)
        
    update_useable_keys(key)


def update_movement():
    global snake, interval_counter

    interval_counter += speed

    if interval_counter >= 40:
        initial_snake = get_list_copy(snake)
        
        turn()
        update_tail(initial_snake)

        update_directions_list()

        if check_if_dead():
            snake = initial_snake

        interval_counter = 0


def start_game():
    global speed
    speed = 4.5



# -----  Game Loop  -----

while run:
    last_tailpiece = get_list_copy(snake)[-1]

    screen.fill(bg_colour)
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, moon_colour, moon)

    for current_tailpiece in snake:
        pygame.draw.rect(screen, snake_colour, current_tailpiece)
    
    if snake[0].colliderect(moon):
        move_moon()
        extend_tail(prev_last_tailpiece)
        
        pygame.draw.rect(screen, snake_colour, prev_last_tailpiece)

    screen.blit(score_surface, score_rect)
    screen.blit(highscore_surface, highscore_rect)


    for e in pygame.event.get():
        match e.type:
            case pygame.QUIT:
                run = False

            case pygame.KEYDOWN:
                key = pygame.key.name(e.key)


                if key in useable_keys:
                    change_direction(key)

                if e.key == pygame.K_SPACE and speed == 0:
                    reset_game()
                    
            case pygame.KEYUP:
                if key in useable_keys:
                    key = pygame.key.name(e.key)


    prev_last_tailpiece = last_tailpiece

    update_movement()

    if directions_list[0] and start_switch:
        start_game()
        start_switch = False

    pygame.display.flip()
    clock.tick(60)



# -----  End  -----

pygame.quit()