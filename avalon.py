# A python script to help manage a local game of Avalon
# Enter the names of your participants and role choices and go on your way.

# Rules are online at https://en.wikipedia.org/wiki/The_Resistance_(game)

# used to execute console commands
import os
# used to assign player roles randomly
import random
from pip._vendor.pkg_resources import require

bad_chars = {"Mordred", "Assassin", "Morgana", "Oberon", "Minion of Mordred"}
good_chars = {"Merlin", "Percival", "Good Guy"}

dict_desc_by_role = {"Mordred": "You are a bad guy who Merlin does not see",
                     "Assassin": "You are a bad guy who decides who to kill should the good guys succeed in passing 3 quests",
                     "Morgana": "You are a bad guy that appears as Merlin to Percival",
                     "Oberon": "You are a bad guy that other bad guys do not know about",
                     "Minion of Mordred": "You are a standard bad guy",
                     "Merlin": "You can see bad guys. If the Assassin guesses who you are at the end of the game, good guys lose.",
                     "Percival": "You know who Merlin is (Morgana also appears as Merlin)",
                     "Good Guy": "You are a good guy. Try to make quests pass."}

# Amount of people required to go on a quest by [playerCount - 5][cur_round]
party_size_for_player_count_and_round = [[2, 3, 2, 3, 3], [2, 3, 4, 3, 4], [2, 3, 3, 4, 4], [3, 4, 4, 5, 5] * 3]
# Number of resistance fighters denoted by [playerCount - 5]
num_resistance = [3, 4, 4, 5, 6, 6]

def main():
    list_players = get_list_players()
    list_possible_roles = chose_possible_roles(len(list_players))
    dict_player_roles = assign_player_roles(list_players, list_possible_roles)
    show_player_roles(list_players, dict_player_roles)
    
    cur_round = 0
    cur_success = 0
    list_rounds_results = list()
    
    # while we did not complete the game and the number of fails < 3 (game ending state)
    while cur_round != 5 and cur_round - cur_success < 3 and cur_success < 3:
        print("Current round map:" + " ".join(list_rounds_results))
        
        required_participants = party_size_for_player_count_and_round[len(list_players) - 5][cur_round]
        input("Commence the party voting stage. Press enter when complete.\n" + 
              "Your party requires %d participants." % required_participants)
        
        participants = [x.lower() for x in input("Please enter the names of the participants (separated by a space on this mission)\n" + 
                                                 "Example: chris logan alex | Please remember to include yourself in the party.\n\n> ").split()]
        while (len(participants) != required_participants):
            participants = [x.lower() for x in input("You need at least %d players on this quest, but you entered %d.\n" % (required_participants, len(participants)) + 
                                                     "Please enter the correct number of participants.\n> ").split()]
            
            
        os.system("cls")
        result = do_round(participants, cur_round)
        cur_success += result
        list_rounds_results.append("PASS" if result else "FAIL")
        os.system("cls")
        
        cur_round += 1
    
    if cur_round - cur_success >= 3:
        print("BAD GUYS WIN HAHA")
    else:
        for player in list_players:
            if dict_player_roles[player] == "Assassin":
                    print("Good guys have completed 3 quests successfully.\n" + 
                          "Bad guys should now reveal themselves and decide who they think Merlin is.")
                    break
            else:
                print("Bad guys lose")
    
    input("GAME OVER")

# get the names of every player
def get_list_players():
    print("Enter the names of the players separated by a space\n")
    return [x.lower() for x in input().split()]    

