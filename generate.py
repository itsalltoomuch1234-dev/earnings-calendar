import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta, date
import time, warnings, json
from zoneinfo import ZoneInfo
warnings.filterwarnings('ignore')

COMPANY_NAMES = {
    "UAA":"Under Armour","AEO":"American Eagle Outfitters",
    "ANF":"Abercrombie & Fitch","VFC":"VF Corporation","GAP":"Gap Inc.",
    "BIRK":"Birkenstock","LEVI":"Levi Strauss & Co.","ONON":"On Holding",
    "LULU":"Lululemon Athletica","DECK":"Deckers Outdoor","NKE":"Nike",
    "DLTR":"Dollar Tree","DG":"Dollar General","ROST":"Ross Stores",
    "TJX":"TJX Companies","GOOS":"Canada Goose","COTY":"Coty Inc.",
    "CPRI":"Capri Holdings","ELF":"e.l.f. Beauty","ULTA":"Ulta Beauty",
    "RL":"Ralph Lauren","TPR":"Tapestry","EL":"Estée Lauder",
    "KSS":"Kohl's","BBWI":"Bath & Body Works","M":"Macy's",
    "ACI":"Albertsons","BBY":"Best Buy","KR":"Kroger","TGT":"Target",
    "LOW":"Lowe's","HD":"Home Depot","COST":"Costco","WMT":"Walmart",
    "NCLH":"Norwegian Cruise Line","RCL":"Royal Caribbean",
    "CCL":"Carnival Corporation","TAP":"Molson Coors",
    "BF-B":"Brown-Forman","STZ":"Constellation Brands",
    "KDP":"Keurig Dr Pepper","PEP":"PepsiCo","KO":"Coca-Cola",
    "BYND":"Beyond Meat","LW":"Lamb Weston","CAG":"Conagra Brands",
    "CPB":"Campbell Soup","SJM":"J.M. Smucker",
    "MKC":"McCormick & Company","HRL":"Hormel Foods",
    "GIS":"General Mills","IFF":"Intl Flavors & Fragrances",
    "KHC":"Kraft Heinz","HSY":"Hershey","MDLZ":"Mondelez International",
    "NWL":"Newell Brands","CLX":"Clorox","CHD":"Church & Dwight",
    "KMB":"Kimberly-Clark","CL":"Colgate-Palmolive",
    "PG":"Procter & Gamble","MO":"Altria Group",
    "PM":"Philip Morris International","MAT":"Mattel","HAS":"Hasbro",
    "DPZ":"Domino's Pizza","DRI":"Darden Restaurants",
    "QSR":"Restaurant Brands Intl","CMG":"Chipotle Mexican Grill",
    "YUM":"Yum! Brands","SBUX":"Starbucks","MCD":"McDonald's",
    "SFD":"Smithfield Foods","TSN":"Tyson Foods","SYY":"Sysco",
    "CART":"Instacart","DASH":"DoorDash",
    "FRT":"Federal Realty","REG":"Regency Centers",
    "KIM":"Kimco Realty","SPG":"Simon Property Group",
    "MAS":"Masco Corporation","BALL":"Ball Corporation",
    "TSCO":"Tractor Supply","AMCR":"Amcor",
    "ROL":"Rollins","CTAS":"Cintas Corporation","IP":"International Paper",
}

IR_URLS = {
    "UAA":"https://about.underarmour.com/en-us/investors",
    "AEO":"https://investors.ae.com",
    "ANF":"https://corporate.abercrombie.com/investors",
    "VFC":"https://investors.vfc.com",
    "GAP":"https://investors.gapinc.com",
    "BIRK":"https://ir.birkenstock.com",
    "LEVI":"https://investors.levistrauss.com",
    "ONON":"https://investors.on-running.com",
    "LULU":"https://investor.lululemon.com",
    "DECK":"https://investors.deckers.com",
    "NKE":"https://investors.nike.com",
    "DLTR":"https://investor.dollartree.com",
    "DG":"https://investor.dollargeneral.com",
    "ROST":"https://investors.rossstores.com",
    "TJX":"https://ir.tjx.com",
    "GOOS":"https://investors.canadagoose.com",
    "COTY":"https://investors.coty.com",
    "CPRI":"https://investors.capriholdings.com",
    "ELF":"https://ir.elfbeauty.com",
    "ULTA":"https://ir.ultabeauty.com",
    "RL":"https://investor.ralphlauren.com",
    "TPR":"https://investors.tapestry.com",
    "EL":"https://ir.elcompanies.com",
    "KSS":"https://investor.kohls.com",
    "BBWI":"https://investors.bathandbodyworks.com",
    "M":"https://investors.macysinc.com",
    "ACI":"https://investors.albertsonscompanies.com",
    "BBY":"https://investors.bestbuy.com",
    "KR":"https://ir.kroger.com",
    "TGT":"https://investors.target.com",
    "LOW":"https://ir.lowes.com",
    "HD":"https://ir.homedepot.com",
    "COST":"https://investor.costco.com",
    "WMT":"https://stock.walmart.com",
    "NCLH":"https://www.nclhltdinvestorrelations.com",
    "RCL":"https://ir.royalcaribbean.com",
    "CCL":"https://www.carnivalcorp.com/investor-relations",
    "TAP":"https://investors.molsoncoors.com",
    "BF-B":"https://investors.brown-forman.com",
    "STZ":"https://www.cbrands.com/investors",
    "KDP":"https://investors.keurigdrpepper.com",
    "PEP":"https://www.pepsico.com/investors",
    "KO":"https://investors.coca-colacompany.com",
    "BYND":"https://investors.beyondmeat.com",
    "LW":"https://ir.lambweston.com",
    "CAG":"https://www.conagrabrands.com/investor-relations",
    "CPB":"https://investor.campbellsoupcompany.com",
    "SJM":"https://investors.jmsmucker.com",
    "MKC":"https://ir.mccormickcorporation.com",
    "HRL":"https://investors.hormelfoods.com",
    "GIS":"https://investors.generalmills.com",
    "IFF":"https://ir.iff.com",
    "KHC":"https://ir.kraftheinzcompany.com",
    "HSY":"https://www.thehersheycompany.com/investors",
    "MDLZ":"https://ir.mondelezinternational.com",
    "NWL":"https://ir.newellbrands.com",
    "CLX":"https://investors.thecloroxcompany.com",
    "CHD":"https://investors.churchdwight.com",
    "KMB":"https://investor.kimberly-clark.com",
    "CL":"https://investor.colgatepalmolive.com",
    "PG":"https://pginvestor.com",
    "MO":"https://investor.altria.com",
    "PM":"https://www.pmi.com/investor-relations",
    "MAT":"https://corporate.mattel.com/investor-relations",
    "HAS":"https://investor.hasbro.com",
    "DPZ":"https://ir.dominos.com",
    "DRI":"https://ir.darden.com",
    "QSR":"https://www.rbi.com/investor-relations",
    "CMG":"https://ir.chipotle.com",
    "YUM":"https://www.yum.com/wps/portal/yumbrands/Yumbrands/investors",
    "SBUX":"https://investor.starbucks.com",
    "MCD":"https://corporate.mcdonalds.com/corpmcd/investors.html",
    "SFD":"https://www.smithfieldfoods.com/investor-relations",
    "TSN":"https://ir.tysonfoods.com",
    "SYY":"https://investors.sysco.com",
    "CART":"https://investors.instacart.com",
    "DASH":"https://ir.doordash.com",
    "FRT":"https://www.federalrealty.com/investor-relations",
    "REG":"https://investors.regencycenters.com",
    "KIM":"https://investors.kimcorealty.com",
    "SPG":"https://investors.simon.com",
    "MAS":"https://investor.masco.com",
    "BALL":"https://investor.ball.com",
    "TSCO":"https://ir.tractorsupply.com",
    "AMCR":"https://www.amcor.com/investors",
    "ROL":"https://ir.rollins.com",
    "CTAS":"https://investors.cintas.com",
    "IP":"https://www.internationalpaper.com/investors",
}

