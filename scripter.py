from bbplayer import *
from ai_opponent import *
from team import *
import random
import math

def calc_mismatch(shooter, defender, pr):
    int_mis = (2*shooter.int_s - defender.int_d) * shooter.ins_t
    mid_mis = (2*shooter.mid_s - (defender.out_d + defender.int_d)/2) * shooter.mid_t
    out_mis = (2*shooter.out_s - defender.out_d) * shooter.out_t
    if pr==1: print(int_mis + mid_mis + out_mis)
    return (((int_mis + mid_mis + out_mis)*shooter.real_fga)**1.3)/100

def detect_mismatch(offense, defense, pr):
    pg_diff = calc_mismatch(offense.pointg, defense.pointg, pr)
    sg_diff = calc_mismatch(offense.shootg, defense.shootg, pr)
    sf_diff = calc_mismatch(offense.smallf, defense.smallf, pr)
    pf_diff = calc_mismatch(offense.powerf, defense.powerf, pr)
    cn_diff = calc_mismatch(offense.center, defense.center, pr)
    matches = [pg_diff, sg_diff, sf_diff, pf_diff, cn_diff]
    return matches

def find_rebounder(team): #who shall receive the rebounding blessing?
    cenreb = random.random()*team.center.rebounding
    powreb = random.random()*team.powerf.rebounding
    smfreb = random.random()*team.smallf.rebounding
    shgreb = random.random()*team.shootg.rebounding
    ptgreb = random.random()*team.pointg.rebounding
    listreb = [cenreb, powreb, smfreb, shgreb, ptgreb]
    listreb.sort()
    if listreb[4]==cenreb:
        team.center.stats_reb += 1
        return team.center
    elif listreb[4]==powreb:
        team.powerf.stats_reb += 1
        return team.powerf
    elif listreb[4]==smfreb:
        team.smallf.stats_reb += 1
        return team.smallf   
    elif listreb[4]==shgreb:
        team.shootg.stats_reb += 1
        return team.shootg
    else:
        team.pointg.stats_reb += 1
        return team.pointg
    
def get_ball_carrier(team):
    smfbc = random.random()*team.smallf.passing
    shgbc = random.random()*team.shootg.passing
    ptgbc = random.random()*team.pointg.passing
    listbc = [smfbc, shgbc, ptgbc]
    listbc.sort()
    if listbc[2]==smfbc:
        return team.smallf
    elif listbc[2]==shgbc:
        return team.shootg
    else:
        return team.pointg
        
def get_season_awards(teams):
    #MVP, Defensive Player, etc
    mvp_score = 0
    mvp = None
    mvp_team = None
    dpy_score = 0
    dpy = None
    dpy_team = None
    nba_first_team = [None, None, None, None, None]
    nba_first_team_from = [None, None, None, None, None]
    nba_first_team_scores = [0, 0, 0, 0, 0]
    for team in teams:
        #all nba first team
        for i in range(5):
            team_calc = team.player_array[i].stats_tot_pts*1.4 + team.player_array[i].stats_tot_ass*1.3 + team.player_array[i].stats_tot_reb*0.8 + team.player_array[i].stats_tot_stl*1.2 + team.player_array[i].stats_tot_blk*1.2 + (team.wins*2)/60
            if team_calc > nba_first_team_scores[i]:
                nba_first_team_scores[i] = team_calc
                nba_first_team[i] = team.player_array[i]
                nba_first_team_from[i] = team
            
        for p in team.player_array:
            #MVP
            mvp_calc = (p.stats_tot_pts*1.4 + p.stats_tot_ass*1.3 + p.stats_tot_reb*0.8 + p.stats_tot_stl*1.2 + p.stats_tot_blk*1.2)/p.stats_gms + (team.wins*30)/60
            if mvp_calc > mvp_score:
                mvp_score = mvp_calc
                mvp = p
                mvp_team = team
                print("FOUND NEW MVP: " + p.name + " from " + team.name + " with score of " + str(int(mvp_score)))
            elif mvp_calc > 75:
                print("big mvp score: " + p.name + " from " + team.name + " with score of " + str(int(mvp_calc)))
            #DPOTY
            dpy_calc = p.stats_tot_reb*0.1 + p.stats_tot_stl + p.stats_tot_blk + team.wins*5
            if dpy_calc > dpy_score:
                dpy_score = dpy_calc
                dpy = p
                dpy_team = team
                
    return mvp, mvp_team, mvp_score, dpy, dpy_team, dpy_score, nba_first_team, nba_first_team_from, nba_first_team_scores