# let the player chose what roles will be activated throughout the game
def chose_possible_roles(player_count):
    cur_roles = list()
    
    # choose good characters
    print("Select your Resistance\n")
    available_chars = list(good_chars)
    available_chars.sort()
    for (index, char) in enumerate(available_chars):
        print("%d: %s" % (index, char))
    for _ in range(0, num_resistance[player_count - 5]):      
        char = get_selection_from_list(available_chars)
        print("Added %s" % char)
        cur_roles.append(char)
    
    # choose spy characters
    print("Select your Spies\n")
    available_chars = list(bad_chars)
    available_chars.sort()
    for (index, char) in enumerate(available_chars):
        print("%d: %s" % (index, char))
    for _ in range(0, player_count - num_resistance[player_count - 5]):
        char = get_selection_from_list(available_chars)
        print("Added %s" % char)
        cur_roles.append(char)
    return cur_roles

# get the selection of a position from a list
# is safe for invalid operations. :)
def get_selection_from_list(list_of_items):
    selection = -1
    while selection < 0 or selection > len(list_of_items):
        try:
            selection = int(input("Please enter an integer value of a character to add\n> "))
        except ValueError:
            print("Please enter a valid integer value.\n> ")
    return list_of_items[selection]

# assigns each player a role in list_roles
def assign_player_roles(list_players, list_possible_roles):
    # prevent stale randomness
    random.seed()
    
    # roles for each player
    dict_roles = {}
    # assign each player a role
    for player in list_players:
        rand_int = random.randint(0, len(list_possible_roles) - 1)
        dict_roles[player] = list_possible_roles[rand_int]
        # delete it so there can't be two merlins or anything of the like. :o
        del list_possible_roles[rand_int]
    
    return dict_roles

# shows players their roles
def show_player_roles(list_players, dict_player_roles):
    os.system("cls")
    for player in list_players:
        input("Please hand the game to %s. If you are this player, press enter" % player)
        os.system("cls")
        print("%s:" % player)
        print("Your role: " + dict_player_roles[player])
        print("Your role description: %s\n" % dict_desc_by_role[dict_player_roles[player]])
        
        # show Merlins and Morganas
        if dict_player_roles[player] == "Percival":
            list_merlins_or_morganas = [player for player in list_players if dict_player_roles[player] in {"Morgana", "Merlin"}]
            print("Possible Merlins:\n" + "\n".join(list_merlins_or_morganas))
        elif dict_player_roles[player] == "Merlin":
            list_bad_guys_except_mordred = [player for player in list_players if dict_player_roles[player] in {"Morgana", "Minion of Mordred", "Assassin", "Oberon"}]
            print("Bad guys excluding Mordred (if he exists):\n" + "\n".join(list_bad_guys_except_mordred))
        elif dict_player_roles[player] in bad_chars:
            list_bad_guys_except_oberon = [player for player in list_players if dict_player_roles[player] in {"Morgana", "Minion of Mordred", "Assassin", "Mordred"}]
            print("Bad guys excluding Oberon (if he exists):\n" + "\n".join(list_bad_guys_except_oberon))
        
        input("When you are ready, press enter to clear the screen.")
        os.system("cls")
            

# start the round with the number of people on the quest
# returns true if the mission was a success, otherwise false
def do_round(participants, cur_round):
    # 4th mission requires 2 fails if >= 4 participants on the 4th round
    # otherwise, we only require one fail.
    required_fails = 1 if not (cur_round == 4 and len(participants) >= 4) else 2
    
    cur_fails = 0
    for participant in participants:
        input("Please pass the game to %s. If you are this player, press enter." % participant)
        os.system("cls")
        
        choice = input("Hello %s\n" % participant + 
                       "Please type 'p' and press enter to pass the mission,\n" + 
                       "otherwise enter any other key and then press enter.\n> ")
        
        print(choice.strip().lower())
        if choice.strip().lower() != "p":
            cur_fails += 1
        
        # cls the command line so others can't see
        os.system("cls")
    # returns success if the number of fails submitted is less than the required fails
    input("The result of the past round was... (press enter to continue)")
    input(("PASS" if cur_fails < required_fails else "FAIL") + " with %d fails played" % cur_fails)
    
    print("Found %d fails")
    
    return cur_fails < required_fails
    
if __name__ == "__main__":
    main()