SECTORS = {
    "APPAREL & FOOTWEAR":  ["UAA","AEO","ANF","VFC","GAP","BIRK","LEVI","ONON","LULU","DECK","NKE"],
    "OFF-PRICE / DOLLAR":  ["DLTR","DG","ROST","TJX"],
    "LUXURY & BEAUTY":     ["GOOS","COTY","CPRI","ELF","ULTA","RL","TPR","EL"],
    "RETAILERS":           ["KSS","BBWI","M","ACI","BBY","KR","TGT","LOW","HD","COST","WMT"],
    "CRUISES":             ["NCLH","RCL","CCL"],
    "BEVERAGES & ALCOHOL": ["TAP","BF-B","STZ","KDP","PEP","KO"],
    "PACKAGED FOOD":       ["BYND","LW","CAG","CPB","SJM","MKC","HRL","GIS","IFF","KHC","HSY","MDLZ"],
    "CONSUMER GOODS":      ["NWL","CLX","CHD","KMB","CL","PG"],
    "CIGARS":              ["MO","PM"],
    "TOYMAKERS":           ["MAT","HAS"],
    "RESTAURANTS":         ["DPZ","DRI","QSR","CMG","YUM","SBUX","MCD"],
    "MEAT COS":            ["SFD","TSN","SYY"],
    "DELIVERY":            ["CART","DASH"],
    "REAL ESTATE":         ["FRT","REG","KIM","SPG"],
    "RANDOS":              ["MAS","BALL","TSCO","AMCR","ROL","CTAS","IP"],
}

SECTOR_COLORS = {
    "APPAREL & FOOTWEAR":  "#4f8ef7",
    "OFF-PRICE / DOLLAR":  "#9b78d4",
    "LUXURY & BEAUTY":     "#c96b9e",
    "RETAILERS":           "#e07d45",
    "CRUISES":             "#3aada8",
    "BEVERAGES & ALCOHOL": "#5fa85a",
    "PACKAGED FOOD":       "#c9a84c",
    "CONSUMER GOODS":      "#4a9e8a",
    "CIGARS":              "#9e7a55",
    "TOYMAKERS":           "#d45f5f",
    "RESTAURANTS":         "#d47a3a",
    "MEAT COS":            "#9a66c0",
    "DELIVERY":            "#5580d4",
    "REAL ESTATE":         "#6a8fa8",
    "RANDOS":              "#7a8fa0",
}

ALL_TICKERS = [t for v in SECTORS.values() for t in v]

# ── Calendar & Earnings Seasons ──────────────────────────────────────────────

def get_calendar_season(d):
    m = d.month
    if m in (12,1,2):  return ("Winter","cal-winter")
    if m in (3,4,5):   return ("Spring","cal-spring")
    if m in (6,7,8):   return ("Summer","cal-summer")
    return                    ("Fall",  "cal-fall")

EARNINGS_SEASON_BY_MONTH = {
    1:  ("Q4 Earnings Season","reporting Oct–Dec results","#4f8ef7","rgba(79,142,247,0.06)"),
    2:  ("Q4 Earnings Season","reporting Oct–Dec results","#4f8ef7","rgba(79,142,247,0.06)"),
    3:  ("Q4 Earnings Season","reporting Oct–Dec results","#4f8ef7","rgba(79,142,247,0.06)"),
    4:  ("Q1 Earnings Season","reporting Jan–Mar results","#5fa85a","rgba(95,168,90,0.06)"),
    5:  ("Q1 Earnings Season","reporting Jan–Mar results","#5fa85a","rgba(95,168,90,0.06)"),
    6:  ("Q1 Earnings Season","reporting Jan–Mar results","#5fa85a","rgba(95,168,90,0.06)"),
    7:  ("Q2 Earnings Season","reporting Apr–Jun results","#c9a84c","rgba(201,168,76,0.06)"),
    8:  ("Q2 Earnings Season","reporting Apr–Jun results","#c9a84c","rgba(201,168,76,0.06)"),
    9:  ("Q2 Earnings Season","reporting Apr–Jun results","#c9a84c","rgba(201,168,76,0.06)"),
    10: ("Q3 Earnings Season","reporting Jul–Sep results","#c96b9e","rgba(201,107,158,0.06)"),
    11: ("Q3 Earnings Season","reporting Jul–Sep results","#c96b9e","rgba(201,107,158,0.06)"),
    12: ("Q3 Earnings Season","reporting Jul–Sep results","#c96b9e","rgba(201,107,158,0.06)"),
}

# ── Holidays ─────────────────────────────────────────────────────────────────

def get_easter(year):
    a=year%19; b=year//100; c=year%100; d=b//4; e=b%4
    f=(b+8)//25; g=(b-f+1)//3; h=(19*a+b-d-g+15)%30
    i=c//4; k=c%4; l=(32+2*e+2*i-h-k)%7
    m=(a+11*h+22*l)//451
    month=(h+l-7*m+114)//31
    day=((h+l-7*m+114)%31)+1
    return date(year,month,day)

def get_us_events(year):
    events={}
    def add(d,label,etype,closed=False):
        ds=d.strftime("%Y-%m-%d")
        events.setdefault(ds,[]).append({"label":label,"type":etype,"closed":closed})

    add(date(year,1,1),  "New Year's Day",   "holiday",closed=True)
    add(date(year,6,19), "Juneteenth",       "holiday",closed=True)
    add(date(year,7,4),  "Independence Day", "holiday",closed=True)
    add(date(year,11,11),"Veterans Day",     "holiday")
    add(date(year,12,25),"Christmas Day",    "holiday",closed=True)
    add(date(year,12,24),"Christmas Eve",    "retail")
    add(date(year,12,31),"New Year's Eve",   "retail")
    add(date(year,2,14), "Valentine's Day",  "retail")
    add(date(year,3,17), "St. Patrick's Day","retail")
    add(date(year,10,31),"Halloween",        "retail")

    jan_mon=[date(year,1,d) for d in range(1,32) if date(year,1,d).weekday()==0]
    add(jan_mon[2],"MLK Day","holiday",closed=True)

    feb_mon=[date(year,2,d) for d in range(1,29) if date(year,2,d).weekday()==0]
    add(feb_mon[2],"Presidents' Day","holiday",closed=True)

    feb_sun=[date(year,2,d) for d in range(1,29) if date(year,2,d).weekday()==6]
    add(feb_sun[1],"Super Bowl Sunday","retail")

    may_mon=[date(year,5,d) for d in range(1,32) if date(year,5,d).weekday()==0]
    add(may_mon[-1],"Memorial Day","holiday",closed=True)

    may_sun=[date(year,5,d) for d in range(1,32) if date(year,5,d).weekday()==6]
    add(may_sun[1],"Mother's Day","retail")

    jun_sun=[date(year,6,d) for d in range(1,31) if date(year,6,d).weekday()==6]
    add(jun_sun[2],"Father's Day","retail")

    sep_mon=[date(year,9,d) for d in range(1,31) if date(year,9,d).weekday()==0]
    add(sep_mon[0],"Labor Day","holiday",closed=True)

    oct_mon=[date(year,10,d) for d in range(1,32) if date(year,10,d).weekday()==0]
    add(oct_mon[1],"Columbus Day","holiday")

    nov_thu=[date(year,11,d) for d in range(1,31) if date(year,11,d).weekday()==3]
    tg=nov_thu[3]
    add(tg,                    "Thanksgiving Day","holiday",closed=True)
    add(tg+timedelta(days=1),  "Black Friday",    "retail")
    add(tg+timedelta(days=3),  "Cyber Monday",    "retail")

    easter=get_easter(year)
    add(easter-timedelta(days=2),"Good Friday",   "holiday",closed=True)
    add(easter,                  "Easter Sunday", "holiday")

    return events