def intelligent_pass(who_poss, offense, defense, matches):

    #calculate real tendencies, ie real life fga with mismatches taken into acct
    mism_factor = 18
    pg_ten = offense.pointg.real_fga + matches[0]/mism_factor
    sg_ten = offense.shootg.real_fga + matches[1]/mism_factor
    sf_ten = offense.smallf.real_fga + matches[2]/mism_factor
    pf_ten = offense.powerf.real_fga + matches[3]/mism_factor
    cn_ten = offense.center.real_fga + matches[4]/mism_factor

    tot_real_ten = pg_ten + sg_ten + sf_ten + pf_ten + cn_ten

    who_pass = random.random()*tot_real_ten

    if who_pass < pg_ten:
        return offense.pointg
    elif who_pass < (pg_ten + sg_ten):
        return offense.shootg
    elif who_pass < (pg_ten + sg_ten + sf_ten):
        return offense.smallf
    elif who_pass < (pg_ten + sg_ten + sf_ten + pf_ten):
        return offense.powerf
    else:
        return offense.center

    """tot_real_fga = offense.pointg.real_fga + offense.shootg.real_fga + offense.smallf.real_fga + offense.powerf.real_fga + offense.center.real_fga

    who_pass = random.random()*tot_real_fga

    if who_pass < offense.pointg.real_fga: #and offense.pointg.real_fga!=who_poss.real_fga:
        return offense.pointg
    elif who_pass < (offense.pointg.real_fga + offense.shootg.real_fga): #and offense.shootg.real_fga!=who_poss.real_fga:
        return offense.shootg
    elif who_pass < (offense.pointg.real_fga + offense.shootg.real_fga + offense.smallf.real_fga): #and offense.smallf.real_fga!=who_poss.real_fga:
        return offense.smallf
    elif who_pass < (offense.pointg.real_fga + offense.shootg.real_fga + offense.smallf.real_fga + offense.powerf.real_fga): #and offense.powerf.real_fga!=who_poss.real_fga:
        return offense.powerf
    else:
        return offense.center"""

    """sorted_matches = sorted(matches)

    for i in range(len(sorted_matches)): #fix crash hopefully
        sorted_matches[i] = abs(sorted_matches[i])
        matches[i] = abs(matches[i])

    weighted = 1.4
    tot_m = matches[0]**weighted + matches[1]**weighted + matches[2]**weighted + matches[3]**weighted + matches[4]**weighted
    sel_target = random.randint(0, int(tot_m))
    if sel_target < sorted_matches[4]**weighted:
        target = sorted_matches[4]
    elif sel_target < (sorted_matches[4]**weighted + sorted_matches[3]**weighted):
        target = sorted_matches[3]
    elif sel_target < (sorted_matches[4]**weighted + sorted_matches[3]**weighted + sorted_matches[2]**weighted):
        target = sorted_matches[2]
    elif sel_target < (sorted_matches[4]**weighted + sorted_matches[3]**weighted + sorted_matches[2]**weighted + sorted_matches[1]**weighted):
        target = sorted_matches[1]
    else:
        target = sorted_matches[0]
    
    if target == matches[0]: #pg target of pass
        return offense.pointg
    elif target == matches[1]: #sg target of pass
        return offense.shootg
    elif target == matches[2]: #sf target of pass
        return offense.smallf
    elif target == matches[3]: #pf target of pass
        return offense.powerf
    elif target == matches[4]: #cn target of pass
        return offense.center"""

