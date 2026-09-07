import json, urllib.request, datetime, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
SEASON=2026
ROSTER=json.loads((ROOT/'data/rosters.json').read_text())
ALIASES={'Sam Houston State':'Sam Houston','Louisiana-Monroe':'ULM','Florida International':'FIU','Miami (FL)':'Miami'}
def api(url):
    req=urllib.request.Request(url,headers={'User-Agent':'WinnersLosersDashboard/1.0'})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def norm(s):return ALIASES.get(s,s)
def add_game(games,sport,event):
    comp=(event.get('competitions') or [{}])[0]; st=event.get('status',{}); typ=st.get('type',{}); state=typ.get('state','')
    teams=comp.get('competitors',[])
    if len(teams)!=2:return
    a=next((x for x in teams if x.get('homeAway')=='away'),teams[0]); h=next((x for x in teams if x.get('homeAway')=='home'),teams[1])
    games.append({'id':event.get('id'),'sport':sport,'away':norm(a.get('team',{}).get('displayName','')),'home':norm(h.get('team',{}).get('displayName','')),'awayScore':int(a.get('score') or 0),'homeScore':int(h.get('score') or 0),'state':state,'statusText':typ.get('shortDetail',''),'date':event.get('date'),'completed':state=='post','inProgress':state=='in'})
def fetch_nfl():
    games=[]
    for week in range(1,19):
        for typ in (2,3):
            u=f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={SEASON}&seasontype={typ}&week={week}'
            try:
                for e in api(u).get('events',[]):add_game(games,'NFL',e)
            except Exception:pass
    return games
def fetch_cfb():
    games=[]
    d=datetime.date(SEASON,8,20); end=datetime.date(SEASON+1,1,20)
    while d<=end:
        u=f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={d:%Y%m%d}&limit=200'
        try:
            for e in api(u).get('events',[]):add_game(games,'CFB',e)
        except Exception:pass
        d+=datetime.timedelta(days=1)
    return games
def main():
    games=fetch_nfl()+fetch_cfb(); uniq={g['id']:g for g in games if g.get('id')}; games=list(uniq.values())
    records={}
    for g in games:
        for team in (g['away'],g['home']):records.setdefault(f'{g["sport"]}|{team}',{'wins':0,'losses':0,'ties':0})
        if not g['completed']:continue
        ak=f'{g["sport"]}|{g["away"]}'; hk=f'{g["sport"]}|{g["home"]}'
        if g['awayScore']>g['homeScore']:records[ak]['wins']+=1;records[hk]['losses']+=1
        elif g['homeScore']>g['awayScore']:records[hk]['wins']+=1;records[ak]['losses']+=1
        else:records[ak]['ties']+=1;records[hk]['ties']+=1
    out={'season':SEASON,'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'team_records':records,'games':games,'projections':{}}
    (ROOT/'data/standings.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()