
text = '''
Quest Hunter

Blood Death Knight

Frost Death Knight

Unholy Death Knight

Thief Rogue

Ramp Druid

Big Spell Mage

Evolve Shaman

Imp Warlock

Aggro Druid

Beast Hunter

Pure Paladin

Quest Priest
Deathrattle Rogue
Mirror matchup
TwitchTwitch VODs available!
Deathrattle Rogue
Versus:	Quest Hunter
Winrate:	48.55%
Games:	138
Twitch VODs available!
48.55%
Deathrattle Rogue
Versus:	Blood Death Knight
Winrate:	63.60%
Games:	4,781
Twitch VODs available!
63.60%
Deathrattle Rogue
Versus:	Frost Death Knight
Winrate:	39.74%
Games:	2,828
Twitch VODs available!
39.74%
Deathrattle Rogue
Versus:	Unholy Death Knight
Winrate:	54.53%
Games:	2,492
Twitch VODs available!
54.53%
Deathrattle Rogue
Versus:	Thief Rogue
Winrate:	49.05%
Games:	2,381
Twitch VODs available!
49.05%
Quest Hunter
Versus:	Deathrattle Rogue
Winrate:	51.44%
Games:	138
Twitch VODs available!
51.44%
Quest Hunter
Mirror matchup
Quest Hunter
Versus:	Blood Death Knight
Winrate:	49.76%
Games:	418
Twitch VODs available!
49.76%
Quest Hunter
Versus:	Frost Death Knight
Winrate:	50.00%
Games:	316
Twitch VODs available!
50.00%
Quest Hunter
Versus:	Unholy Death Knight
Winrate:	47.18%
Games:	320
Twitch VODs available!
47.18%
Quest Hunter
Versus:	Thief Rogue
Winrate:	51.75%
Games:	228
Twitch VODs available!
51.75%
Blood Death Knight
Versus:	Deathrattle Rogue
Winrate:	36.39%
Games:	4,781
Twitch VODs available!
36.39%
Blood Death Knight
Versus:	Quest Hunter
Winrate:	50.23%
Games:	418
Twitch VODs available!
50.23%
Blood Death Knight
Mirror matchup
TwitchTwitch VODs available!
Blood Death Knight
Versus:	Frost Death Knight
Winrate:	51.45%
Games:	11,138
Twitch VODs available!
51.45%
Blood Death Knight
Versus:	Unholy Death Knight
Winrate:	55.63%
Games:	9,777
Twitch VODs available!
55.63%
Big Shaman
Versus: Unholy Death Knight
Winrate:\t57.54%

'''

textLines = text.splitlines()

def matchups(textLines):
    decks = []
    #create list of decks
    for lineNum in range(len(textLines)):
        if 'Versus' in textLines[lineNum]:
            newClass = textLines[lineNum - 1]
            if newClass not in decks:
                decks += [newClass]
            newClass = textLines[lineNum].replace('Versus:\t', '')
            if newClass not in decks:
                decks += [newClass]

    #initialize spreadsheet
    #notably, it starts w 50s, so if no data is inputted for a matchup 50 is default
    size = len(decks)
    sheet = []
    for i in range(size):
        row = [50]*size
        sheet += [row]

    for lineNum in range(len(textLines)):
        if 'Versus' in textLines[lineNum]:
            leftClass = textLines[lineNum - 1]
            topClass = textLines[lineNum].replace('Versus:\t', '')
            winrate = (textLines[lineNum + 1].replace('Winrate:\t', '')).replace('%', '')
            row = decks.index(leftClass)
            col = decks.index(topClass)
            sheet[row][col] = float(winrate)
            sheet[col][row] = 100 - float(winrate)
    return decks, sheet

#returns wr of deck1 into deck2
def oddsFinder(sheet, decks, deck1, deck2):
    row = decks.index(deck1)
    col = decks.index(deck2)
    return (sheet[row][col])/100


def matchOdds(sheet, decks, decks1, decks2):
    if set(decks1) == set(decks2):
         return .5

    if len(decks1) == 1 and len(decks2) == 1:
        return oddsFinder(sheet, decks, decks1[0], decks2[0])