def playoffs(teams_arr):
    #round1
    print("\nROUND OF 8:")
    winner18 = playseries(teams_arr[0], teams_arr[7], 7, 0, 1)
    winner27 = playseries(teams_arr[1], teams_arr[6], 7, 0, 1)
    winner36 = playseries(teams_arr[2], teams_arr[5], 7, 0, 1)
    winner45 = playseries(teams_arr[3], teams_arr[4], 7, 0, 1)
    #round2
    print("\nSEMIFINALS:")
    winner18_45 = playseries(winner18, winner45, 7, 0, 1)
    winner27_36 = playseries(winner27, winner36, 7, 0, 1)
    #finals
    input("\nPress Enter to continue to the NBA FINALS...")
    print("\nNBA FINALS:")
    #gonna play thh NBA finals with the play-by-play printing so make it more dramatic lol
    winner18_45.set_stats_zero()
    winner27_36.set_stats_zero() #reset all the player stats so the pergame box is only for this series
    wins1 = 0
    wins2 = 0
    series_games = 7
    numgames = 7
    winner_decided = False
    toggle_home = True #have toggle to change arenas every game (maybe home adv l8r implement so this might matter)
    while numgames > 0 and winner_decided==False:
        print("\nStandings: ",winner18_45.name,"-",wins1,winner27_36.name,"-",wins2)
        input("\nPress enter to play Game {gm} of the NBA Finals...".format(gm=series_games - numgames + 1))
        if toggle_home == True:
            toggle_home = False
            winner = playgame(winner18_45, winner27_36, 1, 1)
            if winner==winner18_45:
                wins1 += 1
            elif winner==winner27_36: 
                wins2 += 1
        else:
            toggle_home = True
            winner = playgame(winner27_36, winner18_45, 1, 1)
            if winner==winner27_36:
                wins2 += 1
            elif winner==winner18_45: 
                wins1 += 1
        numgames -= 1
        if wins1>(series_games/2) or wins2>(series_games/2):
            winner_decided = True
            
    print("\n")
    print("NBA FINALS RESULTS:",winner18_45.name,"-",wins1,winner27_36.name,"-",wins2,"\n")
    print(winner18_45.name,"-",wins1,"wins")
    winner18_45.print_pergame_box()
    print("\n")
    print(winner27_36.name,"-",wins2,"wins")
    winner27_36.print_pergame_box()
    
    if wins1 > wins2:
        return winner18_45
    else: return winner27_36
    
    #finals_winner = playseries(winner18_45, winner27_36, 7, 1, 1)
    #return finals_winner
        
def playseries(team1, team2, numgames, prbox, prend): #returns winner
    team1.set_stats_zero()
    team2.set_stats_zero() #reset all the player stats so the pergame box is only for this series
    wins1 = 0
    wins2 = 0
    series_games = numgames
    winner_decided = False
    toggle_home = True #have toggle to change arenas every game (maybe home adv l8r implement so this might matter)
    while numgames > 0 and winner_decided==False:
        if toggle_home == True:
            toggle_home = False
            winner = playgame(team1, team2, 0, prbox)
            if winner==team1:
                wins1 += 1
            elif winner==team2: 
                wins2 += 1
        else:
            toggle_home = True
            winner = playgame(team2, team1, 0, prbox)
            if winner==team2:
                wins2 += 1
            elif winner==team1: 
                wins1 += 1
        numgames -= 1
        if wins1>(series_games/2) or wins2>(series_games/2):
            winner_decided = True
    
    print("\n")
    print("Result of",series_games,"game series:",team1.name,"-",wins1,team2.name,"-",wins2,"\n")
    if prend == 1:
        print(team1.name,"-",wins1,"wins")
        team1.print_pergame_box()
        print("\n")
        print(team2.name,"-",wins2,"wins")
        team2.print_pergame_box()
    
    if wins1 > wins2:
        return team1, (series_games - numgames)
    else: return team2, (series_games - numgames)

