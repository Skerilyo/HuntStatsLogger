from PyQt6.QtGui import QColor, QPen
from DbHandler import *
from resources import *
from MainWindow.Chart.Bars import Bars

class WinLoss():
    def __init__(self) -> None:
        self.brushes = [
            QColor("#c800ff00"),
            QColor("#c8ff0000")
        ]
        self.pen = None#QPen(QColor("#000000"))
        self.update()

    def update(self):
        self.data = self.GetData()

        self.bountyBars = Bars(
            x0 = [10,10],
            x1 = [20,20],
            height=[
                self.data['winRate']['bounty']['winPrc'],
                self.data['winRate']['bounty']['lossPrc']
            ],
            y0 = [0,self.data['winRate']['bounty']['winPrc']],
            brushes=self.brushes,
            pens=[self.pen]*2
        )

        self.quickplayBars = Bars(
            x0 = [30,30],
            x1 = [40,40],
            height=[
                self.data['winRate']['qp']['winPrc'],
                self.data['winRate']['qp']['lossPrc']
            ],
            y0 = [0,self.data['winRate']['qp']['winPrc']],
            brushes=self.brushes,
            pens=[self.pen]*2
        )

        self.survivalBars = Bars(
            x0 = [50,50],
            x1 = [60,60],
            height=[
                self.data['survivalRate']['winPrc'],
                self.data['survivalRate']['lossPrc']
            ],
            y0 = [0,self.data['survivalRate']['winPrc']],
            brushes=self.brushes,
            pens=[self.pen]*2
        )

        self.labels = [[
            (15,"Bounty Hunt\n(extract at least 1 token)"),
            (35,"Quick Play\n(soul survivor)"),
            (55, "Survived\n(Bounty)")
        ]]


    def GetData(self):
        wins = self.GetWins()
        survival = self.GetSurvival()
        return {
            "winRate": wins,
            "survivalRate":survival
        }

    def GetWins(self):
        data = {
            'bounty' : {},
            'quickplay' : {}
        }
        vals = execute_query("select 'games'.timestamp, 'accolades'.category, 'games'.MissionBagIsQuickPlay as isQp from 'accolades' join 'games' on 'accolades'.timestamp = 'games'.timestamp")
        cols = ['timestamp', 'category', 'qp']
        try:
            accolades = [ {cols[i] : acc[i] for i in range(len(cols))} for acc in vals]
        except:
            accolades = []

        for accolade in accolades:
            ts = accolade['timestamp']
            if accolade['qp'] == 'true':
                if ts not in data['quickplay']:
                    data['quickplay'][ts] = 0
                if 'extract' in accolade['category']:
                    data['quickplay'][ts] = 1
            else:
                if ts not in data['bounty']:
                    data['bounty'][ts] = 0
                if 'extract' in accolade['category']:
                    data['bounty'][ts] = 1
        
        bountyWins = sum(data['bounty'].values())
        qpWins = sum(data['quickplay'].values())
        totalBounty = execute_query("select count(*) from 'games' where MissionBagIsQuickPlay = 'false'")
        totalBounty = 0 if len(totalBounty) == 0 else totalBounty[0][0]
        totalQp = execute_query("select count(*) from 'games' where MissionBagIsQuickPlay = 'true'")
        totalQp = 0 if len(totalQp) == 0 else totalQp[0][0]

        wins = {
            'bounty': {
                'wins':bountyWins,
                'losses':totalBounty - bountyWins,
                'winPrc':float(bountyWins/totalBounty)*100,
                'lossPrc':(1.0-float(bountyWins/totalBounty))*100,
                'total': totalBounty
            },
            'qp': {
                'wins':qpWins,
                'losses':totalQp - qpWins,
                'winPrc':float(qpWins/totalQp)*100,
                'lossPrc':(1.0-float(qpWins/totalQp))*100,
                'total':totalQp
            }
        }
        return wins

    def GetSurvival(self):
        survived = execute_query("select count(*) from 'games' where MissionBagIsHunterDead = 'false' and MissionBagIsQuickPlay = 'false'")
        survived = 0 if len(survived) == 0 else survived[0][0]
        total = execute_query("select count(*) from 'games' where MissionBagIsQuickPlay = 'false'")
        total = 0 if len(total) == 0 else total[0][0]
        return {
            'survived':survived,
            'died':total - survived,
            'winPrc':float(survived/total)*100,
            'lossPrc':(1.0-float(survived/total))*100,
            'total':total
        }
