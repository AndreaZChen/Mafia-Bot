#!/usr/bin/env python3.4

### The Mafia Bot's token is: [REDACTED]
### The TCoD Mafia chat id is: [REDACTED]
### The Private Testing chat id is: [REDACTED]

###SETUP
from telegram.ext import *
from telegram import *
from random import shuffle
from random import choice
from random import randint
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater = Updater(token='') #TOKEN REDACTED
dispatcher = updater.dispatcher

###FRIEND LIST

friend_dict = {}
#FRIEND IDS REDACTED


###ROLES

class Role:
    def __init__(self,name='Unknown',alignment='Innocent',info='Unknown', has_night_action = False, has_day_action = False, number_of_targets = 0, priority = 0,
    sends_mafia_kill = False, can_self_target = True,shots = -1):
        self.name = name
        self.alignment = alignment
        self.info = info
        self.has_night_action = has_night_action
        self.has_day_action = has_day_action
        self.number_of_targets = number_of_targets
        self.priority = priority
        self.sends_mafia_kill = sends_mafia_kill
        self.can_self_target = can_self_target
        self.shots = shots

    def dayPower(self,bot,update,player):
        global group_id
        if self.name == "Horgie":
            string = "ATTENTION: " + player.name + " is confirmed to be INNOCENT!\n"
            bonus_string = choice(["I mean, they like to knitting in their spare time and everything!",
                                    "They didn't mean to bother anyone!",
                                    "What kind of monster would ever accuse this poor thing of being mafia?",
                                    "How could they be anything but?",
                                    "Look at them. They couldn't hurt a fly!"])
            string += bonus_string
            bot.sendMessage(chat_id=group_id, text=string)

##Create roles
role_database = {}

role_database['Vanilla'] = Role(name='Vanilla',
    alignment='Innocent',
    info = "You are a Vanilla Innocent!\nYou have no special powers.\nYou win when all the mafiosi are dead.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 0,
    sends_mafia_kill = False)

role_database['Cop'] = Role(name='Cop',
    alignment='Innocent',
    info = "You are a Cop!\nDuring the night, you may inspect a player to learn their alignment.\nYou win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 0,
    sends_mafia_kill = False)

role_database['Rolecop'] = Role(name='Rolecop',
    alignment='Innocent',
    info = "You are a Rolecop!\nDuring the night, you may inspect a player to learn their role. " \
    "Note that this will NOT tell you their alignment (so a powerless role would show up as Vanilla regardless of alignment, for example).\n" \
    "You win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 0,
    sends_mafia_kill = False)

role_database['Oracle'] = Role(name='Oracle',
    alignment='Innocent',
    info = "You are an Oracle!\nDuring the night, you may target two players. The first player's alignment is revealed to the second player. " \
    "You cannot target yourself, however.\nYou win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 2,
    priority = 0,
    sends_mafia_kill = False,
    can_self_target = False)

role_database['Doctor'] = Role(name='Doctor',
    alignment='Innocent',
    info = "You are a Doctor!\nDuring the night, you may heal another player to prevent them from dying that night. "
    "However, if the target is healed by several sources at once, they overdose and die!\n"
    "You win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 3,
    sends_mafia_kill = False,
    can_self_target = False)

role_database['Roleblocker'] = Role(name='Roleblocker',
    alignment='Innocent',
    info = "You are a Roleblocker!\nDuring the night, you may roleblock a player, negating their powers.\nYou win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 10,
    sends_mafia_kill = False,
    can_self_target = False)

role_database['Vigilante'] = Role(name='Vigilante',
    alignment='Innocent',
    info = "You are a Vigilante!\nDuring the night, you may kill a player.\nYou win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 5,
    sends_mafia_kill = False)

role_database['Bulletproof'] = Role(name='Bulletproof',
    alignment='Innocent',
    info = "You are a Bulletproof Innocent!\nYou can survive a kill at night, but only once.\nYou win when all the mafiosi are dead.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 5,
    sends_mafia_kill = False,
    shots = 1)

role_database['Horgie'] = Role(name='Horgie',
    alignment='Innocent',
    info = "You are a Horgie!\nDuring the day, you may activate your power to have the bot publicly confirm your innocence.\nYou win when all the mafiosi are dead.",
    has_night_action = False,
    has_day_action = True,
    number_of_targets = 0,
    priority = 5,
    sends_mafia_kill = False)

role_database['Miller'] = Role(name='Miller',
    alignment='Innocent',
    info = "You are a Miller!\nAlthough you are Innocent, investigative roles will see you as Mafia. How unfair!\nYou win when all the mafiosi are dead.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 11,
    sends_mafia_kill = False)

role_database['Tracker'] = Role(name='Tracker',
    alignment='Innocent',
    info = "You are a Tracker!\nDuring the night, you may track a player to learn who their targets were that night (if any).\nYou win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 0,
    sends_mafia_kill = False)

role_database['Watcher'] = Role(name='Watcher',
    alignment='Innocent',
    info = "You are a Watcher!\nDuring the night, you may watch a player to learn who targeted them that night (if anyone).\nYou win when all the mafiosi are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 0,
    sends_mafia_kill = False)

###

role_database['Alien'] = Role(name='Alien',
    alignment='Alien',
    info = "You are an Alien!\nYou can survive a kill at night, but only once. If you do, you become activated.\nYou win if you get lynched while you are activated.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 0,
    sends_mafia_kill = False)

role_database['Serial Killer'] = Role(name='Serial Killer',
    alignment='Serial Killer',
    info = "You are a Serial Killer!\nDuring the night, you may kill a player. Also, you can survive a kill at night, but only once.\nYou win when everybody else is dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 5,
    sends_mafia_kill = False)

###

role_database['Mafioso'] = Role(name='Vanilla',
    alignment='Mafia',
    info = "You are a Mafioso!\nYou may communicate privately with other mafiosi. During the night, you (or another mafia member) may kill a player.\n"
    "You win when all the innocents are dead.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 0,
    sends_mafia_kill = True)

role_database['Godfather'] = Role(name='Godfather',
    alignment='Mafia',
    info = "You are a Mafia Godfather!\nDuring the night, you (or another mafia member) may kill a player.\n"
    "Also, even though you are Mafia, investigative roles will see you as Innocent. How tricksy!\nYou win when all the innocents are dead.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 11,
    sends_mafia_kill = True)

role_database['Mafia Doctor'] = Role(name='Doctor',
    alignment='Mafia',
    info = "You are a Mafia Doctor!\nYou may communicate privately with other mafiosi. During the night, you (or another mafia member) may kill a player.\n" \
    "Also, during the night, you may heal another player to prevent them from dying that night. "
    "However, if the target is healed by several sources at once, they overdose and die!\n"
    "You win when all the innocents are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 3,
    sends_mafia_kill = True,
    can_self_target = False)

role_database['Mafia Roleblocker'] = Role(name='Roleblocker',
    alignment='Mafia',
    info = "You are a Mafia Roleblocker!\nYou may communicate privately with other mafiosi. During the night, you (or another mafia member) may kill a player.\n" \
    "Also, during the night, you may roleblock a player, negating their powers.\n"
    "You win when all the innocents are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 10,
    sends_mafia_kill = True,
    can_self_target = False)

role_database['Mafia Rolecop'] = Role(name='Rolecop',
    alignment='Mafia',
    info = "You are a Mafia Rolecop!\nYou may communicate privately with other mafiosi. During the night, you (or another mafia member) may kill a player.\n" \
    "Also, during the night, you may inspect a player to learn their role.\n"
    "You win when all the innocents are dead.",
    has_night_action = True,
    has_day_action = False,
    number_of_targets = 1,
    priority = 0,
    sends_mafia_kill = True)

role_database['Mafia Bulletproof'] = Role(name='Bulletproof',
    alignment='Mafia',
    info = "You are a Bulletproof Mafioso!\nYou can survive a kill at night, but only once.\nYou win when all the innocents are dead.",
    has_night_action = False,
    has_day_action = False,
    number_of_targets = 0,
    priority = 5,
    sends_mafia_kill = True,
    shots = 1)

###DEFINE PLAYER CLASS

class Player:
    def __init__(self,name='Unknown',id=0,alignment='Innocent',role=role_database['Vanilla'],chat_id = 0):
        self.name = name
        self.id = id
        self.alignment = alignment #'Innocent' or 'Mafia'
        self.role = role
        self.chat_id = chat_id

        self.status = 'Alive' #or 'Dead'
        self.effects = []
        self.targets = []
        self.targeted_by = []
        self.action_used = False
        self.shots = self.role.shots
        self.vote_targets = []
        self.is_abstaining = False
        self.votes = 0
        self.subpriority = 0

    def removeTempEffects(self): #Remove temporary effects
        for temp_effect in ['blocked','dying','healed']:
            while temp_effect in self.effects:
                self.effects.remove(temp_effect)


    def __eq__(self,other):
        if self.id == other.id:
            return(True)
        else:
            return(False)

    def sentMafiaKill(self):
        global mafia_kill
        if mafia_kill[0] and self == mafia_kill[2]:
            return(True)
        else:
            return(False)

    def flip(self):
        if not (self.alignment == 'Innocent' or self.alignment == 'Mafia'):
            return('neither Innocent nor Mafia')
        else:
            return(self.alignment)

