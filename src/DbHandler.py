import sqlite3
from resources import *


def json_to_db(obj):
    print('inserting record into database')
    teams = obj['teams']
    hunters = obj['hunters']
    entries = obj['entries']
    game = obj['game']

    conn = sqlite3.connect(database)
    for teamnum in teams:
        insert_row(conn, "teams", teams[teamnum])
    for hunternum in hunters:
        insert_row(conn, "hunters", hunters[hunternum])
    for entrynum in entries:
        insert_row(conn, "entries", entries[entrynum])
    insert_row(conn, "games", game)
    conn.close()

def insert_row(conn, table, row):
    cursor = conn.cursor()
    cols = [i for i in row.keys()]
    vals = [row[i] for i in cols]
    query = "insert or ignore into %s (%s) values (%s) " % (table, ','.join(cols), (','.join(['?']*len(cols))))
    try:
        cursor.execute(query, (vals))
        conn.commit()
    except Exception as e:
        print('insert_row')
        print(e)


def tables_exist():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "select name from sqlite_master where type = 'table' and name = ? or name = ? or name = ? or name = ?"
    tables = ('games','hunters','entries','teams',)

    try:
        cursor.execute(query,tables)
        nTables = len(cursor.fetchall())
        conn.close()
        return nTables == len(tables)
    except Exception as e:
        print('tables_exist err')
        print(e)
        conn.close()
        return False

def create_tables():
    print('creating tables')
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.executescript(open(resource_path('assets/schema.sql'),'r').read())
    conn.close()



def execute_query(query):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print('execute_query')
        print('requested query: %s' % query)
        print(e)
        return []

def GetTotalHuntCount():
    n = execute_query("select count(*) from 'games'")
    if n == None or len(n) == 0:
        return -1 
    return n[0][0]

def GetCurrentMmr(name = settings.value("steam_name")):
    mmr = execute_query("select mmr from 'hunters' where blood_line_name is '%s' order by timestamp desc" % name)
    if len(mmr) == 0:
        return -1
    mmr = mmr[0][0]
    if mmr == None:
        return -1
    return mmr

def GetBestMmr(name = settings.value("steam_name")):
    mmr = execute_query("select max(mmr) from 'hunters' where blood_line_name is '%s'" % name)
    if len(mmr) == 0:
        return -1
    mmr = mmr[0][0]
    if mmr == None:
        return -1
    return mmr

def GetTopKiller():
    vals = execute_query("select downedme+killedme as kills, blood_line_name, mmr from 'hunters' order by kills desc limit 1")
    cols = ['kills','name','mmr']
    if len(vals) > 0:
        res = { cols[i] : vals[0][i] for i in range(len(cols))}
        return res
    return {}

def GetTopKilled():
    vals = execute_query("select downedbyme+killedbyme as kills, blood_line_name, mmr from 'hunters' order by kills desc limit 1")
    cols = ['kills','name','mmr']
    if len(vals) > 0:
        res = { cols[i] : vals[0][i] for i in range(len(cols))}
        return res
    return {}


def GetTopNHunters(n):
    cols = ['frequency','name', 'profileid', 'mmr','killedme','killedbyme']
    vals = execute_query("select count(profileid) as frequency, blood_line_name, profileid, mmr, killedme+downedme as killedme, killedbyme+downedbyme as killedbyme from 'hunters' where blood_line_name is not '%s' group by profileid order by frequency desc limit %d" % (settings.value("steam_name"), n))
    results = []
    if len(vals) > 0:
        for v in vals:
            results.append(
                { cols[i] : v[i] for i in range(len(cols)) }
            )
    return results

def GetHunts():
    vals = execute_query("select * from 'games' order by timestamp desc")
    cols = execute_query("pragma table_info('games')")
    try:
        return [ { cols[i][1] : hunt[i] for i in range(len(cols)) } for hunt in vals]
    except Exception as e:
        print('dbhandler.gethunts')
        print(e)
        return []

def GetHunt(ts):
    vals = execute_query("select * from 'games' where timestamp is %d" % ts)
    cols = execute_query("pragma table_info('games')")
    try:
        vals = vals[0]
        return { cols[i][1] : vals[i] for i in range(len(cols)) }
    except Exception as e:
        print('dbhandler.gethunt')
        print(e)
        return {}

def GetLastHuntTimestamp():
    ts = execute_query("select timestamp from 'games' order by timestamp desc limit 1")
    if ts == None or len(ts) < 1:
        return -1
    return ts[0][0]

def GetHuntEntries(ts):
    vals = execute_query("select * from 'entries' where timestamp is %s" % ts) 
    cols = execute_query("pragma table_info('entries')")
    try:
        return [ { cols[i][1] : entry[i] for i in range(len(cols)) } for entry in vals]

    except Exception as e:
        print('dbhandler.getentries')
        print(e)
        return {}

def GetTeams(timestamp):
    tVals = execute_query("select * from 'teams' where timestamp is %s" % timestamp)
    tCols = execute_query("pragma table_info('teams')")
    teams = []
    try:
        for team in tVals:
            teams.append({tCols[i][1] : team[i] for i in range(len(tCols))})
        return teams

    except Exception as e:
        print("dbhandler.getteams")
        print(e)
        return teams

def GetHunters(timestamp):
    hVals = execute_query("select * from 'hunters' where timestamp is %s" % timestamp)
    hCols = execute_query("pragma table_info('hunters')")
    hunters = []
    try:
        for hunter in hVals:
            hunters.append({hCols[i][1] : hunter[i] for i in range(len(hCols))})
        return hunters
    except Exception as e:
        print('dbhandler.gethunters')
        print(e)
        return []

def GetAllMmrs(name = settings.value('steam_name')):
    vals = execute_query("select 'hunters'.timestamp, 'hunters'.mmr, 'games'.MissionBagIsQuickPlay as qp from 'hunters' join 'games' on 'hunters'.timestamp = 'games'.timestamp where blood_line_name is '%s' order by 'hunters'.timestamp asc" % name)
    res = {}
    for v in vals:
        res[v[0]] = {
            'mmr': v[1],
            'qp': v[2]
        }
    return res

def GetGameTypes():
    cols = ['timestamp', 'MissionBagIsQuickplay']
    vals = execute_query("select %s from 'games' order by timestamp asc" % ','.join(cols))
    res = {}
    for v in vals:
        res[v[0]] = v[1]
    return res