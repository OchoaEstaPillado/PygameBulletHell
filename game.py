import pygame
import random
import math
import sys

pygame.init()

c = pygame.time.Clock()

width = 600
height = 600

player_speed_x = 0
player_speed_y = 0
player_speed_normalized_x = 0
player_speed_normalized_y = 0
player_score = 0
collectible_size = 20
collectible_x = random.randint(0, width - collectible_size)
collectible_y = random.randint(0, height - collectible_size)


horizontal_enemy_size_x = 150
vertical_enemy_size_x = 7
horizontal_enemy_size_y = 7
vertical_enemy_size_y = 150
enemy_speed = 5
vertical_enemy_position = random.randint(0, width)
horizontal_enemy_position = random.randint(0, height)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mierdijuego")
#pygame.display.set_icon(pygame.image.load("19047.png"))

player = pygame.Rect(width / 2 - 10, height / 2 -10, 30, 30)
collectible = pygame.Rect(collectible_x, collectible_y, collectible_size, collectible_size)

horizontal_enemies = []
vertical_enemies = []

def create_horizontal_enemy():
    global horizontal_enemy_size_x, horizontal_enemy_size_y
    enemy_x = 0 - horizontal_enemy_size_x
    enemy_y = random.randint(0, height-horizontal_enemy_size_y)
    horizontal_enemy = pygame.Rect(enemy_x, enemy_y, horizontal_enemy_size_x, horizontal_enemy_size_y)
    horizontal_enemies.append(horizontal_enemy)

def create_vertical_enemy():
    global vertical_enemy_size_x, vertical_enemy_size_y
    enemy_x = random.randint(0, width - vertical_enemy_size_x)
    enemy_y = 0 - vertical_enemy_size_y
    vertical_enemy = pygame.Rect(enemy_x, enemy_y, vertical_enemy_size_x, vertical_enemy_size_y)
    vertical_enemies.append(vertical_enemy)

def player_movement():
    global player_speed_x, player_speed_y, player_speed_normalized_x, player_speed_normalized_y
    player_speed_magnitude = math.sqrt(player_speed_x ** 2 + player_speed_y ** 2)

    if player_speed_magnitude > 0:
        player_speed_normalized_x = player_speed_x / player_speed_magnitude
        player_speed_normalized_y = player_speed_y / player_speed_magnitude
    else:
        player_speed_normalized_x = 0
        player_speed_normalized_y = 0
    player.x += player_speed_normalized_x * player_speed_magnitude
    player.y += player_speed_normalized_y * player_speed_magnitude    

    if player.left <= 0:
        player.left = 0
    if player.right >= width:
        player.right = width
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height           

def horizontal_enemy_movement():
    global enemy_speed, player_score
    enemy_speed = enemy_speed + (player_score/10000)
    for enemy in horizontal_enemies:
        enemy.x += enemy_speed

def vertical_enemy_movement():
    global enemy_speed, player_score
    enemy_speed = enemy_speed + (player_score/10000)
    for enemy in vertical_enemies:
        enemy.y += enemy_speed        
    
def remove_out_of_window_enemies():
    for enemy in vertical_enemies[:]:
        if enemy.left > width or enemy.right < 0:
            horizontal_enemies.remove(enemy)

font = pygame.font.SysFont("calibri", 20)

def game_over_screen():
    global player_score
    screen.fill((0, 0, 0))
    go_font = pygame.font.SysFont("calibri", 70)
    score_font = pygame.font.SysFont("calibri", 40)
    go = go_font.render("GAME OVER", False, (255, 0, 0))
    go_rect = go.get_rect(center = (width/2, (height/2 - 50)))
    screen.blit(go, go_rect)
    score_board = score_font.render("Your score: " + str(player_score), False, (255, 0, 0))
    score_rect = score_board.get_rect(center = (width/2, height/2))
    screen.blit(score_board, score_rect)
    instructions_font = pygame.font.SysFont("calibri", 20)
    restart = instructions_font.render("Press SPACE to try again", False, (255, 0, 0))
    restart_rect = restart.get_rect(center = (width/2, height - 40))
    quit = instructions_font.render("Press Q to quit", False, (255, 0, 0))
    quit_rect = quit.get_rect(center=(width/2, height - 20))
    screen.blit(restart, restart_rect)
    screen.blit(quit, quit_rect)
   
    pygame.display.update()

def reset_game():
    global player_speed_x, player_speed_y, player_speed_normalized_x, player_speed_normalized_y
    global player_score, collectible_x, collectible_y
    global horizontal_enemies, vertical_enemies, game_over

    player_speed_x = 0
    player_speed_y = 0
    player_speed_normalized_x = 0
    player_speed_normalized_y = 0
    player_score = 0
    collectible_x = random.randint(0, width - collectible_size)
    collectible_y = random.randint(0, height - collectible_size)

    horizontal_enemies = []
    vertical_enemies = []

    game_over = False

game_over = False
while True:
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit() 
        game_over_screen()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player_speed_y -= 5
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player_speed_y +=5
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player_speed_x -= 5
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player_speed_x += 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player_speed_y += 5
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player_speed_y -=5
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player_speed_x += 5
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player_speed_x -= 5

        if random.randint(0, 20) < 1:
            create_horizontal_enemy()
        if random.randint(0, 20) < 1:
            create_vertical_enemy()    

        player_movement()
        horizontal_enemy_movement()
        vertical_enemy_movement()

        if player.colliderect(collectible):
            collectible_x = random.randint(0, width - collectible_size)
            collectible_y = random.randint(0, height - collectible_size)
            collectible = pygame.Rect(collectible_x, collectible_y, collectible_size, collectible_size)
            player_score += 1  

        for enemy in horizontal_enemies:
            if player.colliderect(enemy):
                game_over = True
        for enemy in vertical_enemies:
            if player.colliderect(enemy):
                game_over = True                  


        remove_out_of_window_enemies()

        screen.fill((0, 0, 0))
        player_center_x, player_center_y = player.center
        pygame.draw.rect(screen, (220, 220, 220), player)
        pygame.draw.rect(screen, (180, 255, 0), collectible)
        for enemy in horizontal_enemies:
            pygame.draw.rect(screen, (255, 0, 0), enemy)
        for enemy in vertical_enemies:
            pygame.draw.rect(screen, (255, 0, 0), enemy)    

        score_text = font.render("Score: " + str(player_score), False, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width/2, 20))
        screen.blit(score_text, score_rect)

        pygame.display.update()
        c.tick(60)                    