###DEFINE BEHIND-THE-SCENES FUNCTIONS
def clearGame(): #Cleanup after game is finished
    global group_id
    global player_dict
    global dead_players
    global mafia_ids
    global host_id
    global phase
    global day_count
    global abstain_votes
    global mafia_kill
    global abort_confirmation
    global tiebreaker
    global roles
    group_id = 0 #Default group ID redacted
    player_dict = {}
    dead_players = []
    mafia_ids = []
    host_id = 0
    phase = 'off' #off, startup, day, night
    day_count = 0
    abstain_votes = 0
    mafia_kill = [False,None,None] #Sent bool, victim, killer
    abort_confirmation = False
    tiebreaker = Player()
    roles = []

def playerIsValid(bot,update,user_id, #Checks if player is allowed to input a command
    allow_off = False,
    allow_startup = False,
    allow_day = False,
    allow_night = False,
    allow_nonplayer = False,
    only_host = False,
    only_private = False,
    allow_dead = False):
    global phase
    global player_dict
    global mafia_kill
    global host_id

    if not allow_off and phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="No game exists yet!",reply_to_message_id=update.message.message_id)
        return(False)
    elif not allow_startup and phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="The game hasn't started yet!",reply_to_message_id=update.message.message_id)
        return(False)
    elif not allow_nonplayer and not user_id in player_dict:
        bot.sendMessage(chat_id=update.message.chat_id, text="You are not a player!",reply_to_message_id=update.message.message_id)
        return(False)
    elif only_host and not user_id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can do that!",reply_to_message_id=update.message.message_id)
        return(False)
    elif allow_dead == False and user_id in player_dict and player_dict[user_id].status == 'Dead':
        bot.sendMessage(chat_id=update.message.chat_id, text="You are dead!",reply_to_message_id=update.message.message_id)
        return(False)
    elif only_private and not update.message.chat.type == 'private':
        bot.sendMessage(chat_id=update.message.chat_id, text="Message me privately to do that!",reply_to_message_id=update.message.message_id)
        return(False)
    elif not allow_day and phase == 'day':
        bot.sendMessage(chat_id=update.message.chat_id, text="You can't do that during the day phase!",reply_to_message_id=update.message.message_id)
        return(False)
    elif not allow_night and phase == 'night':
        bot.sendMessage(chat_id=update.message.chat_id, text="You can't do that during the night phase!",reply_to_message_id=update.message.message_id)
        return(False)
    else:
        return(True)

def offerTargets(bot,update,command): ##Prompt the user to pick a target for /action. Provides a handy keyboard too
    global player_dict
    target_keyboard = []
    for target_id in player_dict:
        target = player_dict[target_id]
        target_keyboard.append([command + " " + target.name])
    reply_markup = ReplyKeyboardMarkup(keyboard=target_keyboard,resize_keyboard=True,one_time_keyboard=True,selective=True)
    bot.sendMessage(chat_id=update.message.chat_id, text="Choose a player.", reply_markup=reply_markup,reply_to_message_id=update.message.message_id)

def findTarget(bot,update,args): ##Checks if target is an existing player
    global player_dict
    target_name = ' '.join(args)
    for i in player_dict:
        if player_dict[i].name.upper() == target_name.upper():
            if player_dict[i].status == 'Alive':
                return([True,player_dict[i]])
    else:
        return([False,None])

def setTarget(player,target): #Sets targeting
    player.targets.append(target)
    target.targeted_by.append(player)

def inspect(target): #Returns inspection results
    if (target.alignment == 'Innocent' and not 'misleading' in target.effects) \
    or (target.alignment == 'Mafia' and 'misleading' in target.effects) \
    or (target.alignment == 'Alien' and not 'activated' in target.effects):
        return('Innocent')
    elif (target.alignment == 'Mafia' and not 'misleading' in target.effects) \
    or (target.alignment == 'Innocent' and 'misleading' in target.effects) \
    or (target.alignment == 'Alien' and 'activated' in target.effects):
        return('Mafia')
    else:
        return('neither Innocent nor Mafia')

def sendNightMessage(bot,update):
    global player_dict
    global day_count
    for player in player_dict.values():
            if player.status == 'Alive':
                string = "NIGHT " + str(day_count) + " begins!\n"
                if player.role.has_night_action:
                    string += "Type /action or /target to use your night action, or pass on it with /pass.\n"
                if player.role.sends_mafia_kill:
                    string += "Type /kill to send in the mafia kill, or just /pass. Be sure to discuss this with the other mafiosi, if any.\n"
                elif not player.role.has_night_action:
                    string += "You have nothing to do at night, so just wait for everyone else to send in their actions."
                bot.sendMessage(chat_id=player.chat_id, text=string)

def sendDayMessage(bot,update):
    global player_dict
    global day_count
    for player in player_dict.values():
            if player.status == 'Alive':
                string = "DAY " + str(day_count) + " begins!\n"
                if player.role.has_day_action:
                    string += "Type /action or /target to use your day action.\n"
                string += "Type /vote or /lynch to lynch a player.\nType /abstain if you want to lynch no one.\nType /retract to change your vote."
                bot.sendMessage(chat_id=player.chat_id, text=string)

def sendDeathMessage(bot,victim):
    ##Send personal message too
    message = "YOU HAVE DIED!\n"
    bonus_string = choice(["I'm sorry, pal. But you can still hang around and shitpost if you want!",
                            "That's too bad. But you can stick around and see how the game goes!",
                            "Ouch. But you did your best and that's what really matters!",
                            "Oh my. Well, stuff like this happens, right?",
                            "I hope you don't feel too bad about it, hehe!",
                            "Ah well. At least it's fun, right?"])
    message += bonus_string
    bot.sendMessage(chat_id=victim.chat_id, text=message)

def waitingOn(player):
    global mafia_kill
    if player.status == 'Alive':
        ##If not a mafia killer
        if player.role.sends_mafia_kill == False:
            if player.role.has_night_action and not player.action_used:
                return(True)
            else:
                return(False)
        ##If a mafia killer
        else:
            if player.sentMafiaKill() or player.action_used or (mafia_kill[0] and not player.role.has_night_action):
                return(False)
            else:
                return(True)

    else:
        return(False)

def checkIfNightFinished(bot,update):
    global test_mode
    global player_dict

    for player in player_dict.values():
        if waitingOn(player):
            break
    else:
        if not test_mode:
            resolveNightActions(bot,update) #If we're waiting on no one, resolve the night actions.
        else:
            bot.sendMessage(chat_id=group_id, text="The night actions have now been sent in, but in TEST MODE, "
            "the night phase still needs to be advanced manually.")



def resolveNightKill():
    global mafia_kill
    victim = mafia_kill[1]
    killer = mafia_kill[2]
    if not 'blocked' in killer.effects:
        victim.effects.append('dying')

