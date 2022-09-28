from itertools import count
from math import ceil
from random import randrange, randint
import time


#load scenario settings
def scenario_settings():
    global battlefield
    battlefield = [10, 10]
    global enemy_count
    enemy_count = 5
    global friendly_count
    friendly_count = 6
    global lives
    lives = 15
    return

class Game_Instance():
    def __init__(self):
        self.enemy_actors = []
        self.friendly_actors = []

#Actor class definition
class Actors():
    _ids = count(0)
    def __init__(self, actor_type, faction, actor_stats):
        self.id = next(self._ids)
        self.position = []
        self.actor_type = actor_type
        self.state = 1
        self.faction = faction
        self.damage = actor_stats["damage"]
        self.skill = actor_stats["skill"]
        self.health = actor_stats["health"]
        self.initiative = actor_stats["initiative"]

    def update_position(self, new_position):
        self.position = new_position

    def update_health(self, health_change):
        #TODO add healing
        self.health -= health_change

#define actor stats
def get_actor_stats(actor_type):
    #assign stats based on actor type
    if actor_type == "standard":
        actor_stats = {
            "damage": 2,
            "skill": 2,
            "health": 6,
            "initiative": randint(4, 5)}

    return actor_stats

#assign starting position
def deploy_actors(actors):

    overflow = 0

    symmetricality = 1

    #find number of grid columns of enemy troops
    cols = ceil(len(actors) / battlefield[1])
    if cols != 1:
        if symmetricality == 1:
            actors_in_last_column = len(actors) % battlefield[1]
            #print(f"Actors in last column = {actors_in_last_column}")
            if actors_in_last_column > battlefield[1] / 3 :
                if battlefield[1] % 2 == 0 and actors_in_last_column % 2 == 0 or battlefield[1] % 2 != 0 and actors_in_last_column % 2 != 0:
                    pass
                else:
                    #print("Overflow requried")
                    overflow = 1
            else:
                pass

    #print(f"battlefield = [{battlefield[0]}, {battlefield[1]}]")

    #find number of grid columns of enemy troops
    cols += overflow
    #print(f"Columns required = {cols}")

    if actors[0].faction == "enemy":
        #starting column is battlefield extremity - number of cols required
        column = battlefield[0] - cols
        col_offset = 1
    else:
        column = cols -1
        col_offset = - 1

    #print(f"Starting column = {column}")
    actors_in_column = 1

    #find central grid row of battlefield by halving field
    central_row = ceil(battlefield[1] / 2)
    #print(f"Central row = {central_row}")

    #loop through enemy actors
    for i in range(len(actors)):

        #placement column is front column - completed column
        #if column is full, increment column and restart count
        #print(f"Actors in column = {actors_in_column}, battlefield[1] = {battlefield[1]}")
        if actors_in_column >= battlefield[1] + 1:
            #print(f"Moving to next column - {column+1}")
            actors_in_column = 1
            column += col_offset

        #placement row is central row - row offset
        row_offset = (1/4*(-1)**actors_in_column*(-1+(-1)**actors_in_column+2*actors_in_column))
        #print(f"Row offset = {row_offset}")
        row = central_row - (row_offset)

        #set position of actor and increment actors in column
        actors[i].position = [int(column), int(row)]
        actors_in_column += 1

        #print(f"Actor {enemy_actors[i].id} placed at position {enemy_actors[i].position}")

    if overflow == 1:
        actors[-1].position = [column + col_offset, int(central_row)]
        #print(f"Moving actor {enemy_actors[-1].id} back to position {enemy_actors[-1].position}")
    #print()
    return

def generate_actor(faction):
    actor_type = "standard"
    actor_stats = get_actor_stats(actor_type)
    actor = Actors(actor_type, faction, actor_stats)
    return actor

#generate enemy actor objects and list
def generate_actor_list(count, faction):

    generated_actors = []
    #generate actors
    for i in range(count):
        actor = generate_actor(faction)
        #append to actor_list
        generated_actors.append(actor)

    return generated_actors

#Check for actor overlap
def check_for_actor_overlap(position, actor_list):
    for actor in actor_list:
        if actor.position == position and actor.state == 1:
            return True, actor.id
    return False, None

#Check for edge of board
def check_for_edge_of_board(position):
    if position[0] < 0 or position[0] > battlefield[0]:
        return True
    else:
        return False

