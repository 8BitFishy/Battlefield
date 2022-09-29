import pygame
import os
from math import ceil
from itertools import count
from random import randint

pygame.font.init()
pygame.mixer.init()
WIDTH = 1000
HEIGHT = 500



#BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 2, HEIGHT)

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


class Actors():
    _ids = count(0)

    def __init__(self, actor_type, faction):
        self.actor_type = actor_type
        self.get_actor_stats()
        self.id = next(self._ids) - game_instance.id_modifier
        self.position = []
        self.state = 1
        self.faction = faction
        self.damage = self.actor_stats["damage"]
        self.skill = self.actor_stats["skill"]
        self.health = self.actor_stats["health"]
        self.initiative = self.actor_stats["initiative"]
        self.speed = 1

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
        self.width, self.height = WIDTH, HEIGHT
        self.scenario = None
        self.interface = None
        self.id_modifier = 0
        print("Running game")

    def generate_scenario(self):
        enemy_actor_count = randint(5,
                                    20)
        friendly_actor_count = randint(5, 20)
        print(f"New enemy count = {enemy_actor_count}")
        print(f"Friendly actor count = {friendly_actor_count}")
        if enemy_actor_count > friendly_actor_count:
            lives = ceil(1.1 * (abs(enemy_actor_count - friendly_actor_count)))
        else:
            try:
                lives = int(enemy_actor_count / (abs(enemy_actor_count - friendly_actor_count)))
            except ZeroDivisionError:
                lives = ceil(enemy_actor_count/3)
        scenario = Scenario(enemy_actor_count, friendly_actor_count, lives)
        return scenario

    def generate_interface(self):
        interface = Interface()
        return interface

    def run_game(self):
        game_speed_timer = 0
        button_click_timer = 0

        # initialise game_instance
        clock = pygame.time.Clock()
        run = True
        game_instance.interface.win_lose = False
        '''
        for i in range(len(game_instance.scenario.enemy_actors)):
            game_instance.scenario.enemy_actor_locations.append(game_instance.scenario.enemy_actors[i].position)
        # interface = game_instance.Interface()
        '''

        while run:
            # tick game_instance
            clock.tick(FPS)
            game_speed_timer += 1
            button_click_timer += 1
            # increment timers
            self.interface.arrow_key_delay_timer_x += 1
            self.interface.arrow_key_delay_timer_y += 1



            # collect events in pygame
            for event in pygame.event.get():

                self.interface.keys_pressed = pygame.key.get_pressed()

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if self.interface.lock_interface is not True:
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


            if self.scenario.scenario_running is True:
                if self.scenario.lives <= 0:
                    self.scenario.scenario_running is False
                    self.interface.win_lose = True
                    self.interface.lock_interface = False
                    self.scenario.scenario_running = False

                elif self.scenario.enemy_actor_count <= 0:
                    self.scenario.scenario_running is False
                    self.interface.win_lose = True
                    self.interface.lock_interface = False
                    self.scenario.scenario_running = False

                elif game_speed_timer > 30:
                    game_speed_timer = 0
                    self.scenario.process_move()

            # process non-event driven activities

            # redraw the interface
            self.interface.draw_window()