# ── Fetch ─────────────────────────────────────────────────────────────────────

def fetch_nasdaq(start,end):
    out={}
    hdrs={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "accept":"application/json, text/plain, */*",
        "accept-language":"en-US,en;q=0.9",
        "origin":"https://www.nasdaq.com",
        "referer":"https://www.nasdaq.com/market-activity/earnings",
        "sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site",
    }
    cur=start
    while cur<=end:
        if cur.weekday()>=5: cur+=timedelta(days=1); continue
        ds=cur.strftime("%Y-%m-%d")
        for _ in range(3):
            try:
                r=requests.get(f"https://api.nasdaq.com/api/calendar/earnings?date={ds}",headers=hdrs,timeout=15)
                if r.status_code==429: print(f"  Rate limited {ds} — waiting 15s"); time.sleep(15); continue
                if r.status_code!=200: time.sleep(2); continue
                for row in (r.json().get("data") or {}).get("rows") or []:
                    sym=row.get("symbol","").upper().strip()
                    if sym in ALL_TICKERS:
                        t=row.get("time","").lower()
                        out[sym]={"date":ds,"timing":("BMO" if "pre" in t else "AMC" if ("after" in t or "post" in t) else None)}
                break
            except Exception: time.sleep(2)
        cur+=timedelta(days=1); time.sleep(0.45)
    print(f"NASDAQ: {len(out)} tickers found")
    return out

def fetch_yahoo(ticker):
    try:
        s=yf.Ticker(ticker)
        try:
            cal=s.calendar
            if cal is not None:
                if isinstance(cal,dict):
                    ed=cal.get("Earnings Date")
                    if ed:
                        dates=ed if isinstance(ed,list) else [ed]
                        future=[d for d in dates if pd.Timestamp(d)>pd.Timestamp.now()]
                        if future: return pd.Timestamp(future[0]).strftime("%Y-%m-%d")
                elif hasattr(cal,"index") and "Earnings Date" in cal.index:
                    dv=cal.loc["Earnings Date"].iloc[0]
                    if pd.notna(dv): return pd.to_datetime(dv).strftime("%Y-%m-%d")
        except Exception: pass
        try:
            ed=s.earnings_dates
            if ed is not None and not ed.empty:
                future=ed[ed.index>pd.Timestamp.now()]
                if not future.empty: return future.index[-1].strftime("%Y-%m-%d")
        except Exception: pass
    except Exception: pass
    return None

def run_fetch():
    today=datetime.now(ZoneInfo("America/New_York"))
    end=today+timedelta(days=182)
    print(f"EARNINGS CALENDAR REFRESH — {today.strftime('%B %d, %Y %I:%M %p ET')}")
    print("[1/2] NASDAQ API...")
    nasdaq=fetch_nasdaq(today,end)
    print(f"[2/2] Yahoo Finance ({len(ALL_TICKERS)} tickers)...")
    yf_data={}
    for i,t in enumerate(ALL_TICKERS):
        d=fetch_yahoo(t)
        if d: yf_data[t]=d
        time.sleep(0.4)
        if (i+1)%10==0: print(f"  {i+1}/{len(ALL_TICKERS)}")
    mismatches=0; rows=[]
    for sector,tickers in SECTORS.items():
        for t in tickers:
            nd=nasdaq.get(t); yd=yf_data.get(t)
            if nd:
                mismatch=bool(yd and yd!=nd["date"])
                if mismatch: mismatches+=1; print(f"  ⚠ MISMATCH {t}: NASDAQ={nd['date']} Yahoo={yd}")
                rows.append({"Sector":sector,"Ticker":t,"Earnings Date":nd["date"],"Timing":nd["timing"],
                             "Source":"NASDAQ","Yahoo Date":yd or "N/A","Mismatch":mismatch,"Confirmed":True})
            elif yd:
                rows.append({"Sector":sector,"Ticker":t,"Earnings Date":yd,"Timing":None,
                             "Source":"Yahoo Finance","Yahoo Date":yd,"Mismatch":False,"Confirmed":False})
            else:
                rows.append({"Sector":sector,"Ticker":t,"Earnings Date":None,"Timing":None,
                             "Source":"—","Yahoo Date":"N/A","Mismatch":False,"Confirmed":False})
    df=pd.DataFrame(rows)
    print(f"DONE: {df['Earnings Date'].notna().sum()} dates · {df['Earnings Date'].isna().sum()} unannounced · {mismatches} mismatches")
    return df,today

# ── Build HTML ────────────────────────────────────────────────────────────────

