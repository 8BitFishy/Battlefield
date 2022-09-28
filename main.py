import pygame
import os
from math import ceil
from itertools import count
from random import randint

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

friendly_actor_count_font = pygame.font.SysFont('Engravers MT', 30)

WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60

background = pygame.transform.scale(pygame.image.load(('background.jpg')), (WIDTH, HEIGHT))

class Actors():
    _ids = count(0)

    def __init__(self, actor_type, faction):
        self.actor_type = actor_type
        self.get_actor_stats()
        self.id = next(self._ids)
        self.position = []
        self.state = 1
        self.faction = faction
        self.damage = self.actor_stats["damage"]
        self.skill = self.actor_stats["skill"]
        self.health = self.actor_stats["health"]
        self.initiative = self.actor_stats["initiative"]

    def update_position(self, new_position):
        self.position = new_position

    def update_health(self, health_change):
        # TODO add healing
        self.health -= health_change

    # define actor stats
    def get_actor_stats(self):
        # assign stats based on actor type
        if self.actor_type == "standard":
            self.actor_stats = {
                "damage": 2,
                "skill": 2,
                "health": 6,
                "initiative": randint(4, 5)}

class Game():
    def __init__(self):
        self.test_attribute = "Test Attribute!"
        self.scenario
        print("Game instance scenario generation complete")
        self.interface
        print("Running game")

    def test_function(self):
        print("Test function!")
        print(self.test_attribute)

    def generate_scenario(self):
        scenario = Scenario()
        return scenario

    def generate_interface(self):
        interface = Interface()
        return interface

    def start_scenario(self):
        self.scenario.friendly_actor_count = len(self.interface.friendly_actor_locations)
        self.scenario.friendly_actor_locations = self.interface.friendly_actor_locations

    def run_game():

        # initialise game_instance
        clock = pygame.time.Clock()
        run = True

        for i in range(len(game_instance.enemy_actors)):
            game_instance.interface.enemy_actor_locations.append(game_instance.enemy_actors[i].position)
        # interface = game_instance.Interface()

        while run:
            # tick game_instance
            clock.tick(FPS)

            # increment timers
            game_instance.interface.arrow_key_delay_timer_x += 1
            game_instance.interface.arrow_key_delay_timer_y += 1

            # collect events in pygame
            for event in pygame.event.get():

                game_instance.interface.keys_pressed = pygame.key.get_pressed()

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if game_instance.interface.lock_interface is not True:
                    # print("Processing events")
                    # print(pygame.event.EventType)

                    # if event is quit, exit game_instance

                    # if key is pressed
                    if event.type == pygame.KEYDOWN:
                        # get key presses and store in list variable
                        game_instance.interface.process_key_press()

                    # if mouse-up detected, reset previous tile to none
                    if event.type == pygame.MOUSEBUTTONUP:
                        game_instance.interface.previous_tile_selected = None

                    if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                        # detect mouse button presses
                        left_mouse_button, middle, right = pygame.mouse.get_pressed()
                        # find mouse position
                        mouse_position = pygame.mouse.get_pos()
                        # find tile from mouse position
                        game_instance.interface.highlighted_tile = game_instance.interface.find_tile_from_location(
                            mouse_position)

                        # if left mouse button or arrow key press detected
                        if left_mouse_button:
                            # print(f"Mouse button down")
                            game_instance.interface.process_mouse_click(mouse_position)
                            # update previously selected tile to current tile
                            game_instance.interface.previous_tile_selected = game_instance.interface.selected_tile



                    # otherwise
                    else:
                        pass

            # process non-event driven activities

            # redraw the interface
            game_instance.interface.draw_window()