def resolveNightActions(bot,update):
    global phase
    global group_id
    global player_dict
    global mafia_kill
    global day_count
    global dead_players

    phase = 'day'

    ##Deal with multiple roleblockers
    for player in player_dict.values():
        if player.role.name == 'Roleblocker' or player.role.name == 'Mafia Roleblocker':
            for target in player.targets:
                target.subpriority = -1

    #Sort resolution list by subpriority, then priority
    resolution_list = sorted(player_dict.values(), key=lambda x: x.subpriority, reverse=True)
    resolution_list = sorted(resolution_list, key=lambda x: x.role.priority, reverse=True)

    ##Resolve other powers
    nightkill_resolved = False
    for player in resolution_list:
        role = player.role

        ##Nightkill
        if role.priority < 5 and nightkill_resolved == False: #Nightkill resolves at priority 5
            if mafia_kill[0] == False:
                nightkill_resolved = True
            else:
                resolveNightKill()
                nightkill_resolved = True

        ##Roles
        if role.name == 'Roleblocker':
            if len(player.targets) > 0:
                if not 'blocked' in player.effects:
                    player.targets[0].effects.append('blocked')

        if role.name == 'Bulletproof' or role.name == 'Serial Killer' and day_count == 0:
            player.effects.append('bulletproof')

        if (role.name == 'Miller' or role.name == 'Godfather') and not 'misleading' in player.effects:
            player.effects.append('misleading')

        if role.name == 'Vigilante' or role.name == 'Serial Killer':
            if len(player.targets) > 0:
                if not 'blocked' in player.effects:
                    player.targets[0].effects.append('dying')

        if role.name == 'Doctor':
            if len(player.targets) > 0:
                if not 'blocked' in player.effects:
                    player.targets[0].effects.append('healed')

        if role.name == 'Cop':
            if len(player.targets) > 0:
                if not 'blocked' in player.effects:
                    target = player.targets[0]
                    result = inspect(target)
                    string = "You investigate " + target.name + " and discover that they are " + result + "."
                    if result == 'Innocent':
                        bonus_string = choice(["","","",
                        "\n(Phew! That's a relief, isn't it?)",
                        "\n(Well, at least in the context of this game. Wahaha!)"])
                    elif result == 'Mafia':
                        bonus_string = choice(["","","",
                        "\n(Ack! So they're one of the bad guys!)",
                        "\n(Oh boy! Now that's not a very nice thing to be, is it!)"])
                    else:
                        bonus_string = choice(["\n(Huh? Y-you're not telling me it's...!)",
                        "\n(Are you thinking what I'm thinking...?)",
                        "\n(What!? But... what could that mean!?)"])
                    string += bonus_string
                    bot.sendMessage(chat_id=player.chat_id, text=string)
                else:
                    bot.sendMessage(chat_id=player.chat_id, text="Your investigation turned up no result.")

        if role.name == 'Rolecop':
            if len(player.targets) > 0:
                if not 'blocked' in player.effects:
                    target = player.targets[0]
                    string = "You investigate " + target.name + " and discover that they are a " + target.role.name + "."
                    bot.sendMessage(chat_id=player.chat_id, text=string)
                else:
                    bot.sendMessage(chat_id=player.chat_id, text="Your investigation turned up no result.")

        if role.name == 'Oracle':
            if len(player.targets) == 2:
                if not 'blocked' in player.effects:
                    dream = player.targets[0]
                    dreamer = player.targets[1]
                    result = inspect(dream)
                    string = "Last night, you had a dream about " + dream.name + " and saw that they are " + result + "."
                    bot.sendMessage(chat_id=dreamer.chat_id, text=string)

        if role.name == 'Tracker':
            if len(player.targets) > 0:
                target = player.targets[0]
                if not 'blocked' in player.effects:
                    if len(target.targets) == 0 and (mafia_kill[0] == False or not mafia_kill[2] == target):
                        string = "You tracked " + target.name + ", but they didn't visit anyone last night."
                    else:
                        string = "You tracked " + target.name + " and saw that they targeted the following players last night:\n"
                        for person in target.targets:
                            string += person.name + "\n"
                        if mafia_kill[0] == True and mafia_kill[2] == target:
                            string += mafia_kill[1].name
                    bot.sendMessage(chat_id=player.chat_id, text=string)
                else:
                    bot.sendMessage(chat_id=player.chat_id, text="Your tracking turned up no result.")

        if role.name == 'Watcher':
            if len(player.targets) > 0:
                target = player.targets[0]
                if not 'blocked' in player.effects:
                    visitor_list = []
                    ##Add players who target
                    for visitor in target.targeted_by:
                        if not visitor == player and not visitor in visitor_list:
                            visitor_list.append(visitor)
                    ##Also add mafia kill
                    if mafia_kill[0] == True and mafia_kill[1] == target:
                        visitor_list.append(mafia_kill[2])
                    if len(visitor_list) == 0:
                        string = "You watched " + target.name + ", but no one visited them last night."
                    else:
                        shuffle(visitor_list)
                        string = "You watched " + target.name + " and saw that the following players targeted them last night:\n"
                        for visitor in visitor_list:
                            string += visitor.name + "\n"
                    bot.sendMessage(chat_id=player.chat_id, text=string)
                else:
                    bot.sendMessage(chat_id=player.chat_id, text="Your watching turned up no result.")

        ##If nightkill still not resolved, do it now
        if player == resolution_list[-1] and nightkill_resolved == False:
            if mafia_kill[0] == False:
                nightkill_resolved = True
            else:
                resolveNightKill()
                nightkill_resolved = True

    ##Resolve effects
    deaths = []
    for player in resolution_list:
        ##Check if inactive alien:
        if player.alignment == 'Alien' and 'dying' in player.effects and not 'activated' in player.effects:
            player.effects.remove('dying')
            player.effects.append('activated')
            bonus_string = choice(["Someone tried to kill you... but this wasn't even your final form! You're now an activated Alien!",
                        "Heh heh heh... Fools... Someone tried to kill you, but it only made you stronger - you are now activated.",
                        "Someone tried to kill you - but instead it unleashed your true power! You are now activated!"])
            bot.sendMessage(chat_id=player.chat_id, text=bonus_string)

        ##Check for protections
        if 'healed' in player.effects:
            if player.effects.count('healed') > 1:
                player.effects.append('dying')
            else:
                while 'dying' in player.effects:
                    player.effects.remove('dying')
        else:
            while ('bulletproof' in player.effects) and ('dying' in player.effects):
                player.effects.remove('bulletproof')
                player.effects.remove('dying')
                bonus_string = choice(["Oh my. Someone attacked you, and you lost your bulletproofing.",
                "Looks like you've made enemies. Someone's attack destroyed your bulletproofing!",
                "Someone tried to kill you! But you held up your sign saying 'Bulletproof' and scared them off. Next time you won't be so lucky."])
                bot.sendMessage(chat_id=player.chat_id, text=bonus_string)

        ##If still dying, then dead
        if 'dying' in player.effects:
            player.status = 'Dead'
            deaths.append(player)

    #Begin the day phase
    day_count += 1
    string = "It is now DAY " + str(day_count) + ".\n"
    if len(deaths) == 0:
        string += "No one has died.\n"
    else:
        for victim in deaths:
            string += victim.name + " has died. They were " + victim.flip() +".\n"
            dead_players.append(victim)
            sendDeathMessage(bot,victim)


    ##Bonus string
    bonus_string = ''
    if len(deaths) > 1:
        bonus_string = choice(["(Wow, that's a lot of death.)",
            "(Oh my. Plenty of murder to go around today, huh.)",
            "(So much carnage!)"])
        string += bonus_string

    bot.sendMessage(chat_id=group_id, text=string)

    ##Cleanup
    for player in resolution_list:
        player.targets.clear()
        player.targeted_by.clear()
        player.removeTempEffects()
        player.action_used = False
        mafia_kill = [False,None,None]

    if not checkWinConditions(bot,update):
        sendDayMessage(bot,update)
        bot.sendMessage(chat_id=group_id, text="You may now discuss and vote to lynch.")
        if day_count == 1:
            with open('PW-AA OST- 13 - Search - Opening 2001.mp3', 'rb') as song:
                bot.send_audio(chat_id=group_id, audio=song,duration = 108,title = "Day " + str(day_count))

def checkWinConditions(bot,update):
    global test_mode
    global player_dict
    global group_id

    if test_mode:
        return

    number_of_players = 0
    number_of_innocents = 0
    number_of_mafiosi = 0
    number_of_serial_killers = 0
    number_of_aliens = 0

    alien_win = False
    alien_winner_id = 0

    for player in player_dict.values():
        if player.status == 'Alive':
            number_of_players += 1
            if player.alignment == 'Alien':
                number_of_aliens += 1
                if 'winning' in player.effects:
                    alien_win = True
                    alien_winner_id = player.id
            elif player.alignment == 'Serial Killer':
                number_of_serial_killers += 1
            elif player.alignment == 'Innocent':
                number_of_innocents += 1
            elif player.alignment == 'Mafia':
               number_of_mafiosi += 1

    if ((number_of_mafiosi == number_of_players) #Mafia win
    or (number_of_mafiosi == 0 and number_of_serial_killers == 0) #Innocent win
    or (number_of_players == number_of_serial_killers and number_of_serial_killers == 1) #Serial Killer win
    or alien_win): #Alien win
        if alien_win:
            alien_name = player_dict[alien_winner_id].name
            string = "The alien has played you all! " + alien_name.upper() + " WINS!\n\n"
        elif number_of_players == 0:
            string = "Everyone has died! EMERIC THE MAFIA BOT WINS!\n\n"
        elif number_of_players == number_of_aliens:
            string = "The alien is a failure and everyone else has died! EMERIC THE MAFIA BOT WINS!\n\n"
        elif number_of_players == number_of_serial_killers and number_of_serial_killers == 1:
            ##Find the serial killer
            name = 'No one'
            for player in player_dict.values():
                if player.status == 'Alive' and player.alignment == 'Serial Killer':
                    name = player.name
                    break
            string = "The Serial Killer has murdered everyone!\n" + name.upper() + " WINS!\n\n"
        elif number_of_mafiosi == 0 and number_of_serial_killers == 0:
            string = "All threats to the Innocents have been wiped out! TOWN WINS!\n\n"
        elif number_of_mafiosi == number_of_players:
            string = "The town has been wiped out! MAFIA WINS!\n\n"

        ###Finish

        string += "The setup was:\n"
        for player in player_dict.values():
            string += player.name + ": " + player.role.name + " (" + player.alignment + ")\n"
        string += "\nThanks for playing!"
        bot.sendMessage(chat_id=group_id, text=string)

        ##Send personal messages too
        for player in player_dict.values():
            string = "The game has now ended. Thanks for playing, " + player.name + "!"
            bot.sendMessage(chat_id=player.chat_id, text=string)
        clearGame()
        return(True)
    else:
        return(False)


###DEFINE COMMAND HANDLERS