def playgame(home, away, prplay, prbox): #home team, away team, print play-by-play (0 or 1), print box at end (0 or 1)
    if prbox==1: 
        print("\n")
        print(away.name, " @ ", home.name,"\n")
    
    #set possession
    poss_home, poss_away = tip_off(home, away, prplay)
    gametime = 0
    max_gametime = 2400
    hscore = 0
    ascore = 0
    hspeed = (home.pointg.speed + home.shootg.speed + home.smallf.speed) / 600 + 0.5
    aspeed = (away.pointg.speed + away.shootg.speed + away.smallf.speed) / 600 + 0.5
    playing = True
    
    matches_h = detect_mismatch(home, away, 0)
    for i in range(5):
        home.player_array[i].stats_tot_msm += matches_h[i]
    matches_a = detect_mismatch(away, home, 0)
    for i in range(5):
        away.player_array[i].stats_tot_msm += matches_a[i]
    
    while playing: #40min games
        if poss_home:
            hscore += run_play(home, away, matches_h, prplay)
            poss_away = 1
            poss_home = 0
            gametime += 5 + 19 * random.random()
        elif poss_away:
            ascore += run_play(away, home, matches_a, prplay)
            poss_away = 0
            poss_home = 1
            gametime += 5 + 19 * random.random()
        if gametime > max_gametime:
            gametime = max_gametime
            if hscore != ascore:
                playing = False
            else:
                if prplay==1: print("\n*** OVERTIME! ***\n")
                poss_home, poss_away = tip_off(home, away, prplay)
                max_gametime += 300
        if prplay==1: print("Gametime: ", int(gametime), " | ", home.name, ":", hscore, " ", away.name, ":", ascore,"\n")
    
    #print boxscore if desired
    if prbox==1:
        print("HOME ", home.name, ": ", hscore)
        home.print_box()
        print("\n")
        print("AWAY ", away.name, ": ", ascore)
        away.print_box()
    
    #do some stats management, like adding player stuff to their career totals
    home.game_reset_tstats()
    away.game_reset_tstats()
    
    #return winner
    if hscore > ascore:
        return home
    else: return away

def pot_steal(poss, stlr): #see if the pass is stolen, return 1 if it is
    if random.random() < 0.1: #only 10% of passes are "stealable"
        chance = random.random() * (stlr.steal ** 0.25)
        if chance > 1.95 or random.random() < 0.1:
            #stolen!
            return 1
        else: return 0
    else: return 0