#check obstructing actor for allegiance
def check_for_enemy(actor, target):
    if actor != target:
        return True
    else:
        return False

#reorder actor list based on initiative
def initiative_roll(actors):

    #print("Rolling for initiative")
    initiatives = []
    re_ordered_list = []

    for i in range(len(actors)):
        #print(f"{actors[i].faction} actor {actors[i].id} with initiative {actors[i].initiative}")
        initiatives.append(actors[i].initiative)

    initiatives.sort(reverse=True)
    #print(f"Resorted initiatives = {initiatives}")

    for i in range(len(initiatives)):
        #time.sleep(3)
        #print(f"Checking initiative {i} - {initiatives[i]}")
        for j in range(len(actors)):
            #print(f"checking against actor {actors[j].id} with initiative {actors[j].initiative}")
            if actors[j] not in re_ordered_list:
                if actors[j].initiative == initiatives[i]:
                    #print("Match found, adding to list")
                    re_ordered_list.append(actors[j])
                    break

    #print(f"Reordered list: ")

    #return reordered list in order of initiative
    return re_ordered_list

def roll_for_hit(modifier, enemy_modifier):
    threshold = 10 + enemy_modifier
    for i in range(modifier):
        dice_roll = randint(0, 20)
        print(f"Dice roll {i+1} result...... {dice_roll} / {threshold}")
        if dice_roll > threshold:
            print(f"Hit!")
            return True
        else:
            print(f"Miss!")
    return False

#run an encounter
def run_encounter(actors):
    print(f"Running encounter between {actors[0].faction} actor {actors[0].id} and {actors[1].faction} actor {actors[1].id}")

    #perform initiative roll
    actors = initiative_roll(actors)
    for actor in actors:
        print(f"{actor.faction} actor {actor.id} attacks with initiative {actor.initiative}")

    for actor in actors:
        for target in actors:
            if target.id != actor.id:
                target_actor = target
        print(f"{actor.faction} actor {actor.id} rolling for a hit...")
        if roll_for_hit(actor.skill, target_actor.skill):
            print(f"Rolling for damage...")
            damage = randint(1, actor.damage)
            print(f"{damage} damage dealt!")
            print(f"{target_actor.faction} actor {target_actor.id} health drops from {target_actor.health} to {target_actor.health - damage}")
            target_actor.health -= damage
            if target_actor.health <= 0:
                print(f"Actor killed!")
                target_actor.state = 0
                if target_actor.faction == "enemy":
                    global enemy_count
                    enemy_count -= 1
                return

    return

#process move
def process_move(actor, actor_list):

    action_found = False

    while action_found == False:

        #attempt to move to new position
        new_position = [actor.position[0] -1, actor.position[1]]

        #check for obstruction
        invalid_move, blocking_actor = check_for_actor_overlap(new_position, actor_list)

        #if actor in the way
        if invalid_move:
            print(f"movement blocked ", end = "")

            #check for enemy
            if check_for_enemy(actor.faction, actor_list[blocking_actor].faction):
                print(f"by enemy, attacking!")
                run_encounter([actor, actor_list[blocking_actor]])
                action_found = True

            else:
                print("by ally, staying put")
                action_found = True

            new_position = [actor.position[0], actor.position[1]]

        #if no obstruction
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

    #update actor position
    actor.update_position(new_position)

    return

#run the simulation
def play(actor_list):
    t = 0
    #loop through the rounds
    game_over = False
    end_state = 1

    while game_over == False:

        #check game_over events
        if end_state != 1:
            game_over = True

        #otherwise
        else:

            '''
            active_enemy_actors, active_friendly_actors = 0, 0
            
            for i in range(len(actor_list)):
                if actor_list[i].state == 1 :
                    if actor_list[i].faction == "enemy":
                        active_enemy_actors += 1
                    else:
                        active_friendly_actors += 1
            
            if active_enemy_actors == 0:
                end_state == 
            '''

            #loop through actor_list
            for actor in actor_list:

                #if out of lives, stop game
                if lives <= 0:
                    end_state = 2
                    break

                print(enemy_count)

                if enemy_count <= 0:
                    end_state = 0
                    break

                #if actor is an enemy
                if actor.faction == "enemy":
                    # check state for active
                    if actor.state != 1:
                        pass

                    # attempt to move
                    else:
                        process_move(actor, actor_list)

                    display_battlefield(actor_list)

        t += 1


        #display_battlefield
    #return win / lose state
    return end_state