#assume that both players are selecting optimal decks based on opponent selecting this round randomly
#while this isn't necessarily the case, the game theory aspects cannot be perfectly modeled here
#also note, this only works for 3v3 conquest, no bans (bans are accounted for later in code though)
    elif len(decks1) == 1 and len(decks2) == 2:
        return 1 - (1-oddsFinder(sheet, decks, decks1[0], decks2[0]))* (1- oddsFinder(sheet, decks, decks1[0], decks2[1]))
    elif len(decks1) == 2 and len(decks2) == 1:
        return (oddsFinder(sheet, decks, decks1[0], decks2[0]) * oddsFinder(sheet, decks, decks1[1], decks2[0]))
    elif len(decks1) == 2 and len(decks2) == 2:
        choose = [[0,0], [0,0]]
        for i in range(2):
            for j in range(2):
                decks1copy = decks1.copy()
                decks1copy.remove(decks1[i])
                decks2copy = decks2.copy()
                decks2copy.remove(decks2[j])
                choose[i][j] = (matchOdds(sheet, decks, decks1copy, decks2)* oddsFinder(sheet, decks, decks1[i], decks2[j])
                + matchOdds(sheet, decks, decks1, decks2copy)* (1-oddsFinder(sheet, decks, decks1[i], decks2[j])))
        if abs(choose[0][0] - choose[1][1]) < 0.00001 or abs(choose[1][0] - choose [0][1]) < 0.00001:
            return (choose[0][0] + choose[0][1])/2
        if choose[0][0] + choose[0][1] > choose[1][1] + choose[1][0]:
            p1 = 0
        else: p1 = 1
        if choose[0][0] + choose[1][0] < choose[1][1] + choose[0][1]:
            p2 = 0
        else: p2 = 1
        return choose[p1][p2]
    elif len(decks1) == 3 and len(decks2) == 2:
        choose = [[0,0],[0,0], [0,0]]
        for i in range(3):
            for j in range(2):
                decks1copy = decks1.copy()
                decks1copy.remove(decks1[i])
                decks2copy = decks2.copy()
                decks2copy.remove(decks2[j])
                
                odds1 = matchOdds(sheet, decks, decks1copy, decks2)
                odds2 = matchOdds(sheet, decks, decks1, decks2copy)
                choose[i][j] = ((odds1 * oddsFinder(sheet, decks, decks1[i], decks2[j]))
                + (odds2* (1-oddsFinder(sheet, decks, decks1[i], decks2[j]))))

        p1 = [0,0,0]
        for i in range(len(p1)):
            p1[i] = choose[i][0] + choose[i][1]
        
        p1choice = 0
        for i in range(len(p1)):
            if p1[i] > p1[p1choice]:
                p1choice = i
        

        if choose[0][0] + choose[1][0] + choose[2][0] < choose[1][1] + choose[0][1] + choose[2][1]:
            p2 = 0
        else: p2 = 1
        return choose[p1choice][p2]

    elif len(decks1) == 2 and len(decks2) == 3:
        choose = [[0,0, 0],[0,0,0]]
        for i in range(2):
            for j in range(3):
                decks1copy = decks1.copy()
                decks1copy.remove(decks1[i])
                decks2copy = decks2.copy()
                decks2copy.remove(decks2[j])
                choose[i][j] = (matchOdds(sheet, decks, decks1copy, decks2)* oddsFinder(sheet, decks, decks1[i], decks2[j])
                + matchOdds(sheet, decks, decks1, decks2copy)* (1-oddsFinder(sheet, decks, decks1[i], decks2[j])))
        if choose[0][0] + choose[0][1]  + choose[0][2]> choose[1][1] + choose[1][0] + choose[1][2]:
            p1 = 0
        else: p1 = 1
        
        p2 = [0,0,0]
        for i in range(len(p2)):
            p2[i] = choose[0][i] + choose[1][i]
        
        p2choice = 0
        for i in range(len(p2)):
            if p2[i] < p2[p2choice]:
                p2choice = i
        return choose[p1][p2choice]

    elif len(decks1) == 3 and len(decks2) == 3:
        choose = [[0,0,0],[0,0,0], [0,0,0]]
        for i in range(3):
            for j in range(3):
                decks1copy = decks1.copy()
                decks1copy.remove(decks1[i])
                decks2copy = decks2.copy()
                decks2copy.remove(decks2[j])
                choose[i][j] = (matchOdds(sheet, decks, decks1copy, decks2)* oddsFinder(sheet, decks, decks1[i], decks2[j])
                + matchOdds(sheet, decks, decks1, decks2copy)* (1-oddsFinder(sheet, decks, decks1[i], decks2[j])))

        p1 = [0,0,0]
        for i in range(len(p1)):
            p1[i] = choose[i][0] + choose[i][1] + choose[i][2]
        
        p1choice = 0
        for i in range(len(p1)):
            if p1[i] > p1[p1choice]:
                p1choice = i

        p2 = [0,0,0]
        for i in range(len(p2)):
            p2[i] = choose[0][i] + choose[1][i] + choose[2][i]
        
        p2choice = 0
        for i in range(len(p2)):
            if p2[i] < p2[p2choice]:
                p2choice = i
        return choose[p1choice][p2choice]
    elif len(decks1) == 1 and len(decks2) == 3:
        odds1 = (1-oddsFinder(sheet, decks, decks1[0], decks2[0])) 
        odds2 = (1-oddsFinder(sheet, decks, decks1[0], decks2[1])) 
        odds3 = (1- oddsFinder(sheet, decks, decks1[0], decks2[2])) 
        return 1 - (odds1*odds2*odds3)
    elif len(decks1) == 3 and len(decks2) == 1:
        return (oddsFinder(sheet, decks, decks1[0], decks2[0]) * oddsFinder(sheet, decks, decks1[1], decks2[0]) * 
        oddsFinder(sheet, decks, decks1[2], decks2[0]))