class Scenario():
    def __init__(self, enemy_actor_count, friendly_actor_count, lives):
        self.scenario_running = False
        self.tile_count_x = 20 + 4
        self.tile_count_y = int(self.tile_count_x * (game_instance.height/game_instance.width))
        self.tile_size_x = game_instance.width / self.tile_count_x
        self.tile_size_y = game_instance.height / self.tile_count_y
        self.enemy_actor_count = enemy_actor_count
        self.enemy_actors = self.generate_actor_list(enemy_actor_count, "enemy")
        self.deploy_actors(self.enemy_actors)
        self.friendly_actor_count = friendly_actor_count
        self.friendly_actor_locations = []
        self.friendly_actors = []
        self.lives = lives
        self.full_actor_list = []
        print("Scenario generated")

    def generate_actor(self, faction):
        actor_type = "standard"
        #actor_stats = get_actor_stats(actor_type)
        actor = Actors(actor_type, faction)
        return actor

    def generate_actor_list(self, count, faction):
        # generate enemy actor objects and list
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
        cols = ceil(len(actors) / (self.tile_count_y - 1))
        if cols != 1:
            if symmetricality == 1:
                actors_in_last_column = len(actors) % (self.tile_count_y - 1)
                # print(f"Actors in last column = {actors_in_last_column}")
                if actors_in_last_column > (self.tile_count_y - 1) / 3:
                    if (self.tile_count_y - 1) % 2 == 0 and actors_in_last_column % 2 == 0 or (self.tile_count_y - 1) % 2 != 0 and actors_in_last_column % 2 != 0:
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
        central_row = ceil((self.tile_count_y) / 2)-1
        # print(f"Central row = {central_row}")

        # loop through enemy actors
        for i in range(len(actors)):

            # placement column is front column - completed column
            # if column is full, increment column and restart count
            # print(f"Actors in column = {actors_in_column}, battlefield[1] = {battlefield[1]}")
            if actors_in_column >= (self.tile_count_y - 1) + 1:
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

    def generate_full_actor_list(self):
        print("Run Scenario")

        self.friendly_actors = self.generate_actor_list(len(self.friendly_actor_locations), "friendly")

        for i in range(len(self.friendly_actors)):
            self.friendly_actors[i].position = self.friendly_actor_locations[i]
            print(f"Friendly actor {self.friendly_actors[i].id} placed at {self.friendly_actors[i].position}")
        self.full_actor_list = self.enemy_actors + self.friendly_actors
        self.friendly_actor_count = len(self.friendly_actors)

    def process_move(self):
        # process move
        # loop through actor_list
        for actor in self.full_actor_list:

            if actor.faction != "enemy":
                continue

            #if actor is active (1 = active, 0 = dead, 2 = escaped
            if actor.state != 1:
                continue

            # attempt to move
            else:
                action_found = False

                while action_found == False:

                    # attempt to move to new position
                    new_position = [actor.position[0] - actor.speed, actor.position[1]]

                    # check for obstruction
                    invalid_move, blocking_actor = self.check_for_actor_overlap(new_position)

                    # if actor in the way
                    if invalid_move:
                        print(f"movement blocked ", end="")

                        # check for enemy
                        print(f"Full actor list = {len(self.full_actor_list)}")
                        print(f"Actor assessed = {blocking_actor}")
                        if self.check_for_enemy(actor.faction, self.full_actor_list[blocking_actor].faction):
                            print(f"by enemy, attacking!")
                            self.run_encounter([actor, self.full_actor_list[blocking_actor]])
                            action_found = True

                        else:
                            print("by ally, staying put")
                            action_found = True

                        new_position = [actor.position[0], actor.position[1]]

                    # if no obstruction
                    else:
                        if self.check_for_edge_of_board(new_position):
                            print("life lost!")
                            actor.state = 2
                            self.lives -= 1
                            if actor.faction == "enemy":
                                self.enemy_actor_count -= 1
                        action_found = True

                # update actor position
                actor.update_position(new_position)

        return

    def check_for_actor_overlap(self, position):
        # Check for actor overlap
        for actor in self.full_actor_list:
            if actor.position == position and actor.state == 1:
                return True, actor.id
        return False, None

    def check_for_enemy(self, actor, target):
        # check obstructing actor for allegiance
        if actor != target:
            return True
        else:
            return False

    def check_for_edge_of_board(self, position):
        # Check for edge of board
        if position[0] < game_instance.interface.safe_zone_width or position[0] > self.tile_count_x:
            return True
        else:
            return False

    def run_encounter(self, actors):
        # run an encounter
        print(
            f"Running encounter between {actors[0].faction} actor {actors[0].id} and {actors[1].faction} actor {actors[1].id}")

        # perform initiative roll
        actors = self.initiative_roll(actors)
        for actor in actors:
            print(f"{actor.faction} actor {actor.id} attacks with initiative {actor.initiative}")

        for actor in actors:
            for target in actors:
                if target.id != actor.id:
                    target_actor = target
            print(f"{actor.faction} actor {actor.id} rolling for a hit...")
            if self.roll_for_hit(actor.skill, target_actor.skill):
                print(f"Rolling for damage...")
                damage = randint(1, actor.damage)
                print(f"{damage} damage dealt!")
                print(
                    f"{target_actor.faction} actor {target_actor.id} health drops from {target_actor.health} to {target_actor.health - damage}")
                target_actor.health -= damage
                if target_actor.health <= 0:
                    print(f"Actor killed!")
                    target_actor.state = 0
                    if target_actor.faction == "enemy":
                        self.enemy_actor_count -= 1
                    else:
                        self.friendly_actor_count -= 1
                    return


        return

    def initiative_roll(self, actors):
        # reorder actor list based on initiative
        initiatives = []
        re_ordered_list = []

        for i in range(len(actors)):
            initiatives.append(actors[i].initiative)

        initiatives.sort(reverse=True)

        for i in range(len(initiatives)):
            for j in range(len(actors)):
                if actors[j] not in re_ordered_list:
                    if actors[j].initiative == initiatives[i]:
                        re_ordered_list.append(actors[j])
                        break

        # return reordered list in order of initiative
        return re_ordered_list

    def roll_for_hit(self, modifier, enemy_modifier):
        threshold = 10 + enemy_modifier
        for i in range(modifier):
            dice_roll = randint(0, 20)
            print(f"Dice roll {i + 1} result...... {dice_roll} / {threshold}")
            if dice_roll > threshold:
                print(f"Hit!")
                return True
            else:
                print(f"Miss!")
        return False