def build_html(df,generated_at):
    dated=df[df["Earnings Date"].notna()].copy()
    dated["dt"]=pd.to_datetime(dated["Earnings Date"])

    if dated.empty:
        months=[generated_at.replace(day=1)]
    else:
        mn=dated["dt"].min().replace(day=1); mx=dated["dt"].max().replace(day=1)
        months=[]; c=mn
        while c<=mx:
            months.append(c)
            c=(c.replace(month=c.month+1) if c.month<12 else c.replace(year=c.year+1,month=1))

    dl={}
    for _,r in dated.iterrows():
        dl.setdefault(r["dt"].strftime("%Y-%m-%d"),[]).append((
            r["Ticker"],r["Sector"],r["Timing"],r["Source"],
            str(r["Yahoo Date"]) if pd.notna(r["Yahoo Date"]) else "N/A",
            bool(r["Mismatch"]),bool(r["Confirmed"]),
        ))

    all_years=set(m.year for m in months); all_years.add(generated_at.year)
    event_map={}
    for yr in all_years:
        for ds,evs in get_us_events(yr).items():
            event_map.setdefault(ds,[]).extend(evs)

    today_str=generated_at.strftime("%Y-%m-%d")
    DAYS=["MON","TUE","WED","THU","FRI","SAT","SUN"]
    cal=""

    for ms in months:
        cal_season_name,cal_season_cls=get_calendar_season(ms)
        es_name,es_sub,es_color,es_bg=EARNINGS_SEASON_BY_MONTH[ms.month]

        # season emoji — inline SVG for quality
        season_svgs = {
            "cal-winter": '<svg class="szn-icon" viewBox="0 0 20 20"><line x1="10" y1="2" x2="10" y2="18" stroke="#90bfee" stroke-width="1.5" stroke-linecap="round"/><line x1="2" y1="10" x2="18" y2="10" stroke="#90bfee" stroke-width="1.5" stroke-linecap="round"/><line x1="4.4" y1="4.4" x2="15.6" y2="15.6" stroke="#90bfee" stroke-width="1.5" stroke-linecap="round"/><line x1="15.6" y1="4.4" x2="4.4" y2="15.6" stroke="#90bfee" stroke-width="1.5" stroke-linecap="round"/><circle cx="10" cy="10" r="2" fill="#90bfee"/><circle cx="10" cy="2" r="1" fill="#90bfee"/><circle cx="10" cy="18" r="1" fill="#90bfee"/><circle cx="2" cy="10" r="1" fill="#90bfee"/><circle cx="18" cy="10" r="1" fill="#90bfee"/></svg>',
            "cal-spring": '<svg class="szn-icon" viewBox="0 0 20 20"><circle cx="10" cy="8" r="3" fill="none" stroke="#80e09a" stroke-width="1.4"/><circle cx="10" cy="4" r="1.8" fill="#80e09a" opacity=".7"/><circle cx="14" cy="6" r="1.8" fill="#c96b9e" opacity=".7"/><circle cx="14" cy="10" r="1.8" fill="#80e09a" opacity=".7"/><circle cx="10" cy="12" r="1.8" fill="#c96b9e" opacity=".7"/><circle cx="6" cy="10" r="1.8" fill="#80e09a" opacity=".7"/><circle cx="6" cy="6" r="1.8" fill="#c96b9e" opacity=".7"/><line x1="10" y1="11" x2="10" y2="18" stroke="#80e09a" stroke-width="1.4" stroke-linecap="round"/></svg>',
            "cal-summer": '<svg class="szn-icon" viewBox="0 0 20 20"><circle cx="10" cy="10" r="4" fill="#e8c860"/><line x1="10" y1="1" x2="10" y2="3.5" stroke="#e8c860" stroke-width="1.6" stroke-linecap="round"/><line x1="10" y1="16.5" x2="10" y2="19" stroke="#e8c860" stroke-width="1.6" stroke-linecap="round"/><line x1="1" y1="10" x2="3.5" y2="10" stroke="#e8c860" stroke-width="1.6" stroke-linecap="round"/><line x1="16.5" y1="10" x2="19" y2="10" stroke="#e8c860" stroke-width="1.6" stroke-linecap="round"/><line x1="3.5" y1="3.5" x2="5.3" y2="5.3" stroke="#e8c860" stroke-width="1.4" stroke-linecap="round"/><line x1="14.7" y1="14.7" x2="16.5" y2="16.5" stroke="#e8c860" stroke-width="1.4" stroke-linecap="round"/><line x1="16.5" y1="3.5" x2="14.7" y2="5.3" stroke="#e8c860" stroke-width="1.4" stroke-linecap="round"/><line x1="5.3" y1="14.7" x2="3.5" y2="16.5" stroke="#e8c860" stroke-width="1.4" stroke-linecap="round"/></svg>',
            "cal-fall":   '<svg class="szn-icon" viewBox="0 0 20 20"><path d="M10 17 C6 17 3 14 3 10 C3 6 6 4 10 4 C10 4 8 8 10 10 C12 8 14 5 17 4 C17 8 16 12 14 14 C13 15.5 11.5 17 10 17Z" fill="#e09050" opacity=".9"/><line x1="10" y1="17" x2="10" y2="19" stroke="#9e7a55" stroke-width="1.4" stroke-linecap="round"/></svg>',
        }
        szn_svg = season_svgs[cal_season_cls]

        lbl=ms.strftime("%B %Y").upper()
        heads="".join(f'<div class="dname">{d}</div>' for d in DAYS)
        blank="".join('<div class="dcell empty"></div>' for _ in range(ms.weekday()))
        nm=(ms.replace(month=ms.month+1) if ms.month<12 else ms.replace(year=ms.year+1,month=1))
        cells=""

        for day in range(1,(nm-ms).days+1):
            do=ms.replace(day=day); ds=do.strftime("%Y-%m-%d")
            cls="dcell"
            if do.weekday()>=5: cls+=" wknd"
            if ds==today_str:   cls+=" today"
            rpts=dl.get(ds,[])
            if rpts: cls+=" has-e"
            day_events=event_map.get(ds,[])
            if any(e["closed"] for e in day_events): cls+=" mkt-closed"

            event_html=""
            for ev in day_events:
                ecls=("evbadge-holiday" if ev["type"]=="holiday" else
                      "evbadge-retail"  if ev["type"]=="retail"  else "evbadge-market")
                closed_tag=' <span class="ev-closed">CLOSED</span>' if ev["closed"] else ""
                event_html+=f'<div class="evbadge {ecls}">{ev["label"]}{closed_tag}</div>'

            chips=""
            for ticker,sector,timing,source,yahoo_date,mismatch,confirmed in rpts:
                col=SECTOR_COLORS.get(sector,"#666")
                safe=sector.replace(" ","_").replace("/","_").replace("&","_")
                cn=COMPANY_NAMES.get(ticker,ticker).replace("'","\\'").replace('"',"&quot;")
                st=sector.replace("'","\\'")
                yd_safe=yahoo_date.replace("'","\\'") if yahoo_date else "N/A"
                ir_url=IR_URLS.get(ticker,f"https://finance.yahoo.com/quote/{ticker}")

                # SVG sun / moon badges
                if timing=="BMO":
                    badge=(
                        '<span class="bdg bmo" title="Before Market Open">'
                        '<svg viewBox="0 0 16 16" width="11" height="11" style="vertical-align:middle;margin-right:1px">'
                        '<circle cx="8" cy="8" r="3.2" fill="#ffd95a"/>'
                        '<line x1="8" y1="1" x2="8" y2="3" stroke="#ffd95a" stroke-width="1.4" stroke-linecap="round"/>'
                        '<line x1="8" y1="13" x2="8" y2="15" stroke="#ffd95a" stroke-width="1.4" stroke-linecap="round"/>'
                        '<line x1="1" y1="8" x2="3" y2="8" stroke="#ffd95a" stroke-width="1.4" stroke-linecap="round"/>'
                        '<line x1="13" y1="8" x2="15" y2="8" stroke="#ffd95a" stroke-width="1.4" stroke-linecap="round"/>'
                        '<line x1="3.1" y1="3.1" x2="4.5" y2="4.5" stroke="#ffd95a" stroke-width="1.2" stroke-linecap="round"/>'
                        '<line x1="11.5" y1="11.5" x2="12.9" y2="12.9" stroke="#ffd95a" stroke-width="1.2" stroke-linecap="round"/>'
                        '<line x1="12.9" y1="3.1" x2="11.5" y2="4.5" stroke="#ffd95a" stroke-width="1.2" stroke-linecap="round"/>'
                        '<line x1="4.5" y1="11.5" x2="3.1" y2="12.9" stroke="#ffd95a" stroke-width="1.2" stroke-linecap="round"/>'
                        '</svg></span>'
                    )
                elif timing=="AMC":
                    badge=(
                        '<span class="bdg amc" title="After Market Close">'
                        '<svg viewBox="0 0 16 16" width="11" height="11" style="vertical-align:middle;margin-right:1px">'
                        '<path d="M11.5 8 A5 5 0 1 1 8 2.5 A3.8 3.8 0 0 0 11.5 8Z" fill="#c8b8ff"/>'
                        '<circle cx="12.5" cy="4.5" r=".7" fill="#c8b8ff" opacity=".6"/>'
                        '<circle cx="14" cy="7" r=".5" fill="#c8b8ff" opacity=".5"/>'
                        '<circle cx="11" cy="2.5" r=".5" fill="#c8b8ff" opacity=".4"/>'
                        '</svg></span>'
                    )
                else:
                    badge=""

                unconf='<span class="bdg unconf" title="Unconfirmed — Yahoo only">?</span>' if not confirmed else ""
                warn='<span class="bdg mismatch" title="Date conflict">!</span>' if mismatch else ""
                chips+=(
                    f'<div class="chip s-{safe}" style="--cc:{col}" data-ticker="{ticker}" '
                    f'onclick="showCard(\'{ticker}\',\'{cn}\',\'{st}\',\'{timing or "TBD"}\','
                    f'\'{ds}\',\'{col}\',\'{source}\',\'{yd_safe}\','
                    f'{str(mismatch).lower()},{str(confirmed).lower()},\'{ir_url}\')">'
                    f'{ticker}{badge}{unconf}{warn}</div>'
                )

            cells+=(f'<div class="{cls}"><span class="dno">{day}</span>'
                    f'{event_html}<div class="chips">{chips}</div></div>')

        cal+=(
            f'<div class="mblock {cal_season_cls}" style="--es-bg:{es_bg};--es-col:{es_color}">'
            f'<div class="mblock-header">'
            f'<div class="mlabel-group">'
            f'  <span class="mlabel">{lbl}</span>'
            f'  <span class="cal-season-badge {cal_season_cls}-badge">{szn_svg}{cal_season_name}</span>'
            f'</div>'
            f'<span class="earn-season-badge" style="--ec:{es_color}">'
            f'  <svg viewBox="0 0 14 14" width="11" height="11" style="vertical-align:middle;margin-right:4px">'
            f'  <rect x="1" y="5" width="2" height="7" rx="1" fill="{es_color}"/>'
            f'  <rect x="4.5" y="3" width="2" height="9" rx="1" fill="{es_color}" opacity=".85"/>'
            f'  <rect x="8" y="1" width="2" height="11" rx="1" fill="{es_color}" opacity=".7"/>'
            f'  <rect x="11.5" y="4" width="2" height="8" rx="1" fill="{es_color}" opacity=".6"/>'
            f'  </svg>'
            f'  {es_name} <span class="earn-season-sub">{es_sub}</span>'
            f'</span>'
            f'</div>'
            f'<div class="cgrid">{heads}{blank}{cells}</div>'
            f'</div>'
        )

    # ── Unannounced ──────────────────────────────────────────────────────────
    unann=df[df["Earnings Date"].isna()]
    uhtml=""
    if not unann.empty:
        rows_h=""
        for s,tickers in SECTORS.items():
            miss=unann[unann["Sector"]==s]["Ticker"].tolist()
            if not miss: continue
            col=SECTOR_COLORS[s]
            safe=s.replace(" ","_").replace("/","_").replace("&","_")
            chips_u="".join(
                f'<span class="uchip s-{safe}" style="--cc:{col}" data-ticker="{t}" '
                f'onclick="showCard(\'{t}\','
                f'\'{COMPANY_NAMES.get(t,t).replace(chr(39),chr(92)+chr(39))}\','
                f'\'{s.replace(chr(39),chr(92)+chr(39))}\','
                f'\'TBD\',\'TBD\',\'{col}\',\'—\',\'N/A\',false,false,'
                f'\'{IR_URLS.get(t,f"https://finance.yahoo.com/quote/{t}")}\')">{t}</span>'
                for t in miss
            )
            rows_h+=(f'<tr><td><span class="sbadge" style="background:{col}">{s}</span></td>'
                     f'<td>{chips_u}</td></tr>')
        uhtml=(f'<div class="ubox"><div class="ubox-head">'
               f'<span class="ubox-title">NOT YET ANNOUNCED</span>'
               f'<span class="ubox-sub">Click any ticker for details</span>'
               f'</div><table class="utable">'
               f'<thead><tr><th>SECTOR</th><th>TICKERS</th></tr></thead>'
               f'<tbody>{rows_h}</tbody></table></div>')

    nf=len(dated); nu=len(unann); nm=int(df["Mismatch"].sum())
    ts=generated_at.strftime("%d %b %Y, %I:%M %p ET")
    sj=json.dumps(SECTORS); cj=json.dumps(SECTOR_COLORS); nj=json.dumps(COMPANY_NAMES)

    sector_legend_chips="".join(
        f'<div class="sleg-row">'
        f'<span class="sleg-chip" style="--cc:{SECTOR_COLORS[s]}">{s}</span>'
        f'<span class="sleg-tickers">'
        + "".join(f'<span class="sleg-ticker">{t}</span>' for t in SECTORS[s])
        + f'</span></div>'
        for s in SECTORS
    )

    html=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="21600">
