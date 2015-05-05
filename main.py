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

        self.done_butt = Button(self, text = "DONE", command = lambda: self.play_season(player_team, opponents_list))
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
            team_recs.insert(END, str(t.name) + " W-L: " + str(t.wins) + "-" + str(60-t.wins) )
        team_recs.grid()

        examine = Button( self, text="Examine Team", command = lambda: self.examine_team(teams_arr[team_recs.index(ACTIVE)], teams_arr) )
        examine.grid()

    def examine_team(self, team, teams_arr):
        for widget in self.winfo_children():
            widget.destroy()

        team_recs = Listbox(self, height = 20, width = 30)
        for t in teams_arr:
            team_recs.insert(END, str(t.name) + " W-L: " + str(t.wins) + "-" + str(60-t.wins) )
        team_recs.grid()

        examine = Button( self, text="Examine Team", command = lambda: self.examine_team(teams_arr[team_recs.index(ACTIVE)], teams_arr) )
        examine.grid()

        names = Listbox(self, height=10, width=15)
        names.grid(row=0,column=1)
        ppg = Listbox(self, height=10, width=7)
        ppg.grid(row=0,column=2)
        fgp = Listbox(self, height=10, width=7)
        fgp.grid(row=0,column=3)
        fp3 = Listbox(self, height=10, width=7)
        fp3.grid(row=0,column=4)
        reb = Listbox(self, height=10, width=7)
        reb.grid(row=0,column=5)
        ass = Listbox(self, height=10, width=7)
        ass.grid(row=0,column=6)
        stl = Listbox(self, height=10, width=7)
        stl.grid(row=0,column=7)
        blk = Listbox(self, height=10, width=7)
        blk.grid(row=0,column=8)
        fga = Listbox(self, height=10, width=7)
        fga.grid(row=0,column=9)
        ga3 = Listbox(self, height=10, width=7)
        ga3.grid(row=0,column=10)
        msm = Listbox(self, height=10, width=7)
        msm.grid(row=0,column=11)
        for p in team.player_array:
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
            msm.insert(END, "  " + str(int(p.stats_tot_msm/p.stats_gms)))


root = Tk()

app = App(root)

root.geometry("800x600")
root.mainloop()
root.destroy()