def help_command(bot,update): #Help
    helptext = "Here are the commands you can use with the mafia bot.\n" \
    "\nGAME SETUP COMMANDS:\n" \
    "/start: Gives a welcome message and shows the most recent updates.\n" \
    "/create: Create a new mafia game.\n" \
    "/join: Join the game during startup.\n" \
    "/playerlist: See a list of all players in the game.\n" \
    "/add: Add roles to the game's setup. Type /add with no argument to see a list of available roles.\n" \
    "/rolelist: Show all roles in the current setup.\n" \
    "/randomize [x] [y] [z]: Create a random setup with [x] players, [y] of whom are mafia, where one in [z] roles are power roles.\n" \
    "/resetroles: Reset the game's setup.\n" \
    "/ready: Begin playing the mafia game (use this once everybody has joined). Only the host can use this command. \n" \
    "\nPLAYER COMMANDS:\n" \
    "/role: Receive information about your role.\n" \
    "/lynch or /vote [name]: Vote to lynch a player (during the day). Type /lynch with no argument to bring up a keyboard.\n" \
    "/abstain: Vote to lynch no one.\n" \
    "/retract: Retract your vote.\n" \
    "/votelist: See how many lynch votes each player has.\n" \
    "/action or /target [name]: Use your role's power, if applicable. Type /action with no argument to bring up a keyboard.\n" \
    "/kill [name]: Nightkill a player. Only the mafia can use this, and only one of them each night.\n" \
    "/undo: Undo your action or nightkill.\n" \
    "/pass: Pass on using your night action/nightkill.\n" \
    "\nHOST-ONLY COMMANDS:\n" \
    "/advance: Advance day phase to night phase, or night phase to day phase. " \
    "(Note that the night phase also advances automatically when all actions are sent in.)\n" \
    "/remind: Sends reminders to all players who haven't yet submitted their night actions.\n" \
    "/abort: Abort the current game."

    bot.sendMessage(chat_id=update.message.chat_id, text=helptext,reply_to_message_id=update.message.message_id)


help_handler = CommandHandler('help', help_command)
dispatcher.add_handler(help_handler)

###

def start(bot,update): #Start message
    bot.sendMessage(chat_id=update.message.chat_id, text="Welcome! I'm Emeric, the TCoD Mafia Bot. "
    "To create a new game, type /create in the group you want to play in. "
    "Use /help to see what commands are available. Have fun, and don't forget to tell MD about any bugs you find!\n\n"
    "RECENT UPDATES:\n"
    "[*] Please try to avoid sending messages to Emeric while he is sleeping, or he'll panic when he wakes up.\n"
    "[*] I've rewritten the way night actions work. THE MAFIA CAN NO LONGER SEND IN A NIGHTKILL AND A NIGHT ACTION AT THE SAME TIME. "
    "As a result, there are only three commands: /action, /kill, and /undo. "
    "The old /passkill and /undokill commands have been removed. "
    "This is a significant change, so be on the lookout for strange behavior.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

###

def create(bot, update): #Creates a new game
    global host_id
    global phase
    global group_id
    global test_mode
    if not phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="A game already exists.",reply_to_message_id=update.message.message_id)
    elif update.message.chat.type == 'private' or update.message.chat.type == 'channel':
        bot.sendMessage(chat_id=update.message.chat_id, text="Type /create in the group where you want to play. Be sure to invite me to it first!",
        reply_to_message_id=update.message.message_id)
    else:
        host_id = update.message.from_user.id
        host_name = update.message.from_user.first_name
        group_id = update.message.chat_id
        print('Group ID: ' + str(group_id)) #Testing
        phase = 'startup'
        bot.sendMessage(chat_id=group_id, text="A new game has been created by " + host_name + "!\n"
        "Message /join to the bot to join.\n"
        "Type /playerlist to see who has joined so far.\n\n" +
        host_name + ", choose roles for the setup using /add.\nUse /rolelist to show the current setup and /resetroles to clear it.\n"
        "Use /randomize to generate a random setup.\n\n" +
        host_name + " must type /ready when everyone has joined to begin the game.")
        if test_mode:
            bot.sendMessage(chat_id=group_id, text="NOTE: The bot has been set to TEST MODE, meaning games will never actually end, "
            "even if win conditions are met. If you see this, you're not supposed to. Use /testmode to turn it off.")


create_handler = CommandHandler('create', create)
dispatcher.add_handler(create_handler)

###

def testmode(bot,update): #Turn on test mode
    global test_mode
    global group_id
    test_mode = not test_mode
    if phase == 'off':
        chat_id = update.message.chat_id
    else:
        chat_id = group_id
    bot.sendMessage(chat_id=chat_id, text="TEST MODE has now been set to " + str(test_mode) + ".")

testmode_handler = CommandHandler('testmode', testmode)
dispatcher.add_handler(testmode_handler)

###

def join(bot, update): #Lets a player join during startup
    global player_dict
    global group_id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="There is no game to join.",reply_to_message_id=update.message.message_id)
    elif update.message.from_user.id in player_dict:
        bot.sendMessage(chat_id=update.message.chat_id, text="You have already joined.",reply_to_message_id=update.message.message_id)
    elif not phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, the game has already started. Join the next one!",
        reply_to_message_id=update.message.message_id)
    elif not update.message.chat.type == 'private':
        bot.sendMessage(chat_id=update.message.chat_id, text="To /join, please message me privately.",
        reply_to_message_id=update.message.message_id)
    else:
        ##Add the player
        new_user = update.message.from_user
        new_player = Player(name=new_user.first_name,id=new_user.id,chat_id=update.message.chat_id)
        player_dict[new_user.id] = new_player
        ##Make announcement
        name = new_user.first_name

        print(name + ": " + str(new_user.id))

        string = name + " has joined the game!\n"
        bonus_string = choice(["Watch out for that one.",
                        "Take good care of " + name + "!",
                        "You do want this egg, don't you?",
                        "That's going to spice things up, surely!",
                        "Oh boy!",
                        "Make them feel welcome.",
                        "I don't know who they are, but they sound attractive.",
                        "Amazing! They're a Fully Trained Pokémon!"])
        if new_user.id in friend_dict:
            if friend_dict[new_user.id] == 'MD':
                bonus_string = choice(["I am duty-bound to describe him as 'handsome'.",
                        "As if we haven't seen enough of each other already. Hmph!",
                        "Oh, it's *you*. Hrrm.",
                        "\"Emeric Eggert Bot, you were named after two of the bravest men I ever knew...\"",
                        "You... you made me what I am..."])
            elif friend_dict[new_user.id] == 'Flora':
                bonus_string = choice(["Time for a friendly game of subs vs. doms!",
                        "What!? No, *I'm* the real Emeric, I swear! The other one's the robot!",
                        "You haven't seen the Flora Bot around, by any chance?",
                        "Welp, I guess we know who the mafia is already.",
                        "Watch out for those stompy boots!"])
            elif friend_dict[new_user.id] == 'hope':
                bonus_string = choice(['Ah, excellent. That means I get to put a Vigilante in the game.',
                        "You're Vanilla Townie. AGAIN. Ha!",
                        "What's the matter? Eat your burgers, hope.",
                        "WEBECCA! ~dramatic music plays~",
                        "That Mafia",
                        "No one with naturally wavy hair can be that bad.",
                        "I'm sorry, but \"Vocaloid\" is not an alignment in this game."])
            elif friend_dict[new_user.id] == 'ZM':
                bonus_string = choice(['meme too danks',
                        "Praise the Sun!",
                        "Me too thanks",
                        "Greetings.",
                        "The feast of souls begins now!",
                        "( ͡° ͜ʖ ͡°)",
                        "Heh, Greetings."])
            elif friend_dict[new_user.id] == 'VM':
                bonus_string = choice(['Time for a friendly game of Snakes and Ladders!',
                        "I have had it with these goddamn snakes on this goddamn plane!",
                        "This game will now include a third faction, the Furries.",
                        "Ha! Now it's MY turn to host the games!",
                        "Life has many mafiosi, long boy!"])
            elif friend_dict[new_user.id] == 'Butterfree':
                bonus_string = choice(["If you run into the Leppa Bot, tell them I said hi.",
                        "Time for a friendly game of Íslendinga-Mafia!",
                        "Eftirlýstur síðan 2015 fyrir morð.",
                        "(You know, my parents would have named me Eggert if it wasn't for the fact that they didn't want to name me that. True story.)",
                        "Computer scientists always make me feel woefully inadequate."])
            elif friend_dict[new_user.id] == 'Eifie':
                bonus_string = choice(["Some people bug me, but here's a person who DE-bugs me. Hehe, get it!?",
                        "Nya ha! I sure do love mafia and ripping thumbs off!",
                        "(Please don't look at my code, please don't look at my code...)",
                        "The Messenger of Truth and Ideals, Eifie Girl, enters!",
                        "Eep!"])
            elif friend_dict[new_user.id] == 'Jack':
                bonus_string = choice(["Don't give him all your prize like fools!",
                        "Bendytoots...!?!",
                        '"I choose violence."',
                        "Ass right there, freezehole!",
                        "You know nothing, Jack Snow."])
            elif friend_dict[new_user.id] == 'Murkrow':
                bonus_string = choice(["He's a mathioso. Hehe, get it!?",
                        "By which I mean, joined the mathia game.",
                        "I feel like \"True Neutral\" could go either way here, really.",
                        "He's Innocent up to isomorphism."])
            elif friend_dict[new_user.id] == 'Alex':
                bonus_string = choice(["Or is it Karousever now? I get confused.",
                        "The artist formerly known as Jake.",
                        "He has learned well... Don't underestimate him just because he's new!",
                        "(No, I am not going to make the obvious joke. Too easy.)"])
            elif friend_dict[new_user.id] == 'Walker':
                bonus_string = choice(["Go on, ask about complex numbers!",
                        "xoxoxor~",
                        "Boy am I glad that Walker is in there, and that they're the vigilante and that I'm out here, and -"])
            elif friend_dict[new_user.id] == 'Faorzia':
                bonus_string = choice(["Even a sheltered bean can be deadly...",
                        "!!! lowkey cover enabled!"])
            elif friend_dict[new_user.id] == 'SS':
                bonus_string = choice(["Fallen Innocents... You will be avenged!!",
                        "Mafia! The time of your reckoning is at hand!",
                        "The light of justice shining bright!",
                        "Sword of Justice!!"])
            elif friend_dict[new_user.id] == 'ILS':
                bonus_string = choice(["This astropolitician will defeat you using space governance!",
                        "I suppose political science really primes you for this sort of game.",
                        "Obviously aligned with the Squirtles faction.",
                        "Playing mafia is basically the same as studying UK politics, right?"])
            elif friend_dict[new_user.id] == 'ILS':
                bonus_string = choice(["This astropolitician will defeat you using space governance!",
                        "I suppose political science really primes you for this sort of game.",
                        "Obviously aligned with the Squirtles faction.",
                        "Playing mafia is basically the same as studying UK politics, right?"])
            elif friend_dict[new_user.id] == 'Stryke':
                bonus_string = choice(["Wow! I can't believe the entire mafia crew has come to Telecod!",
                        "Let's we go!",
                        "Stryke one! Stryke two! Aaaand you're out."])

        string += bonus_string
        bot.sendMessage(chat_id=group_id, text=string)

        ##Personal confirmation
        string = "You have joined the game!\n"
        bonus_string = choice(["Let's show them who's boss!",
                        name + ", I believe in you!",
                        "Your time to shine, " + name + "!",
                        "Nice to meet you, " + name + ".",
                        "I hope you know what you're getting yourself into...!",
                        "It's important to stay hydrated. Drink some water before playing mafia!",
                        "Ah, I see you've played knifey-spooney before. Then this game should be no match for you!",
                        "Wahahaha!",
                        "Now let's see if you'll be the hunter or the hunted...",
                        "Hehehe!",
                        "Your friends believe in you, " + name + "! You can do it!",
                        "Glad to have you on board the murder train, " + name + ".",
                        "I hope you'll enjoy it. I've cooked up a good one this time!"])
        string += bonus_string
        bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)



