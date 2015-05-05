from bbplayer import *
from team import *
import random
import math

class ai_opponent:

    def __init__(self, name=None, ai_team=None):
        if name == None:
            names_list = ["Sterling", "Cuban", "Rivers", "Riley", "Blatt", "Carlisle", "Gilbert", "Adolf", "Dolan", "Popovich"]
            self.name = random.choice(names_list)
            names_list.remove(self.name)
        else:
            self.name = name
        if ai_team == None:
            self.ai_team = team.empty()
        else:
            self.ai_team = ai_team

    def select_player(self, player_list):
        overalls = []
        for p in player_list:
            overalls.append(p.overall)
        overalls.sort()
        draft_position = 0
        made_selection = False
        top = 1
        while made_selection==False:
            for p in player_list:
                if p.overall == overalls[len(player_list)-top]:
                    if self.ai_team.player_array[p.pref_pos-1] == None:
                        print(self.name, "has selected", p.name, p.pref_pos)
                        made_selection = True
                        return draft_position
                    else: #don't pick top guy since we already have a guy in that position 
                        if top == len(player_list): #no guys in the position we want
                            sec_draft_position = 0
                            for p in player_list:
                                if p.overall == overalls[len(player_list)-1]: #just pick best overall guy
                                    if self.ai_team.player_array[0] == None:
                                        p.pref_pos = 1
                                    elif self.ai_team.player_array[1] == None:
                                        p.pref_pos = 2
                                    elif self.ai_team.player_array[2] == None:
                                        p.pref_pos = 3
                                    elif self.ai_team.player_array[3] == None:
                                        p.pref_pos = 4
                                    elif self.ai_team.player_array[4] == None:
                                        p.pref_pos = 5
                                    
                                    print(self.name, "has selected", p.name, p.pref_pos)
                                    made_selection = True
                                    return sec_draft_position
                                    
                                sec_draft_position += 1
                        top += 1
                draft_position += 1
            draft_position = 0

    def get_team(self):
        return self.ai_team