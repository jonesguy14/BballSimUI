from tkinter import *
from drafter import *
from bbplayer import *
from ai_opponent import *
from team import *
from scripter import *
import random
import math

class App(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)
        self.grid()

        drafter = Drafter()
        draft_players = drafter.draft_generate(90)

        num_opponents = 15
        player_pick_num = 1

        opponents_list = []
        for i in range(num_opponents):
            opponents_list.append(ai_opponent())
        player_team = team.empty()
        player_team.name = "PLAYER TEAM"

        self.draft_buttons(draft_players, player_team, opponents_list, 1)


    def draft_player(self, player, player_list, opponents_list, team, dround):
        team.add_player(player)
        player_list.remove(player)
        print("I drafted " + player.name)
        self.draft(player_list, team, opponents_list, dround)

    def draft_buttons(self, player_list, player_team, opponents_list, dround):
        print("HERE READY TO DRAFT")
        draft_list = Listbox(self, height=35, width=35)
        curr_player = Listbox(self, height=15, width=20)
        draft_list.grid(row=0,column=0)
        curr_player.grid(row=0,column=1)
        for pnum in range(len(player_list)):
            player = player_list[pnum]
            draft_list.insert(END, "POS: "+str(player.pref_pos)+" OVR: "+str(int(100*player.overall/2500))+" NAME: "+str(player.name))

        self.button = Button(self,
                        text = "Scout Selected Player",
                        command = lambda: self.update_scout(player_list, curr_player, draft_list)
                      )
        self.button.grid(row=0,column=2)

        self.button = Button(self,
                        text = "Draft Selected Player",
                        command = lambda pnum=pnum: self.draft_player(player_list[draft_list.index(ACTIVE)], player_list, opponents_list, player_team, dround)
                      )
        self.button.grid(row=0,column=3)

        cteam = Listbox(self, height=15, width=25)
        cteam.grid(row=0, column=4)
        for p in player_team.bench_array:
            cteam.insert(END, str(p.pref_pos) + " " + p.name + " OVR: " + str(int(100*p.overall/2500)))
        
        

    def update_scout(self, player_list, curr_player, draft_list):
        curr_player.grid(row=0,column=1)
        curr_player.delete(0, END)
        p = player_list[draft_list.index(ACTIVE)]
        curr_player.insert(END, str(p.pref_pos) + " " + str( p.name ) )
        curr_player.insert(END, "   HT: "+str(p.height))
        curr_player.insert(END, "   WT: "+str(p.weight))
        curr_player.insert(END, "   AG: "+str(p.age))
        curr_player.insert(END, "   SP: "+str(p.speed))
        curr_player.insert(END, "   IN: "+str(p.int_s))
        curr_player.insert(END, "   MD: "+str(p.mid_s))
        curr_player.insert(END, "   OT: "+str(p.out_s))
        curr_player.insert(END, "   PS: "+str(p.passing))
        curr_player.insert(END, "   HD: "+str(p.handling))
        curr_player.insert(END, "   ST: "+str(p.steal))
        curr_player.insert(END, "   BL: "+str(p.block))
        curr_player.insert(END, "   ID: "+str(p.int_d))
        curr_player.insert(END, "   OD: "+str(p.out_d))
        curr_player.insert(END, "   RB: "+str(p.rebounding))

    def draft(self, player_list, player_team, opponents_list, dround):
        print("AI will draft here, round = "+str(dround))

        for k in range(len(opponents_list)):
            opponents_choice = opponents_list[k].select_player(player_list)
            chosen_player = player_list.pop(opponents_choice)
            opponents_list[k].ai_team.add_player(chosen_player, chosen_player.pref_pos)

        dround+=1

        for widget in self.winfo_children():
            widget.destroy()

        if dround <= 5:
            self.draft_buttons(player_list, player_team, opponents_list, dround)
        else:
            self.setup_team(player_team, opponents_list)

    def setup_team(self, player_team, opponents_list):
        bench = Listbox(self, height=15, width=20)
        bench.grid()
        for p in player_team.bench_array:
            bench.insert(END, str(p.pref_pos) + " " + p.name + " OVR: " + str(int(100*p.overall/2500)))

        starting = Listbox(self, height=15, width=20)

        for i in range(5):
            self.button = Button(self, text = "Set as #"+str(i+1),
                            command = lambda i=i: self.set_player(bench, starting, i, player_team, player_team.bench_array[bench.index(ACTIVE)])
                          )
            self.button.grid()

        starting = Listbox(self, height=15, width=20)
        starting.grid(row=0,column=2)
        for s in range(5):
            starting.insert(END, str(s+1) + " NONE")

        self.done_butt = Button(self, text = "Play Season", command = lambda: self.play_season(player_team, opponents_list))
        self.done_butt.grid(row=1,column=2)

    def set_player(self, bench, starting, index, player_team, bench_player):
        player_team.player_array[index] = bench_player
        player_team.bench_array.remove(bench_player)

        bench.delete(0, END)
        for p in player_team.bench_array:
            bench.insert(END, str(p.pref_pos) + " " + p.name + " OVR: " + str(int(100*p.overall/2500)))

        starting.delete(index)
        starting.insert(index, str(index+1) + " " + bench_player.name + " OVR: " + str(int(100*bench_player.overall/2500)))

    def play_season(self, player_team, opponents_list):
        for widget in self.winfo_children():
            widget.destroy()

        league = []
        league.append(player_team)
        for ai in opponents_list:
            league.append(ai.get_team())

        teams_arr = league
        itr = 0
        while itr < len(teams_arr):
            ttr = itr + 1
            while ttr < len(teams_arr):
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                ttr += 1
            itr += 1

        self.review_season(teams_arr)

    def review_season(self, teams_arr):
        team_recs = Listbox(self, height = 20, width = 30)
        for t in teams_arr:
            team_recs.insert(END, str(t.wins) + "-" + str(60-t.wins) + " : " + str(t.name) )
        team_recs.grid()

        examine = Button( self, text="Examine Team", command = lambda: self.examine_team(teams_arr[team_recs.index(ACTIVE)], teams_arr) )
        examine.grid()

        season_awards = Button( self, text="Season Awards", command = lambda: self.season_awards(teams_arr) )
        season_awards.grid(row=2,column=0)

    def examine_team(self, team, teams_arr):
        for widget in self.winfo_children():
            widget.destroy()

        team_recs = Listbox(self, height = 20, width = 30)
        for t in teams_arr:
            team_recs.insert(END, str(t.wins) + "-" + str(60-t.wins) + " : " + str(t.name) )
        team_recs.grid()

        examine = Button( self, text="Examine Team", command = lambda: self.examine_team(teams_arr[team_recs.index(ACTIVE)], teams_arr) )
        examine.grid()

        season_awards = Button( self, text="Season Awards", command = lambda: self.season_awards(teams_arr) )
        season_awards.grid(row=2,column=0)

        names = Listbox(self, height=15, width=16)
        names.grid(row=0,column=1)
        names.insert(END, str(team.name)+":")
        ppg = Listbox(self, height=15, width=7)
        ppg.grid(row=0,column=2)
        ppg.insert(END, "PPG:")
        fgp = Listbox(self, height=15, width=7)
        fgp.grid(row=0,column=3)
        fgp.insert(END, "FG%:")
        fp3 = Listbox(self, height=15, width=7)
        fp3.grid(row=0,column=4)
        fp3.insert(END, "3ptFG%:")
        reb = Listbox(self, height=15, width=7)
        reb.grid(row=0,column=5)
        reb.insert(END, "REB:")
        ass = Listbox(self, height=15, width=7)
        ass.grid(row=0,column=6)
        ass.insert(END, "ASS:")
        stl = Listbox(self, height=15, width=7)
        stl.grid(row=0,column=7)
        stl.insert(END, "STL:")
        blk = Listbox(self, height=15, width=7)
        blk.grid(row=0,column=8)
        blk.insert(END, "BLK:")
        fga = Listbox(self, height=15, width=7)
        fga.grid(row=0,column=9)
        fga.insert(END, "FGA:")
        ga3 = Listbox(self, height=15, width=7)
        ga3.grid(row=0,column=10)
        ga3.insert(END, "3ptFGA:")
        ofg = Listbox(self, height=15, width=7)
        ofg.grid(row=0,column=11)
        ofg.insert(END, "OpFG%:")
        msm = Listbox(self, height=15, width=7)
        msm.grid(row=0,column=12)
        msm.insert(END, "MSM:")

        for p in team.player_array: #stats
            names.insert(END, str(p.name))
            ppg.insert(END, "  " + str(int(p.ppg*10)/10))
            fgp.insert(END, "  " + str(int(p.fgp*1000)/10)+"%")
            fp3.insert(END, "  " + str(int(p.fp3*999)/10)+"%")
            reb.insert(END, "  " + str(int(p.rpg*10)/10))
            ass.insert(END, "  " + str(int(p.apg*10)/10))
            stl.insert(END, "  " + str(int(p.spg*10)/10)) 
            blk.insert(END, "  " + str(int(p.bpg*10)/10))
            fga.insert(END, "  " + str(int(p.stats_tot_fga/p.stats_gms)))
            ga3.insert(END, "  " + str(int(p.stats_tot_3ga/p.stats_gms)))
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/p.stats_tot_ofa)/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team.pointg.ppg + team.shootg.ppg + team.smallf.ppg + team.powerf.ppg + team.center.ppg
        tot_fgp = (team.pointg.stats_tot_fgm + team.shootg.stats_tot_fgm+ team.smallf.stats_tot_fgm + team.powerf.stats_tot_fgm +
                   team.center.stats_tot_fgm)/(team.pointg.stats_tot_fga + team.shootg.stats_tot_fga+ team.smallf.stats_tot_fga + team.powerf.stats_tot_fga + team.center.stats_tot_fga)
        tot_3fp = (team.pointg.stats_tot_3gm + team.shootg.stats_tot_3gm+ team.smallf.stats_tot_3gm + team.powerf.stats_tot_3gm + 
                   team.center.stats_tot_3gm)/(team.pointg.stats_tot_3ga + team.shootg.stats_tot_3ga+ team.smallf.stats_tot_3ga + team.powerf.stats_tot_3ga + team.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team.pointg.rpg + team.shootg.rpg + team.smallf.rpg + team.powerf.rpg + team.center.rpg
        tot_apg = team.pointg.apg + team.shootg.apg + team.smallf.apg + team.powerf.apg + team.center.apg
        tot_spg = team.pointg.spg + team.shootg.spg + team.smallf.spg + team.powerf.spg + team.center.spg
        tot_bpg = team.pointg.bpg + team.shootg.bpg + team.smallf.bpg + team.powerf.bpg + team.center.bpg
        tot_fga = (team.pointg.stats_tot_fga + team.shootg.stats_tot_fga+ team.smallf.stats_tot_fga + team.powerf.stats_tot_fga + team.center.stats_tot_fga)/team.pointg.stats_gms
        tot_3ga = (team.pointg.stats_tot_3ga + team.shootg.stats_tot_3ga+ team.smallf.stats_tot_3ga + team.powerf.stats_tot_3ga + team.center.stats_tot_3ga)/team.pointg.stats_gms
        tot_ofp = (team.pointg.stats_tot_ofm + team.shootg.stats_tot_ofm+ team.smallf.stats_tot_ofm + team.powerf.stats_tot_ofm +
                   team.center.stats_tot_ofm)/(team.pointg.stats_tot_ofa + team.shootg.stats_tot_ofa + team.smallf.stats_tot_ofa + team.powerf.stats_tot_ofa + team.center.stats_tot_ofa)

        ppg.insert(END, "  " + str(int(tot_ppg*10)/10))
        fgp.insert(END, "  " + str(int(tot_fgp*1000)/10)+"%")
        fp3.insert(END, "  " + str(int(tot_3fp*999)/10)+"%")
        reb.insert(END, "  " + str(int(tot_rpg*10)/10))
        ass.insert(END, "  " + str(int(tot_apg*10)/10))
        stl.insert(END, "  " + str(int(tot_spg*10)/10)) 
        blk.insert(END, "  " + str(int(tot_bpg*10)/10))
        fga.insert(END, "  " + str(int(tot_fga)))
        ga3.insert(END, "  " + str(int(tot_3ga)))
        ofg.insert(END, "  " + str(int(tot_ofp*1000)/10)+"%")
        msm.insert(END, "  ")

        names.insert(END, " ")
        ppg.insert(END, "  ")
        fgp.insert(END, "  ")
        fp3.insert(END, "  ")
        reb.insert(END, "  ")
        ass.insert(END, "  ")
        stl.insert(END, "  ") 
        blk.insert(END, "  ")
        fga.insert(END, "  ")
        ga3.insert(END, "  ")
        ofg.insert(END, "  ")
        msm.insert(END, "  ")

        names.insert(END, "NAME:")
        ppg.insert(END, "HGT:")
        fgp.insert(END, "INS:")
        fp3.insert(END, "MID:")
        reb.insert(END, "OUT:")
        ass.insert(END, "PAS:")
        stl.insert(END, "STL:") 
        blk.insert(END, "BLK:")
        fga.insert(END, "IND:")
        ga3.insert(END, "OTD:")
        ofg.insert(END, "REB:")
        msm.insert(END, "OVR:")

        for p in team.player_array: #ratings
            names.insert(END, str(p.name))
            ppg.insert(END, "  " + str(p.height))
            fgp.insert(END, "  " + str(p.int_s))
            fp3.insert(END, "  " + str(p.mid_s))
            reb.insert(END, "  " + str(p.out_s))
            ass.insert(END, "  " + str(p.passing))
            stl.insert(END, "  " + str(p.steal))
            blk.insert(END, "  " + str(p.block))
            fga.insert(END, "  " + str(p.int_d))
            ga3.insert(END, "  " + str(p.out_d))
            ofg.insert(END, "  " + str(p.rebounding))
            msm.insert(END, "  " + str(int(100*p.overall/2500)))

    def season_awards(self, teams_arr):
        mvp, mvp_team, mvp_score, dpy, dpy_team, dpy_score, team, nba_first_team_from, nba_first_team_scores = get_season_awards(teams_arr)
        for widget in self.winfo_children():
            widget.destroy()


        #mvp and dpoy list
        mvp_list = Listbox(self, height = 28, width = 27)
        mvp_list.insert(END, "MVP: "+str(mvp.name))
        mvp_list.insert(END, "from " + str(mvp_team.name) + " (" + str(mvp_team.wins) + "-" + str(60-mvp_team.wins) + ")")
        mvp_list.insert(END, "  PPG: " + str(int(mvp.ppg*10)/10))
        mvp_list.insert(END, "  FGP: " + str(int(mvp.fgp*1000)/10)+"%")
        mvp_list.insert(END, "  3GP: " + str(int(mvp.fp3*999)/10)+"%")
        mvp_list.insert(END, "  RPG: " + str(int(mvp.rpg*10)/10))
        mvp_list.insert(END, "  APG: " + str(int(mvp.apg*10)/10))
        mvp_list.insert(END, "  SPG: " + str(int(mvp.spg*10)/10)) 
        mvp_list.insert(END, "  BPG: " + str(int(mvp.bpg*10)/10))
        mvp_list.insert(END, "  FGA: " + str(int(mvp.stats_tot_fga/mvp.stats_gms)))
        mvp_list.insert(END, "  3GA: " + str(int(mvp.stats_tot_3ga/mvp.stats_gms)))
        mvp_list.insert(END, "  OFP: " + str(int(1000*mvp.stats_tot_ofm/mvp.stats_tot_ofa)/10) + "%")
        mvp_list.insert(END, "  MSM: " + str(int(mvp.stats_tot_msm/mvp.stats_gms)))

        mvp_list.insert(END, " ")
        mvp_list.insert(END, "DPOY: "+str(dpy.name))
        mvp_list.insert(END, "from " + str(dpy_team.name) + " (" + str(dpy_team.wins) + "-" + str(60-dpy_team.wins) + ")")
        mvp_list.insert(END, "  PPG: " + str(int(dpy.ppg*10)/10))
        mvp_list.insert(END, "  FGP: " + str(int(dpy.fgp*1000)/10)+"%")
        mvp_list.insert(END, "  3GP: " + str(int(dpy.fp3*999)/10)+"%")
        mvp_list.insert(END, "  RPG: " + str(int(dpy.rpg*10)/10))
        mvp_list.insert(END, "  APG: " + str(int(dpy.apg*10)/10))
        mvp_list.insert(END, "  SPG: " + str(int(dpy.spg*10)/10)) 
        mvp_list.insert(END, "  BPG: " + str(int(dpy.bpg*10)/10))
        mvp_list.insert(END, "  FGA: " + str(int(dpy.stats_tot_fga/dpy.stats_gms)))
        mvp_list.insert(END, "  3GA: " + str(int(dpy.stats_tot_3ga/dpy.stats_gms)))
        mvp_list.insert(END, "  OFP: " + str(int(1000*dpy.stats_tot_ofm/dpy.stats_tot_ofa)/10) + "%")
        mvp_list.insert(END, "  MSM: " + str(int(dpy.stats_tot_msm/dpy.stats_gms)))

        mvp_list.grid()

        #nba first team stats and ratings
        names = Listbox(self, height=15, width=16)
        names.grid(row=0,column=1)
        names.insert(END, "ALL-NBA TEAM:")
        ppg = Listbox(self, height=15, width=7)
        ppg.grid(row=0,column=2)
        ppg.insert(END, "PPG:")
        fgp = Listbox(self, height=15, width=7)
        fgp.grid(row=0,column=3)
        fgp.insert(END, "FG%:")
        fp3 = Listbox(self, height=15, width=7)
        fp3.grid(row=0,column=4)
        fp3.insert(END, "3ptFG%:")
        reb = Listbox(self, height=15, width=7)
        reb.grid(row=0,column=5)
        reb.insert(END, "REB:")
        ass = Listbox(self, height=15, width=7)
        ass.grid(row=0,column=6)
        ass.insert(END, "ASS:")
        stl = Listbox(self, height=15, width=7)
        stl.grid(row=0,column=7)
        stl.insert(END, "STL:")
        blk = Listbox(self, height=15, width=7)
        blk.grid(row=0,column=8)
        blk.insert(END, "BLK:")
        fga = Listbox(self, height=15, width=7)
        fga.grid(row=0,column=9)
        fga.insert(END, "FGA:")
        ga3 = Listbox(self, height=15, width=7)
        ga3.grid(row=0,column=10)
        ga3.insert(END, "3ptFGA:")
        ofg = Listbox(self, height=15, width=7)
        ofg.grid(row=0,column=11)
        ofg.insert(END, "OpFG%:")
        msm = Listbox(self, height=15, width=7)
        msm.grid(row=0,column=12)
        msm.insert(END, "MSM:")

        for p in team: #stats
            names.insert(END, str(p.name))
            ppg.insert(END, "  " + str(int(p.ppg*10)/10))
            fgp.insert(END, "  " + str(int(p.fgp*1000)/10)+"%")
            fp3.insert(END, "  " + str(int(p.fp3*999)/10)+"%")
            reb.insert(END, "  " + str(int(p.rpg*10)/10))
            ass.insert(END, "  " + str(int(p.apg*10)/10))
            stl.insert(END, "  " + str(int(p.spg*10)/10)) 
            blk.insert(END, "  " + str(int(p.bpg*10)/10))
            fga.insert(END, "  " + str(int(p.stats_tot_fga/p.stats_gms)))
            ga3.insert(END, "  " + str(int(p.stats_tot_3ga/p.stats_gms)))
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/p.stats_tot_ofa)/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, " ")
        ppg.insert(END, "  ")
        fgp.insert(END, "  ")
        fp3.insert(END, "  ")
        reb.insert(END, "  ")
        ass.insert(END, "  ")
        stl.insert(END, "  ") 
        blk.insert(END, "  ")
        fga.insert(END, "  ")
        ga3.insert(END, "  ")
        ofg.insert(END, "  ")
        msm.insert(END, "  ")

        names.insert(END, "FROM TEAMS:")
        ppg.insert(END, "HGT:")
        fgp.insert(END, "INS:")
        fp3.insert(END, "MID:")
        reb.insert(END, "OUT:")
        ass.insert(END, "PAS:")
        stl.insert(END, "STL:") 
        blk.insert(END, "BLK:")
        fga.insert(END, "IND:")
        ga3.insert(END, "OTD:")
        ofg.insert(END, "REB:")
        msm.insert(END, "OVR:")

        #all-nba teams from
        for t in nba_first_team_from:
            names.insert(END, str(t.wins) + "W " + str(t.name))

        for p in team: #ratings
            ppg.insert(END, "  " + str(p.height))
            fgp.insert(END, "  " + str(p.int_s))
            fp3.insert(END, "  " + str(p.mid_s))
            reb.insert(END, "  " + str(p.out_s))
            ass.insert(END, "  " + str(p.passing))
            stl.insert(END, "  " + str(p.steal))
            blk.insert(END, "  " + str(p.block))
            fga.insert(END, "  " + str(p.int_d))
            ga3.insert(END, "  " + str(p.out_d))
            ofg.insert(END, "  " + str(p.rebounding))
            msm.insert(END, "  " + str(int(100*p.overall/2500)))



root = Tk()

app = App(root)

root.geometry("800x600")
root.mainloop()
root.destroy()