import random
import math
from bbplayer import *

class Drafter:

    def draft_generate_from_file(self):
        player_list = []
        f = open("player_stats.txt", "r")
        for line in f:
            stats = line.split(" ")

            if stats[2] == "PG":
                pref_pos = 1
            elif stats[2] == "SG":
                pref_pos = 2 
            elif stats[2] == "SF":
                pref_pos = 3 
            elif stats[2] == "PF":
                pref_pos = 4 
            elif stats[2] == "C":
                pref_pos = 5 
            
            #stats[26] is ppg
            #39 is allnba
            #40 is alldef

            height = 78
            weight = 180
            speed = 75
            age = 25
            int_s = int( 50 + 65 * float(stats[8]) + 3 * float(stats[6]) )
            print(stats[0]+stats[1])
            print(stats[9])
            print(stats[11])
            if float(stats[9])>0.3:
                out_s = int( 50 + 70 * float(stats[11]) + 6 * float(stats[9]) )
            else:
                out_s = 30
            mid_s = int( (int_s+out_s)/2.7 * (0.45 + float(stats[17])) )
            passing = 60 + int( 10 * float(stats[21]) / float(stats[24]) + float(stats[21]) )
            handling = 75
            steal = int( 50 + 20 * float(stats[22]) )
            block = int( 50 + 20 * float(stats[23]) )
            rebounding = 50 + int( float(stats[20])*5 )
            int_d = int( (block + rebounding)/2.1 )
            out_d = int( (steal + out_s + passing)/3 )
            ins_t = float(stats[28])+float(stats[29]) #% of shots from within 10 ft
            mid_t = float(stats[30])+float(stats[31]) #% of mid range shots
            out_t = float(stats[32]) #%of 3pt shots
            real_fga = float(stats[7])
            name = stats[0] + " " + stats[1] + " " + stats[2]
            gained_attributes = []

            if int(stats[39])!=0: #on all nba team
                int_s += (4 - int(stats[39])) * 2
                mid_s += (4 - int(stats[39]))* 2
                out_s += (4 - int(stats[39])) * 2
                passing += (4 - int(stats[39])) * 2
            if int(stats[40])!=0: #alldef
                int_d += (5 - int(stats[40])) * 2
                out_d += (5 - int(stats[40])) * 2

            gen_player = bbplayer(name, pref_pos, height, weight, speed, age, int_s, mid_s, out_s, passing, handling, steal, block, int_d, out_d, rebounding, ins_t, mid_t, out_t, real_fga, gained_attributes)
            player_list.append(gen_player)

        return player_list


    
    def draft_generate(self, num_players):
        player_list = []
        first_names_list = ["A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.",
                      "J.", "K.", "L.", "M.", "N.", "O.", "P.", "Q.", "R.",
                      "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."]
        last_names_list = ["James", "Bryant", "Iverson", "Bird", "Baddie",
                           "Vanderbilt", "Notgood", "DaBest", "McGrady",
                           "Bud", "Swag", "Jam", "Rockafella", "Snipes", "Durant",
                           "Jordan", "Dogg", "Carter", "Wayne", "Tang", "Jones",
                           "Jesus", "Hooplife", "Buckets", "Curry", "Splash",
                           "Dunkins", "Jumpson"]
        player_name_set = self.generate_name_set(num_players, first_names_list, last_names_list)

        for name in player_name_set:
            position = math.ceil(random.random() * 5)
            player_list.append(self.generate_player(position, 0, name))
        return player_list

    def generate_name_set(self, size, first_names_list, last_names_list=None):
        player_name_set = set()
        if last_names_list is not None:
            if size > len(first_names_list) * len(last_names_list):
                raise KeyError('Don\'t have enough names')
            while len(player_name_set) < size:
                player_name_set.add(random.choice(first_names_list) + " " + random.choice(last_names_list))
        else:
            if size > len(first_names_list):
                raise KeyError('Don\'t have enough names')
            while len(player_name_set) < size:
                player_name_set.add(random.choice(first_names_list))
        return player_name_set

    def generate_player(self, pref_pos, pr, name="Generic"):
        #default values
        def_rat = 75
        height     = 78 #6'6"
        weight     = 180
        speed      = def_rat
        age        = 25
        int_s      = def_rat
        mid_s      = def_rat
        out_s      = def_rat
        passing    = def_rat
        handling   = def_rat
        steal      = def_rat
        block      = def_rat
        int_d      = def_rat
        out_d      = def_rat
        rebounding = def_rat
        if pref_pos==1: #point guard
            if pr==1: print("\nPOINT GUARD")
            height -= random.randint(3, 6)
            weight -= random.randint(0, 30)
            speed += random.randint(5, 10)
            int_s -= random.randint(8, 16)
            mid_s += random.randint(0, 10) - 5
            out_s += random.randint(0, 10) - 5
            passing += random.randint(5, 15)
            handling += random.randint(0, 10)
            steal += random.randint(0, 10) - 2
            block -= random.randint(20, 40)
            int_d -= random.randint(8, 16)
            out_d += random.randint(0, 10) - 5
            rebounding -= random.randint(10, 30)
        elif pref_pos==2: #shooting guard
            if pr==1: print("\nSHOOTING GUARD")
            height += random.randint(0, 4) - 3
            weight += random.randint(0, 30) - 15
            speed += random.randint(0, 6)
            int_s += random.randint(0, 16) - 8
            mid_s += random.randint(0, 13) - 5
            out_s += random.randint(0, 13) - 5
            passing += random.randint(0, 10)
            handling += random.randint(0, 10) - 2
            steal += random.randint(0, 10) - 5
            block -= random.randint(10, 30)
            int_d -= random.randint(5, 10)
            out_d += random.randint(0, 10) - 5
            rebounding -= random.randint(5, 15)
        elif pref_pos==3: #small forward
            if pr==1: print("\nSMALL FORWARD")
            height += random.randint(0, 6) - 2
            weight += random.randint(0, 40) - 10
            speed += random.randint(0, 16) - 8
            int_s += random.randint(0, 20) - 8
            mid_s += random.randint(0, 20) - 10
            out_s += random.randint(0, 20) - 10
            passing += random.randint(0, 20) - 10
            handling += random.randint(0, 20) - 10
            steal += random.randint(0, 20) - 10
            block += random.randint(0, 15) - 5
            int_d += random.randint(0, 15) - 5
            out_d += random.randint(0, 15) - 5
            rebounding += random.randint(0, 15) - 5
        elif pref_pos==4: #power forward
            if pr==1: print("\nPOWER FORWARD")
            height += random.randint(1, 7)
            weight += random.randint(20, 60)
            speed += random.randint(0, 15) - 15
            int_s += random.randint(0, 20) - 5
            mid_s += random.randint(0, 16) - 8
            out_s += random.randint(0, 12) - 6
            passing += random.randint(0, 20) - 20
            handling += random.randint(0, 20) - 20
            steal += random.randint(0, 20) - 20
            block += random.randint(0, 20) - 5
            int_d += random.randint(0, 20) - 5
            out_d += random.randint(0, 10) - 8
            rebounding += random.randint(0, 20) - 5
        elif pref_pos==5: #center
            if pr==1: print("\nCENTER")
            height += random.randint(2, 12)
            weight += random.randint(40, 80)
            speed += random.randint(0, 20) - 30
            int_s += random.randint(5, 15)
            mid_s += random.randint(0, 20) - 15
            out_s += random.randint(0, 30) - 45
            passing += random.randint(0, 20) - 40
            handling += random.randint(0, 30) - 40
            steal += random.randint(0, 30) - 40
            block += random.randint(5, 15)
            int_d += random.randint(5, 15)
            out_d += random.randint(0, 20) - 20
            rebounding += random.randint(5, 15)
        #choose 5(?) of these "attributes" to make a player. Some are good, some bad, some funny
        list_attributes = ["Passer", "Offensive Weapon", "Blocker", "Tall", "Short", "On-ball Defense", "Rebounder", "Fumbler", "Fatty", "Slow", "No Threes", "Dunker", "Defensive Liability", "Offensive Liability",
                           "Mid-range Specialist", "The Whole Package", "The Wall", "3pt Specialist", "Two-way inside", "Two-way outside"]
        num_att = 0
        tries = 0
        gained_attributes = []
        while num_att<5 or tries>10:
            att = random.randint(0, len(list_attributes)-1)
            gained_attributes.append(list_attributes[att])
            num_att+=1
        for a in gained_attributes:
            if pr==1: print(a)
            if a=="Passer":
                passing += random.randint(15, 20)
            elif a=="Offensive Weapon":
                out_s += random.randint(0, 10)
                mid_s += random.randint(10, 15)
                int_s += random.randint(10, 15)
            elif a=="Blocker":
                block += random.randint(10, 15)
            elif a=="Tall":
                height += random.randint(4,8)
            elif a=="Short":
                height -= random.randint(3,5)
            elif a=="On-ball Defense":
                steal += random.randint(5, 10)
                out_d += random.randint(5, 10)
            elif a=="Rebounder":
                rebounding += random.randint(10, 15)
                height += random.randint(0, 2)
            elif a=="Fumbler":
                passing -= random.randint(5, 10)
                handling -= random.randint(5, 10)
            elif a=="Fatty":
                weight += random.randint(50, 100)
            elif a=="Slow":
                speed -= random.randint(20, 40)
                if speed<10: speed=10
            elif a=="No Threes":
                out_s -= random.randint(20, 30)
                if out_s<10: out_s=10
            elif a=="Dunker":
                int_s += random.randint(15, 20)
            elif a=="Defensive Liability":
                steal -= random.randint(5, 10)
                block -= random.randint(5, 10)
                int_d -= random.randint(5, 10)
                out_d -= random.randint(5, 10)
            elif a=="Offensive Liability":
                int_s -= random.randint(5, 10)
                out_s -= random.randint(5, 10)
                mid_s -= random.randint(5, 10)
                if mid_s<10: mid_s=10
                if int_s<10: int_s=10
                if out_s<10: out_s=10
            elif a=="Mid-range Specialist":
                mid_s += random.randint(12, 17)
            elif a=="The Whole Package":
                steal += random.randint(2, 4)
                block += random.randint(2, 4)
                int_d += random.randint(2, 4)
                out_d += random.randint(2, 4)
                int_s += random.randint(2, 4)
                out_s += random.randint(2, 4)
                mid_s += random.randint(2, 4)
                passing += random.randint(2, 4)
            elif a=="The Wall":
                int_d += random.randint(12, 17)
                block += random.randint(6, 12)
            elif a=="3pt Specialist":
                out_s += random.randint(12, 17)
                mid_s -= random.randint(5, 15)
                int_s -= random.randint(5, 15)
                passing -= random.randint(5, 15)
                if passing<10: passin=10
                if mid_s<10: mid_s=10
                if int_s<10: int_s=10
            elif a=="Two-way inside":
                int_s += random.randint(8, 12)
                int_d += random.randint(8, 12)
            elif a=="Two-way outside":
                out_s += random.randint(8, 12)
                out_d += random.randint(8, 12)
                
        return bbplayer(name, pref_pos, height, weight, speed, age, int_s, mid_s, out_s, passing, handling, steal, block, int_d, out_d, rebounding, gained_attributes)