def run_play(offense, defense, matches, prplay): #take it possession at time yo

    off_tot_outd = offense.pointg.out_d + offense.shootg.out_d + offense.smallf.out_d + offense.powerf.out_d + offense.center.out_d
    def_tot_outd = defense.pointg.out_d + defense.shootg.out_d + defense.smallf.out_d + defense.powerf.out_d + defense.center.out_d

    fastbreak_possibility = off_tot_outd - def_tot_outd

    if prplay==1: print(offense.name, "have the ball.")
    passes = 0
    off_poss = 1
    who_poss = get_ball_carrier(offense)
    if who_poss == offense.pointg:
        who_def  = defense.pointg
    if who_poss == offense.shootg:
        who_def  = defense.shootg
    if who_poss == offense.smallf:
        who_def  = defense.smallf
    if who_poss == offense.powerf:
        who_def  = defense.powerf
    if who_poss == offense.center:
        who_def  = defense.center
    assister = who_poss
    while off_poss == 1:
        #mismatch = calc_mismatch(who_poss, who_def, 0)
        if ((random.randint(0,6) + passes < 5) or (passes==0 and random.random()<0.97)): # or (who_poss.passing*3 - who_poss.out_s - who_poss.mid_s - who_poss.int_s > 80 and random.random() < 0.9)
            #pass
            passes+=1
            ifsteal = pot_steal(who_poss, who_def)
            if ifsteal == 1:
                #stolen
                if prplay==1: print(who_def.name, "has stolen the ball!")
                who_def.stats_stl += 1
                return 0
            assister = who_poss
            who_poss = intelligent_pass(who_poss, offense, defense, matches)
            if who_poss == offense.pointg:
                who_def  = defense.pointg
            if who_poss == offense.shootg:
                who_def  = defense.shootg
            if who_poss == offense.smallf:
                who_def  = defense.smallf
            if who_poss == offense.powerf:
                who_def  = defense.powerf
            if who_poss == offense.center:
                who_def  = defense.center
        elif ( fastbreak_possibility * random.random() > 60 ):
            #fastbreak to punish big lineups
            points = 2
            who_poss.stats_pts += 2
            who_poss.stats_fga += 1
            who_poss.stats_fgm += 1
            who_def.stats_ofa +=1
            who_def.stats_ofm +=1
            if assister == who_poss:
                if prplay==1: print(who_poss.name, "made a 2pt fastbreak dunk!")
                return points
            else:
                if ((assister.passing/14)**2.4)*random.random() > 20: assister.stats_ass += 1
                if prplay==1: print(who_poss.name, "made a 2pt fastbreak lay-up with an assist from", assister.name)
                return points
        else:
            #shoot
            points = take_shot(who_poss, who_def, defense, assister, prplay)
            if points > 0:
                #made it!
                if assister == who_poss:
                    if prplay==1: print(who_poss.name, "made a", points, "pt shot")
                    return points
                else:
                    if ((assister.passing/14)**2.4)*random.random() > 20: assister.stats_ass += 1
                    if prplay==1: print(who_poss.name, "made a", points, "pt shot with an assist from", assister.name)
                    return points
            else:
                #rebounding, defenders have 3:1 advantage
                #weighted rebounding advantage calculator, maybe add height adv too l8r
                reb_advs = [(defense.center.rebounding - offense.center.rebounding) , (defense.powerf.rebounding - offense.powerf.rebounding) , (defense.smallf.rebounding - offense.smallf.rebounding)*0.8 , (defense.shootg.rebounding - offense.shootg.rebounding)*0.7 + (defense.pointg.rebounding - offense.pointg.rebounding)*0.5]
                #reb_adv = (defense.center.rebounding - offense.center.rebounding) + (defense.powerf.rebounding - offense.powerf.rebounding)+ (defense.smallf.rebounding - offense.smallf.rebounding)*0.8 + (defense.shootg.rebounding - offense.shootg.rebounding)*0.7 + (defense.pointg.rebounding - offense.pointg.rebounding)*0.5
                reb_adv = reb_advs[ random.randint(0,3) ] + reb_advs[ random.randint(0,3) ]
                reb_adv *= 0.175
                if (random.random()*100 + reb_adv) > 25: #defensive reb
                    rebounder = find_rebounder(defense)
                    if prplay==1: print(rebounder.name,"grabs the defensive rebound!")
                    return 0
                else: #offensive reb
                    rebounder = find_rebounder(offense)
                    if prplay==1: print(rebounder.name,"snatches the offensive rebound!")
                    who_poss = rebounder
                    passes = 2