join_handler = CommandHandler('join', join)
dispatcher.add_handler(join_handler)

###

def playerlist(bot,update): #Returns a list of players who have joined
    global player_dict
    if len(player_dict) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="No players yet.",reply_to_message_id=update.message.message_id)
    else:
        string = 'The players are:\n'
        for player_id in player_dict:
            player = player_dict[player_id]
            if player.status == 'Alive':
                string += player.name + ' (' + player.status + ')\n'
            elif player.status == 'Dead':
                string += player.name + ' (' + player.status + ", " + player.alignment + ')\n'
        string = string[:-1]
        bot.sendMessage(chat_id=update.message.chat_id, text=string)

playerlist_handler = CommandHandler('playerlist',playerlist)
dispatcher.add_handler(playerlist_handler)

###

def addrole(bot,update,args): #Add role to setup
    global phase
    global host_id
    global roles
    global role_database
    player_id = update.message.from_user.id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="Create a game first.",reply_to_message_id=update.message.message_id)
    elif not player_id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can add roles.",reply_to_message_id=update.message.message_id)
    elif not phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="You can only add roles during startup.",reply_to_message_id=update.message.message_id)
    elif len(args) == 0:
        string = 'Type "/add [role]" to add it to the current setup.\nThe available roles right now are:'
        for role in sorted(role_database):
            string += "\n" + role
        bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)
    else:
        #Not case sensitive
        for i in range(len(args)):
            args[i] = args[i][:1].upper() + args[i][1:].lower()
        role_name = ' '.join(args)
        ##Check if role exists
        if not role_name in role_database:
            bot.sendMessage(chat_id=update.message.chat_id, text="There is no role with that exact name. Type /add, without an argument, to see a list of all roles.",
            reply_to_message_id=update.message.message_id)
        else:
            roles.append(role_database[role_name])
            string = "You have added " + role_name + " to the setup!\n\nThe current setup includes:"
            for role in roles:
                string += "\n" + role.name + " (" + role.alignment + ")"
            bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)



addrole_handler = CommandHandler('add',addrole,pass_args=True)
dispatcher.add_handler(addrole_handler)

###

def rolelist(bot,update): #View the role setup
    global phase
    global host_id
    global roles
    player_id = update.message.from_user.id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="Create a game first.",reply_to_message_id=update.message.message_id)
    elif not player_id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can request the role setup.",reply_to_message_id=update.message.message_id)
    elif len(roles) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="No roles yet.",reply_to_message_id=update.message.message_id)
    else:
        string = "The current setup includes:\n"
        for role in roles:
            string += role.name + " (" + role.alignment + ")\n"
        if not update.message.chat.type == 'private':
            string += "\n... You did mean to do that in public, didn't you?"
        bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)

rolelist_handler = CommandHandler('rolelist',rolelist)
dispatcher.add_handler(rolelist_handler)

###

def resetroles(bot,update): #Reset the role setup
    global phase
    global host_id
    global roles
    player_id = update.message.from_user.id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="Create a game first.",reply_to_message_id=update.message.message_id)
    elif not player_id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can reset the role setup.",reply_to_message_id=update.message.message_id)
    elif not phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="You can only reset the roles during startup.",reply_to_message_id=update.message.message_id)
    else:
        roles = []
        bot.sendMessage(chat_id=update.message.chat_id, text="Okay! The roles have now been reset.",reply_to_message_id=update.message.message_id)

resetroles_handler = CommandHandler('resetroles',resetroles)
dispatcher.add_handler(resetroles_handler)

###

def randomize(bot,update,args):
    global phase
    global host_id
    global roles
    global role_database
    player_id = update.message.from_user.id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="Create a game first.",reply_to_message_id=update.message.message_id)
    elif not player_id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can add roles.",reply_to_message_id=update.message.message_id)
    elif not phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="You can only add roles during startup.",reply_to_message_id=update.message.message_id)
    elif len(args) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="Type /randomize [number of players] [number of mafiosi] [power role ratio] to randomize. "
        "[number of mafiosi] must be less than [number of players]. "
        "[power role ratio] works like this: if the ratio is set to X, then 1 in X players will have a power role, rounded up, for each faction.\n\n"
        "Example: /randomize 8 2 3 will add 8 roles, 2 of whom are mafia. One in 3 innocents have a power (so two innocents) and one in 3 mafiosi have "
        "a power (so one mafioso).",
        reply_to_message_id=update.message.message_id)
    elif not len(args) == 3:
        bot.sendMessage(chat_id=update.message.chat_id, text="You need to specify three integers. Come on, pal. Work with me here.",
            reply_to_message_id=update.message.message_id)
    else:
        try:
            number_of_players = int(args[0])
            number_of_mafiosi = int(args[1])
            power_role_ratio = int(args[2])
            number_of_innocents = number_of_players - number_of_mafiosi
            if (number_of_players > number_of_mafiosi) and (number_of_mafiosi > 0) and (power_role_ratio >= 0):
                roles = []
                innocent_power_roles = []
                mafia_power_roles = []
                for role in role_database.values():
                    if not role.name == 'Vanilla':
                        if role.alignment == 'Innocent':
                            innocent_power_roles.append(role)
                        if role.alignment == 'Mafia':
                            mafia_power_roles.append(role)
                if not power_role_ratio == 0: #Can't divide by zero
                    while len(roles) < number_of_mafiosi/power_role_ratio: #Number of mafia power roles
                        roles.append(choice(mafia_power_roles))
                while len(roles) < number_of_mafiosi: #Remaining mafia Vanilla
                    roles.append(role_database['Mafioso'])
                if not power_role_ratio == 0: #Can't divide by zero
                    while len(roles) < (number_of_innocents/power_role_ratio + number_of_mafiosi): #Number of town power roles
                        roles.append(choice(innocent_power_roles))
                while len(roles) < number_of_players: #Remaining town Vanilla
                    roles.append(role_database['Vanilla'])

                bot.sendMessage(chat_id=update.message.chat_id, text="A random setup has been generated! "
                "You can view it with /rolelist, or you can keep it secret even from yourself. Wahahaha!",reply_to_message_id=update.message.message_id)


            else: #If numbers are wonky
                bot.sendMessage(chat_id=update.message.chat_id, text="That doesn't sound like a balanced setup to me...",reply_to_message_id=update.message.message_id)

        except ValueError:
            bot.sendMessage(chat_id=update.message.chat_id, text="You need to specify three integers. Come on, pal. Work with me here.",
            reply_to_message_id=update.message.message_id)



