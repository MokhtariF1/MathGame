import sys
import pygame
import random
from game_math import shirzad_prime


# -- init pygame -- #
pygame.init()
# -- get width and height -- #
display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
# -- set window size -- #
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# -- load images -- #
start_image = pygame.image.load("assets/img/start.jpg")
start_image = pygame.transform.scale(start_image, (width, height))
background = pygame.image.load("assets/img/background.jpg")
background = pygame.transform.scale(background, (width, height))
lose_image = pygame.image.load("assets/img/game_over.png")
bird = pygame.image.load("assets/img/bird.png")
bird = pygame.transform.scale(bird, (100, 100))
bird_rect = bird.get_rect()
banana_image = pygame.image.load("assets/img/banana.png")
banana_image = pygame.transform.scale(banana_image, (50, 50))
# -- Main Variables -- #
back_x = 0
back_t_x = 800
bird_rect_jazebeh = 0.25
move = 0
bananas = []
claimed_numbers = []
game_status = True
score = 0
user_time = 60
clock = pygame.time.Clock()
show_image = True
start_time = pygame.time.get_ticks()
# -- load fonts -- #
font = pygame.font.Font("assets/font/shirzad.otf", 70)
font_circle = pygame.font.Font("assets/font/num.otf", 25)
# -- create pygame events -- #
create_circle = pygame.USEREVENT
pygame.time.set_timer(create_circle, 5000)
game_time = pygame.USEREVENT + 1
pygame.time.set_timer(game_time, 1000)
# -- load sounds -- #
correct_choice_sound = pygame.mixer.Sound("assets/sounds/correct-choice.mp3")
game_over_sound = pygame.mixer.Sound("assets/sounds/game-over.mp3")
# -- make Banana class -- #
class Banana:
    def __init__(self, x, y, radius, color, num, is_prime):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.num = num
        self.is_claimed = False
        self.is_prime = is_prime

    def draw(self, screen):
        screen.blit(banana_image, (self.x, self.y))
    def get_rect(self):
        banana_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 10, 10)
        return banana_rect
# -- defined a method to create bananas -- #
def create_random_bananas(bananas_count):
    local_bananas = []
    pos = {
        0: (width / 2, height - 300),
        1: (width / 2, height - 700),
    }
    for i in range(bananas_count):
        dest = pos[i]
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        num = random.randint(1, 99)
        is_prime = shirzad_prime(num)
        banana_instance = Banana(dest[0], dest[1], 25, color, num, is_prime)
        local_bananas.append(banana_instance)
    return local_bananas
# -- defined a method to display user score -- #
def display_score():
    text_score = font.render("Score: " + str(score), False, (0, 0, 0))
    text_score_rect = text_score.get_rect()
    text_score_rect.center = (200, 50)
    screen.blit(text_score, text_score_rect)
# -- defined a method to check collision between bird and bananas
def check_collision(bananas_rect):
    if game_status is False:
        return False
    global score
    for banana_rect in bananas_rect:
        banana_num = banana_rect.num
        banana_is_claimed = banana_rect.is_claimed
        banana_rect_ = banana_rect.get_rect()
        if bird_rect.colliderect(banana_rect_):
            if banana_is_claimed is False:
                if banana_rect.is_prime:
                    score += 1
                    correct_choice_sound.play()
                else:
                    score -= 1
                claimed_numbers.append((banana_num, banana_rect.is_prime))
                banana_rect.is_claimed = True
            else:
                continue
            banana_index = bananas.index(banana_rect)
            bananas.pop(banana_index)
            return True
    if bird_rect.top <= -10 or bird_rect.bottom >= height:
        game_over_sound.play()
        return False
    return True

# -- write game loop -- #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                show_image = False
            if event.key == pygame.K_UP:
                if show_image is False:
                    move = 0
                    move -= 8
            if event.key == pygame.K_r and game_status is False:
                game_status = True
                move = 0
                bird_rect.center = (100, 300)
                bananas.clear()
                claimed_numbers.clear()
                score = 0
                user_time = 60
        if event.type == create_circle:
            circle = create_random_bananas(2)
            bananas.extend(circle)
        if event.type == game_time:
            if user_time - 1 < 0:
                game_status = False
            else:
                user_time -= 1
    # Display the background image based on the show_image flag
    if show_image:
        screen.blit(start_image, (0, 0))
    else:
        screen.fill((0, 0, 0))
        screen.blit(background, (back_x, 0))
        screen.blit(background, (back_t_x, 0))
        timeing = font.render("Time: " + str(user_time), False, (0, 0, 0))
        screen.blit(timeing, (width - 300, 15))
        back_t_x -= 0.25
        back_x -= 0.25
        if back_x <= -800:
            back_x = 0
            back_t_x = 800
        game_status = check_collision(bananas)
        if game_status:
            rects = []
            for banana in bananas:
                banana.x -= 1.5
                banana.draw(screen)
                rect = banana.get_rect()
                rects.append(rect)
                num = banana.num
                text = font_circle.render(f"{num}", True, (0, 0, 0))
                screen.blit(text, (banana.x - 10, banana.y - 10))
            # CHECK GAME STATUS
            move += bird_rect_jazebeh
            bird_rect.centery += move
            screen.blit(bird, (100, bird_rect.centery))
            display_score()
        else:
            screen.blit(lose_image, ((width / 2) - (lose_image.get_width() / 2), (height / 2) - (lose_image.get_height() / 2)))
            display_score()
    pygame.display.update()
    clock.tick(90)  # Limit the frame rate to 60 FPS
