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
        draft_players = drafter.draft_generate_from_file()
        #self.play_real_season(draft_players)
        
        #sort draft_players by overall for easier drafting
        player_sort_ovr = []
        for p in draft_players:
            player_sort_ovr.append(p.overall)
        player_sort_ovr.sort(reverse=True)

        final_sort = []
        pool = draft_players
        for o in player_sort_ovr:
            for p in pool:
                if p.overall == o:
                    final_sort.append(p)
                    pool.remove(p)
                    break



        num_opponents = 15
        player_pick_num = 1

        opponents_list = []
        for i in range(num_opponents):
            opponents_list.append(ai_opponent())
        player_team = team.empty()
        player_team.name = "PLAYER TEAM"

        self.draft_buttons(final_sort, player_team, opponents_list, 1)


    def draft_player(self, player, player_list, opponents_list, team, dround):
        team.add_player(player)
        player_list.remove(player)
        print("I drafted " + player.name)
        self.draft(player_list, team, opponents_list, dround)

    def draft_buttons(self, player_list, player_team, opponents_list, dround):
        print("HERE READY TO DRAFT")

        dlabel = Label(self, text="Draft Round "+str(dround))
        dlabel.grid()

        scrollbar = Scrollbar(self)
        #scrollbar.pack(side=RIGHT, fill=Y)

        draft_list = Listbox(self, height=35, width=45, yscrollcommand=scrollbar.set)
        curr_player = Listbox(self, height=15, width=20)
        draft_list.grid(row=1,column=0)
        curr_player.grid(row=1,column=2)
        for pnum in range(len(player_list)):
            player = player_list[pnum]
            draft_list.insert(END, "#"+str(pnum+1)+" OVR: "+str(int(100*player.overall/2500))+" POS: "+str(player.pref_pos)+" NAME: "+str(player.name)) 
            #draft_list.insert(END, "   " + player.atts[0]+", "+player.atts[1]+", "+ player.atts[2]+",")
            #draft_list.insert(END, "   " + player.atts[3]+", "+player.atts[4])
            #+", "+player.atts[1]+", "+ player.atts[2]+", "+ player.atts[3]+", "+ player.atts[4] )

        scrollbar.grid(row=1, column=1, sticky='nsew')
        scrollbar.config(command=draft_list.yview)

        self.button = Button(self,
                        text = "Scout Selected Player",
                        command = lambda: self.update_scout(player_list, curr_player, draft_list)
                      )
        self.button.grid(row=1,column=3)

        self.button = Button(self,
                        text = "Draft Selected Player", fg="green",
                        command = lambda pnum=pnum: self.draft_player(player_list[int(draft_list.index(ACTIVE))], player_list, opponents_list, player_team, dround)
                      )
        self.button.grid(row=1,column=4)

        cteam = Listbox(self, height=15, width=25)
        cteam.grid(row=1, column=5)
        for p in player_team.bench_array:
            cteam.insert(END, str(p.pref_pos) + " " + p.name + " OVR: " + str(int(100*p.overall/2500)))
        
        

    def update_scout(self, player_list, curr_player, draft_list):
        curr_player.grid(row=1,column=2)
        curr_player.delete(0, END)
        p = player_list[int(draft_list.index(ACTIVE))]
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
        label = Label(self, text="Current Bench:")
        label.grid()

        label2 = Label(self, text="Starting Five:")
        label2.grid(row=0, column=2)

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
        starting.grid(row=1,column=2)
        for s in range(5):
            starting.insert(END, str(s+1) + " NONE")

        self.done_butt = Button(self, text = "Play Season", command = lambda: self.play_season(player_team, opponents_list))
        self.done_butt.grid(row=2,column=2)

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

    def play_real_season(self, player_list):
        league = []
        team_names = ["ATL","BOS","BKN","CHA","CHI","CLE","DAL","DEN","DET","GSW","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOL","NYK","OKC","ORL","PHI","PHX","POR","SAC","SAN","TOR","UTA","WSH"]
        for p in range(30):
            new_team = team(team_names[p], player_list[p*5], player_list[p*5+1], player_list[p*5+2], player_list[p*5+3], player_list[p*5+4])
            league.append(new_team)

        teams_arr = league
        itr = 0
        gp = 0
        while itr < len(teams_arr):
            ttr = itr + 1
            while ttr < len(teams_arr):
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                playgame(teams_arr[itr], teams_arr[ttr], 0, 0).wins += 1
                playgame(teams_arr[ttr], teams_arr[itr], 0, 0).wins += 1
                ttr += 1
                gp += 4
                print( str(gp) + " games played;\n")
            itr += 1
        print("done simming")

        tot_avg_ppg = 0
        tot_avg_fgp = 0     
        tot_avg_3fp = 0    
        tot_avg_rpg = 0
        tot_avg_apg = 0
        tot_avg_spg = 0
        tot_avg_bpg = 0
        tot_avg_fga = 0
        tot_avg_3ga = 0
        tot_avg_ofp = 0

        for teaml in teams_arr:
            tot_avg_ppg += (teaml.pointg.ppg + teaml.shootg.ppg + teaml.smallf.ppg + teaml.powerf.ppg + teaml.center.ppg)/30
            tot_avg_fgp += ((teaml.pointg.stats_tot_fgm + teaml.shootg.stats_tot_fgm+ teaml.smallf.stats_tot_fgm + teaml.powerf.stats_tot_fgm +
                            teaml.center.stats_tot_fgm)/(teaml.pointg.stats_tot_fga + teaml.shootg.stats_tot_fga+ teaml.smallf.stats_tot_fga + teaml.powerf.stats_tot_fga + teaml.center.stats_tot_fga))/30
            tot_avg_3fp += ((teaml.pointg.stats_tot_3gm + teaml.shootg.stats_tot_3gm+ teaml.smallf.stats_tot_3gm + teaml.powerf.stats_tot_3gm + 
                            teaml.center.stats_tot_3gm)/(teaml.pointg.stats_tot_3ga + teaml.shootg.stats_tot_3ga+ teaml.smallf.stats_tot_3ga + teaml.powerf.stats_tot_3ga + teaml.center.stats_tot_3ga + 1))/30 #so no div 0
            tot_avg_rpg += (teaml.pointg.rpg + teaml.shootg.rpg + teaml.smallf.rpg + teaml.powerf.rpg + teaml.center.rpg)/30
            tot_avg_apg += (teaml.pointg.apg + teaml.shootg.apg + teaml.smallf.apg + teaml.powerf.apg + teaml.center.apg)/30
            tot_avg_spg += (teaml.pointg.spg + teaml.shootg.spg + teaml.smallf.spg + teaml.powerf.spg + teaml.center.spg)/30
            tot_avg_bpg += (teaml.pointg.bpg + teaml.shootg.bpg + teaml.smallf.bpg + teaml.powerf.bpg + teaml.center.bpg)/30
            tot_avg_fga += ((teaml.pointg.stats_tot_fga + teaml.shootg.stats_tot_fga+ teaml.smallf.stats_tot_fga + teaml.powerf.stats_tot_fga + teaml.center.stats_tot_fga)/teaml.pointg.stats_gms)/30
            tot_avg_3ga += ((teaml.pointg.stats_tot_3ga + teaml.shootg.stats_tot_3ga+ teaml.smallf.stats_tot_3ga + teaml.powerf.stats_tot_3ga + teaml.center.stats_tot_3ga)/teaml.pointg.stats_gms)/30
            tot_avg_ofp += ((teaml.pointg.stats_tot_ofm + teaml.shootg.stats_tot_ofm+ teaml.smallf.stats_tot_ofm + teaml.powerf.stats_tot_ofm +
                            teaml.center.stats_tot_ofm)/(teaml.pointg.stats_tot_ofa + teaml.shootg.stats_tot_ofa + teaml.smallf.stats_tot_ofa + teaml.powerf.stats_tot_ofa + teaml.center.stats_tot_ofa))/30

        print("TOTAL AVERAGES PER TEAM:")
        print("PPG: "+str(int(tot_avg_ppg*10)/10)+" FGP: "+str(int(tot_avg_fgp*1000)/10)+" 3FP: "+str(int(tot_avg_3fp*1000)/10)+" REB: "+str(int(tot_avg_rpg*10)/10)+" APG: "+str(int(tot_avg_apg*10)/10)+" STL: "+
               str(int(tot_avg_spg*10)/10)+" BLK: "+str(int(tot_avg_bpg*10)/10)+" FGA: "+str(int(tot_avg_fga*10)/10)+" 3GA: "+str(int(tot_avg_3ga*10)/10))

        team_sort_wins = []
        for t in teams_arr:
            team_sort_wins.append(t.wins)
        team_sort_wins.sort(reverse=True)

        final_sort = []
        pool = teams_arr
        for o in team_sort_wins:
            for tt in pool:
                if tt.wins == o:
                    final_sort.append(tt)
                    pool.remove(tt)
                    break

        teams_arr = final_sort
        self.review_season(teams_arr)

    def review_season(self, teams_arr):
        label = Label(self, text="Season Results:")
        label.grid()

        team_recs = Listbox(self, height = 20, width = 30)
        for t in teams_arr:
            t.fudge_num_games()
            team_recs.insert(END, str(t.wins) + "-" + str(82-t.wins) + " : " + str(t.name) )
        team_recs.grid()

        examine = Button( self, text="Examine Team", command = lambda: self.examine_team(teams_arr[team_recs.index(ACTIVE)], teams_arr) )
        examine.grid()

        season_awards = Button( self, text="Season Awards", command = lambda: self.season_awards(teams_arr) )
        season_awards.grid()

    def examine_team(self, team, teams_arr):
        for widget in self.winfo_children():
            widget.destroy()

        label = Label(self, text="Season Results:")
        label.grid()

        team_recs = Listbox(self, height = 20, width = 30)
        for t in teams_arr:
            team_recs.insert(END, str(t.wins) + "-" + str(82-t.wins) + " : " + str(t.name) )
        team_recs.grid()

        examine = Button( self, text="Examine Team", command = lambda: self.examine_team(teams_arr[team_recs.index(ACTIVE)], teams_arr) )
        examine.grid()

        season_awards = Button( self, text="Season Awards", command = lambda: self.season_awards(teams_arr) )
        season_awards.grid()

        names = Listbox(self, height=15, width=16)
        names.grid(row=1,column=1)
        names.insert(END, str(team.name)+":")
        ppg = Listbox(self, height=15, width=7)
        ppg.grid(row=1,column=2)
        ppg.insert(END, "PPG:")
        fgp = Listbox(self, height=15, width=7)
        fgp.grid(row=1,column=3)
        fgp.insert(END, "FG%:")
        fp3 = Listbox(self, height=15, width=7)
        fp3.grid(row=1,column=4)
        fp3.insert(END, "3ptFG%:")
        reb = Listbox(self, height=15, width=7)
        reb.grid(row=1,column=5)
        reb.insert(END, "REB:")
        ass = Listbox(self, height=15, width=7)
        ass.grid(row=1,column=6)
        ass.insert(END, "ASS:")
        stl = Listbox(self, height=15, width=7)
        stl.grid(row=1,column=7)
        stl.insert(END, "STL:")
        blk = Listbox(self, height=15, width=7)
        blk.grid(row=1,column=8)
        blk.insert(END, "BLK:")
        fga = Listbox(self, height=15, width=7)
        fga.grid(row=1,column=9)
        fga.insert(END, "FGA:")
        ga3 = Listbox(self, height=15, width=7)
        ga3.grid(row=1,column=10)
        ga3.insert(END, "3ptFGA:")
        ofg = Listbox(self, height=15, width=7)
        ofg.grid(row=1,column=11)
        ofg.insert(END, "OpFG%:")
        msm = Listbox(self, height=15, width=7)
        msm.grid(row=1,column=12)
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
        mvp_list.insert(END, "from " + str(mvp_team.name) + " (" + str(mvp_team.wins) + "-" + str(82-mvp_team.wins) + ")")
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
        mvp_list.insert(END, "from " + str(dpy_team.name) + " (" + str(dpy_team.wins) + "-" + str(82-dpy_team.wins) + ")")
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

        goto_playoffs = Button( self, text="Begin Playoffs", command = lambda: self.playoffsrnd1(teams_arr) )
        goto_playoffs.grid(row=2,column=0)


    def playoffsrnd1(self, teams_arr):
        for widget in self.winfo_children():
            widget.destroy()

        #sort teams by wins to seed
        teamwins = []
        for team in teams_arr:
            teamwins.append(team.wins)
        teamwins.sort()
        playoff_teams = []
        while len(playoff_teams) < 8:
            for team in teams_arr:
                if len(teamwins) > 0:
                    if team.wins == teamwins[len(teamwins) - 1]: #most wins
                        playoff_teams.append(team)
                        teamwins.remove(team.wins)

        winner18, games18 = playseries(playoff_teams[0], playoff_teams[7], 7, 0, 1)
        winner27, games27 = playseries(playoff_teams[1], playoff_teams[6], 7, 0, 1)
        winner36, games36 = playseries(playoff_teams[2], playoff_teams[5], 7, 0, 1)
        winner45, games45 = playseries(playoff_teams[3], playoff_teams[4], 7, 0, 1)

        winners = []
        winners.append(winner18)
        winners.append(winner27)
        winners.append(winner36)
        winners.append(winner45)

        games_took = []
        games_took.append(games18)
        games_took.append(games27)
        games_took.append(games36)
        games_took.append(games45)

        self.examine_series(playoff_teams, 0, winners, games_took)

        """playoff_list = Listbox(self, height = 25, width = 30)
        playoff_list.insert(END, "1 " + str(playoff_teams[0].name) + "(" + str(playoff_teams[0].wins)+"W)")
        playoff_list.insert(END, "   vs 8 " + str(playoff_teams[7].name) + "(" + str(playoff_teams[7].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winner18.name) + " in " + str(games18))
        playoff_list.insert(END, "2 " + str(playoff_teams[1].name) + "(" + str(playoff_teams[1].wins)+"W)")
        playoff_list.insert(END, "   vs 7 " + str(playoff_teams[6].name) + "(" + str(playoff_teams[6].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winner27.name) + " in " + str(games27))
        playoff_list.insert(END, "3 " + str(playoff_teams[2].name) + "(" + str(playoff_teams[2].wins)+"W)")
        playoff_list.insert(END, "   vs 6 " + str(playoff_teams[5].name) + "(" + str(playoff_teams[5].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winner36.name) + " in " + str(games36))
        playoff_list.insert(END, "4 " + str(playoff_teams[3].name) + "(" + str(playoff_teams[3].wins)+"W)")
        playoff_list.insert(END, "   vs 5 " + str(playoff_teams[4].name) + "(" + str(playoff_teams[4].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winner45.name) + " in " + str(games45))

        playoff_list.grid()

        exam_series_butt = Button(self, text="Examine Series", command= lambda: self.examine_series(playoff_teams, playoff_list.index(ACTIVE), winners, games_took))
        exam_series_butt.grid()

        next_round_butt = Button(self, text="Next Round", command= lambda: self.playoffsrnd2(winners))
        next_round_butt.grid()"""

    def examine_series(self, teams, index, winners, games_took):
        for widget in self.winfo_children():
            widget.destroy()

        label = Label(self, text="Playoffs Round 1")
        label.grid()

        playoff_list = Listbox(self, height = 25, width = 30)
        playoff_list.insert(END, "1 " + str(teams[0].name) + " (" + str(teams[0].wins)+"W)")
        playoff_list.insert(END, "   vs 8 " + str(teams[7].name) + " (" + str(teams[7].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winners[0].name) + " in " + str(games_took[0]))
        playoff_list.insert(END, "2 " + str(teams[1].name) + " (" + str(teams[1].wins)+"W)")
        playoff_list.insert(END, "   vs 7 " + str(teams[6].name) + " (" + str(teams[6].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winners[1].name) + " in " + str(games_took[1]))
        playoff_list.insert(END, "3 " + str(teams[2].name) + " (" + str(teams[2].wins)+"W)")
        playoff_list.insert(END, "   vs 6 " + str(teams[5].name) + " (" + str(teams[5].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winners[2].name) + " in " + str(games_took[2]))
        playoff_list.insert(END, "4 " + str(teams[3].name) + " (" + str(teams[3].wins)+"W)")
        playoff_list.insert(END, "   vs 5 " + str(teams[4].name) + " (" + str(teams[4].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winners[3].name) + " in " + str(games_took[3]))

        playoff_list.grid()

        exam_series_butt = Button(self, text="Examine Series", command= lambda: self.examine_series(teams, playoff_list.index(ACTIVE), winners, games_took))
        exam_series_butt.grid()

        next_round_butt = Button(self, text="Next Round", command= lambda: self.playoffsrnd2(winners))
        next_round_butt.grid()

        if index==0 or index==1 or index==2:
            #1vs8 matchup
            team1 = teams[0]
            team2 = teams[7]
        elif index==3 or index==4 or index==5:
            #2vs7 matchup
            team1 = teams[1]
            team2 = teams[6]
        elif index==6 or index==7 or index==8:
            #3vs6 matchup
            team1 = teams[2]
            team2 = teams[5]
        elif index==9 or index==10 or index==11:
            #4vs5 matchup
            team1 = teams[3]
            team2 = teams[4]

        names = Listbox(self, height=15, width=16)
        names.grid(row=1,column=1)
        names.insert(END, str(team1.wins)+"W "+str(team1.name)+":")
        ppg = Listbox(self, height=15, width=7)
        ppg.grid(row=1,column=2)
        ppg.insert(END, "PPG:")
        fgp = Listbox(self, height=15, width=7)
        fgp.grid(row=1,column=3)
        fgp.insert(END, "FG%:")
        fp3 = Listbox(self, height=15, width=7)
        fp3.grid(row=1,column=4)
        fp3.insert(END, "3ptFG%:")
        reb = Listbox(self, height=15, width=7)
        reb.grid(row=1,column=5)
        reb.insert(END, "REB:")
        ass = Listbox(self, height=15, width=7)
        ass.grid(row=1,column=6)
        ass.insert(END, "ASS:")
        stl = Listbox(self, height=15, width=7)
        stl.grid(row=1,column=7)
        stl.insert(END, "STL:")
        blk = Listbox(self, height=15, width=7)
        blk.grid(row=1,column=8)
        blk.insert(END, "BLK:")
        fga = Listbox(self, height=15, width=7)
        fga.grid(row=1,column=9)
        fga.insert(END, "FGA:")
        ga3 = Listbox(self, height=15, width=7)
        ga3.grid(row=1,column=10)
        ga3.insert(END, "3ptFGA:")
        ofg = Listbox(self, height=15, width=7)
        ofg.grid(row=1,column=11)
        ofg.insert(END, "OpFG%:")
        msm = Listbox(self, height=15, width=7)
        msm.grid(row=1,column=12)
        msm.insert(END, "MSM:")

        for p in team1.player_array: #stats
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
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/(p.stats_tot_ofa+1))/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team1.pointg.ppg + team1.shootg.ppg + team1.smallf.ppg + team1.powerf.ppg + team1.center.ppg
        tot_fgp = (team1.pointg.stats_tot_fgm + team1.shootg.stats_tot_fgm+ team1.smallf.stats_tot_fgm + team1.powerf.stats_tot_fgm +
                   team1.center.stats_tot_fgm)/(team1.pointg.stats_tot_fga + team1.shootg.stats_tot_fga+ team1.smallf.stats_tot_fga + team1.powerf.stats_tot_fga + team1.center.stats_tot_fga)
        tot_3fp = (team1.pointg.stats_tot_3gm + team1.shootg.stats_tot_3gm+ team1.smallf.stats_tot_3gm + team1.powerf.stats_tot_3gm + 
                   team1.center.stats_tot_3gm)/(team1.pointg.stats_tot_3ga + team1.shootg.stats_tot_3ga+ team1.smallf.stats_tot_3ga + team1.powerf.stats_tot_3ga + team1.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team1.pointg.rpg + team1.shootg.rpg + team1.smallf.rpg + team1.powerf.rpg + team1.center.rpg
        tot_apg = team1.pointg.apg + team1.shootg.apg + team1.smallf.apg + team1.powerf.apg + team1.center.apg
        tot_spg = team1.pointg.spg + team1.shootg.spg + team1.smallf.spg + team1.powerf.spg + team1.center.spg
        tot_bpg = team1.pointg.bpg + team1.shootg.bpg + team1.smallf.bpg + team1.powerf.bpg + team1.center.bpg
        tot_fga = (team1.pointg.stats_tot_fga + team1.shootg.stats_tot_fga+ team1.smallf.stats_tot_fga + team1.powerf.stats_tot_fga + team1.center.stats_tot_fga)/team1.pointg.stats_gms
        tot_3ga = (team1.pointg.stats_tot_3ga + team1.shootg.stats_tot_3ga+ team1.smallf.stats_tot_3ga + team1.powerf.stats_tot_3ga + team1.center.stats_tot_3ga)/team1.pointg.stats_gms
        tot_ofp = (team1.pointg.stats_tot_ofm + team1.shootg.stats_tot_ofm+ team1.smallf.stats_tot_ofm + team1.powerf.stats_tot_ofm +
                   team1.center.stats_tot_ofm)/(team1.pointg.stats_tot_ofa + team1.shootg.stats_tot_ofa + team1.smallf.stats_tot_ofa + team1.powerf.stats_tot_ofa + team1.center.stats_tot_ofa)

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

        
        #team2
        names.insert(END, str(team2.wins)+"W "+str(team2.name)+":")
        ppg.insert(END, "PPG:")
        fgp.insert(END, "FG%:")
        fp3.insert(END, "3ptFG%:")
        reb.insert(END, "REB:")
        ass.insert(END, "ASS:")
        stl.insert(END, "STL:")
        blk.insert(END, "BLK:")
        fga.insert(END, "FGA:")
        ga3.insert(END, "3ptFGA:")
        ofg.insert(END, "OpFG%:")
        msm.insert(END, "MSM:")

        for p in team2.player_array: #stats
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
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/(p.stats_tot_ofa+1))/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team2.pointg.ppg + team2.shootg.ppg + team2.smallf.ppg + team2.powerf.ppg + team2.center.ppg
        tot_fgp = (team2.pointg.stats_tot_fgm + team2.shootg.stats_tot_fgm+ team2.smallf.stats_tot_fgm + team2.powerf.stats_tot_fgm +
                   team2.center.stats_tot_fgm)/(team2.pointg.stats_tot_fga + team2.shootg.stats_tot_fga+ team2.smallf.stats_tot_fga + team2.powerf.stats_tot_fga + team2.center.stats_tot_fga)
        tot_3fp = (team2.pointg.stats_tot_3gm + team2.shootg.stats_tot_3gm+ team2.smallf.stats_tot_3gm + team2.powerf.stats_tot_3gm + 
                   team2.center.stats_tot_3gm)/(team2.pointg.stats_tot_3ga + team2.shootg.stats_tot_3ga+ team2.smallf.stats_tot_3ga + team2.powerf.stats_tot_3ga + team2.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team2.pointg.rpg + team2.shootg.rpg + team2.smallf.rpg + team2.powerf.rpg + team2.center.rpg
        tot_apg = team2.pointg.apg + team2.shootg.apg + team2.smallf.apg + team2.powerf.apg + team2.center.apg
        tot_spg = team2.pointg.spg + team2.shootg.spg + team2.smallf.spg + team2.powerf.spg + team2.center.spg
        tot_bpg = team2.pointg.bpg + team2.shootg.bpg + team2.smallf.bpg + team2.powerf.bpg + team2.center.bpg
        tot_fga = (team2.pointg.stats_tot_fga + team2.shootg.stats_tot_fga+ team2.smallf.stats_tot_fga + team2.powerf.stats_tot_fga + team2.center.stats_tot_fga)/team2.pointg.stats_gms
        tot_3ga = (team2.pointg.stats_tot_3ga + team2.shootg.stats_tot_3ga+ team2.smallf.stats_tot_3ga + team2.powerf.stats_tot_3ga + team2.center.stats_tot_3ga)/team2.pointg.stats_gms
        tot_ofp = (team2.pointg.stats_tot_ofm + team2.shootg.stats_tot_ofm+ team2.smallf.stats_tot_ofm + team2.powerf.stats_tot_ofm +
                   team2.center.stats_tot_ofm)/(team2.pointg.stats_tot_ofa + team2.shootg.stats_tot_ofa + team2.smallf.stats_tot_ofa + team2.powerf.stats_tot_ofa + team2.center.stats_tot_ofa)

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

    def playoffsrnd2(self, playoff_teams):
        for widget in self.winfo_children():
            widget.destroy()

        winner18_45, games18_45 = playseries(playoff_teams[0], playoff_teams[3], 7, 0, 1)
        winner27_36, games27_36 = playseries(playoff_teams[1], playoff_teams[2], 7, 0, 1)

        winners = []
        winners.append(winner18_45)
        winners.append(winner27_36)

        games_took = []
        games_took.append(games18_45)
        games_took.append(games27_36)

        self.examine_series2(playoff_teams, 0, winners, games_took)

    def examine_series2(self, teams, index, winners, games_took):
        for widget in self.winfo_children():
            widget.destroy()

        label = Label(self, text="Playoffs Round 2")
        label.grid()

        playoff_list = Listbox(self, height = 25, width = 30)
        playoff_list.insert(END, "1/8 " + str(teams[0].name) + " (" + str(teams[0].wins)+"W)")
        playoff_list.insert(END, "   vs 4/5 " + str(teams[3].name) + " (" + str(teams[3].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winners[0].name) + " in " + str(games_took[0]))
        playoff_list.insert(END, "2/7 " + str(teams[1].name) + " (" + str(teams[1].wins)+"W)")
        playoff_list.insert(END, "   vs 3/6 " + str(teams[2].name) + " (" + str(teams[2].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winners[1].name) + " in " + str(games_took[1]))

        playoff_list.grid()

        exam_series_butt = Button(self, text="Examine Series", command= lambda: self.examine_series2(teams, playoff_list.index(ACTIVE), winners, games_took))
        exam_series_butt.grid()

        next_round_butt = Button(self, text="Next Round", command= lambda: self.playoffsrnd3(winners))
        next_round_butt.grid()

        if index==0 or index==1 or index==2:
            #18vs45 matchup
            team1 = teams[0]
            team2 = teams[3]
        elif index==3 or index==4 or index==5:
            #27vs36 matchup
            team1 = teams[1]
            team2 = teams[2]

        names = Listbox(self, height=15, width=16)
        names.grid(row=1,column=1)
        names.insert(END, str(team1.wins)+"W "+str(team1.name)+":")
        ppg = Listbox(self, height=15, width=7)
        ppg.grid(row=1,column=2)
        ppg.insert(END, "PPG:")
        fgp = Listbox(self, height=15, width=7)
        fgp.grid(row=1,column=3)
        fgp.insert(END, "FG%:")
        fp3 = Listbox(self, height=15, width=7)
        fp3.grid(row=1,column=4)
        fp3.insert(END, "3ptFG%:")
        reb = Listbox(self, height=15, width=7)
        reb.grid(row=1,column=5)
        reb.insert(END, "REB:")
        ass = Listbox(self, height=15, width=7)
        ass.grid(row=1,column=6)
        ass.insert(END, "ASS:")
        stl = Listbox(self, height=15, width=7)
        stl.grid(row=1,column=7)
        stl.insert(END, "STL:")
        blk = Listbox(self, height=15, width=7)
        blk.grid(row=1,column=8)
        blk.insert(END, "BLK:")
        fga = Listbox(self, height=15, width=7)
        fga.grid(row=1,column=9)
        fga.insert(END, "FGA:")
        ga3 = Listbox(self, height=15, width=7)
        ga3.grid(row=1,column=10)
        ga3.insert(END, "3ptFGA:")
        ofg = Listbox(self, height=15, width=7)
        ofg.grid(row=1,column=11)
        ofg.insert(END, "OpFG%:")
        msm = Listbox(self, height=15, width=7)
        msm.grid(row=1,column=12)
        msm.insert(END, "MSM:")

        for p in team1.player_array: #stats
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
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/(p.stats_tot_ofa+1))/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team1.pointg.ppg + team1.shootg.ppg + team1.smallf.ppg + team1.powerf.ppg + team1.center.ppg
        tot_fgp = (team1.pointg.stats_tot_fgm + team1.shootg.stats_tot_fgm+ team1.smallf.stats_tot_fgm + team1.powerf.stats_tot_fgm +
                   team1.center.stats_tot_fgm)/(team1.pointg.stats_tot_fga + team1.shootg.stats_tot_fga+ team1.smallf.stats_tot_fga + team1.powerf.stats_tot_fga + team1.center.stats_tot_fga)
        tot_3fp = (team1.pointg.stats_tot_3gm + team1.shootg.stats_tot_3gm+ team1.smallf.stats_tot_3gm + team1.powerf.stats_tot_3gm + 
                   team1.center.stats_tot_3gm)/(team1.pointg.stats_tot_3ga + team1.shootg.stats_tot_3ga+ team1.smallf.stats_tot_3ga + team1.powerf.stats_tot_3ga + team1.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team1.pointg.rpg + team1.shootg.rpg + team1.smallf.rpg + team1.powerf.rpg + team1.center.rpg
        tot_apg = team1.pointg.apg + team1.shootg.apg + team1.smallf.apg + team1.powerf.apg + team1.center.apg
        tot_spg = team1.pointg.spg + team1.shootg.spg + team1.smallf.spg + team1.powerf.spg + team1.center.spg
        tot_bpg = team1.pointg.bpg + team1.shootg.bpg + team1.smallf.bpg + team1.powerf.bpg + team1.center.bpg
        tot_fga = (team1.pointg.stats_tot_fga + team1.shootg.stats_tot_fga+ team1.smallf.stats_tot_fga + team1.powerf.stats_tot_fga + team1.center.stats_tot_fga)/team1.pointg.stats_gms
        tot_3ga = (team1.pointg.stats_tot_3ga + team1.shootg.stats_tot_3ga+ team1.smallf.stats_tot_3ga + team1.powerf.stats_tot_3ga + team1.center.stats_tot_3ga)/team1.pointg.stats_gms
        tot_ofp = (team1.pointg.stats_tot_ofm + team1.shootg.stats_tot_ofm+ team1.smallf.stats_tot_ofm + team1.powerf.stats_tot_ofm +
                   team1.center.stats_tot_ofm)/(team1.pointg.stats_tot_ofa + team1.shootg.stats_tot_ofa + team1.smallf.stats_tot_ofa + team1.powerf.stats_tot_ofa + team1.center.stats_tot_ofa)

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

        
        #team2
        names.insert(END, str(team2.wins)+"W "+str(team2.name)+":")
        ppg.insert(END, "PPG:")
        fgp.insert(END, "FG%:")
        fp3.insert(END, "3ptFG%:")
        reb.insert(END, "REB:")
        ass.insert(END, "ASS:")
        stl.insert(END, "STL:")
        blk.insert(END, "BLK:")
        fga.insert(END, "FGA:")
        ga3.insert(END, "3ptFGA:")
        ofg.insert(END, "OpFG%:")
        msm.insert(END, "MSM:")

        for p in team2.player_array: #stats
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
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/(p.stats_tot_ofa+1))/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team2.pointg.ppg + team2.shootg.ppg + team2.smallf.ppg + team2.powerf.ppg + team2.center.ppg
        tot_fgp = (team2.pointg.stats_tot_fgm + team2.shootg.stats_tot_fgm+ team2.smallf.stats_tot_fgm + team2.powerf.stats_tot_fgm +
                   team2.center.stats_tot_fgm)/(team2.pointg.stats_tot_fga + team2.shootg.stats_tot_fga+ team2.smallf.stats_tot_fga + team2.powerf.stats_tot_fga + team2.center.stats_tot_fga)
        tot_3fp = (team2.pointg.stats_tot_3gm + team2.shootg.stats_tot_3gm+ team2.smallf.stats_tot_3gm + team2.powerf.stats_tot_3gm + 
                   team2.center.stats_tot_3gm)/(team2.pointg.stats_tot_3ga + team2.shootg.stats_tot_3ga+ team2.smallf.stats_tot_3ga + team2.powerf.stats_tot_3ga + team2.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team2.pointg.rpg + team2.shootg.rpg + team2.smallf.rpg + team2.powerf.rpg + team2.center.rpg
        tot_apg = team2.pointg.apg + team2.shootg.apg + team2.smallf.apg + team2.powerf.apg + team2.center.apg
        tot_spg = team2.pointg.spg + team2.shootg.spg + team2.smallf.spg + team2.powerf.spg + team2.center.spg
        tot_bpg = team2.pointg.bpg + team2.shootg.bpg + team2.smallf.bpg + team2.powerf.bpg + team2.center.bpg
        tot_fga = (team2.pointg.stats_tot_fga + team2.shootg.stats_tot_fga+ team2.smallf.stats_tot_fga + team2.powerf.stats_tot_fga + team2.center.stats_tot_fga)/team2.pointg.stats_gms
        tot_3ga = (team2.pointg.stats_tot_3ga + team2.shootg.stats_tot_3ga+ team2.smallf.stats_tot_3ga + team2.powerf.stats_tot_3ga + team2.center.stats_tot_3ga)/team2.pointg.stats_gms
        tot_ofp = (team2.pointg.stats_tot_ofm + team2.shootg.stats_tot_ofm+ team2.smallf.stats_tot_ofm + team2.powerf.stats_tot_ofm +
                   team2.center.stats_tot_ofm)/(team2.pointg.stats_tot_ofa + team2.shootg.stats_tot_ofa + team2.smallf.stats_tot_ofa + team2.powerf.stats_tot_ofa + team2.center.stats_tot_ofa)

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

    def playoffsrnd3(self, playoff_teams):
        for widget in self.winfo_children():
            widget.destroy()

        winner_finals, games_finals = playseries(playoff_teams[0], playoff_teams[1], 7, 0, 1)

        self.examine_series3(playoff_teams, 0, winner_finals, games_finals)

    def examine_series3(self, teams, index, winner, games_took):
        for widget in self.winfo_children():
            widget.destroy()

        label = Label(self, text="NBA Finals")
        label.grid()

        playoff_list = Listbox(self, height = 25, width = 30)
        playoff_list.insert(END, "1/8 " + str(teams[0].name) + " (" + str(teams[0].wins)+"W)")
        playoff_list.insert(END, "   vs 4/5 " + str(teams[1].name) + " (" + str(teams[1].wins)+"W)")
        playoff_list.insert(END, "      WINNER: " + str(winner.name) + " in " + str(games_took))

        playoff_list.grid()

        #exam_series_butt = Button(self, text="Examine Series", command= lambda: self.examine_series2(teams, playoff_list.index(ACTIVE), winners, games_took))
        #exam_series_butt.grid()

        #next_round_butt = Button(self, text="Next Round", command= lambda: self.playoffsrnd3(winners))
        #next_round_butt.grid()

        team1 = teams[0]
        team2 = teams[1]

        names = Listbox(self, height=15, width=16)
        names.grid(row=1,column=1)
        names.insert(END, str(team1.wins)+"W "+str(team1.name)+":")
        ppg = Listbox(self, height=15, width=7)
        ppg.grid(row=1,column=2)
        ppg.insert(END, "PPG:")
        fgp = Listbox(self, height=15, width=7)
        fgp.grid(row=1,column=3)
        fgp.insert(END, "FG%:")
        fp3 = Listbox(self, height=15, width=7)
        fp3.grid(row=1,column=4)
        fp3.insert(END, "3ptFG%:")
        reb = Listbox(self, height=15, width=7)
        reb.grid(row=1,column=5)
        reb.insert(END, "REB:")
        ass = Listbox(self, height=15, width=7)
        ass.grid(row=1,column=6)
        ass.insert(END, "ASS:")
        stl = Listbox(self, height=15, width=7)
        stl.grid(row=1,column=7)
        stl.insert(END, "STL:")
        blk = Listbox(self, height=15, width=7)
        blk.grid(row=1,column=8)
        blk.insert(END, "BLK:")
        fga = Listbox(self, height=15, width=7)
        fga.grid(row=1,column=9)
        fga.insert(END, "FGA:")
        ga3 = Listbox(self, height=15, width=7)
        ga3.grid(row=1,column=10)
        ga3.insert(END, "3ptFGA:")
        ofg = Listbox(self, height=15, width=7)
        ofg.grid(row=1,column=11)
        ofg.insert(END, "OpFG%:")
        msm = Listbox(self, height=15, width=7)
        msm.grid(row=1,column=12)
        msm.insert(END, "MSM:")

        for p in team1.player_array: #stats
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
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/(p.stats_tot_ofa+1))/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team1.pointg.ppg + team1.shootg.ppg + team1.smallf.ppg + team1.powerf.ppg + team1.center.ppg
        tot_fgp = (team1.pointg.stats_tot_fgm + team1.shootg.stats_tot_fgm+ team1.smallf.stats_tot_fgm + team1.powerf.stats_tot_fgm +
                   team1.center.stats_tot_fgm)/(team1.pointg.stats_tot_fga + team1.shootg.stats_tot_fga+ team1.smallf.stats_tot_fga + team1.powerf.stats_tot_fga + team1.center.stats_tot_fga)
        tot_3fp = (team1.pointg.stats_tot_3gm + team1.shootg.stats_tot_3gm+ team1.smallf.stats_tot_3gm + team1.powerf.stats_tot_3gm + 
                   team1.center.stats_tot_3gm)/(team1.pointg.stats_tot_3ga + team1.shootg.stats_tot_3ga+ team1.smallf.stats_tot_3ga + team1.powerf.stats_tot_3ga + team1.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team1.pointg.rpg + team1.shootg.rpg + team1.smallf.rpg + team1.powerf.rpg + team1.center.rpg
        tot_apg = team1.pointg.apg + team1.shootg.apg + team1.smallf.apg + team1.powerf.apg + team1.center.apg
        tot_spg = team1.pointg.spg + team1.shootg.spg + team1.smallf.spg + team1.powerf.spg + team1.center.spg
        tot_bpg = team1.pointg.bpg + team1.shootg.bpg + team1.smallf.bpg + team1.powerf.bpg + team1.center.bpg
        tot_fga = (team1.pointg.stats_tot_fga + team1.shootg.stats_tot_fga+ team1.smallf.stats_tot_fga + team1.powerf.stats_tot_fga + team1.center.stats_tot_fga)/team1.pointg.stats_gms
        tot_3ga = (team1.pointg.stats_tot_3ga + team1.shootg.stats_tot_3ga+ team1.smallf.stats_tot_3ga + team1.powerf.stats_tot_3ga + team1.center.stats_tot_3ga)/team1.pointg.stats_gms
        tot_ofp = (team1.pointg.stats_tot_ofm + team1.shootg.stats_tot_ofm+ team1.smallf.stats_tot_ofm + team1.powerf.stats_tot_ofm +
                   team1.center.stats_tot_ofm)/(team1.pointg.stats_tot_ofa + team1.shootg.stats_tot_ofa + team1.smallf.stats_tot_ofa + team1.powerf.stats_tot_ofa + team1.center.stats_tot_ofa)

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

        
        #team2
        names.insert(END, str(team2.wins)+"W "+str(team2.name)+":")
        ppg.insert(END, "PPG:")
        fgp.insert(END, "FG%:")
        fp3.insert(END, "3ptFG%:")
        reb.insert(END, "REB:")
        ass.insert(END, "ASS:")
        stl.insert(END, "STL:")
        blk.insert(END, "BLK:")
        fga.insert(END, "FGA:")
        ga3.insert(END, "3ptFGA:")
        ofg.insert(END, "OpFG%:")
        msm.insert(END, "MSM:")

        for p in team2.player_array: #stats
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
            ofg.insert(END, "  " + str(int(1000*p.stats_tot_ofm/(p.stats_tot_ofa+1))/10) + "%")
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))

        names.insert(END, "TOTAL:")

        tot_ppg = team2.pointg.ppg + team2.shootg.ppg + team2.smallf.ppg + team2.powerf.ppg + team2.center.ppg
        tot_fgp = (team2.pointg.stats_tot_fgm + team2.shootg.stats_tot_fgm+ team2.smallf.stats_tot_fgm + team2.powerf.stats_tot_fgm +
                   team2.center.stats_tot_fgm)/(team2.pointg.stats_tot_fga + team2.shootg.stats_tot_fga+ team2.smallf.stats_tot_fga + team2.powerf.stats_tot_fga + team2.center.stats_tot_fga)
        tot_3fp = (team2.pointg.stats_tot_3gm + team2.shootg.stats_tot_3gm+ team2.smallf.stats_tot_3gm + team2.powerf.stats_tot_3gm + 
                   team2.center.stats_tot_3gm)/(team2.pointg.stats_tot_3ga + team2.shootg.stats_tot_3ga+ team2.smallf.stats_tot_3ga + team2.powerf.stats_tot_3ga + team2.center.stats_tot_3ga + 1) #so no div 0
        tot_rpg = team2.pointg.rpg + team2.shootg.rpg + team2.smallf.rpg + team2.powerf.rpg + team2.center.rpg
        tot_apg = team2.pointg.apg + team2.shootg.apg + team2.smallf.apg + team2.powerf.apg + team2.center.apg
        tot_spg = team2.pointg.spg + team2.shootg.spg + team2.smallf.spg + team2.powerf.spg + team2.center.spg
        tot_bpg = team2.pointg.bpg + team2.shootg.bpg + team2.smallf.bpg + team2.powerf.bpg + team2.center.bpg
        tot_fga = (team2.pointg.stats_tot_fga + team2.shootg.stats_tot_fga+ team2.smallf.stats_tot_fga + team2.powerf.stats_tot_fga + team2.center.stats_tot_fga)/team2.pointg.stats_gms
        tot_3ga = (team2.pointg.stats_tot_3ga + team2.shootg.stats_tot_3ga+ team2.smallf.stats_tot_3ga + team2.powerf.stats_tot_3ga + team2.center.stats_tot_3ga)/team2.pointg.stats_gms
        tot_ofp = (team2.pointg.stats_tot_ofm + team2.shootg.stats_tot_ofm+ team2.smallf.stats_tot_ofm + team2.powerf.stats_tot_ofm +
                   team2.center.stats_tot_ofm)/(team2.pointg.stats_tot_ofa + team2.shootg.stats_tot_ofa + team2.smallf.stats_tot_ofa + team2.powerf.stats_tot_ofa + team2.center.stats_tot_ofa)

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


root = Tk()

app = App(root)

root.geometry("800x600")
root.mainloop()
root.destroy()