<title>Earnings Calendar — Consumer &amp; Retail</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg0:#080a12;--bg1:#0d1020;--bg2:#111525;--bg3:#181d30;
  --line:rgba(255,255,255,0.08);--line2:rgba(255,255,255,0.15);
  --t0:#ffffff;--t1:#c8cfe8;--t2:#7a84aa;
  --accent:#4f8ef7;--warn:#f7a94f;
  --mono:'JetBrains Mono',monospace;
  --sans:'Inter',-apple-system,sans-serif;
  --sidebar:260px;
}}
body{{font-family:var(--sans);background:var(--bg0);color:var(--t1);min-height:100vh;-webkit-font-smoothing:antialiased;}}

/* ── Layout ── */
.page-wrap{{display:flex;min-height:100vh;}}
.sidebar{{width:var(--sidebar);flex-shrink:0;background:var(--bg1);border-right:1px solid var(--line);position:sticky;top:0;height:100vh;overflow-y:auto;display:flex;flex-direction:column;}}
.content{{flex:1;min-width:0;display:flex;flex-direction:column;}}

/* ── Topbar ── */
.topbar{{height:58px;background:var(--bg1);border-bottom:1px solid var(--line2);display:flex;align-items:center;justify-content:space-between;padding:0 24px;position:sticky;top:0;z-index:300;gap:16px;}}
.topbar-left{{display:flex;align-items:center;gap:14px;}}
.page-title{{font-size:15px;font-weight:700;color:var(--t0);letter-spacing:-.2px;white-space:nowrap;}}
.divider{{width:1px;height:22px;background:var(--line2);}}
.topbar-meta{{font-size:11px;color:var(--t1);white-space:nowrap;}}
.topbar-right{{display:flex;align-items:center;gap:20px;flex-shrink:0;}}
.tstat{{display:flex;flex-direction:column;align-items:flex-end;}}
.tstat-num{{font-family:var(--mono);font-size:17px;font-weight:700;color:var(--t0);line-height:1;}}
.tstat-lbl{{font-size:9px;color:var(--t2);text-transform:uppercase;letter-spacing:.7px;margin-top:3px;}}