randomize_handler = CommandHandler('randomize',randomize,pass_args = True)
dispatcher.add_handler(randomize_handler)

###

def ready(bot,update): #Starts the game
    global phase
    global player_dict
    global mafia_ids
    global host_id
    global group_id
    global roles
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="No game exists yet. Make one with /create.",reply_to_message_id=update.message.message_id)
    elif not phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="Game already started.",reply_to_message_id=update.message.message_id)
    elif not update.message.from_user.id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can start the game.",reply_to_message_id=update.message.message_id)
    elif len(player_dict) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="The game can't start with no players!",reply_to_message_id=update.message.message_id)
    elif len(roles) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="The setup needs some roles first. Use /add to add roles to the game.",reply_to_message_id=update.message.message_id)
    else:
        ###ASSIGN ROLES
        shuffle(roles)
        i = 0
        mafia_players = []
        for player in player_dict.values():
            role = roles[i % len(roles)]
            player.role = role
            player.alignment = player.role.alignment
            if player.alignment == 'Mafia':
                mafia_players.append(player)
            bot.sendMessage(chat_id=player.chat_id,text=role.info) #Send role PM
            i += 1

        ##Send mafia PM
        string = "The mafia players are:"
        for mafioso in mafia_players:
            string += "\n" + mafioso.name
        for mafioso in mafia_players:
            bot.sendMessage(chat_id=mafioso.chat_id,text=string)

        phase = 'night'
        string = "The game begins! It is now NIGHT " + str(day_count) + ".\nIf you have a night action, message the bot privately and input it now.\n" \
        "Please do not speak in the group chat during the night phase.\nWhen all night actions have been received, or the host uses /advance, the day phase will begin."

        bot.sendMessage(chat_id=group_id, text=string)

        sendNightMessage(bot,update)
        if not checkWinConditions(bot,update):
            checkIfNightFinished(bot,update)

ready_handler = CommandHandler('ready',ready)
dispatcher.add_handler(ready_handler)

###

def role(bot,update): ##Provide info about your role
    global player_dict
    player_id = update.message.from_user.id
    if player_id in player_dict:
        chat = player_dict[player_id].chat_id
        if phase == 'off' or phase == 'startup':
            bot.sendMessage(chat_id=chat,text="The game has not yet started.",reply_to_message_id=update.message.message_id)
        else:
            player = player_dict[player_id]
            role = player.role
            bot.sendMessage(chat_id=chat,text=role.info)
            if player.alignment == 'Mafia':
                string = "The mafia players are:\n"
                for mafia_id in mafia_ids:
                    string += player_dict[mafia_id].name + "\n"
                bot.sendMessage(chat_id=player.chat_id,text=string)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="You are not a player!",reply_to_message_id=update.message.message_id)


role_handler = CommandHandler('role',role)
dispatcher.add_handler(role_handler)

###

def action(bot,update,args): ##Use role power
    global phase
    global player_dict
    player_id = update.message.from_user.id
    if playerIsValid(bot,update,player_id,allow_day = True,allow_night=True,only_private = True):
        player = player_dict[player_id]
        role = player.role
        if phase == 'night' and role.has_night_action == False:
            bot.sendMessage(chat_id=update.message.chat_id, text="You don't have a night action.",reply_to_message_id=update.message.message_id)
        elif phase == 'day' and role.has_day_action == False:
            bot.sendMessage(chat_id=update.message.chat_id, text="You don't have a day action.",reply_to_message_id=update.message.message_id)
        elif player.action_used:
            bot.sendMessage(chat_id=update.message.chat_id, text="You've already used your action.\nTo change your mind, type /undo before it resolves.",
            reply_to_message_id=update.message.message_id)
        elif player.sentMafiaKill():
            bot.sendMessage(chat_id=update.message.chat_id, text="You've already sent in the mafia nightkill, and "
            "you can't use your night action at the same time.\n To change your mind, type /undo.",
            reply_to_message_id=update.message.message_id)
        elif role.number_of_targets > 0 and len(args) == 0: #If no target was given but one is needed
            offerTargets(bot,update,'/target')
        elif role.number_of_targets == 0:
            player.action_used = True
            if phase == 'day':
                player.role.dayPower(bot,update,player)
        else:
            [valid_target,target] = findTarget(bot,update,args) #If there is an argument, check if it is a valid player name
            if not valid_target:
                bot.sendMessage(chat_id=update.message.chat_id, text="There is no living player with that name.",reply_to_message_id=update.message.message_id)
            elif target == player and not player.role.can_self_target:
                bot.sendMessage(chat_id=update.message.chat_id, text="This role can't target itself.",reply_to_message_id=update.message.message_id)
            else:
                setTarget(player,target)
                string = "You have chosen to target " + target.name + "."
                remaining_targets = role.number_of_targets - len(player.targets)
                if remaining_targets == 0:
                    player.action_used = True
                else:
                    string += "\nYou must choose " + str(remaining_targets) + " more target(s)."
                bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)
    checkIfNightFinished(bot,update)

action_handler = CommandHandler('action',action,pass_args=True)
target_handler = CommandHandler('target',action,pass_args=True)
dispatcher.add_handler(action_handler)
dispatcher.add_handler(target_handler)

###

def kill(bot,update,args): ##Use mafia nightkill
    global phase
    global player_dict
    global mafia_kill
    player_id = update.message.from_user.id
    if playerIsValid(bot,update,player_id,allow_night = True,only_private = True):
        player = player_dict[player_id]
        role = player.role
        if not role.sends_mafia_kill:
            bot.sendMessage(chat_id=update.message.chat_id, text="Your role doesn't send in the mafia nightkill.",
            reply_to_message_id=update.message.message_id)
        elif player.action_used:
            bot.sendMessage(chat_id=update.message.chat_id, text="You've already used your night action, "
            "and you can't send in the mafia nightkill at the same time.\nTo change your mind, type /undo.",
            reply_to_message_id=update.message.message_id)
        elif mafia_kill[0] == True: #If mafia tries to send in a second kill
            string = "The mafia is already targeting " + mafia_kill[1].name + " tonight, courtesy of " + mafia_kill[2].name + "."
            bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)
        elif len(args) == 0: #If no target was given but one is needed
            offerTargets(bot,update,'/kill')
        else:
            [valid_target,target] = findTarget(bot,update,args) #If there is an argument, check if it is a valid player name
            if not valid_target:
                bot.sendMessage(chat_id=update.message.chat_id, text="There is no living player with that name.",reply_to_message_id=update.message.message_id)
            else:
                string = "You have chosen to kill " + target.name + ".\nTo change your mind, type /undo before the night ends."
                mafia_kill = [True,target,player]
                bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)
    checkIfNightFinished(bot,update)

kill_handler = CommandHandler('kill',kill,pass_args=True)
dispatcher.add_handler(kill_handler)

##

def undo(bot,update):
    global phase
    global player_dict
    global mafia_kill
    player_id = update.message.from_user.id
    if playerIsValid(bot,update,player_id,allow_night = True,allow_day = True,only_private = True):
        player = player_dict[player_id]
        if player.sentMafiaKill():
            mafia_kill = [False, None, None]
            bot.sendMessage(chat_id=update.message.chat_id, text="The nightkill has been undone.",reply_to_message_id=update.message.message_id)
        elif player.action_used == False:
            bot.sendMessage(chat_id=update.message.chat_id, text="No action to undo.",reply_to_message_id=update.message.message_id)
        elif not phase == 'night':
            bot.sendMessage(chat_id=update.message.chat_id, text="Too late now!",reply_to_message_id=update.message.message_id)
        else:
            #Remove the player from its targets' "targeted_by" list
            for target in player.targets:
                if player in target.targeted_by:
                    target.targeted_by.remove(player)
            #Empty list of targets
            player.targets.clear()

            player.action_used = False
            bot.sendMessage(chat_id=update.message.chat_id, text="Your action has been undone.",reply_to_message_id=update.message.message_id)

undo_handler = CommandHandler('undo',undo)
dispatcher.add_handler(undo_handler)

###