class Scenario():
    def __init__(self):
        self.tile_count_x = 20 + 4
        self.tile_count_y = int(self.tile_count_x * 1.5)
        self.enemy_actor_count = 10
        self.enemy_actors = self.generate_actor_list(self.enemy_actor_count, "enemy")
        self.deploy_actors(self.enemy_actors)
        self.friendly_actor_count = 10
        self.friendly_actors = []
        
        print("Scenario generated")
        

    def generate_actor(self, faction):
        actor_type = "standard"
        #actor_stats = get_actor_stats(actor_type)
        actor = Actors(actor_type, faction)
        return actor

    # generate enemy actor objects and list
    def generate_actor_list(self, count, faction):
        generated_actors = []
        # generate actors
        for i in range(count):
            actor = self.generate_actor(faction)
            # append to actor_list
            generated_actors.append(actor)

        return generated_actors

    def deploy_actors(self, actors):
        overflow = 0

        symmetricality = 1

        # find number of grid columns of enemy troops
        cols = ceil(len(actors) / self.tile_count_y)
        if cols != 1:
            if symmetricality == 1:
                actors_in_last_column = len(actors) % game_instance.interface.tile_count_y
                # print(f"Actors in last column = {actors_in_last_column}")
                if actors_in_last_column > self.tile_count_y / 3:
                    if self.tile_count_y % 2 == 0 and actors_in_last_column % 2 == 0 or self.interface.tile_count_y % 2 != 0 and actors_in_last_column % 2 != 0:
                        pass
                    else:
                        # print("Overflow requried")
                        overflow = 1
                else:
                    pass

        # print(f"battlefield = [{battlefield[0]}, {battlefield[1]}]")

        # find number of grid columns of enemy troops
        cols += overflow
        # print(f"Columns required = {cols}")

        if actors[0].faction == "enemy":
            # starting column is battlefield extremity - number of cols required
            column = self.tile_count_x - cols
            col_offset = 1
        else:
            column = cols - 1
            col_offset = - 1

        # print(f"Starting column = {column}")
        actors_in_column = 1

        # find central grid row of battlefield by halving field
        central_row = ceil(self.tile_count_y / 2)
        # print(f"Central row = {central_row}")

        # loop through enemy actors
        for i in range(len(actors)):

            # placement column is front column - completed column
            # if column is full, increment column and restart count
            # print(f"Actors in column = {actors_in_column}, battlefield[1] = {battlefield[1]}")
            if actors_in_column >= self.tile_count_y + 1:
                # print(f"Moving to next column - {column+1}")
                actors_in_column = 1
                column += col_offset

            # placement row is central row - row offset
            row_offset = (1 / 4 * (-1) ** actors_in_column * (-1 + (-1) ** actors_in_column + 2 * actors_in_column))
            # print(f"Row offset = {row_offset}")
            row = central_row - (row_offset)

            # set position of actor and increment actors in column
            actors[i].position = [int(column), int(row)]
            actors_in_column += 1

            # print(f"Actor {enemy_actors[i].id} placed at position {enemy_actors[i].position}")

        if overflow == 1:
            actors[-1].position = [column + col_offset, int(central_row)]
            # print(f"Moving actor {enemy_actors[-1].id} back to position {enemy_actors[-1].position}")
        # print()
        return

    def run_scenario(self):
        print("Run Scenario")
        t = 0
        # loop through the rounds
        game_over = False
        end_state = 1

        while game_over == False:

            # check game_over events
            if end_state != 1:
                game_over = True

            # otherwise
            else:

                # loop through actor_list
                for actor in actor_list:

                    # if out of lives, stop game
                    if lives <= 0:
                        end_state = 2
                        break

                    print(enemy_count)

                    if enemy_count <= 0:
                        end_state = 0
                        break

                    # if actor is an enemy
                    if actor.faction == "enemy":
                        # check state for active
                        if actor.state != 1:
                            pass

                        # attempt to move
                        else:
                            process_move(actor, actor_list)

                        display_battlefield(actor_list)

            t += 1

            # display_battlefield
            game.interface.draw_window()
        # return win / lose state

    # process move
    def process_move(actor, actor_list):
        action_found = False

        while action_found == False:

            # attempt to move to new position
            new_position = [actor.position[0] - 1, actor.position[1]]

            # check for obstruction
            invalid_move, blocking_actor = check_for_actor_overlap(new_position, actor_list)

            # if actor in the way
            if invalid_move:
                print(f"movement blocked ", end="")

                # check for enemy
                if check_for_enemy(actor.faction, actor_list[blocking_actor].faction):
                    print(f"by enemy, attacking!")
                    run_encounter([actor, actor_list[blocking_actor]])
                    action_found = True

                else:
                    print("by ally, staying put")
                    action_found = True

                new_position = [actor.position[0], actor.position[1]]

            # if no obstruction
            else:
                if check_for_edge_of_board(new_position):
                    print("life lost!")
                    actor.state = 2
                    global lives
                    lives -= 1
                    if actor.faction == "enemy":
                        global enemy_count
                        enemy_count -= 1
                action_found = True

        # update actor position
        actor.update_position(new_position)

        return

