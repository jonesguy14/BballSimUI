from bbplayer import *
import random
import math

class team:
    def __init__(self, name, pointg, shootg, smallf, powerf, center):
        self.name = name
        self.player_array = [None] * 5
        self.bench_array = []
        self.player_array[0] = pointg
        self.player_array[1] = shootg
        self.player_array[2] = smallf
        self.player_array[3] = powerf
        self.player_array[4] = center
        self.wins = 0
        self.losses = 0

    @classmethod
    def empty(cls):
        team_prefixes = ["Mc", "Un", "Not", "Big", "Tiny", "Giant", "Red", "Blue",
                         "Neon", "Swaggy", "White", "Black", "Last", "Best", "Worst"]
        team_suffixes = ["Armadillos", "Lumberjacks", "Killas", "Dicks", "Diamonds",
                         "Senators", "Warriors", "Heat", "Bulls", "Techies",
                         "Ballers", "Rioters", "Mofos", "Nazis", "Klansmen"]
        team_name = team_prefixes[random.randint(0, len(team_prefixes)-1)] + " " + team_suffixes[random.randint(0, len(team_suffixes)-1)]
        return cls(team_name, None, None, None, None, None)
    @property
    def size(self):
        _size = 0
        for player in self.player_array:
            if player != None:
                _size += 1
        for player in self.bench_array:
            if player != None:
                _size += 1
        return _size
    @property
    def pointg(self):
        return self.player_array[0]
    @property
    def shootg(self):
        return self.player_array[1]
    @property
    def smallf(self):
        return self.player_array[2]
    @property
    def powerf(self):
        return self.player_array[3]
    @property
    def center(self):
        return self.player_array[4]

    def add_player(self, player, player_position=None):
        if player_position == None:
            self.bench_array.append(player)
        elif player_position >= 1 and player_position <= 5:
            self.player_array[player_position - 1] = player
        else:
            raise KeyError('Not a valid position')

    def game_reset_tstats(self):
        for player in self.player_array:
            player.game_reset_pstats()

    def set_stats_zero(self):
        for player in self.player_array:
            player.set_stats_zero()

    def print_team(self):
        print(self.name)
        count = 1
        print("NAME:          | HT|WGT|AG|SP|IN|MD|OT|PS|HD|ST|BL|ID|OD|RB|")
        for player in self.player_array:
            print(count, end=" ")
            if player is not None:
                player.print_ratings(0)
            else: print("None")
            count += 1
        for player in self.bench_array:
            print(count, end=" ")
            if player is not None:
                player.print_ratings(0)
            else: print("None")
            count += 1

    def print_team_ratings(self):
        print(self.name)
        print("NAME:        | HT|WGT|AG|SP|IN|MD|OT|PS|HD|ST|BL|ID|OD|RB|")
        for player in self.player_array:
            player.print_ratings(0)
    
    def print_pergame_box(self):
        print("PER GAME AVG | PPG  | FG%  | 3G%  | RPG  | APG  | SPG | BPG | FGA | 3GA | MSM")
        for player in self.player_array:
            player.print_pergame_boxplayer()
        tot_ppg = self.pointg.ppg + self.shootg.ppg + self.smallf.ppg + self.powerf.ppg + self.center.ppg
        tot_fgp = (self.pointg.stats_tot_fgm + self.shootg.stats_tot_fgm+ self.smallf.stats_tot_fgm + self.powerf.stats_tot_fgm +
                   self.center.stats_tot_fgm)/(self.pointg.stats_tot_fga + self.shootg.stats_tot_fga+ self.smallf.stats_tot_fga + self.powerf.stats_tot_fga + self.center.stats_tot_fga)
        tot_3fp = (self.pointg.stats_tot_3gm + self.shootg.stats_tot_3gm+ self.smallf.stats_tot_3gm + self.powerf.stats_tot_3gm + 
                   self.center.stats_tot_3gm)/(self.pointg.stats_tot_3ga + self.shootg.stats_tot_3ga+ self.smallf.stats_tot_3ga + self.powerf.stats_tot_3ga + self.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = self.pointg.rpg + self.shootg.rpg + self.smallf.rpg + self.powerf.rpg + self.center.rpg
        tot_apg = self.pointg.apg + self.shootg.apg + self.smallf.apg + self.powerf.apg + self.center.apg
        tot_spg = self.pointg.spg + self.shootg.spg + self.smallf.spg + self.powerf.spg + self.center.spg
        tot_bpg = self.pointg.bpg + self.shootg.bpg + self.smallf.bpg + self.powerf.bpg + self.center.bpg
        print("-----------------------------------------------------------")
        print("TOTAL:       | {ppg:<5}| {fgp:<4} | {fp3:<4} | {reb:<4} | {ass:<4} | {stl:<4}| {blk:<4}".format(ppg=int(tot_ppg*10)/10, fgp=int(tot_fgp*1000)/10, fp3=int(tot_3fp*1000)/10, reb=int(tot_rpg*10)/10,
              ass=int(tot_apg*10)/10, stl=int(tot_spg*10)/10, blk=int(tot_bpg*10)/10))
    
    def print_box(self):
        print("NAME:        |  PTS | FGM/FGA| 3GM/3GA| REB  | ASS  | STL  | BLK")
        for player in self.player_array:
            player.print_boxplayer()
        tot_pts = self.pointg.stats_pts + self.shootg.stats_pts + self.smallf.stats_pts + self.powerf.stats_pts + self.center.stats_pts
        tot_fgm = self.pointg.stats_fgm + self.shootg.stats_fgm + self.smallf.stats_fgm + self.powerf.stats_fgm + self.center.stats_fgm
        tot_fga = self.pointg.stats_fga + self.shootg.stats_fga + self.smallf.stats_fga + self.powerf.stats_fga + self.center.stats_fga
        tot_3gm = self.pointg.stats_3gm + self.shootg.stats_3gm + self.smallf.stats_3gm + self.powerf.stats_3gm + self.center.stats_3gm
        tot_3ga = self.pointg.stats_3ga + self.shootg.stats_3ga + self.smallf.stats_3ga + self.powerf.stats_3ga + self.center.stats_3ga
        tot_reb = self.pointg.stats_reb + self.shootg.stats_reb + self.smallf.stats_reb + self.powerf.stats_reb + self.center.stats_reb
        tot_ass = self.pointg.stats_ass + self.shootg.stats_ass + self.smallf.stats_ass + self.powerf.stats_ass + self.center.stats_ass
        tot_stl = self.pointg.stats_stl + self.shootg.stats_stl + self.smallf.stats_stl + self.powerf.stats_stl + self.center.stats_stl
        tot_blk = self.pointg.stats_blk + self.shootg.stats_blk + self.smallf.stats_blk + self.powerf.stats_blk + self.center.stats_blk
        print("----------------------------------------------------------")
        print("TOTAL:       |  {points:<3} | {fgm:<2}/ {fga:<2} | {gm3:<2}/ {ga3:<2} |  {rebounds:<3} |  {assists:<3} |  {steals:<3} |  {blocks:<3}".format(points=tot_pts, fgm=tot_fgm, fga=tot_fga,
              gm3=tot_3gm, ga3=tot_3ga, rebounds=tot_reb, assists=tot_ass, steals=tot_stl, blocks=tot_blk))

    def random_assignment(self):
        if self.size >= 5:
            for player in self.player_array:
                if player is None:
                    self.player_array[self.player_array.index(player)] = self.bench_array.pop()
        self.name = "PLAYER TEAM"

    def swap_players(self, pos_1, pos_2):
        if pos_1 <= 10 and pos_2 <= 10 and pos_1 != pos_2:
            player_list = []
            for player in self.player_array:
                player_list.append(player)
            if len(self.bench_array) != 0:
                for player in self.bench_array:
                    player_list.append(player)
            player_1 = player_list[pos_1 - 1]
            player_list[pos_1 - 1] = player_list[pos_2 - 1]
            player_list[pos_2 - 1] = player_1
            for i in range(5):
                self.player_array[i] = player_list[i]
            for i in range(5, len(player_list)):
                self.bench_array[i - 5] = player_list[i]
        else:
            raise KeyError("ur dumb")

    def fudge_num_games(self):
        self.wins = int( 82/60 * self.wins )