#both players ban assuming other bans randomly
def banFind(sheet, decks, decks1, decks2):
    choices = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for ban1 in range(4):
        for ban2 in range(4):
            p1copy = decks1.copy()
            p1copy.remove(decks1[ban1])
            p2copy = decks2.copy()
            p2copy.remove(decks2[ban2])
            choices[ban1][ban2] = matchOdds(sheet, decks, p1copy, p2copy)
     
    p1max = 0
    p2max = 500
    p1best = 0
    p2best = 0
    for i in range(4):
        sum = 0
        for j in range(4):
            sum += choices[i][j]
        if sum < p2max:
            p2max = sum
            p2best = i

    for i in range(4):
        sum = 0
        for j in range(4):
            sum += choices[j][i]
        if sum > p1max:
            p1max = sum
            p1best = i
    
    return choices[p2best][p1best], decks1[p2best], decks2[p1best]


def validList(lineup, decks):
    classList = ['Death Knight', 'Demon Hunter', 'Druid', 'Mage', 'Paladin', 'Priest', 'Warlock', 'Warrior', 'Rogue',
        'Hunter', 'Shaman']
    if len(lineup) != 4:
        return False
    for name in classList:

        count = 0
        for deck in lineup:
        
            if deck not in decks:
                return False
            if name in deck:
                count += 1
                if name == 'Hunter' and 'Demon Hunter' in deck:
                    count -= 1
        if count > 1:
            return False
    return True

   



def matchSolver(decks, sheet, opp):
    bestWR = 0
    bestBan = ''
    bestOppBan = ''
    bestList = []
    for deck1 in decks:
        for deck2 in decks:
            for deck3 in decks:
                for deck4 in decks:
                    player = [deck1, deck2, deck3, deck4]
                    if validList(player, decks):
                        #player ban is which of players decks are banned
                        wr, playerBan, opponentBan = banFind(sheet, decks, player, opp)
                        if wr > bestWR:
                            bestWR = wr
                            bestBan = opponentBan
                            bestOppBan = playerBan
                            bestList = player
        #returns best list, winrate if ideal bans, ideal ban for player to submit, ideal ban for opponent to choose
    return bestList, bestWR, bestBan, bestOppBan





decks, matchupSheet = matchups(textLines)
print(matchSolver(decks, matchupSheet, ['Deathrattle Rogue', 'Quest Hunter', 'Blood Death Knight', 'Frost Death Knight']))