def validate_position_input(position):
    try:
        position = position.strip()
        position = position.split(",")
        position = [int(position[0]), int(position[1])]
        return True, position

    except:
        return False, None

#take player input
def position_troops(enemy_actors):
    print(f"You have {friendly_count} soldiers to position")
    print("Input the coordinates of your soldiers in the format [x_coord, y_coord]")
    troop_positions = []
    troops_placed = 0
    friendly_actors = []
    enemy_actor_positions = []
    for enemy in enemy_actors:
        enemy_actor_positions.append(enemy.position)

    #loop while all troops have not been placed
    while troops_placed < friendly_count:
        print(f"Please place soldier {troops_placed + 1} of {friendly_count}: ")
        valid_position = False

        #loop while no valid position found
        while valid_position == False:

            #accept position input
            position = input()

            if "-" in position:
                print("Speed position")

            #validate format of input
            valid_input, position = validate_position_input(position)

            if position in troop_positions or position in enemy_actor_positions:
                valid_input = False

            if not valid_input:
                print("Invalid entry, please try again: ")

            else:
                valid_position = True
                troop_positions.append(position)
                actor = generate_actor("friendly")
                actor.position = position
                friendly_actors.append(actor)
                print(f"Soldier {troops_placed + 1} placed at coordinates {position}")
                troops_placed += 1
                display_battlefield(enemy_actors + friendly_actors)



    return friendly_actors

#display the battlefield
def display_battlefield(actor_list):
    battlefield_display = []

    #loop through all rows
    for row in range(battlefield[1]):
        battlefield_row = []
        #loop through all columns
        for col in range(battlefield[0]):
            #fill row with empty slots
            battlefield_row.append("   ")

        #fill battlefield display with row
        battlefield_display.append(battlefield_row)

    #print(f"Battlefield of size {len(battlefield_display[0])} x {len(battlefield_display)} created")
    #print x values

    #loop through actor_list
    for actor in actor_list:

        #if actor is active
        if actor.state == 1:

            #Use appropriate marker for faction
            if actor.faction == "enemy":
                marker = "X"
            else:
                marker = "Y"
            #generate display icon
            icon = f"{marker}{actor.id}"
            while len(icon) < 3:
                icon += " "

            #place display icon at actor position
            #print(f"Actor {actor.id} at position [{actor.position[0]}], [{actor.position[1]}]")
            #print(f"placing in battlefield display at {battlefield_display[actor.position[0]]}")
            battlefield_display[actor.position[1]][actor.position[0]] = icon


    #print the battlefield
    #print x values
    board = ""
    board += "\n________________________________________________________________________\n"
    for i in range(battlefield[0]):
        board += f"     {i} "
    board += "\n"

    for i in range(len(battlefield_display)):
        label = str(i)
        while len(label) < 3:
            label = label + " "
        board += label
        board += str(battlefield_display[i])
        board += "\n"

    board += "\n________________________________________________________________________\n"

    print(board)

    return

#print welcome message and instructions
def print_welcome():
    #print welcome
    print("Welcome to the game")
    return

#print the scenario
def print_scenario():
    print(f"The enemy army approaches! They have {enemy_count} soldiers!")
    print(f"Position your army before they attack!")
    return


if __name__ == '__main__':


    #print welcome messages
    print_welcome()

    #main game loop
    play_game = True

    while play_game == True:

        #game = Game_Instance()

        #load scenario settings
        scenario_settings()
        print_scenario()

        #generate enemy actors
        enemy_actors = generate_actor_list(enemy_count, "enemy")
        deploy_actors(enemy_actors)

        #for i in range(len(enemy_actors)):
        #    print(f"Enemy actor {enemy_actors[i].id} generated at position {enemy_actors[i].position}")
        #print()
        display_battlefield(enemy_actors)
        print(f"Actor {enemy_actors[0].id} at position {enemy_actors[0].position}")

        skip_positioning = 1
        if not skip_positioning:
            friendly_actors = position_troops(enemy_actors)

        else:
            friendly_actors = generate_actor_list(friendly_count, "friendly")
            deploy_actors(friendly_actors)

        actor_list = enemy_actors + friendly_actors
        end_state = play(actor_list)

        if end_state == 2:
            print("You lost! The enemy broke through your defences!")
        else:
            print("You won! You held the enemy off.... for now....!")

        play_game = False
