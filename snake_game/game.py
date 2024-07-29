import pygame
import sys
import random
import time

pygame.init()
# Ecran du jeu 
NB_COL = 7
NB_ROW = 7
CELL_SIZE = 80

screen = pygame.display.set_mode((NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Fonction pour afficher la grille
def show_grid():
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (45, 45, 42), rect, width=1)
            
# La bouffe du serpent
class Food:
    def __init__(self):
        self.position = (random.randint(0, NB_COL - 1), random.randint(0, NB_ROW - 1))
        self.color = (218, 47, 47)
        
    def draw(self):
        rect = pygame.Rect(self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)  # Bordure rouge vif

class Block:
    def __init__(self, x, y):
        self.position = (x, y)

class Snake:
    def __init__(self):
        self.body = [Block(3, 3), Block(4, 3), Block(5, 3)]
        self.direction = "RIGHT"
        self.direction_buffer = self.direction
        self.head_animation_frame = 0  # Variable pour suivre l'état de l'animation de la tête
    
    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_coord = block.position[0] * CELL_SIZE
            y_coord = block.position[1] * CELL_SIZE
            
            if index == len(self.body) - 1:  # Tête du serpent
                # Animation de la tête
                if self.head_animation_frame > 0:
                    size_increase = 5  # Taille d'agrandissement de la tête
                    block_rect = pygame.Rect(x_coord - size_increase // 2, y_coord - size_increase // 2, CELL_SIZE + size_increase, CELL_SIZE + size_increase)
                    self.head_animation_frame -= 1  # Décrémenter le compteur d'animation
                else:
                    block_rect = pygame.Rect(x_coord, y_coord, CELL_SIZE, CELL_SIZE)
                
                pygame.draw.rect(screen, (0, 255, 0), block_rect)  # Vert pour la tête
                pygame.draw.rect(screen, (0, 200, 0), block_rect, 3)  # Bordure plus foncée
            else:  # Corps du serpent
                # Utiliser un dégradé cyclique pour le corps
                color_value = 255 - ((index % 25) * 10)  # Dégradé cyclique
                block_rect = pygame.Rect(x_coord, y_coord, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (0, color_value, 0), block_rect)  # Vert dégradé pour le corps
                pygame.draw.rect(screen, (0, max(color_value - 50, 0), 0), block_rect, 3)  # Bordure plus foncée
    
    def move_snake(self):
        self.direction = self.direction_buffer
        old_head = self.body[-1]
        
        if self.direction == "RIGHT":
            new_head = Block(old_head.position[0] + 1, old_head.position[1])
        elif self.direction == "LEFT":
            new_head = Block(old_head.position[0] - 1, old_head.position[1])
        elif self.direction == "UP":
            new_head = Block(old_head.position[0], old_head.position[1] - 1)
        elif self.direction == "DOWN":
            new_head = Block(old_head.position[0], old_head.position[1] + 1)
        
        # Vérifier la collision avec les bords du jeu
        if (new_head.position[0] < 0 or new_head.position[0] >= NB_COL or
            new_head.position[1] < 0 or new_head.position[1] >= NB_ROW):
            return True  # Collision détectée
        
        # Vérifier la collision avec la queue du serpent
        for block in self.body:
            if new_head.position == block.position:
                return True  # Collision détectée
        
        self.body.append(new_head)
        self.body.pop(0)
        
        # Démarrer l'animation de la tête
        self.head_animation_frame = 5  # Nombre de frames pour l'animation de la tête
        
        return False  # Pas de collision

# Création custom event
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 300)  # Réduit pour des mises à jour plus fréquentes

# La game loop principal
game_over = False
food = Food()
snake = Snake()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
        if event.type == SCREEN_UPDATE:
            if snake.move_snake():
                game_over = True  # Collision détectée, fin du jeu
            
            # Vérifier la collision avec la nourriture
            if snake.body[-1].position == food.position:
                # Ajouter un nouveau segment au serpent
                snake.body.insert(0, Block(snake.body[0].position[0], snake.body[0].position[1]))
                
                # Repositionner la nourriture
                food.position = (random.randint(0, NB_COL - 1), random.randint(0, NB_ROW - 1))
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction_buffer = "UP"
            if event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction_buffer = "DOWN"
            if event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction_buffer = "LEFT"
            if event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction_buffer = "RIGHT"

    screen.fill((0, 0, 0))
    show_grid()
    food.draw()
    snake.draw_snake()
    pygame.display.flip()
    clock.tick(10)  # FPS

pygame.quit()
sys.exit()

# Jeu en 5x5 pour l'ia si 7x7 trop dur
# NB_COL = 5
# NB_ROW = 5
# CELL_SIZE = 60
# Position initial du serpent en 5x5 = [Block(2, 2), Block(3, 2), Block(4, 2)].