class Interface():
    def __init__(self):
        print("Generating interface")

        self.lock_interface = False
        self.WIN = pygame.display.set_mode((game_instance.width, game_instance.height))
        self.title = pygame.display.set_caption("First Class Game")
        self.start_button_dims = [200, game_instance.scenario.tile_size_y+1]
        self.tile_select_mode = False
        self.arrow_key_delay_timer_x = 0
        self.arrow_key_delay_timer_y = 0
        self.keys_pressed = []
        self.highlighted_tile = []
        self.previous_tile_selected = None
        self.friendly_actor = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(('friendly_soldier.png')), (game_instance.scenario.tile_size_x, game_instance.scenario.tile_size_y)), 90)
        self.enemy_actor = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(('enemy_soldier.png')), (game_instance.scenario.tile_size_x + 10, game_instance.scenario.tile_size_y + 10)), -90)
        self.start_button = pygame.Rect(game_instance.width/2 - self.start_button_dims[0]/2, game_instance.height - game_instance.scenario.tile_size_y, self.start_button_dims[0], self.start_button_dims[1])
        self.adding_actors = True
        self.unavailable_tiles = []
        self.safe_zone_width = 2
        for j in range(game_instance.scenario.tile_count_x):
            for i in range(game_instance.scenario.tile_count_y):
                if j < 2 or i > game_instance.scenario.tile_count_y - self.safe_zone_width or j > game_instance.scenario.tile_count_x//2 - 1:
                    self.unavailable_tiles.append([j, i])

        self.selected_tile = [2, 0]
        self.friendly_actors_to_place = game_instance.scenario.friendly_actor_count

        self.background = pygame.transform.scale(pygame.image.load(('background.jpg')), (game_instance.width, game_instance.height))
        self.win_lose = False

    def draw_window(self):
        #Generate background image
        self.WIN.blit(self.background, (0, 0))

        #generate safe zone fill box
        safe_zone_fill = pygame.Surface((self.safe_zone_width * game_instance.scenario.tile_size_x, game_instance.height - game_instance.scenario.tile_size_y),
                                      pygame.SRCALPHA)
        safe_zone_fill.fill((255, 255, 255, 50))
        self.WIN.blit(safe_zone_fill, (0, 0))

        #generate safe zone text
        if game_instance.scenario.lives <= 0:
            lives_string = "0 LIVES LEFT"
        else:
            if game_instance.scenario.lives != 1:
                lives_string_modifier = "VES"
            else:
                lives_string_modifier = "FE"
            lives_string = f"{game_instance.scenario.lives} LI{lives_string_modifier} LEFT!"


        defend_text = friendly_actor_count_font.render(
            f"DEFEND! {lives_string}", 1, text_colour)
        defend_text = pygame.transform.rotate(defend_text, 90)
        self.WIN.blit(defend_text, (safe_zone_fill.get_width()/2 - defend_text.get_width()/2, safe_zone_fill.get_height()/2 - defend_text.get_height()/2))

        #generate bottom info boarder
        info_boarder = pygame.Surface((game_instance.width, game_instance.scenario.tile_size_y + 10), pygame.SRCALPHA)  # per-pixel alpha
        info_boarder.fill((0, 0, 0, 100))  # notice the alpha value in the color
        self.WIN.blit(info_boarder, (0, self.start_button.topright[1]))



        #if interface lock is not false (i.e. interface is interactible) show controls

        start_button_border_colour = RED
        start_button_border_thickness = 2
        pygame.draw.rect(self.WIN, BLACK, (self.start_button))
        start_button_text_string = "Start Battle!"



        #pygame.draw.line(self.WIN, start_button_border_colour,
        #                 (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1]),
        #                 (self.start_button.topright[0], self.start_button.topright[1]), start_button_border_thickness)
        #pygame.draw.line(self.WIN, start_button_border_colour,
        #                 (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1] + self.start_button.height),
        #                 (self.start_button.topright[0], self.start_button.topright[1] + self.start_button.height), start_button_border_thickness)
        pygame.draw.line(self.WIN, start_button_border_colour,
                         (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1]),
                         (self.start_button.topright[0] - self.start_button.width, self.start_button.topright[1]+ self.start_button.height), start_button_border_thickness)
        pygame.draw.line(self.WIN, start_button_border_colour,
                         (self.start_button.topright[0], self.start_button.topright[1]),
                         (self.start_button.topright[0], self.start_button.topright[1]+ self.start_button.height), start_button_border_thickness)


        '''
        #generate tile borders
        for i in range(0, (game_instance.scenario.tile_count_x)):
            pygame.draw.rect(self.WIN, BLACK, pygame.Rect(game_instance.scenario.tile_size_x * i, 0, 2, HEIGHT))
        for i in range(0, (game_instance.scenario.tile_count_y)):
            pygame.draw.rect(self.WIN, BLACK, pygame.Rect(0, game_instance.scenario.tile_size_y * i, game_instance.width, 2))
        '''
        if self.lock_interface is False and self.win_lose is False:
            # generate start button
            #if showing selected tile
            if self.tile_select_mode == True:
                #draw selected tile
                if self.selected_tile not in self.unavailable_tiles:
                    tile_coords = self.find_location_from_tile(self.selected_tile)
                    selected_tile = pygame.Surface((game_instance.scenario.tile_size_x, game_instance.scenario.tile_size_y), pygame.SRCALPHA)  # per-pixel alpha
                    selected_tile.fill((255, 255, 255, 100))  # notice the alpha value in the color

                    self.WIN.blit(selected_tile, (tile_coords[0], tile_coords[1]))

                '''
                selected_tile = pygame.Rect(tile_coords[0], tile_coords[1],
                            game_instance.scenario.tile_size_x - 2, game_instance.scenario.tile_size_y - 2)
                pygame.draw.rect(self.WIN, RED,selected_tile, 2)
                '''

            if self.highlighted_tile not in self.unavailable_tiles:

                tile_coords = self.find_location_from_tile(self.highlighted_tile)
                higlighted_tile = pygame.Surface((game_instance.scenario.tile_size_x, game_instance.scenario.tile_size_y), pygame.SRCALPHA)  # per-pixel alpha
                higlighted_tile.fill((255, 255, 255, 50))  # notice the alpha value in the color


                if tile_coords is not None:
                    self.WIN.blit(higlighted_tile, (tile_coords[0], tile_coords[1]))

        for i in range(len(game_instance.scenario.friendly_actor_locations)):
            if game_instance.scenario.scenario_running is not True and self.win_lose is not True:
                actor_location = self.find_location_from_tile(game_instance.scenario.friendly_actor_locations[i])
                self.WIN.blit(self.friendly_actor, (actor_location[0], actor_location[1]))
            else:
                try:
                    if game_instance.scenario.friendly_actors[i].state == 1:
                        actor_location = self.find_location_from_tile(game_instance.scenario.friendly_actors[i].position)
                        self.WIN.blit(self.friendly_actor, (actor_location[0], actor_location[1]))
                except:
                    print(f"Attempting to place friendly actor {i} with friendly actor count {len(game_instance.scenario.friendly_actors)}")
        for i in range(len(game_instance.scenario.enemy_actors)):
            if game_instance.scenario.enemy_actors[i].state == 1:
                actor_location = self.find_location_from_tile(game_instance.scenario.enemy_actors[i].position)
                self.WIN.blit(self.enemy_actor, (actor_location[0], actor_location[1]-10))

        if game_instance.scenario.scenario_running is True:
            friendly_actor_text = f"{game_instance.scenario.friendly_actor_count} friendly soldiers left!"
        else:
            friendly_actor_text = f"{self.friendly_actors_to_place} soldiers left to place"
        friendly_actor_count_text = friendly_actor_count_font.render(friendly_actor_text, 1, text_colour)
        self.WIN.blit(friendly_actor_count_text, (10, game_instance.height - friendly_actor_count_text.get_height() - 10))

        enemy_actor_count_text = friendly_actor_count_font.render(f"{game_instance.scenario.enemy_actor_count} enemy soldiers attacking!", 1, text_colour)
        self.WIN.blit(enemy_actor_count_text, (game_instance.width - enemy_actor_count_text.get_width()-10, game_instance.height - friendly_actor_count_text.get_height() - 10))

        if self.win_lose is True:
            start_button_text = "Restart?"
            if game_instance.scenario.lives <= 0:
                text = "You lose!"
            else:
                text = "You win!"

            #restart_text = friendly_actor_count_font.render("Replay?", 1, text_colour)

            #restart_button = pygame.Rect(game_instance.width / 2 - restart_text.get_width() / 2 + 10, game_instance.height / 2 - restart_text.get_height() / 2 + 10 + end_text.get_height(), restart_text.get_width() + 10, restart_text.get_height() + 10)
            #pygame.draw.rect(self.WIN, BLACK, (restart_button))
            #self.WIN.blit(restart_text, (restart_button.center[0] - restart_text.get_width()/2, restart_button.center[1] - restart_text.get_height()/2))

            end_text = friendly_actor_count_font.render(text, 1, text_colour)
            end_text_background_dims = [400, 200]
            end_text_background = pygame.draw.rect(self.WIN, BLACK, pygame.Rect(game_instance.width / 2 - end_text_background_dims[0]/2, game_instance.height / 2 - end_text_background_dims[1]/2, end_text_background_dims[0], end_text_background_dims[1]))
            self.WIN.blit(end_text, (end_text_background.centerx - end_text.get_width()/2, end_text_background.centery - end_text.get_height()/2))

            start_button_text_string = "Restart?"

        start_button_text = friendly_actor_count_font.render(
            start_button_text_string, 1, text_colour)
        self.WIN.blit(start_button_text, (self.start_button.centerx - start_button_text.get_width() / 2,
                                          self.start_button.centery - start_button_text.get_height() / 2 + 2))

        #update the display
        pygame.display.update()

    def find_tile_from_location(self, mouse_click_position):
        # if mouse click detected, generate position of selected tile from mouse position
        #selected tile is taken from division of position of mouse by tile size
        return [int(mouse_click_position[0] // game_instance.scenario.tile_size_x), int(mouse_click_position[1] // game_instance.scenario.tile_size_y)]

    def find_location_from_tile(self, tile):
        try:
            location = [tile[0] * game_instance.scenario.tile_size_x + 2, tile[1] * game_instance.scenario.tile_size_y + 2]
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
        if self.selected_tile not in game_instance.scenario.friendly_actor_locations and self.selected_tile not in self.unavailable_tiles and self.adding_actors is True:
            self.add_actor_to_tile()

        #otherwise, remove actor
        elif self.selected_tile in game_instance.scenario.friendly_actor_locations and self.adding_actors is False:
            self.remove_actor_from_tile()

    def add_actor_to_tile(self):
        if self.friendly_actors_to_place > 0:
            game_instance.scenario.friendly_actor_locations.append([self.selected_tile[0], self.selected_tile[1]])
            self.friendly_actors_to_place -= 1

    def remove_actor_from_tile(self):
        game_instance.scenario.friendly_actor_locations.remove(self.selected_tile)
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

        #print(mouse_position)

        if mouse_position[0] < self.start_button.topright[0] and mouse_position[1] > self.start_button.topright[1] and mouse_position[0] > self.start_button.bottomleft[0] and mouse_position[1] < self.start_button.bottomleft[1]:
            if self.win_lose is False:
                game_instance.scenario.generate_full_actor_list()
                game_instance.scenario.scenario_running = True
                game_instance.interface.lock_interface = True
            else:
                game_instance.id_modifier += len(game_instance.scenario.full_actor_list)
                game_instance.scenario = game_instance.generate_scenario()
                game_instance.interface = game_instance.generate_interface()

        #only update previously selected tile if there is a previously selected tile
        if self.previous_tile_selected != None:
            self.previous_tile_selected = self.selected_tile
        self.selected_tile = self.find_tile_from_location(mouse_position)
        #add or remove actor from tile if tile select mode is active and tile is not previously selected tile
        if self.tile_select_mode and self.previous_tile_selected != self.selected_tile:
            self.add_remove_actor_from_tile()











if __name__ == "__main__":
    game_instance = Game()
    game_instance.scenario = game_instance.generate_scenario()
    game_instance.interface = game_instance.generate_interface()
    game_instance.run_game()