def take_shot(shooter, defender, defense, assister, prplay): #return points of shot, 0 if miss
    
    #give assist bonus for having a good passer pass to you
    ass_bonus = 0
    if assister != shooter:
        ass_bonus = (assister.passing - 75) / 5
    
    """#select shot, use tendencies
    out_ten = 0
    mid_ten = 0
    int_ten = 0
    if shooter.out_s>50: out_ten = (shooter.out_s / defender.out_d) * shooter.out_s**1.2
    #if shooter.out_s + 20 < shooter.mid_s or shooter.out_s + 20 < shooter.int_s: out_ten -= 200 #see if one stat is sig worse than other two so he never takes that shot
    out_ten += 3*(shooter.out_s - 75)
    
    if shooter.mid_s>50: mid_ten = (shooter.mid_s / (defender.out_d*0.5 + 0.5*defender.int_d)) * shooter.mid_s**1.2
    #if shooter.mid_s + 20 < shooter.out_s or shooter.mid_s + 20 < shooter.int_s: mid_ten -= 200
    mid_ten += 3*(shooter.mid_s - 75)
    
    if shooter.int_s>50: int_ten = (shooter.int_s / defender.int_d) * shooter.int_s**1.2
    #if shooter.int_s + 20 < shooter.out_s or shooter.int_s + 20 < shooter.mid_s: int_ten -= 200
    int_ten += 3*(shooter.int_s - 75)
    
    if out_ten<0: out_ten=0
    if mid_ten<0: mid_ten=0
    if int_ten<0: int_ten=0

    tot_ten = out_ten + mid_ten + int_ten
    sel_shot = random.randint(0, int(tot_ten))"""

    sel_shot = random.random()

    intel_out_t = shooter.out_t
    intel_mid_t = shooter.mid_t
    mism_mid = shooter.mid_s - (defender.out_d*0.5 + 0.5*defender.int_d)
    if mism_mid > 30:
        intel_mid_t += mism_mid/7
    mism_out = shooter.out_s - defender.out_d
    if mism_out > 30 and defender.out_d <= 70:
        intel_out_t += mism_out/7
    
    if sel_shot < intel_out_t and intel_out_t>=0 and shooter.out_s>40: #3point shot selected
        chance = 22 + (shooter.out_s)/3 + ass_bonus - (defender.out_d)/5 #70 norm multy
        if chance > random.random()*100: #chance > 60:
            #made it!
            shooter.stats_pts += 3
            shooter.stats_fga += 1
            shooter.stats_fgm += 1
            shooter.stats_3ga += 1
            shooter.stats_3gm += 1
            defender.stats_ofa +=1
            defender.stats_ofm +=1
            return 3
        else:
            if prplay==1: print(shooter.name, "misses from downtown!")
            shooter.stats_fga += 1
            shooter.stats_3ga += 1
            defender.stats_ofa +=1
            return 0
    
    elif sel_shot < intel_mid_t and intel_mid_t>=0: #midrange jumper selected
        def_mid_d = defender.out_d*0.5 + 0.5*defender.int_d
        chance = 30 + (shooter.mid_s)/3 + ass_bonus - (def_mid_d)/5 #80 norm multy
        if chance > random.random()*100:
            #made it!
            shooter.stats_pts += 2
            shooter.stats_fga += 1
            shooter.stats_fgm += 1
            defender.stats_ofa +=1
            defender.stats_ofm +=1
            return 2
        else:
            if prplay==1: print(shooter.name, "bricks the midrange jumper!")        
            shooter.stats_fga += 1
            defender.stats_ofa +=1
            return 0
    
    else: #inside layup/dunk/etc

        #block?
        if random.random() * (defender.block ** 0.25) > 2.75 or random.random() < 0.02:
            #NOT IN MY HOUSE MOFO
            if prplay==1: print(defender.name,"has blocked",shooter.name,"!")
            shooter.stats_fga += 1
            defender.stats_blk += 1
            defender.stats_ofa +=1
            return 0

        chance = 35 + (shooter.int_s)/3 + ass_bonus - (defender.int_d/2 + defense.powerf.int_d/4 + defense.center.int_d/4)/5
        if chance > random.random()*100:
            #made it!
            if random.random() < 0.3:
                if prplay==1: print(shooter.name, "slams it down over", defender.name, "!")
            else:
                if prplay==1: print(shooter.name, "lays it in!")
            shooter.stats_pts += 2
            shooter.stats_fga += 1
            shooter.stats_fgm += 1
            defender.stats_ofa += 1
            defender.stats_ofm += 1
            return 2
        else:
            if prplay==1: print(shooter.name, "can't connect on the inside shot!") 
            shooter.stats_fga += 1
            defender.stats_ofa +=1
            return 0

def tip_off(home, away, prplay):
    poss = random.random()
    if poss > 0.5:
        poss_home = True
        poss_away = False
        if prplay==1: print(home.name, "wins the tip-off!")
    else:
        poss_away = True
        poss_home = False
        if prplay==1: print(away.name, "wins the tip-off!")
    return poss_home, poss_away