/* ── Key bar ── */
.timingbar{{background:var(--bg0);border-bottom:1px solid var(--line);padding:7px 24px 10px;display:flex;align-items:center;gap:12px;font-size:11.5px;color:var(--t1);flex-wrap:wrap;}}
.tpill{{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:3px 9px;border-radius:5px;font-family:var(--mono);letter-spacing:.3px;white-space:nowrap;}}
.tpill.pre{{background:rgba(255,217,90,.1);color:#ffd95a;border:1px solid rgba(255,217,90,.3);}}
.tpill.aft{{background:rgba(200,184,255,.1);color:#c8b8ff;border:1px solid rgba(200,184,255,.3);}}
.tpill.mis{{background:rgba(220,60,60,.2);color:#ff7070;border:1px solid rgba(220,60,60,.4);}}
.tpill.unc{{background:rgba(30,30,30,.6);color:#888;border:1px solid rgba(255,255,255,.12);}}

/* BMO sun SVG in pill */
.tpill-sun{{display:inline-block;vertical-align:middle;}}
/* AMC moon SVG in pill */
.tpill-moon{{display:inline-block;vertical-align:middle;}}

/* ── Event legend ── */
.event-legend{{display:flex;flex-wrap:wrap;align-items:center;gap:6px;width:100%;margin-top:6px;padding-top:6px;border-top:1px solid var(--line);}}
.evleg-label{{font-family:var(--mono);font-size:9px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.8px;margin-right:4px;white-space:nowrap;}}
.evleg-item{{display:inline-flex;align-items:center;gap:4px;font-size:9px;color:var(--t2);}}
.evleg-dot{{width:8px;height:8px;border-radius:2px;flex-shrink:0;}}
.evleg-dot.holiday{{background:#4a6fa8;}}
.evleg-dot.retail{{background:#7a5a2a;}}
.evleg-dot.closed{{background:rgba(220,60,60,.5);border:1px solid rgba(220,60,60,.6);}}

/* ── Sidebar sector legend ── */
.sidebar-head{{padding:14px 16px 10px;border-bottom:1px solid var(--line);}}
.sidebar-title{{font-family:var(--mono);font-size:10px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:.8px;}}
.sleg-row{{padding:5px 12px;border-bottom:1px solid var(--line);}}
.sleg-row:last-child{{border-bottom:none;}}
.sleg-chip{{display:block;font-family:var(--mono);font-size:9.5px;font-weight:700;color:#fff;background:var(--cc,#444);padding:2px 8px;border-radius:4px;text-shadow:0 1px 2px rgba(0,0,0,.4);margin-bottom:4px;}}
.sleg-tickers{{display:flex;flex-wrap:wrap;gap:2px;}}
.sleg-ticker{{font-family:var(--mono);font-size:8.5px;color:var(--t2);background:var(--bg2);border:1px solid var(--line);border-radius:3px;padding:1px 4px;}}

/* ── Search ── */
.search-bar{{background:var(--bg1);border-bottom:1px solid var(--line);padding:8px 24px;display:flex;align-items:center;gap:10px;position:sticky;top:58px;z-index:299;}}
.search-input{{background:var(--bg2);border:1px solid var(--line2);border-radius:7px;padding:6px 12px;font-family:var(--mono);font-size:12px;color:var(--t0);outline:none;width:220px;transition:border-color .15s;}}
.search-input::placeholder{{color:var(--t2);}}
.search-input:focus{{border-color:var(--accent);}}
.search-clear{{background:none;border:none;color:var(--t2);cursor:pointer;font-size:16px;line-height:1;padding:0 4px;display:none;}}
.search-clear.on{{display:block;}}
.search-hint{{font-size:11px;color:var(--t2);}}

/* ── Calendar ── */
.main{{padding:28px 24px;max-width:1400px;margin:0 auto;}}
.mblock{{margin-bottom:44px;border-radius:12px;overflow:hidden;border:1px solid var(--line);}}
.mblock-header{{padding:12px 16px 10px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;background:var(--es-bg,var(--bg1));}}
.mlabel-group{{display:flex;align-items:center;gap:10px;}}
.mlabel{{font-family:var(--mono);font-size:13px;font-weight:700;color:var(--t0);letter-spacing:.5px;}}

/* Calendar season badge */
.cal-season-badge{{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);font-size:10px;font-weight:700;padding:3px 9px;border-radius:5px;white-space:nowrap;}}
.szn-icon{{display:inline-block;vertical-align:middle;}}
.cal-winter-badge{{background:rgba(100,160,230,.1);color:#90bfee;border:1px solid rgba(100,160,230,.22);}}
.cal-spring-badge{{background:rgba(100,200,120,.1);color:#80e09a;border:1px solid rgba(100,200,120,.22);}}
.cal-summer-badge{{background:rgba(230,180,60,.1);color:#e8c860;border:1px solid rgba(230,180,60,.22);}}
.cal-fall-badge{{background:rgba(210,120,50,.1);color:#e09050;border:1px solid rgba(210,120,50,.22);}}

/* Earnings season badge */
.earn-season-badge{{display:inline-flex;align-items:center;font-family:var(--mono);font-size:10px;font-weight:700;padding:3px 9px;border-radius:5px;white-space:nowrap;background:color-mix(in srgb,var(--ec) 10%,transparent);color:var(--ec);border:1px solid color-mix(in srgb,var(--ec) 25%,transparent);}}
.earn-season-sub{{font-size:8.5px;font-weight:400;opacity:.7;margin-left:5px;}}

/* Season left accent */
.cal-winter{{border-left:3px solid rgba(100,160,230,.35)!important;}}
.cal-spring{{border-left:3px solid rgba(100,200,120,.35)!important;}}
.cal-summer{{border-left:3px solid rgba(230,180,60,.35)!important;}}
.cal-fall{{border-left:3px solid rgba(210,120,50,.35)!important;}}

.cgrid{{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;padding:10px;background:var(--bg1);}}
.dname{{text-align:center;font-family:var(--mono);font-size:10px;font-weight:700;color:var(--t1);padding:6px 0;letter-spacing:.8px;}}
.dcell{{background:var(--bg2);border:1px solid var(--line);border-radius:8px;min-height:96px;padding:9px 7px 7px;transition:border-color .12s,background .12s;}}
.dcell.empty{{background:transparent;border-color:transparent;pointer-events:none;}}
.dcell.wknd{{background:#0c0e14;opacity:.4;}}
.dcell.today{{border-color:var(--accent)!important;background:color-mix(in srgb,var(--accent) 7%,var(--bg2));}}
.dcell.today .dno{{color:var(--accent)!important;font-weight:700;}}
.dcell.has-e{{border-color:var(--line2);}}
.dcell.mkt-closed{{background:color-mix(in srgb,#1a0808 80%,var(--bg2));}}
.dno{{font-family:var(--mono);font-size:11px;font-weight:500;color:var(--t1);margin-bottom:3px;display:block;}}

/* ── Event badges ── */
.evbadge{{font-family:var(--mono);font-size:8px;font-weight:700;padding:1px 5px;border-radius:3px;margin-bottom:3px;display:inline-block;letter-spacing:.2px;white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis;}}
.evbadge-holiday{{background:rgba(74,111,168,.22);color:#8aabdf;border:1px solid rgba(74,111,168,.35);}}
.evbadge-retail{{background:rgba(122,90,42,.28);color:#c9a870;border:1px solid rgba(122,90,42,.45);}}
.evbadge-market{{background:rgba(60,173,168,.13);color:#6dccc8;border:1px solid rgba(60,173,168,.28);}}
.ev-closed{{font-size:7px;font-weight:900;background:rgba(220,60,60,.7);color:#fff;padding:0 3px;border-radius:2px;margin-left:3px;letter-spacing:.3px;vertical-align:middle;}}

/* ── Ticker chips ── */
.chips{{display:flex;flex-wrap:wrap;gap:3px;margin-top:2px;}}
.chip{{display:inline-flex;align-items:center;gap:2px;background:var(--cc,#444);font-family:var(--mono);font-size:10px;font-weight:700;color:#fff;padding:3px 6px;border-radius:5px;cursor:pointer;white-space:nowrap;transition:transform .12s,filter .12s,opacity .15s;letter-spacing:.2px;text-shadow:0 1px 2px rgba(0,0,0,.4);}}
.chip:hover{{transform:scale(1.08);filter:brightness(1.18);z-index:10;position:relative;}}
.chip.dimmed{{opacity:.12;pointer-events:none;}}
.bdg{{display:inline-flex;align-items:center;justify-content:center;line-height:1;}}
.bdg.bmo,.bdg.amc{{background:transparent;}}
.bdg.unconf{{font-family:var(--mono);font-size:8px;font-weight:900;background:rgba(255,255,255,.1);color:#888;border-radius:3px;padding:0 3px;}}
.bdg.mismatch{{font-family:var(--mono);font-size:8px;font-weight:900;background:rgba(220,60,60,.85);color:#fff;border-radius:3px;padding:0 4px;}}

/* ── Unannounced ── */
.ubox{{margin:32px 24px 44px;background:var(--bg2);border:1px solid var(--line);border-radius:12px;overflow:hidden;}}
.ubox-head{{padding:14px 20px;border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:14px;}}
.ubox-title{{font-family:var(--mono);font-size:13px;font-weight:700;color:var(--t0);letter-spacing:.4px;}}
.ubox-sub{{font-size:11px;color:var(--t1);}}
.utable{{width:100%;border-collapse:collapse;font-size:12px;}}
.utable th{{text-align:left;padding:8px 14px;font-family:var(--mono);font-size:9px;font-weight:700;color:var(--t1);border-bottom:1px solid var(--line);text-transform:uppercase;letter-spacing:.6px;}}
.utable td{{padding:8px 14px;border-bottom:1px solid var(--line);vertical-align:middle;}}
.utable tr:last-child td{{border-bottom:none;}}
.sbadge{{font-family:var(--mono);font-size:10px;font-weight:700;color:#fff;padding:3px 9px;border-radius:4px;white-space:nowrap;text-shadow:0 1px 2px rgba(0,0,0,.4);}}
.uchip{{display:inline-flex;align-items:center;background:var(--cc,#444);font-family:var(--mono);font-size:10px;font-weight:700;color:#fff;padding:3px 7px;border-radius:5px;margin:2px;cursor:pointer;transition:transform .12s,filter .12s,opacity .15s;text-shadow:0 1px 2px rgba(0,0,0,.4);}}
.uchip:hover{{transform:scale(1.07);filter:brightness(1.18);}}
.uchip.dimmed{{opacity:.12;pointer-events:none;}}

/* ── Footer ── */
.footer{{border-top:1px solid var(--line);padding:12px 24px;font-family:var(--mono);font-size:10px;color:var(--t2);display:flex;justify-content:space-between;align-items:center;}}

/* ── Modal ── */
.overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.82);backdrop-filter:blur(10px);z-index:999;align-items:center;justify-content:center;}}
.overlay.on{{display:flex;}}
.modal{{background:var(--bg3);border:1px solid var(--line2);border-radius:16px;padding:28px;max-width:440px;width:90%;box-shadow:0 24px 48px rgba(0,0,0,.8);position:relative;animation:popIn .2s cubic-bezier(.34,1.4,.64,1);}}
@keyframes popIn{{from{{transform:scale(.9);opacity:0}}to{{transform:scale(1);opacity:1}}}}
.modal-close{{position:absolute;top:12px;right:14px;background:none;border:none;font-size:22px;color:var(--t1);cursor:pointer;line-height:1;}}
.modal-close:hover{{color:var(--t0);}}
.modal-ticker{{font-family:var(--mono);font-size:30px;font-weight:700;margin-bottom:4px;line-height:1;}}
.modal-name{{font-size:13px;color:var(--t1);margin-bottom:20px;}}
.modal-row{{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid var(--line);font-size:13px;}}
.modal-row:last-child{{border-bottom:none;}}
.modal-key{{color:var(--t2);font-size:11px;text-transform:uppercase;letter-spacing:.6px;font-weight:600;}}
.modal-val{{color:var(--t0);font-family:var(--mono);font-size:12px;font-weight:600;}}
.modal-val.secondary{{color:var(--t1);font-size:11px;font-weight:400;}}
.modal-mismatch-banner{{background:rgba(220,60,60,.12);border:1px solid rgba(220,60,60,.35);border-radius:8px;padding:10px 14px;margin-bottom:16px;font-size:11.5px;color:#ff7070;display:none;line-height:1.5;}}
.modal-mismatch-banner.on{{display:block;}}
.modal-unconf-banner{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:10px 14px;margin-bottom:16px;font-size:11.5px;color:#aaa;display:none;line-height:1.5;}}
.modal-unconf-banner.on{{display:block;}}
.modal-source-row{{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line);gap:12px;}}
.modal-source-col{{display:flex;flex-direction:column;gap:4px;flex:1;}}
.modal-source-label{{color:var(--t2);font-size:10px;text-transform:uppercase;letter-spacing:.6px;font-weight:600;}}
.modal-source-date{{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--t0);}}
.modal-source-date.conflict{{color:#ff7070;}}
.modal-ir-link{{display:inline-flex;align-items:center;gap:6px;margin-top:16px;font-family:var(--mono);font-size:11px;font-weight:600;color:var(--accent);text-decoration:none;border:1px solid rgba(79,142,247,.3);border-radius:6px;padding:6px 12px;transition:background .15s,border-color .15s;}}
.modal-ir-link:hover{{background:rgba(79,142,247,.1);border-color:rgba(79,142,247,.6);}}
</style>
</head>
<body>
<div class="page-wrap">

<!-- ── Sidebar sector legend ── -->
<aside class="sidebar">
  <div class="sidebar-head">
    <div class="sidebar-title">Sectors</div>
  </div>
  {sector_legend_chips}
</aside>

<div class="content">
<header class="topbar">
  <div class="topbar-left">
    <span class="page-title">Earnings Calendar</span>
    <span class="divider"></span>
    <span class="topbar-meta">Consumer &amp; Retail · Updated {ts}</span>
  </div>
  <div class="topbar-right">
    <div class="tstat"><span class="tstat-num" style="color:#4f8ef7">{nf}</span><span class="tstat-lbl">Dates Found</span></div>
    <div class="tstat"><span class="tstat-num" style="color:#9098c0">{nu}</span><span class="tstat-lbl">Unannounced</span></div>
    <div class="tstat"><span class="tstat-num" style="color:#ff7070">{nm}</span><span class="tstat-lbl">Mismatches</span></div>
  </div>
</header>

<div class="timingbar">
  <span style="color:var(--t0);font-weight:600;font-size:11px;">KEY</span>

  <span class="tpill pre">
    <svg class="tpill-sun" viewBox="0 0 16 16" width="13" height="13">
      <circle cx="8" cy="8" r="3.2" fill="#ffd95a"/>
      <line x1="8" y1="1" x2="8" y2="3.2" stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="8" y1="12.8" x2="8" y2="15" stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="1" y1="8" x2="3.2" y2="8" stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="12.8" y1="8" x2="15" y2="8" stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="3.1" y1="3.1" x2="4.6" y2="4.6" stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>
      <line x1="11.4" y1="11.4" x2="12.9" y2="12.9" stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>
      <line x1="12.9" y1="3.1" x2="11.4" y2="4.6" stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>
      <line x1="4.6" y1="11.4" x2="3.1" y2="12.9" stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>
    </svg>
    BMO
  </span>
  <span style="font-size:11px;">Before market open</span>

  <span class="tpill aft">
    <svg class="tpill-moon" viewBox="0 0 16 16" width="13" height="13">
      <path d="M12 8.5 A5.5 5.5 0 1 1 7.5 3 A4 4 0 0 0 12 8.5Z" fill="#c8b8ff"/>
      <circle cx="13" cy="5" r=".8" fill="#c8b8ff" opacity=".55"/>
      <circle cx="14.5" cy="8" r=".6" fill="#c8b8ff" opacity=".45"/>
      <circle cx="12" cy="3" r=".6" fill="#c8b8ff" opacity=".4"/>
    </svg>
    AMC
  </span>
  <span style="font-size:11px;">After market close</span>

  <span class="tpill unc">? Unconfirmed</span>
  <span style="font-size:11px;">Yahoo only, not on NASDAQ</span>
  <span class="tpill mis">! Conflict</span>
  <span style="font-size:11px;">NASDAQ &amp; Yahoo dates differ</span>
  <span style="margin-left:4px;font-size:11px;color:var(--t2);">All times ET · Click any ticker for details</span>

  <div class="event-legend">
    <span class="evleg-label">EVENTS</span>
    <span class="evleg-item"><span class="evleg-dot holiday"></span>Federal Holiday</span>
    <span class="evleg-item"><span class="evleg-dot retail"></span>Retail / Consumer Event</span>
    <span class="evleg-item"><span class="evleg-dot closed"></span>Market Closed</span>
  </div>
</div>

<div class="search-bar">
  <input class="search-input" id="searchInput" type="text" placeholder="Search ticker e.g. NKE" autocomplete="off" spellcheck="false">
  <button class="search-clear" id="searchClear" onclick="clearSearch()">×</button>
  <span class="search-hint" id="searchHint"></span>
</div>

<main class="main" id="calMain">{cal}</main>
{uhtml}

<footer class="footer">
  <span>Neil J Kanatt · Data: NASDAQ API + Yahoo Finance cross-check</span>
  <span>Auto-refreshes every 6 hours · Generated {ts}</span>
</footer>
</div><!-- end .content -->
</div><!-- end .page-wrap -->

<div class="overlay" id="overlay" onclick="closeModal(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeModal()">×</button>
    <div class="modal-ticker" id="mTicker"></div>
    <div class="modal-name"   id="mName"></div>
    <div class="modal-mismatch-banner" id="mMismatch">
      ⚠ Date conflict — NASDAQ and Yahoo Finance show different dates. Verify before acting.
    </div>
    <div class="modal-unconf-banner" id="mUnconf">
      ❗ Unconfirmed — date sourced from Yahoo Finance only. Not yet listed on NASDAQ.
    </div>
    <div class="modal-row">
      <span class="modal-key">Sector</span>
      <span class="modal-val" id="mSector"></span>
    </div>
    <div class="modal-source-row">
      <div class="modal-source-col">
        <span class="modal-source-label">NASDAQ Date</span>
        <span class="modal-source-date" id="mNasdaqDate"></span>
      </div>
      <div class="modal-source-col">
        <span class="modal-source-label">Yahoo Date</span>
        <span class="modal-source-date" id="mYahooDate"></span>
      </div>
    </div>
    <div class="modal-row">
      <span class="modal-key">Timing</span>
      <span class="modal-val" id="mTiming"></span>
    </div>
    <div class="modal-row">
      <span class="modal-key">Source</span>
      <span class="modal-val secondary" id="mSource"></span>
    </div>
    <a class="modal-ir-link" id="mIRLink" href="#" target="_blank" rel="noopener">
      ↗ Investor Relations Page
    </a>
  </div>
</div>

<script>
const SECTORS       = {sj};
const SECTOR_COLORS = {cj};
const COMPANY_NAMES = {nj};
setTimeout(function(){{ location.reload(); }}, 6*60*60*1000);

const searchInput = document.getElementById('searchInput');
const searchClear = document.getElementById('searchClear');
const searchHint  = document.getElementById('searchHint');

searchInput.addEventListener('input', function(){{
  const q = this.value.trim().toUpperCase();
  searchClear.classList.toggle('on', q.length > 0);
  applySearch(q);
}});

function clearSearch(){{
  searchInput.value=''; searchClear.classList.remove('on');
  searchHint.textContent=''; applySearch('');
}}

function applySearch(q){{
  const chips=document.querySelectorAll('.chip');
  const uchips=document.querySelectorAll('.uchip');
  if(!q){{
    chips.forEach(c=>c.classList.remove('dimmed'));
    uchips.forEach(c=>c.classList.remove('dimmed'));
    searchHint.textContent=''; return;
  }}
  let found=0;
  chips.forEach(c=>{{
    const match=c.dataset.ticker&&c.dataset.ticker.toUpperCase().includes(q);
    c.classList.toggle('dimmed',!match); if(match) found++;
  }});
  uchips.forEach(c=>{{
    const match=c.dataset.ticker&&c.dataset.ticker.toUpperCase().includes(q);
    c.classList.toggle('dimmed',!match); if(match) found++;
  }});
  searchHint.textContent=found>0?found+' result'+(found>1?'s':''):'No results';
}}

function showCard(ticker,name,sector,timing,nasdaqDate,color,source,yahooDate,mismatch,confirmed,irUrl){{
  document.getElementById('mTicker').textContent=ticker;
  document.getElementById('mTicker').style.color=color;
  document.getElementById('mName').textContent=name;
  document.getElementById('mSector').textContent=sector;
  document.getElementById('mNasdaqDate').textContent=(nasdaqDate==='TBD'||!confirmed)?'Not on NASDAQ':nasdaqDate;
  document.getElementById('mYahooDate').textContent=yahooDate&&yahooDate!=='N/A'?yahooDate:'Not available';
  document.getElementById('mYahooDate').classList.toggle('conflict',mismatch);
  document.getElementById('mNasdaqDate').classList.toggle('conflict',mismatch);
  document.getElementById('mTiming').textContent=
    timing==='BMO'?'Before Market Open (SVG sun shown on chip)':
    timing==='AMC'?'After Market Close (SVG moon shown on chip)':
    timing==='TBD'?'Not yet confirmed':'Unconfirmed';
  document.getElementById('mSource').textContent=source;
  document.getElementById('mMismatch').classList.toggle('on',mismatch);
  document.getElementById('mUnconf').classList.toggle('on',!confirmed&&nasdaqDate!=='TBD');
  document.getElementById('mIRLink').href=irUrl||('https://finance.yahoo.com/quote/'+ticker);
  document.getElementById('overlay').classList.add('on');
}}

function closeModal(e){{
  if(!e||e.target===document.getElementById('overlay'))
    document.getElementById('overlay').classList.remove('on');
}}
document.addEventListener('keydown',e=>{{
  if(e.key==='Escape') document.getElementById('overlay').classList.remove('on');
}});
</script>
</body>
</html>"""
    return html

# ── RUN ──
df, generated_at = run_fetch()
html = build_html(df, generated_at)
with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print("Done — index.html written")
