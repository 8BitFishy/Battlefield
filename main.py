import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 2, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
text_colour = (255, 255, 255)
#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

friendly_actor_count_font = pygame.font.SysFont('Engravers MT', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60

background = pygame.transform.scale(pygame.image.load(('background.jpg')), (WIDTH, HEIGHT))



class Game():
    def __init__(self):
        self.interface = Interface()
        self.scenario = Scenario()

class Scenario():
    def __init__(self):
        self.friendly_actor_locations = []

class Interface():
    def __init__(self):
        self.lock_interface = False
        self.width = WIDTH
        self.height = HEIGHT
        self.WIN = pygame.display.set_mode((self.width, self.height))
        self.title = pygame.display.set_caption("First Class Game")
        self.tile_count_x = 20 + 4
        self.tile_count_y = int((self.height/self.width) * self.tile_count_x)
        self.tile_size_x = self.width / (self.tile_count_x)
        self.tile_size_y = self.height / self.tile_count_y
        self.tile_select_mode = False
        self.arrow_key_delay_timer_x = 0
        self.arrow_key_delay_timer_y = 0
        self.keys_pressed = []
        self.highlighted_tile = []
        self.previous_tile_selected = None
        self.friendly_actor = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(('friendly_soldier.png')), (self.tile_size_x, self.tile_size_y)), 90)
        self.enemy_actor = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(('enemy_soldier.png')), (self.tile_size_x, self.tile_size_y)), -90)
        self.adding_actors = True
        self.unavailable_tiles = []

        for j in range(self.tile_count_x):
            for i in range(self.tile_count_y):
                if j < 2 or i > self.tile_count_y - 2 or j > self.tile_count_x//2:
                    self.unavailable_tiles.append([j, i])

        self.selected_tile = [2, 0]
        self.friendly_actor_locations = []
        self.friendly_actor_count = 10
        self.friendly_actors_to_place = 10


    def draw_window(self):
        #Generate background image
        WIN.blit(background, (0, 0))

        '''
        #generate tile borders
        for i in range(0, (self.tile_count_x)):
            pygame.draw.rect(WIN, BLACK, pygame.Rect(self.tile_size_x * i, 0, 2, HEIGHT))
        for i in range(0, (self.tile_count_y)):
            pygame.draw.rect(WIN, BLACK, pygame.Rect(0, self.tile_size_y * i, self.width, 2))
        '''

        #if showing selected tile
        if self.tile_select_mode == True:
            #draw selected tile
            if self.selected_tile not in self.unavailable_tiles:
                tile_coords = self.find_location_from_tile(self.selected_tile)
                selected_tile = pygame.Surface((self.tile_size_x, self.tile_size_y), pygame.SRCALPHA)  # per-pixel alpha
                selected_tile.fill((255, 255, 255, 100))  # notice the alpha value in the color

                WIN.blit(selected_tile, (tile_coords[0], tile_coords[1]))

            '''
            selected_tile = pygame.Rect(tile_coords[0], tile_coords[1],
                        self.tile_size_x - 2, self.tile_size_y - 2)
            pygame.draw.rect(WIN, RED,selected_tile, 2)
            '''

        for i in range(len(self.friendly_actor_locations)):
            actor_location = self.find_location_from_tile(self.friendly_actor_locations[i])
            WIN.blit(self.friendly_actor, (actor_location[0], actor_location[1]))


        if self.highlighted_tile not in self.unavailable_tiles:

            tile_coords = self.find_location_from_tile(self.highlighted_tile)
            higlighted_tile = pygame.Surface((self.tile_size_x, self.tile_size_y), pygame.SRCALPHA)  # per-pixel alpha
            higlighted_tile.fill((255, 255, 255, 50))  # notice the alpha value in the color


            if tile_coords is not None:
                WIN.blit(higlighted_tile, (tile_coords[0], tile_coords[1]))

        friendly_actor_count_text = friendly_actor_count_font.render(
            f"actors left to place = {self.friendly_actors_to_place}", 1, text_colour)

        WIN.blit(friendly_actor_count_text, (10, self.height - friendly_actor_count_text.get_height() - 10))

        #update the display
        pygame.display.update()

    def find_tile_from_location(self, mouse_click_position):
        # if mouse click detected, generate position of selected tile from mouse position
        #selected tile is taken from division of position of mouse by tile size
        return [int(mouse_click_position[0] // self.tile_size_x), int(mouse_click_position[1] // self.tile_size_y)]

    def find_location_from_tile(self, tile):
        try:
            location = [tile[0] * self.tile_size_x + 2, tile[1] * self.tile_size_y + 2]
            return location
        except:
            return None

    def process_key_press(self):
        #process key presses

        # if escape is pressed, handle response
        if self.keys_pressed[pygame.K_ESCAPE]:
            self.tile_select_mode = False

        #if key press is an arrow key, send to handler
        if self.keys_pressed[pygame.K_UP] or self.keys_pressed[pygame.K_DOWN] or self.keys_pressed[pygame.K_LEFT] or self.keys_pressed[pygame.K_RIGHT]:
            #handle arrow key presses, return boolean variable if arrow keys pressed
            self.tile_select_mode = True
            self.arrow_key_press_handler()


        #if key press is space key, send to handler
        if self.keys_pressed[pygame.K_SPACE]:
            self.tile_select_mode = True
            self.add_remove_actor_from_tile()

    def add_remove_actor_from_tile(self):
        if self.keys_pressed[pygame.K_LCTRL]:
            self.adding_actors = False
        else:
            self.adding_actors = True

        #if no actor in selected tile, add actor
        if self.selected_tile not in self.friendly_actor_locations and self.selected_tile not in self.unavailable_tiles and self.adding_actors is True:
            self.add_actor_to_tile()

        #otherwise, remove actor
        elif self.selected_tile in self.friendly_actor_locations and self.adding_actors is False:
            self.remove_actor_from_tile()

    def add_actor_to_tile(self):
        if self.friendly_actors_to_place > 0:
            self.friendly_actor_locations.append([self.selected_tile[0], self.selected_tile[1]])
            self.friendly_actors_to_place -= 1

    def remove_actor_from_tile(self):
        self.friendly_actor_locations.remove(self.selected_tile)
        self.friendly_actors_to_place += 1

    def arrow_key_press_handler(self):
        # handle arrow key presses, checking for edge of interface and updating selected tile variable

        #timer to prevent multiple arrow key presses
        arrow_key_delay_timer_delay = 0.15

        if self.keys_pressed[pygame.K_LEFT] and self.arrow_key_delay_timer_x > FPS * arrow_key_delay_timer_delay and self.selected_tile[0] > 0 and [self.selected_tile[0]-1, self.selected_tile[1]] not in self.unavailable_tiles:  # LEFT
            self.selected_tile[0] -= 1
            self.arrow_key_delay_timer_x = 0
        elif self.keys_pressed[pygame.K_RIGHT] and self.arrow_key_delay_timer_x > FPS * arrow_key_delay_timer_delay and self.selected_tile[
            0] < self.tile_count_x - 1 and [self.selected_tile[0]+1, self.selected_tile[1]] not in self.unavailable_tiles:  # RIGHT
            self.selected_tile[0] += 1
            self.arrow_key_delay_timer_x = 0
        elif self.keys_pressed[pygame.K_UP] and self.arrow_key_delay_timer_y > FPS * arrow_key_delay_timer_delay and self.selected_tile[1] > 0:  # UP
            self.selected_tile[1] -= 1
            self.arrow_key_delay_timer_y = 0
        elif self.keys_pressed[pygame.K_DOWN] and self.arrow_key_delay_timer_y > FPS * arrow_key_delay_timer_delay and self.selected_tile[
            1] < self.tile_count_y - 1:  # DOWN
            self.selected_tile[1] += 1
            self.arrow_key_delay_timer_y = 0

    def process_mouse_click(self, mouse_position):
        # if mouse button pressed, find position of mouse press and reset tile selection mode / visibility
        self.tile_select_mode = True
        #only update previously selected tile if there is a previously selected tile
        if self.previous_tile_selected != None:
            self.previous_tile_selected = self.selected_tile
        self.selected_tile = self.find_tile_from_location(mouse_position)
        #add or remove actor from tile if tile select mode is active and tile is not previously selected tile
        if self.tile_select_mode and self.previous_tile_selected != self.selected_tile:
            self.add_remove_actor_from_tile()








def main():

    #initialise game
    clock = pygame.time.Clock()
    run = True
    game = Game()
    #interface = game.Interface()

    while run:
        #tick game
        clock.tick(FPS)
        
        #increment timers
        game.interface.arrow_key_delay_timer_x += 1
        game.interface.arrow_key_delay_timer_y += 1

        
        #collect events in pygame
        for event in pygame.event.get():

            game.interface.keys_pressed = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if game.interface.lock_interface is not True:
                #print("Processing events")
                #print(pygame.event.EventType)

                #if event is quit, exit game


                #if key is pressed
                if event.type == pygame.KEYDOWN:
                    # get key presses and store in list variable
                    game.interface.process_key_press()

                #if mouse-up detected, reset previous tile to none
                if event.type == pygame.MOUSEBUTTONUP:
                    game.interface.previous_tile_selected = None


                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    # detect mouse button presses
                    left_mouse_button, middle, right = pygame.mouse.get_pressed()
                    #find mouse position
                    mouse_position = pygame.mouse.get_pos()
                    #find tile from mouse position
                    game.interface.highlighted_tile = game.interface.find_tile_from_location(mouse_position)

                    # if left mouse button or arrow key press detected
                    if left_mouse_button:
                        #print(f"Mouse button down")
                        game.interface.process_mouse_click(mouse_position)
                        #update previously selected tile to current tile
                        game.interface.previous_tile_selected = game.interface.selected_tile



                #otherwise
                else:
                    pass


        #process non-event driven activities





        #redraw the interface
        game.interface.draw_window()




if __name__ == "__main__":
    main()