class Interface():
    def __init__(self):
        print("Generating interface")
        self.lock_interface = False
        self.width = WIDTH
        self.height = HEIGHT
        self.WIN = pygame.display.set_mode((self.width, self.height))
        self.title = pygame.display.set_caption("First Class Game")
        print(Game.run_game())
        self.tile_size_x = self.width / game_instance.scenario.tile_count_x
        self.tile_size_y = self.height / game_instance.scenario.tile_count_y
        self.start_button_dims = [200, self.tile_size_y+1]
        self.tile_select_mode = False
        self.arrow_key_delay_timer_x = 0
        self.arrow_key_delay_timer_y = 0
        self.keys_pressed = []
        self.highlighted_tile = []
        self.previous_tile_selected = None
        self.friendly_actor = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(('friendly_soldier.png')), (self.tile_size_x, self.tile_size_y)), 90)
        self.enemy_actor = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(('enemy_soldier.png')), (self.tile_size_x + 10, self.tile_size_y + 10)), -90)
        self.start_button = pygame.Rect(self.width/2 - self.start_button_dims[0]/2, self.height - self.tile_size_y, self.start_button_dims[0], self.start_button_dims[1])
        self.adding_actors = True
        self.unavailable_tiles = []

        for j in range(game_instance.scenario.tile_count_x):
            for i in range(game_instance.scenario.tile_count_y):
                if j < 2 or i > game_instance.scenario.tile_count_y - 2 or j > game_instance.scenario.tile_count_x//2:
                    self.unavailable_tiles.append([j, i])

        self.selected_tile = [2, 0]
        self.friendly_actor_locations = []
        self.friendly_actor_count = 10
        self.friendly_actors_to_place = 10
        self.enemy_actor_count = 10
        self.enemy_actor_locations = []

    def draw_window(self):
        #Generate background image

        WIN.blit(background, (0, 0))

        info_boarder = pygame.Surface((self.width, self.tile_size_y + 10), pygame.SRCALPHA)  # per-pixel alpha
        info_boarder.fill((0, 0, 0, 100))  # notice the alpha value in the color
        WIN.blit(info_boarder, (0, self.start_button.topright[1]))

        start_button_border_colour = RED
        start_button_border_thickness = 2
        if self.lock_interface is False:
            pygame.draw.rect(WIN, BLACK, (self.start_button))
            start_button_text = friendly_actor_count_font.render(
                f"Start Battle!", 1, text_colour)
            #pygame.draw.line(WIN, start_button_border_colour,
            #                 (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1]),
            #                 (self.start_button.topright[0], self.start_button.topright[1]), start_button_border_thickness)
            #pygame.draw.line(WIN, start_button_border_colour,
            #                 (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1] + self.start_button.height),
            #                 (self.start_button.topright[0], self.start_button.topright[1] + self.start_button.height), start_button_border_thickness)
            pygame.draw.line(WIN, start_button_border_colour,
                             (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1]),
                             (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1]+ self.start_button.height), start_button_border_thickness)
            pygame.draw.line(WIN, start_button_border_colour,
                             (self.start_button.topright[0], self.start_button.topright[1]),
                             (self.start_button.topright[0], self.start_button.topright[1]+ self.start_button.height), start_button_border_thickness)

            WIN.blit(start_button_text, (self.start_button.centerx - start_button_text.get_width()/2, self.start_button.centery - start_button_text.get_height()/2 + 2))


            '''
            #generate tile borders
            for i in range(0, (game_instance.scenario.tile_count_x)):
                pygame.draw.rect(WIN, BLACK, pygame.Rect(self.tile_size_x * i, 0, 2, HEIGHT))
            for i in range(0, (game_instance.scenario.tile_count_y)):
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

            if self.highlighted_tile not in self.unavailable_tiles:

                tile_coords = self.find_location_from_tile(self.highlighted_tile)
                higlighted_tile = pygame.Surface((self.tile_size_x, self.tile_size_y), pygame.SRCALPHA)  # per-pixel alpha
                higlighted_tile.fill((255, 255, 255, 50))  # notice the alpha value in the color


                if tile_coords is not None:
                    WIN.blit(higlighted_tile, (tile_coords[0], tile_coords[1]))

        for i in range(len(self.friendly_actor_locations)):
            actor_location = self.find_location_from_tile(self.friendly_actor_locations[i])
            WIN.blit(self.friendly_actor, (actor_location[0], actor_location[1]))

        for i in range(len(self.enemy_actor_locations)):
            actor_location = self.find_location_from_tile(self.enemy_actor_locations[i])
            WIN.blit(self.enemy_actor, (actor_location[0], actor_location[1]-10))


        friendly_actor_count_text = friendly_actor_count_font.render(
            f"{self.friendly_actors_to_place} soldiers left to place", 1, text_colour)

        enemy_actor_count_text = friendly_actor_count_font.render(f"{self.enemy_actor_count} enemy soldiers attacking!", 1, text_colour)

        WIN.blit(friendly_actor_count_text, (10, self.height - friendly_actor_count_text.get_height() - 10))
        WIN.blit(enemy_actor_count_text, (self.width - enemy_actor_count_text.get_width()-10, self.height - friendly_actor_count_text.get_height() - 10))

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
            0] < game_instance.scenario.tile_count_x - 1 and [self.selected_tile[0]+1, self.selected_tile[1]] not in self.unavailable_tiles:  # RIGHT
            self.selected_tile[0] += 1
            self.arrow_key_delay_timer_x = 0
        elif self.keys_pressed[pygame.K_UP] and self.arrow_key_delay_timer_y > FPS * arrow_key_delay_timer_delay and self.selected_tile[1] > 0:  # UP
            self.selected_tile[1] -= 1
            self.arrow_key_delay_timer_y = 0
        elif self.keys_pressed[pygame.K_DOWN] and self.arrow_key_delay_timer_y > FPS * arrow_key_delay_timer_delay and self.selected_tile[
            1] < game_instance.scenario.tile_count_y - 1:  # DOWN
            self.selected_tile[1] += 1
            self.arrow_key_delay_timer_y = 0

    def process_mouse_click(self, mouse_position):
        # if mouse button pressed, find position of mouse press and reset tile selection mode / visibility
        self.tile_select_mode = True

        print(mouse_position)

        if mouse_position[0] < self.start_button.topright[0] and mouse_position[1] > self.start_button.topright[1] and mouse_position[0] > self.start_button.bottomleft[0] and mouse_position[1] < self.start_button.bottomleft[1]:
            game_instance.scenario.run_scenario()


        #only update previously selected tile if there is a previously selected tile
        if self.previous_tile_selected != None:
            self.previous_tile_selected = self.selected_tile
        self.selected_tile = self.find_tile_from_location(mouse_position)
        #add or remove actor from tile if tile select mode is active and tile is not previously selected tile
        if self.tile_select_mode and self.previous_tile_selected != self.selected_tile:
            self.add_remove_actor_from_tile()











if __name__ == "__main__":
    game_instance = Game()
    game_instance.interface = game_instance.generate_interface()