def skip(bot,update):
    global phase
    global player_dict
    global mafia_kill
    player_id = update.message.from_user.id
    if playerIsValid(bot,update,player_id,allow_night = True,only_private = True):
        player = player_dict[player_id]
        role = player.role
        if phase == 'day' or (not role.has_night_action and not role.sends_mafia_kill):
            bot.sendMessage(chat_id=update.message.chat_id, text="You have no action to pass on.",reply_to_message_id=update.message.message_id)
        elif player.action_used or player.sentMafiaKill():
            bot.sendMessage(chat_id=update.message.chat_id, text="You've already made your choice.\nTo change your mind, type /undo before the night ends.",
            reply_to_message_id=update.message.message_id)
        else:
            player.action_used = True
            bot.sendMessage(chat_id=update.message.chat_id, text="You've passed on using your action. To change your mind, type /undo before the night ends.",
            reply_to_message_id=update.message.message_id)
    checkIfNightFinished(bot,update)

pass_handler = CommandHandler('pass',skip)
dispatcher.add_handler(pass_handler)

###

def lynch(bot,update,args):
    global phase
    global player_dict
    global group_id
    global tiebreaker

    player_id = update.message.from_user.id
    #Check if the user is the tiebreaker
    if player_id == tiebreaker.id:
        is_tiebreaker = True
    else:
        is_tiebreaker = False
    ##Bonus if trying to lynch Emeric
    if len(args) == 2 and str(" ".join(args).upper()) == 'EMERIC BOT':
        name = update.message.from_user.first_name
        bonus_string = choice(["Objection overruled. Try to think before you make accusations, " + name + "!",
                                "... I'm sorry, but I can see nothing faulty. Unfortunately, I will have to penalize you, " + name + ".",
                                "You don't sound very convinced, " + name + ". Objection overruled.",
                                "Emeric has voted to lynch " + name + ", a spectacular asshole!",
                                "Emeric has voted to lynch " + name + ", a supreme jerk!",
                                "Emeric has voted to lynch " + name + ", some random loser!",
                                "Emeric has voted to lynch " + name + ", who totally has it coming!",
                                "(Just smile and pretend you didn't hear that...)",
                                "(It's okay, just keep your retail face on...)",
                                "(When will this customer go away...)",
                                "(Guh. So entitled...)",
                                "The town has voted to lynch " + name + "! They are not dead, but they will be if they keep this up! HINT HINT.",
                                "The town has voted to lynch " + name + "! " + name + " has died! Their alignment was FUCKBOY.",
                                "The town has voted to lynch " + name + "! " + name + " has died! Their alignment was UNGRATEFUL BASTARD.",
                                "The town has voted to lynch " + name + "! " + name + " has died! Their alignment was GOOD FUCKING RIDDANCE.",
                                "The town has voted to lynch " + name + "! " + name + " has died! Their alignment was ASSHAT.",
                                "Oh, so now *I'm* the bad guy.",
                                "You don't offer friendship. You don't even think to call me \"Godfather\". "
                                "You come into my house on the day my mafia is to be married and you ask me to lynch myself.",
                                name + ". You are truly the most unpredictable defense attorney I've ever known."])
        if player_id == 0: #Flora's player ID redacted
            bonus_string = choice(["But why, Flora Bot!? Why!?",
                            "Maybe you should talk to your boyfriend instead of taking it out on me.",
                            "Just to be clear, you're talking about your boyfriend and not me, right?"])

        bot.sendMessage(chat_id=update.message.chat_id, text=bonus_string,reply_to_message_id=update.message.message_id)
    ##Bonus if trying to lynch Eifie
    elif len(args) == 1 and str(args[0]).upper() == 'EIFIE' and not 252627090 in player_dict:
        name = update.message.from_user.first_name
        bonus_string = choice(["Yes, I can see why you would want to do that. Alas...",
                                name + " has voted to lynch Eifie! It's not an actual vote, but I'll highlight it anyway, for encouragement.",
                                name + " has voted to lynch Eifie! I don't know what she did this time but I trust your judgment!",
                                name + " has voted to lynch Eifie! A somewhat unorthodox decision I admit, but I'll allow it.",
                                name + " has voted to lynch Eifie! Not how it works, but I can appreciate the intent.",
                                name + " has voted to lynch Eifie! I like your style, kid.",
                                name + " has voted to lynch Eifie! Heh. That's funny. Alright, just this once.",
                                name + " has voted to lynch Eifie! Hehe, this one gets it!",
                                name + " has voted to lynch Eifie! Me too, buddy. Me too.",
                                name + " has voted to lynch Eifie! NICE. I mean, I don't want to give the rest of you any ideas, but...",
                                name + " has voted to lynch Eifie!\nEmeric has voted to lynch Eifie too!",
                                name + " has voted to lynch Eifie! Good thinking, but this isn't one of those lateral thinking puzzles.",
                                name + " has voted to lynch Eifie! Won't actually do anything, but it'd make for a nice plot twist, hey.",
                                name + " has voted to lynch Eifie! It's too bad I haven't yet been programmed to do Bastard Mafia.",
                                name + " has voted to lynch Eifie! I mean, we've all been there, right?",
                                "Sigh. If only."])
        bot.sendMessage(chat_id=update.message.chat_id, text=bonus_string,reply_to_message_id=update.message.message_id)
    ##Bonus if trying to lynch MF
    elif (len(args) == 1 and str(args[0]).upper() == 'MF') or (len(args) == 2 and str(" ".join(args).upper()) == 'METALLICA FANBOY'):
        name = update.message.from_user.first_name
        bonus_string = choice(["Hey now! Let's not be mean to him just because he's become a meme.",
                                name + " has voted to lynch Mesheegorath Fromgomb!",
                                name + " has voted to lynch Molasses Freshsnoot!",
                                name + " has voted to lynch Metecklekeck Fyuckhyuck!",
                                name + " has voted to lynch Meshiggles Fetimbers!",
                                name + " has voted to lynch Mehicular Fanslaughter!",
                                name + " has voted to lynch Meminuteman Fockleclock!",
                                name + " has voted to lynch Medullica Famham!",
                                name + " has voted to lynch Meringue-man Fruitloops!",
                                name + " has voted to lynch Maractusite Flaktrack!",
                                name + " has voted to lynch Mangogular Freefbeef!",
                                name + " has voted to lynch Meticular Flickflock!",
                                name + " has voted to lynch Methuselah Flamberge!",
                                name + " has voted to lynch Metropolis Floopflap!",
                                name + " has voted to lynch Mettattytron Flamboyant!",
                                name + " has voted to lynch Metickles Fedora!"])
        bot.sendMessage(chat_id=update.message.chat_id, text=bonus_string,reply_to_message_id=update.message.message_id)
    #Moving on...
    elif playerIsValid(bot,update,player_id,allow_day = True,allow_dead = is_tiebreaker):
        player = player_dict[player_id]
        if not (tiebreaker.id == 0) and not (player == tiebreaker):
            string = "Tiebreaking in progress. Only " + tiebreaker.name + " can vote now."
            bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)

        elif len(player.vote_targets) > 0 or player.is_abstaining:
            bot.sendMessage(chat_id=update.message.chat_id, text="You have already voted. You may /retract your vote if you wish.",
            reply_to_message_id=update.message.message_id)

        elif len(args) == 0: #No argument provided
            offerTargets(bot,update,'/lynch')
        else:
            [valid_target,target] = findTarget(bot,update,args)
            ##Find max vote for tiebreaking
            vote_order = sorted(player_dict.values(), key=lambda x: x.votes, reverse=True)
            max_vote = vote_order[0].votes
            ##
            if not valid_target:
                bot.sendMessage(chat_id=update.message.chat_id, text="There is no living player with that name.",
                reply_to_message_id=update.message.message_id)
            elif target.votes < max_vote and not tiebreaker.id == 0:
                bot.sendMessage(chat_id=update.message.chat_id, text="Vote for one of the top candidates, please!",
                reply_to_message_id=update.message.message_id)
            else:
                player.vote_targets.append(target)
                target.votes += 1
                string = player.name + " has voted to lynch " + target.name + "!"
                bot.sendMessage(chat_id=group_id, text=string)
                #Clear the tiebreaker
                if player == tiebreaker:
                    advance(bot,update,bypass_host=True)



lynch_handler = CommandHandler('lynch',lynch,pass_args=True)
vote_handler = CommandHandler('vote',lynch,pass_args=True)
dispatcher.add_handler(lynch_handler)
dispatcher.add_handler(vote_handler)

###

def abstain(bot,update):
    global phase
    global player_dict
    global abstain_votes
    global group_id
    global tiebreaker

    player_id = update.message.from_user.id
    #Check if the user is the tiebreaker
    if player_id == tiebreaker.id:
        is_tiebreaker = True
    else:
        is_tiebreaker = False
    #Moving on...
    if playerIsValid(bot,update,player_id,allow_day = True,allow_dead = is_tiebreaker):
        player = player_dict[player_id]
        if not (tiebreaker.id == 0):
            if not (player == tiebreaker):
                string = "Tiebreaking in progress. Only " + tiebreaker.name + " can vote now."
            else:
                string = choice(["You had one job, " + tiebreaker.name + "...",
                "Seriously? I brought you back from the dead for this?",
                "Ha ha, real funny. Now cast your vote!"])

            bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)
        elif len(player.vote_targets) > 0 or player.is_abstaining:
            bot.sendMessage(chat_id=update.message.chat_id, text="You have already voted. You may /retract your vote if you wish.",
            reply_to_message_id=update.message.message_id)
        else:
            player.is_abstaining = True
            abstain_votes += 1
            string = player.name + " has voted to abstain!"
            bot.sendMessage(chat_id=group_id, text=string)

