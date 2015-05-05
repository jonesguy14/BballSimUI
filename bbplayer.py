import random
import math

class bbplayer:
    #stats_array = [[0 for x in range(2)] 0 for x in range(9)]
    #2manystats
    stats_pts = 0
    stats_fga = 0
    stats_fgm = 0
    stats_3ga = 0
    stats_3gm = 0
    stats_ass = 0
    stats_reb = 0
    stats_stl = 0
    stats_blk = 0
    stats_ofa = 0
    stats_ofm = 0
    
    stats_gms = 0
    stats_tot_pts = 0
    stats_tot_fga = 0
    stats_tot_fgm = 0
    stats_tot_3ga = 0
    stats_tot_3gm = 0
    stats_tot_ass = 0
    stats_tot_reb = 0
    stats_tot_stl = 0
    stats_tot_blk = 0
    stats_tot_msm = 0
    stats_tot_ofa = 0
    stats_tot_ofm = 0
    
    def __init__(self, name, pref_pos, height, weight, speed, age, int_s, mid_s, out_s, passing, handling, steal, block, int_d, out_d, rebounding):
        self.name       = name
        self.height     = height
        self.pref_pos   = pref_pos
        self.weight     = weight
        self.speed      = speed
        self.age        = age
        self.int_s      = int_s
        self.mid_s      = mid_s
        self.out_s      = out_s
        self.passing    = passing
        self.handling   = handling
        self.steal      = steal
        self.block      = block
        self.int_d      = int_d
        self.out_d      = out_d
        self.rebounding = rebounding
        self.ovrshoot   = (int_s + mid_s + out_s) / 3

    def game_reset_pstats(self):
        self.stats_gms += 1
        self.stats_tot_pts += self.stats_pts
        self.stats_pts = 0
        self.stats_tot_fga += self.stats_fga
        self.stats_fga = 0
        self.stats_tot_fgm += self.stats_fgm
        self.stats_fgm = 0
        self.stats_tot_3ga += self.stats_3ga
        self.stats_3ga = 0
        self.stats_tot_3gm += self.stats_3gm
        self.stats_3gm = 0
        self.stats_tot_ass += self.stats_ass
        self.stats_ass = 0
        self.stats_tot_reb += self.stats_reb
        self.stats_reb = 0
        self.stats_tot_stl += self.stats_stl
        self.stats_stl = 0
        self.stats_tot_blk += self.stats_blk
        self.stats_blk = 0
        self.stats_tot_blk += self.stats_blk
        self.stats_blk = 0
        self.stats_tot_ofa += self.stats_ofa
        self.stats_ofa = 0
        self.stats_tot_ofm += self.stats_ofm
        self.stats_ofm = 0
    '''
        for x in stats_array:
            x[1] += x[0]
            x[0] = 0
    '''

    def set_stats_zero(self):
        self.stats_gms = 0
        self.stats_tot_pts = 0
        self.stats_tot_fga = 0
        self.stats_tot_fgm = 0
        self.stats_tot_3ga = 0
        self.stats_tot_3gm = 0
        self.stats_tot_ass = 0
        self.stats_tot_reb = 0
        self.stats_tot_stl = 0
        self.stats_tot_blk = 0
        self.stats_tot_msm = 0
        self.stats_tot_ofa = 0
        self.stats_tot_ofm = 0
    
    @property
    def overall(self):
        return int(self.speed + self.int_s**1.3 + self.mid_s**1.3 + self.out_s**1.3 + self.passing**1.1 + self.handling + self.steal**1.1 + self.block**1.1 + self.int_d**1.2 + self.out_d**1.2 + self.rebounding**1.2)
    @property
    def ppg(self):
        return self.stats_tot_pts/self.stats_gms
    @property
    def fgp(self):
        if self.stats_tot_fga > 0:
            return self.stats_tot_fgm/self.stats_tot_fga
        else: return 0
    @property
    def fp3(self):
        if self.stats_tot_3ga > 0:
            return self.stats_tot_3gm/self.stats_tot_3ga
        else: return 0
    @property
    def rpg(self):
        return self.stats_tot_reb/self.stats_gms
    @property
    def apg(self):
        return self.stats_tot_ass/self.stats_gms
    @property
    def spg(self):
        return self.stats_tot_stl/self.stats_gms
    @property
    def bpg(self):
        return self.stats_tot_blk/self.stats_gms
        
    def print_ratings(self, labels): #labels = 1 if they want headings, 0 if jsut raw stats
        if labels==1:
            print("NAME:        | HT|WGT|AG|SP|IN|MD|OT|PS|HD|ST|BL|ID|OD|RB|")
        
        if self.height>99: disp_height = 99
        else: disp_height = self.height
        
        if self.speed>99: disp_speed = 99
        else: disp_speed = self.speed
        
        if self.int_s>99: disp_int_s = 99
        else: disp_int_s = self.int_s
        
        if self.mid_s>99: disp_mid_s = 99
        else: disp_mid_s = self.mid_s
        
        if self.out_s>99: disp_out_s = 99
        else: disp_out_s = self.out_s
        
        if self.passing>99: disp_passing = 99
        else: disp_passing = self.passing
        
        if self.handling>99: disp_handling = 99
        else: disp_handling = self.handling
        
        if self.steal>99: disp_steal = 99
        else: disp_steal = self.steal
        
        if self.block>99: disp_block = 99
        else: disp_block = self.block
        
        if self.int_d>99: disp_int_d = 99
        else: disp_int_d = self.int_d
        
        if self.out_d>99: disp_out_d = 99
        else: disp_out_d = self.out_d
        
        if self.rebounding>99: disp_rebounding = 99
        else: disp_rebounding = self.rebounding
        
        print("{name:<13}|".format(name=self.name), disp_height, self.weight, self.age, disp_speed, disp_int_s, disp_mid_s, disp_out_s, disp_passing, disp_handling, disp_steal, disp_block, disp_int_d, disp_out_d, disp_rebounding, self.overall, self.pref_pos)
    
    def print_pergame_boxplayer(self):
        print("{name:<13}| {ppg:<4} | {fgp:<4} | {fp3:<4} | {reb:<4} | {ass:<4} | {stl:<4}| {blk:<4}|  {fga:<2} |  {ga3:<2} | {msm:<3} {pos}".format(name=self.name, ppg=int(self.ppg*10)/10, fgp=int(self.fgp*1000)/10, fp3=int(self.fp3*999)/10,
              reb=int(self.rpg*10)/10, ass=int(self.apg*10)/10, stl=int(self.spg*10)/10, blk=int(self.bpg*10)/10, fga=int(self.stats_tot_fga/self.stats_gms), ga3=int(self.stats_tot_3ga/self.stats_gms), msm=int(self.stats_tot_msm/self.stats_gms), pos=self.pref_pos))

    def print_boxplayer(self):
        print("{name:<13}|  {points:<3} | {fgm:<2}/ {fga:<2} | {gm3:<2}/ {ga3:<2} |  {rebounds:<3} |  {assists:<3} |  {steals:<3} |  {blocks:<3}".format(name=self.name, points=self.stats_pts, fgm=self.stats_fgm, 
              fga=self.stats_fga, gm3=self.stats_3gm, ga3=self.stats_3ga, rebounds=self.stats_reb, assists=self.stats_ass, steals=self.stats_stl, blocks=self.stats_blk))