abstain_handler = CommandHandler('abstain',abstain)
dispatcher.add_handler(abstain_handler)

###

def retract(bot,update):
    global phase
    global player_dict
    global abstain_votes
    global group_id
    global tiebreaker

    player_id = update.message.from_user.id
    #Check if the user is the tiebreaker
    if player_id == tiebreaker.id:
        is_tiebreaker = True
    else:
        is_tiebreaker = False
    #Moving on...
    if playerIsValid(bot,update,player_id,allow_day = True,allow_dead = is_tiebreaker):
        player = player_dict[player_id]
        if not tiebreaker.id == 0:
            string_1 = "Please don't retract your vote during the tiebreak. It makes my head hurt."
            string_2 = "Let's just have the tiebreaker break the tie, shall we?"
            string = choice([string_1,string_2])
            bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)
        elif len(player.vote_targets) == 0 and not player.is_abstaining:
            bot.sendMessage(chat_id=update.message.chat_id, text="There is no vote to retract.",reply_to_message_id=update.message.message_id)
        else:
            if player.is_abstaining:
                abstain_votes -= 1
                player.is_abstaining = False
            if len(player.vote_targets) > 0:
                for target in player.vote_targets:
                    target.votes -= 1
                player.vote_targets.clear()
            string = player.name + " has retracted their vote!"
            bot.sendMessage(chat_id=group_id, text=string)

retract_handler = CommandHandler('retract',retract)
dispatcher.add_handler(retract_handler)

###

def votelist(bot,update):
    global phase
    global player_dict
    global abstain_votes
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="No game exists.",reply_to_message_id=update.message.message_id)
    elif phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="The game hasn't started yet!",reply_to_message_id=update.message.message_id)
    elif phase == 'night':
        bot.sendMessage(chat_id=update.message.chat_id, text="Voting only happens during the day.",reply_to_message_id=update.message.message_id)
    else:
        string = ''
        for player in player_dict.values():
            if player.status == 'Alive':
                string += player.name + " has " + str(player.votes) + " votes.\n"
        string += "Abstaining has " + str(abstain_votes) + " votes."
        bot.sendMessage(chat_id=update.message.chat_id, text=string,reply_to_message_id=update.message.message_id)

votelist_handler = CommandHandler('votelist',votelist)
dispatcher.add_handler(votelist_handler)

###

def advance(bot,update,bypass_host = False):
    global phase
    global host_id
    global player_dict
    global abstain_votes
    global day_count
    global group_id
    global tiebreaker

    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="No game exists.",reply_to_message_id=update.message.message_id)
    elif phase == 'startup':
        ready(bot,update)
    elif not (update.message.from_user.id == host_id) and bypass_host == False:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can use /advance.",reply_to_message_id=update.message.message_id)
    elif phase == 'night':
        resolveNightActions(bot,update)
    else:
        #Add players to "vote_order" in order of decreasing votes
        vote_order = sorted(player_dict.values(), key=lambda x: x.votes, reverse=True)
        ##Retrieve players with most votes
        candidates = []
        for player in vote_order:
            if player.votes >= vote_order[0].votes and player.votes >= abstain_votes:
                candidates.append(player)
        ##If many candidates, last dead player tiebreaks
        if len(candidates) > 1 and len(dead_players) > 0 and not vote_order[0].votes == 0:
            tiebreaker = dead_players[-1]
            string = "The vote is tied! The most recently dead player, " + tiebreaker.name + ", must tiebreak. They may now cast a vote."
            bot.sendMessage(chat_id=group_id, text=string)
            bot.sendMessage(chat_id=tiebreaker.chat_id, text="You have been called upon to tiebreak! Cast your vote now!")

        else:
            phase = 'night'
            string = ''
            ##Town abstains
            if len(candidates) == 0 or vote_order[0].votes == 0:
                string += "The town has voted to abstain from lynching anyone.\n"
                pass

            else:
                ##If single candidate
                if len(candidates) == 1:
                    lynchee = candidates[0]
                ##If many candidates and no dead player
                else:
                    lynchee = choice(candidates)
                    string += "The vote is tied! That means Emeric the Mafia Bot gets to pick...!\n"


                lynchee.status = 'Dead'
                dead_players.append(lynchee)
                string += "The town has voted to lynch " + lynchee.name + "!\n"
                bonus_string = ''

                if lynchee.alignment == 'Alien' and 'activated' in lynchee.effects:
                    string += "But... " + lynchee.name + " is an Activated Alien! T-that's impossible!"
                    lynchee.effects.append('winning')
                    lynchee.status = 'Alive'
                else:
                    string += lynchee.name + " has died. They were " + lynchee.flip() + ".\n"
                    sendDeathMessage(bot,lynchee)
                    if lynchee.flip() == 'Mafia':
                        bonus_string = choice(["~WASTED~",
                            lynchee.name + " scurried to the nearest Pokémon Center...",
                            "Get your head in the game, mafia!",
                            "That's the last we'll see of them, I bet.",
                            "(But of course, I already knew they were. Wahahaha!)",
                            "I suppose " + lynchee.name + " had that coming, then.",
                            "RIP in peace, " + lynchee.name + "."])
                    elif lynchee.flip() == 'Innocent':
                        bonus_string = choice(["~WASTED~",
                            lynchee.name + " scurried to the nearest Pokémon Center...",
                            "... Well, you know what they say, you've got to break a few eggs...",
                            "[Mafia Bot patiently awaits the next sacrifice.]",
                            "smh...",
                            "RIP in peace, " + lynchee.name + ".",
                            "As blingy in death as they were in life.",
                            "Alas, poor " + lynchee.name + ".",
                            "I think that may have been a mistake."])
                    else:
                        bonus_string = choice(["So mysterious~!",
                            "What could it mean...?",
                            "The plot thickens!",
                            "Well well well.",
                            "Most curious.",
                            "Huh...!? So, all this time...?",
                            "(As is true of most people in life, I suppose...)",
                            "RIP in peace, " + lynchee.name + "."])
                    string += bonus_string

            bot.sendMessage(chat_id=group_id, text=string)


            ##Cleanup
            abstain_votes = 0
            tiebreaker = Player()
            for player in player_dict.values():
                player.vote_targets.clear()
                player.is_abstaining = False
                player.votes = 0
                player.action_used = False

            if not checkWinConditions(bot,update):
                string = "It is now NIGHT " + str(day_count) + ".\nIf you have a night action, message the bot privately and input it now.\n" \
                "Please do not speak in the group chat during the night phase.\nWhen all night actions have been received, the day phase will begin."
                bot.sendMessage(chat_id=group_id, text=string)
                sendNightMessage(bot,update)
                checkIfNightFinished(bot,update)

advance_handler = CommandHandler('advance',advance)
dispatcher.add_handler(advance_handler)

###

def abort(bot,update):
    global phase
    global abort_confirmation
    global group_id
    global host_id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="No game exists.",reply_to_message_id=update.message.message_id)
    elif not update.message.from_user.id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can use /abort.",reply_to_message_id=update.message.message_id)
    elif abort_confirmation == False:
        bot.sendMessage(chat_id=update.message.chat_id, text="If you really want to abort, type /abort a second time.",reply_to_message_id=update.message.message_id)
        abort_confirmation = True
    else:
        bot.sendMessage(chat_id=group_id, text="The host has aborted the game.")
        clearGame()


abort_handler = CommandHandler('abort',abort)
dispatcher.add_handler(abort_handler)

###

def remind(bot,update):
    global phase
    global host_id
    global player_dict
    global mafia_kill

    player_id = update.message.from_user.id
    if phase == 'off':
        bot.sendMessage(chat_id=update.message.chat_id, text="No game exists.",reply_to_message_id=update.message.message_id)
    elif phase == 'startup':
        bot.sendMessage(chat_id=update.message.chat_id, text="The game hasn't started yet!",reply_to_message_id=update.message.message_id)
    elif not player_id == host_id:
        bot.sendMessage(chat_id=update.message.chat_id, text="Only the host can use /remind!",reply_to_message_id=update.message.message_id)
    elif not phase == 'night':
        bot.sendMessage(chat_id=update.message.chat_id, text="Use /remind during the night phase only!",reply_to_message_id=update.message.message_id)
    else:
        for player in player_dict.values():
            if waitingOn(player):
                    bot.sendMessage(chat_id=player.chat_id, text="Don't forget to use /action, /kill, or /pass tonight!")
        bot.sendMessage(chat_id=update.message.chat_id, text="Reminders sent!",reply_to_message_id=update.message.message_id)


remind_handler = CommandHandler('remind',remind)
dispatcher.add_handler(remind_handler)

###MAIN LOOP
test_mode = False
clearGame()
updater.start_polling()
