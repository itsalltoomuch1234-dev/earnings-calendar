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
    "DOLLAR STORES":       ["DLTR","DG","ROST","TJX"],
    "LUXURY & BEAUTY":     ["GOOS","COTY","CPRI","ELF","ULTA","RL","TPR","EL"],
    "RETAILERS":           ["KSS","BBWI","M","ACI","BBY","KR","TGT","LOW","HD","COST","WMT"],
    "CRUISES":             ["NCLH","RCL","CCL"],
    "BEVERAGES & ALCOHOL": ["TAP","BF-B","STZ","KDP","PEP","KO"],
    "PACKAGED FOOD":       ["BYND","LW","CAG","CPB","SJM","MKC","HRL","GIS","IFF","KHC","HSY","MDLZ"],
    "CONSUMER GOODS":      ["NWL","CLX","CHD","KMB","CL","PG"],
    "CIGARETTES":          ["MO","PM"],
    "TOYMAKERS":           ["MAT","HAS"],
    "RESTAURANTS":         ["DPZ","DRI","QSR","CMG","YUM","SBUX","MCD"],
    "MEAT COS":            ["SFD","TSN","SYY"],
    "DELIVERY":            ["CART","DASH"],
    "REAL ESTATE":         ["FRT","REG","KIM","SPG"],
    "OTHERS":              ["MAS","BALL","TSCO","AMCR","ROL","CTAS","IP"],
}

SECTOR_COLORS = {
    "APPAREL & FOOTWEAR":  "#4f8ef7",
    "DOLLAR STORES":       "#9b78d4",
    "LUXURY & BEAUTY":     "#c96b9e",
    "RETAILERS":           "#e07d45",
    "CRUISES":             "#3aada8",
    "BEVERAGES & ALCOHOL": "#5fa85a",
    "PACKAGED FOOD":       "#c9a84c",
    "CONSUMER GOODS":      "#4a9e8a",
    "CIGARETTES":          "#9e7a55",
    "TOYMAKERS":           "#d45f5f",
    "RESTAURANTS":         "#d47a3a",
    "MEAT COS":            "#9a66c0",
    "DELIVERY":            "#5580d4",
    "REAL ESTATE":         "#6a8fa8",
    "OTHERS":              "#7a8fa0",
}

ALL_TICKERS = [t for v in SECTORS.values() for t in v]

EARNINGS_SEASON_BY_MONTH = {
    1:  ("Q4 Earnings Season","Oct–Dec results","#4f8ef7","rgba(79,142,247,0.07)"),
    2:  ("Q4 Earnings Season","Oct–Dec results","#4f8ef7","rgba(79,142,247,0.07)"),
    3:  ("Q4 Earnings Season","Oct–Dec results","#4f8ef7","rgba(79,142,247,0.07)"),
    4:  ("Q1 Earnings Season","Jan–Mar results","#5fa85a","rgba(95,168,90,0.07)"),
    5:  ("Q1 Earnings Season","Jan–Mar results","#5fa85a","rgba(95,168,90,0.07)"),
    6:  ("Q1 Earnings Season","Jan–Mar results","#5fa85a","rgba(95,168,90,0.07)"),
    7:  ("Q2 Earnings Season","Apr–Jun results","#c9a84c","rgba(201,168,76,0.07)"),
    8:  ("Q2 Earnings Season","Apr–Jun results","#c9a84c","rgba(201,168,76,0.07)"),
    9:  ("Q2 Earnings Season","Apr–Jun results","#c9a84c","rgba(201,168,76,0.07)"),
    10: ("Q3 Earnings Season","Jul–Sep results","#c96b9e","rgba(201,107,158,0.07)"),
    11: ("Q3 Earnings Season","Jul–Sep results","#c96b9e","rgba(201,107,158,0.07)"),
    12: ("Q3 Earnings Season","Jul–Sep results","#c96b9e","rgba(201,107,158,0.07)"),
}

# ── Holidays ──────────────────────────────────────────────────────────────────

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
    add(tg,                   "Thanksgiving Day","holiday",closed=True)
    add(tg+timedelta(days=1), "Black Friday",    "retail")
    add(tg+timedelta(days=3), "Cyber Monday",    "retail")
    easter=get_easter(year)
    add(easter-timedelta(days=2),"Good Friday",  "holiday",closed=True)
    add(easter,                  "Easter Sunday","holiday")
    return events

# ── Fetch ─────────────────────────────────────────────────────────────────────

def fetch_nasdaq(start, end):
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
    while cur <= end:
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
    days_since_monday=today.weekday()
    fetch_start=today.date()-timedelta(days=days_since_monday+7)
    end = today.date() + timedelta(days=182)
    print(f"EARNINGS CALENDAR REFRESH — {today.strftime('%B %d, %Y %I:%M %p ET')}")
    print("[1/2] NASDAQ API...")
    nasdaq=fetch_nasdaq(fetch_start,end)
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

# ── SVG constants ─────────────────────────────────────────────────────────────

BMO_SVG = (
    '<svg viewBox="0 0 16 16" width="10" height="10" '
    'style="vertical-align:middle;flex-shrink:0;margin-right:1px">'
    '<circle cx="8" cy="8" r="3" fill="#000"/>'
    '<line x1="8" y1="1"    x2="8"  y2="3.2"  stroke="#000" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="8" y1="12.8" x2="8"  y2="15"   stroke="#000" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="1" y1="8"    x2="3.2" y2="8"   stroke="#000" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="12.8" y1="8" x2="15" y2="8"    stroke="#000" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="3.1" y1="3.1"   x2="4.6" y2="4.6"   stroke="#000" stroke-width="1.3" stroke-linecap="round"/>'
    '<line x1="11.4" y1="11.4" x2="12.9" y2="12.9" stroke="#000" stroke-width="1.3" stroke-linecap="round"/>'
    '<line x1="12.9" y1="3.1"  x2="11.4" y2="4.6"  stroke="#000" stroke-width="1.3" stroke-linecap="round"/>'
    '<line x1="4.6" y1="11.4"  x2="3.1" y2="12.9"  stroke="#000" stroke-width="1.3" stroke-linecap="round"/>'
    '</svg>'
)

AMC_SVG = (
    '<svg viewBox="0 0 16 16" width="10" height="10" '
    'style="vertical-align:middle;flex-shrink:0;margin-right:1px">'
    '<path d="M11.5 8 A5.5 5.5 0 1 1 7.5 3 A4 4 0 0 0 11.5 8Z" fill="#000"/>'
    '</svg>'
)

BMO_SVG_KEY = (
    '<svg viewBox="0 0 16 16" width="13" height="13" style="vertical-align:middle">'
    '<circle cx="8" cy="8" r="3" fill="#ffd95a"/>'
    '<line x1="8" y1="1"    x2="8"  y2="3.2"  stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="8" y1="12.8" x2="8"  y2="15"   stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="1" y1="8"    x2="3.2" y2="8"   stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="12.8" y1="8" x2="15" y2="8"    stroke="#ffd95a" stroke-width="1.5" stroke-linecap="round"/>'
    '<line x1="3.1" y1="3.1"   x2="4.6" y2="4.6"   stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>'
    '<line x1="11.4" y1="11.4" x2="12.9" y2="12.9" stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>'
    '<line x1="12.9" y1="3.1"  x2="11.4" y2="4.6"  stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>'
    '<line x1="4.6" y1="11.4"  x2="3.1" y2="12.9"  stroke="#ffd95a" stroke-width="1.3" stroke-linecap="round"/>'
    '</svg>'
)

AMC_SVG_KEY = (
    '<svg viewBox="0 0 16 16" width="13" height="13" style="vertical-align:middle">'
    '<path d="M12 8.5 A5.5 5.5 0 1 1 7.5 3 A4 4 0 0 0 12 8.5Z" fill="#c8b8ff"/>'
    '<circle cx="13" cy="5"   r=".8" fill="#c8b8ff" opacity=".55"/>'
    '<circle cx="14.5" cy="8" r=".6" fill="#c8b8ff" opacity=".45"/>'
    '<circle cx="12"   cy="3" r=".6" fill="#c8b8ff" opacity=".4"/>'
    '</svg>'
)

# ── Build HTML ────────────────────────────────────────────────────────────────

def build_html(df, generated_at):
    dated = df[df["Earnings Date"].notna()].copy()
    dated["dt"] = pd.to_datetime(dated["Earnings Date"])

    today_dt = generated_at.date()  # this is a datetime.date
    days_since_monday = today_dt.weekday()
    this_monday  = today_dt - timedelta(days=days_since_monday)
    prior_monday = this_monday - timedelta(days=7)
    prior_sunday = this_monday - timedelta(days=1)

    if dated.empty:
        months = [today_dt.replace(day=1)]
    else:
        # FIX: convert Timestamps to date before comparing/replacing
        mn = min(
            dated["dt"].min().date().replace(day=1),
            prior_monday.replace(day=1)
        )
        mx = dated["dt"].max().date().replace(day=1)
        months = []
        c = mn
        while c <= mx:
            months.append(c)
            c = (c.replace(month=c.month+1) if c.month < 12
                 else c.replace(year=c.year+1, month=1))

    dl = {}
    for _, r in dated.iterrows():
        dl.setdefault(r["dt"].strftime("%Y-%m-%d"), []).append((
            r["Ticker"], r["Sector"], r["Timing"], r["Source"],
            str(r["Yahoo Date"]) if pd.notna(r["Yahoo Date"]) else "N/A",
            bool(r["Mismatch"]), bool(r["Confirmed"]),
        ))

    all_years = set(m.year for m in months)
    all_years.add(generated_at.year)
    event_map = {}
    for yr in all_years:
        for ds, evs in get_us_events(yr).items():
            event_map.setdefault(ds, []).extend(evs)

    today_str   = generated_at.strftime("%Y-%m-%d")
    prior_mon_s = prior_monday.strftime("%Y-%m-%d")
    prior_sun_s = prior_sunday.strftime("%Y-%m-%d")
    DAYS = ["MON","TUE","WED","THU","FRI","SAT","SUN"]

    def build_chips(rpts, ds):
        chips = ""
        for ticker, sector, timing, source, yahoo_date, mismatch, confirmed in rpts:
            col  = SECTOR_COLORS.get(sector, "#666")
            safe = sector.replace(" ","_").replace("/","_").replace("&","_")
            cn   = COMPANY_NAMES.get(ticker, ticker).replace("'","\\'").replace('"',"&quot;")
            st   = sector.replace("'","\\'")
            yd_safe = yahoo_date.replace("'","\\'") if yahoo_date else "N/A"
            ir_url  = IR_URLS.get(ticker, f"https://finance.yahoo.com/quote/{ticker}")
            badge = (f'<span class="bdg bmo" title="Before Market Open">{BMO_SVG}</span>' if timing == "BMO"
                     else f'<span class="bdg amc" title="After Market Close">{AMC_SVG}</span>' if timing == "AMC"
                     else "")
            unconf = ('<span class="bdg-uc" title="Unconfirmed — Yahoo only">?</span>') if not confirmed else ""
            warn   = ('<span class="bdg-mm" title="Date conflict">!</span>') if mismatch else ""
            chips += (
                f'<div class="chip s-{safe}" style="--cc:{col}" data-ticker="{ticker}" '
                f'onclick="showCard(\'{ticker}\',\'{cn}\',\'{st}\',\'{timing or "TBD"}\','
                f'\'{ds}\',\'{col}\',\'{source}\',\'{yd_safe}\','
                f'{str(mismatch).lower()},{str(confirmed).lower()},\'{ir_url}\')">'
                f'{ticker}{badge}{unconf}{warn}</div>'
            )
        return chips

    def render_month(ms):
        # ms is a datetime.date (first of the month)
        es_name, es_sub, es_color, es_bg = EARNINGS_SEASON_BY_MONTH[ms.month]
        lbl  = ms.strftime("%B %Y").upper()
        heads = "".join(f'<div class="dname">{d}</div>' for d in DAYS)
        blank = "".join('<div class="dcell empty"></div>' for _ in range(ms.weekday()))
        nm = (ms.replace(month=ms.month+1) if ms.month < 12
              else ms.replace(year=ms.year+1, month=1))
        cells = ""
        for day in range(1, (nm - ms).days + 1):
            do = ms.replace(day=day)          # datetime.date
            ds = do.strftime("%Y-%m-%d")
            cls = "dcell"
            if do.weekday() >= 5: cls += " wknd"
            if ds == today_str:   cls += " today"
            # FIX: do is already a date, compare directly with today_dt (also a date)
            if do < today_dt and ds != today_str: cls += " past"
            rpts = dl.get(ds, [])
            if rpts: cls += " has-e"
            day_events = event_map.get(ds, [])
            if any(e["closed"] for e in day_events): cls += " mkt-closed"
            ev_html = "".join(
                f'<div class="evbadge evbadge-{"holiday" if e["type"]=="holiday" else "retail" if e["type"]=="retail" else "market"}">'
                f'{e["label"]}{"<span class=ev-closed>CLOSED</span>" if e["closed"] else ""}</div>'
                for e in day_events
            )
            chips = build_chips(rpts, ds)
            cells += (f'<div class="{cls}"><span class="dno">{day}</span>'
                      f'{ev_html}<div class="chips">{chips}</div></div>')
        return (
            f'<div class="mblock" style="--es-bg:{es_bg};--es-col:{es_color}">'
            f'<div class="mblock-header">'
            f'<span class="mlabel">{lbl}</span>'
            f'<span class="earn-season-badge" style="--ec:{es_color}">'
            f'<svg viewBox="0 0 14 14" width="10" height="10" style="vertical-align:middle;margin-right:4px">'
            f'<rect x="1" y="5" width="2" height="7" rx="1" fill="{es_color}"/>'
            f'<rect x="4.5" y="3" width="2" height="9" rx="1" fill="{es_color}" opacity=".85"/>'
            f'<rect x="8" y="1" width="2" height="11" rx="1" fill="{es_color}" opacity=".7"/>'
            f'<rect x="11.5" y="4" width="2" height="8" rx="1" fill="{es_color}" opacity=".6"/>'
            f'</svg>{es_name}<span class="earn-season-sub">{es_sub}</span>'
            f'</span></div>'
            f'<div class="cgrid">{heads}{blank}{cells}</div>'
            f'</div>'
        )

    cal = "".join(render_month(ms) for ms in months)

    pw_dates = [prior_monday + timedelta(days=i) for i in range(7)]
    pw_label = f"{prior_monday.strftime('%b %d')} – {prior_sunday.strftime('%b %d, %Y')}"
    has_pw   = any(dl.get(d.strftime("%Y-%m-%d")) for d in pw_dates)

    if has_pw:
        pw_days_html = ""
        for d in pw_dates:
            if d.weekday() >= 5: continue
            ds = d.strftime("%Y-%m-%d")
            rpts = dl.get(ds, [])
            day_events = event_map.get(ds, [])
            is_closed  = any(e["closed"] for e in day_events)
            ev_html = "".join(
                f'<div class="evbadge evbadge-{"holiday" if e["type"]=="holiday" else "retail" if e["type"]=="retail" else "market"}">'
                f'{e["label"]}{"<span class=ev-closed>CLOSED</span>" if e["closed"] else ""}</div>'
                for e in day_events
            )
            chips = build_chips(rpts, ds)
            pw_days_html += (
                f'<div class="pw-day{"  pw-closed" if is_closed else ""}">'
                f'<div class="pw-day-head">'
                f'<span class="pw-dname">{d.strftime("%a").upper()}</span>'
                f'<span class="pw-ddate">{d.strftime("%b %d")}</span>'
                f'</div>{ev_html}'
                f'<div class="chips">{chips if chips else "<span class=pw-none>—</span>"}</div>'
                f'</div>'
            )
        pw_html = (
            f'<div class="pw-panel" id="priorWeekPanel">'
            f'<div class="pw-header">'
            f'<div class="pw-title-group">'
            f'<span class="pw-icon">◷</span>'
            f'<span class="pw-title">Prior Week</span>'
            f'<span class="pw-range">{pw_label}</span>'
            f'</div>'
            f'<button class="pw-toggle" id="pwToggle" onclick="togglePriorWeek()">'
            f'<span id="pwToggleLabel">Show</span>'
            f'<span class="pw-chevron" id="pwChevron">›</span>'
            f'</button></div>'
            f'<div class="pw-body" id="pwBody">'
            f'<div class="pw-grid">{pw_days_html}</div>'
            f'</div></div>'
        )
    else:
        pw_html = (
            f'<div class="pw-panel pw-empty">'
            f'<div class="pw-header">'
            f'<div class="pw-title-group">'
            f'<span class="pw-icon">◷</span>'
            f'<span class="pw-title">Prior Week</span>'
            f'<span class="pw-range">{pw_label}</span>'
            f'</div>'
            f'<span class="pw-none-label">No tracked earnings that week</span>'
            f'</div></div>'
        )

    unann = df[df["Earnings Date"].isna()]
    uhtml = ""
    if not unann.empty:
        rows_h = ""
        for s, tickers in SECTORS.items():
            miss = unann[unann["Sector"] == s]["Ticker"].tolist()
            if not miss: continue
            col  = SECTOR_COLORS[s]
            safe = s.replace(" ","_").replace("/","_").replace("&","_")
            chips_u = "".join(
                f'<span class="uchip s-{safe}" style="--cc:{col}" data-ticker="{t}" '
                f'onclick="showCard(\'{t}\','
                f'\'{COMPANY_NAMES.get(t,t).replace(chr(39),chr(92)+chr(39))}\','
                f'\'{s.replace(chr(39),chr(92)+chr(39))}\','
                f'\'TBD\',\'TBD\',\'{col}\',\'—\',\'N/A\',false,false,'
                f'\'{IR_URLS.get(t,f"https://finance.yahoo.com/quote/{t}")}\')">{t}</span>'
                for t in miss
            )
            rows_h += (f'<tr><td><span class="sbadge" style="background:{col}">{s}</span></td>'
                       f'<td>{chips_u}</td></tr>')
        uhtml = (
            f'<div class="ubox"><div class="ubox-head">'
            f'<span class="ubox-title">NOT YET ANNOUNCED</span>'
            f'<span class="ubox-sub">Click any ticker for details</span>'
            f'</div><table class="utable">'
            f'<thead><tr><th>SECTOR</th><th>TICKERS</th></tr></thead>'
            f'<tbody>{rows_h}</tbody></table></div>'
        )

    nf = len(dated); nu = len(unann); nm = int(df["Mismatch"].sum())
    ts = generated_at.strftime("%d %b %Y, %I:%M %p ET")
    sj = json.dumps(SECTORS); cj = json.dumps(SECTOR_COLORS); nj = json.dumps(COMPANY_NAMES)

    sidebar_html = ""
    for s in SECTORS:
        col  = SECTOR_COLORS[s]
        safe = s.replace(" ","_").replace("/","_").replace("&","_")
        tickers_html = "".join(f'<span class="sleg-ticker">{t}</span>' for t in SECTORS[s])
        sidebar_html += (
            f'<div class="sleg-group">'
            f'<button class="sleg-toggle" onclick="toggleSector(\'{safe}\')" style="--cc:{col}">'
            f'<span class="sleg-label">{s}</span>'
            f'<span class="sleg-arrow" id="arrow-{safe}">›</span>'
            f'</button>'
            f'<div class="sleg-tickers" id="tickers-{safe}">{tickers_html}</div>'
            f'</div>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Earnings Calendar — Consumer &amp; Retail</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}

:root{{
  --bg0:#03040d;
  --bg1:#070a18;
  --bg2:#0a0e20;
  --bg3:#0e1228;
  --bg4:#131830;
  --bg5:#181e38;
  --glass-light:rgba(255,255,255,0.04);
  --glass-mid:rgba(255,255,255,0.07);
  --glass-heavy:rgba(255,255,255,0.10);
  --glass-border:rgba(255,255,255,0.08);
  --glass-border2:rgba(255,255,255,0.14);
  --glass-border3:rgba(255,255,255,0.22);
  --t0:#f2f4ff;
  --t1:#b4bcd8;
  --t2:#636b8a;
  --t3:#363c58;
  --accent:#5b9cf6;
  --accent2:#7eb8ff;
  --accent-glow:rgba(91,156,246,0.18);
  --bmo:#ffd95a;
  --amc:#c8b8ff;
  --unconf:#ff9f43;
  --conflict:#ff5757;
  --mono:'JetBrains Mono',monospace;
  --sans:'Inter',-apple-system,sans-serif;
  --sidebar-w:256px;
  --r:10px;
  --r-lg:16px;
  --r-xl:20px;
  --ease:cubic-bezier(0.4,0,0.2,1);
  --dur:0.22s;
}}

::-webkit-scrollbar{{width:4px;height:4px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--bg5);border-radius:4px}}
::-webkit-scrollbar-thumb:hover{{background:var(--glass-border2)}}

body{{
  font-family:var(--sans);
  background:var(--bg0);
  color:var(--t1);
  min-height:100vh;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
  background-image:
    radial-gradient(ellipse 80% 50% at 20% 0%, rgba(59,91,180,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 100%, rgba(120,60,180,0.08) 0%, transparent 60%);
}}
.page-wrap{{display:flex;min-height:100vh;}}

.sidebar{{
  width:var(--sidebar-w);flex-shrink:0;
  background:linear-gradient(180deg,rgba(10,14,32,0.95) 0%,rgba(7,10,24,0.98) 100%);
  border-right:1px solid var(--glass-border);
  position:sticky;top:0;height:100vh;
  display:flex;flex-direction:column;
  transition:width var(--dur) var(--ease);
  z-index:200;overflow:hidden;
  backdrop-filter:blur(24px);
  -webkit-backdrop-filter:blur(24px);
}}
.sidebar.collapsed{{width:0;border-right-color:transparent;}}
.content{{flex:1;min-width:0;display:flex;flex-direction:column;}}

.sidebar-head{{
  padding:18px 16px 14px;
  border-bottom:1px solid var(--glass-border);
  flex-shrink:0;
  background:var(--glass-light);
}}
.sidebar-title{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:var(--t3);text-transform:uppercase;letter-spacing:1.4px;
  white-space:nowrap;
}}
.sidebar-body{{overflow-y:auto;flex:1;padding:4px 0 20px;}}

.sleg-group{{border-bottom:1px solid var(--glass-border);}}
.sleg-toggle{{
  display:flex;align-items:center;justify-content:space-between;
  width:100%;padding:7px 14px;
  background:none;border:none;cursor:pointer;
  transition:background var(--dur);gap:8px;
}}
.sleg-toggle:hover{{background:var(--glass-light);}}
.sleg-label{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:#fff;background:var(--cc,#444);
  padding:2px 8px;border-radius:4px;
  text-shadow:0 1px 4px rgba(0,0,0,.6);
  white-space:nowrap;flex:1;text-align:left;
  border:1px solid rgba(255,255,255,0.1);
}}
.sleg-arrow{{
  font-size:12px;color:var(--t3);
  transition:transform var(--dur) var(--ease);flex-shrink:0;
}}
.sleg-arrow.open{{transform:rotate(90deg);color:var(--t2);}}
.sleg-tickers{{
  display:flex;flex-wrap:wrap;gap:3px;
  padding:0 14px;overflow:hidden;
  max-height:0;
  transition:max-height 0.3s var(--ease),padding 0.2s;
}}
.sleg-tickers.open{{max-height:220px;padding:0 14px 10px;}}
.sleg-ticker{{
  font-family:var(--mono);font-size:7.5px;color:var(--t2);
  background:var(--glass-light);border:1px solid var(--glass-border);
  border-radius:3px;padding:1px 5px;
  transition:color var(--dur),border-color var(--dur);
}}
.sleg-ticker:hover{{color:var(--t0);border-color:var(--glass-border2);}}

.topbar{{
  height:54px;
  background:rgba(7,10,24,0.7);
  backdrop-filter:blur(28px) saturate(180%);
  -webkit-backdrop-filter:blur(28px) saturate(180%);
  border-bottom:1px solid var(--glass-border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;position:sticky;top:0;z-index:300;gap:12px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.06);
}}
.topbar-left{{display:flex;align-items:center;gap:12px;}}
.page-title{{
  font-size:13.5px;font-weight:700;color:var(--t0);
  letter-spacing:-.3px;white-space:nowrap;
}}
.title-dot{{
  width:6px;height:6px;border-radius:50%;
  background:var(--accent);
  box-shadow:0 0 10px var(--accent),0 0 20px rgba(91,156,246,0.4);
  flex-shrink:0;
  animation:dotPulse 3s ease-in-out infinite;
}}
@keyframes dotPulse{{
  0%,100%{{box-shadow:0 0 8px var(--accent),0 0 16px rgba(91,156,246,0.3);}}
  50%{{box-shadow:0 0 14px var(--accent),0 0 28px rgba(91,156,246,0.5);}}
}}
.vdiv{{width:1px;height:18px;background:var(--glass-border2);}}
.topbar-meta{{font-size:10px;color:var(--t2);white-space:nowrap;}}
.topbar-right{{display:flex;align-items:center;gap:10px;flex-shrink:0;}}

.tstat{{
  display:flex;flex-direction:column;align-items:center;
  padding:5px 12px;border-radius:10px;
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  backdrop-filter:blur(8px);
  transition:background var(--dur),border-color var(--dur);
}}
.tstat:hover{{background:var(--glass-mid);border-color:var(--glass-border2);}}
.tstat-num{{
  font-family:var(--mono);font-size:15px;font-weight:700;
  color:var(--t0);line-height:1.1;
}}
.tstat-lbl{{
  font-size:7.5px;color:var(--t2);
  text-transform:uppercase;letter-spacing:.9px;margin-top:2px;
}}

.sidebar-toggle{{
  display:flex;align-items:center;justify-content:center;
  width:28px;height:28px;border-radius:8px;
  background:var(--glass-light);border:1px solid var(--glass-border);
  color:var(--t1);cursor:pointer;font-size:15px;line-height:1;
  transition:background var(--dur),color var(--dur),transform var(--dur);
  flex-shrink:0;
}}
.sidebar-toggle:hover{{background:var(--glass-mid);color:var(--t0);}}
.sidebar-toggle.open{{transform:scaleX(-1);}}

.timingbar{{
  background:rgba(7,10,24,0.6);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--glass-border);
  padding:9px 20px 11px;
  display:flex;align-items:center;gap:9px;
  font-size:11px;color:var(--t2);flex-wrap:wrap;
}}
.key-label{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:var(--t2);text-transform:uppercase;letter-spacing:1px;
}}
.tpill{{
  display:inline-flex;align-items:center;gap:5px;
  font-size:9px;font-weight:700;
  padding:3px 9px;border-radius:6px;
  font-family:var(--mono);letter-spacing:.3px;white-space:nowrap;
  backdrop-filter:blur(8px);
}}
.tpill.pre{{
  background:rgba(255,217,90,.1);color:var(--bmo);
  border:1px solid rgba(255,217,90,.25);
}}
.tpill.aft{{
  background:rgba(200,184,255,.1);color:var(--amc);
  border:1px solid rgba(200,184,255,.25);
}}
.tpill.unc{{
  background:rgba(255,159,67,.1);color:var(--unconf);
  border:1px solid rgba(255,159,67,.25);
}}
.tpill.mis{{
  background:rgba(255,87,87,.12);color:var(--conflict);
  border:1px solid rgba(255,87,87,.3);
}}
.key-sep{{color:var(--t3);}}
.key-desc{{font-size:10px;color:var(--t2);}}
.event-legend{{
  display:flex;flex-wrap:wrap;align-items:center;gap:7px;
  width:100%;margin-top:8px;padding-top:8px;
  border-top:1px solid var(--glass-border);
}}
.evleg-label{{
  font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t3);text-transform:uppercase;letter-spacing:1px;
}}
.evleg-item{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;color:var(--t2);}}
.evleg-dot{{width:7px;height:7px;border-radius:2px;flex-shrink:0;}}
.evleg-dot.holiday{{background:#3d5f96;}}
.evleg-dot.retail{{background:#7a5a2a;}}
.evleg-dot.closed{{background:rgba(200,50,50,.6);border:1px solid rgba(200,50,50,.8);}}

.search-bar{{
  background:rgba(7,10,24,0.55);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--glass-border);
  padding:8px 20px;
  display:flex;align-items:center;gap:10px;
  position:sticky;top:54px;z-index:299;
}}
.search-wrap{{position:relative;display:flex;align-items:center;}}
.search-icon{{
  position:absolute;left:10px;color:var(--t3);
  font-size:13px;pointer-events:none;
}}
.search-input{{
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  border-radius:8px;
  padding:6px 30px 6px 30px;
  font-family:var(--mono);font-size:11px;color:var(--t0);
  outline:none;width:210px;
  transition:border-color var(--dur),background var(--dur),box-shadow var(--dur);
}}
.search-input::placeholder{{color:var(--t3);}}
.search-input:focus{{
  border-color:rgba(91,156,246,.5);
  background:var(--glass-mid);
  box-shadow:0 0 0 3px rgba(91,156,246,.1),inset 0 1px 0 rgba(255,255,255,.05);
}}
.search-clear{{
  position:absolute;right:8px;
  background:none;border:none;color:var(--t3);
  cursor:pointer;font-size:14px;line-height:1;
  padding:0;display:none;
  transition:color var(--dur);
}}
.search-clear:hover{{color:var(--t1);}}
.search-clear.on{{display:block;}}
.search-hint{{font-size:10px;color:var(--t2);font-family:var(--mono);}}

.pw-panel{{
  margin:18px 20px 0;
  border-radius:var(--r-lg);
  border:1px solid var(--glass-border);
  overflow:hidden;
  background:rgba(10,14,32,0.6);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  box-shadow:0 4px 24px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.05);
}}
.pw-panel.pw-empty{{margin-bottom:8px;}}
.pw-header{{
  padding:10px 16px;
  display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(90deg,rgba(91,156,246,0.06) 0%,transparent 70%);
  border-bottom:1px solid var(--glass-border);
}}
.pw-title-group{{display:flex;align-items:center;gap:10px;}}
.pw-icon{{font-size:13px;color:var(--accent);opacity:.8;}}
.pw-title{{
  font-family:var(--mono);font-size:10.5px;font-weight:700;
  color:var(--t0);letter-spacing:.3px;
}}
.pw-range{{
  font-family:var(--mono);font-size:9px;color:var(--t2);
  padding:2px 8px;
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  border-radius:4px;
}}
.pw-none-label{{font-size:10px;color:var(--t3);font-style:italic;}}
.pw-toggle{{
  display:inline-flex;align-items:center;gap:5px;
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  border-radius:7px;padding:4px 11px;
  font-family:var(--mono);font-size:9.5px;font-weight:700;
  color:var(--t1);cursor:pointer;
  transition:background var(--dur),border-color var(--dur),color var(--dur);
}}
.pw-toggle:hover{{
  background:var(--glass-mid);
  border-color:rgba(91,156,246,.4);
  color:var(--t0);
}}
.pw-chevron{{
  font-size:13px;line-height:1;
  transition:transform var(--dur) var(--ease);
  display:inline-block;
}}
.pw-chevron.open{{transform:rotate(90deg);}}
.pw-body{{
  max-height:0;overflow:hidden;
  transition:max-height 0.38s var(--ease);
}}
.pw-body.open{{max-height:620px;}}
.pw-grid{{
  display:grid;grid-template-columns:repeat(5,1fr);
  gap:6px;padding:10px;
}}
.pw-day{{
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  border-radius:var(--r);
  padding:9px 8px 8px;min-height:76px;
  transition:background var(--dur);
}}
.pw-day.pw-closed{{
  background:rgba(30,8,8,0.4);
  border-color:rgba(180,40,40,.15);
}}
.pw-day-head{{
  display:flex;align-items:baseline;gap:6px;margin-bottom:6px;
}}
.pw-dname{{
  font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t3);letter-spacing:.8px;
}}
.pw-ddate{{
  font-family:var(--mono);font-size:10.5px;font-weight:600;color:var(--t1);
}}
.pw-none{{font-family:var(--mono);font-size:8.5px;color:var(--t3);}}

.main{{padding:18px 20px 32px;max-width:1440px;margin:0 auto;}}

.mblock{{
  margin-bottom:28px;
  border-radius:var(--r-lg);overflow:hidden;
  border:1px solid var(--glass-border);
  background:rgba(10,14,32,0.5);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  box-shadow:0 8px 32px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,0.05);
}}
.mblock-header{{
  padding:11px 16px 9px;
  border-bottom:1px solid var(--glass-border);
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:8px;
  background:linear-gradient(90deg,var(--es-bg,rgba(255,255,255,0.02)) 0%,transparent 60%);
}}
.mlabel{{
  font-family:var(--mono);font-size:12.5px;font-weight:700;
  color:var(--t0);letter-spacing:.5px;
}}
.earn-season-badge{{
  display:inline-flex;align-items:center;
  font-family:var(--mono);font-size:9px;font-weight:700;
  padding:3px 10px;border-radius:6px;white-space:nowrap;
  background:color-mix(in srgb,var(--ec) 8%,transparent);
  color:var(--ec);
  border:1px solid color-mix(in srgb,var(--ec) 20%,transparent);
  backdrop-filter:blur(8px);
}}
.earn-season-sub{{
  font-size:7.5px;font-weight:400;opacity:.6;margin-left:6px;
}}

.cgrid{{
  display:grid;grid-template-columns:repeat(7,1fr);
  gap:3px;padding:6px;
  background:rgba(7,10,24,0.4);
}}
.dname{{
  text-align:center;font-family:var(--mono);
  font-size:8.5px;font-weight:700;
  color:var(--t3);padding:5px 0;letter-spacing:1px;
}}

.dcell{{
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  border-radius:var(--r);
  min-height:98px;padding:8px 7px 6px;
  transition:border-color var(--dur),background var(--dur);
  position:relative;
}}
.dcell.empty{{background:transparent;border-color:transparent;pointer-events:none;}}
.dcell.wknd{{background:rgba(3,4,13,0.5);opacity:.3;}}
.dcell.past{{opacity:.4;filter:saturate(0.6);}}
.dcell.today{{
  border-color:rgba(91,156,246,.55) !important;
  background:rgba(91,156,246,0.07);
  box-shadow:0 0 0 1px rgba(91,156,246,.15),0 4px 16px rgba(91,156,246,.08),inset 0 1px 0 rgba(91,156,246,.12);
}}
.dcell.today::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent 0%,var(--accent) 30%,var(--accent2) 70%,transparent 100%);
  border-radius:var(--r) var(--r) 0 0;
}}
.dcell.today .dno{{color:var(--accent)!important;font-weight:700;}}
.dcell.has-e{{border-color:rgba(255,255,255,0.09);}}
.dcell.mkt-closed{{background:rgba(28,6,6,0.5);border-color:rgba(160,30,30,.12);}}

.dno{{
  font-family:var(--mono);font-size:10px;font-weight:500;
  color:var(--t2);margin-bottom:4px;display:block;
}}

.evbadge{{
  font-family:var(--mono);font-size:7px;font-weight:700;
  padding:1px 5px;border-radius:3px;margin-bottom:2px;
  display:inline-block;letter-spacing:.2px;
  white-space:nowrap;max-width:100%;
  overflow:hidden;text-overflow:ellipsis;
  backdrop-filter:blur(4px);
}}
.evbadge-holiday{{
  background:rgba(61,95,150,.18);color:#7aa0d4;
  border:1px solid rgba(61,95,150,.3);
}}
.evbadge-retail{{
  background:rgba(122,90,42,.2);color:#c9a870;
  border:1px solid rgba(122,90,42,.35);
}}
.evbadge-market{{
  background:rgba(60,173,168,.1);color:#6dccc8;
  border:1px solid rgba(60,173,168,.22);
}}
.ev-closed{{
  font-size:6px;font-weight:900;
  background:rgba(200,40,40,.8);color:#fff;
  padding:0 3px;border-radius:2px;
  margin-left:3px;letter-spacing:.3px;vertical-align:middle;
}}

.chips{{display:flex;flex-wrap:wrap;gap:3px;margin-top:3px;}}
.chip{{
  display:inline-flex;align-items:center;gap:2px;
  background:var(--cc,#444);
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:#fff;
  padding:3px 6px;border-radius:6px;
  cursor:pointer;white-space:nowrap;
  transition:transform 0.14s,filter 0.14s,box-shadow 0.14s,opacity 0.14s;
  letter-spacing:.15px;
  text-shadow:0 1px 4px rgba(0,0,0,.55);
  border:1px solid rgba(255,255,255,0.1);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.15);
}}
.chip:hover{{
  transform:translateY(-2px) scale(1.07);
  filter:brightness(1.25) saturate(1.1);
  box-shadow:0 6px 16px rgba(0,0,0,.5),0 0 0 1px rgba(255,255,255,.18),inset 0 1px 0 rgba(255,255,255,.2);
  z-index:10;position:relative;
}}
.chip.dimmed{{opacity:.08;pointer-events:none;}}

.bdg{{display:inline-flex;align-items:center;line-height:1;}}
.bdg-uc{{
  font-family:var(--mono);font-size:8px;font-weight:900;
  background:rgba(255,159,67,.25);color:var(--unconf);
  border:1px solid rgba(255,159,67,.45);
  border-radius:3px;padding:0 3px;line-height:1.4;
}}
.bdg-mm{{
  font-family:var(--mono);font-size:8px;font-weight:900;
  background:rgba(255,87,87,.3);color:var(--conflict);
  border:1px solid rgba(255,87,87,.5);
  border-radius:3px;padding:0 3px;line-height:1.4;
  animation:warnPulse 2s ease-in-out infinite;
}}
@keyframes warnPulse{{
  0%,100%{{box-shadow:0 0 0 0 rgba(255,87,87,0);}}
  50%{{box-shadow:0 0 0 3px rgba(255,87,87,.2);}}
}}

.ubox{{
  margin:0 20px 32px;
  background:rgba(10,14,32,0.55);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border:1px solid var(--glass-border);
  border-radius:var(--r-lg);overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,.3),inset 0 1px 0 rgba(255,255,255,.04);
}}
.ubox-head{{
  padding:13px 20px;border-bottom:1px solid var(--glass-border);
  display:flex;align-items:baseline;gap:14px;
  background:var(--glass-light);
}}
.ubox-title{{
  font-family:var(--mono);font-size:11px;font-weight:700;
  color:var(--t0);letter-spacing:.5px;
}}
.ubox-sub{{font-size:10px;color:var(--t2);}}
.utable{{width:100%;border-collapse:collapse;}}
.utable th{{
  text-align:left;padding:7px 16px;
  font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t2);border-bottom:1px solid var(--glass-border);
  text-transform:uppercase;letter-spacing:.8px;
}}
.utable td{{
  padding:8px 16px;border-bottom:1px solid var(--glass-border);
  vertical-align:middle;
}}
.utable tr:last-child td{{border-bottom:none;}}
.utable tr:hover td{{background:var(--glass-light);}}
.sbadge{{
  font-family:var(--mono);font-size:9px;font-weight:700;color:#fff;
  padding:2px 8px;border-radius:4px;white-space:nowrap;
  text-shadow:0 1px 4px rgba(0,0,0,.5);
  border:1px solid rgba(255,255,255,.1);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.12);
}}
.uchip{{
  display:inline-flex;align-items:center;
  background:var(--cc,#444);
  font-family:var(--mono);font-size:9px;font-weight:700;color:#fff;
  padding:3px 7px;border-radius:5px;margin:2px;cursor:pointer;
  transition:transform 0.14s,filter 0.14s,opacity 0.14s;
  text-shadow:0 1px 4px rgba(0,0,0,.5);
  border:1px solid rgba(255,255,255,.1);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.12);
}}
.uchip:hover{{
  transform:translateY(-1px) scale(1.07);
  filter:brightness(1.22);
  box-shadow:0 4px 12px rgba(0,0,0,.4);
}}
.uchip.dimmed{{opacity:.08;pointer-events:none;}}

.footer{{
  border-top:1px solid var(--glass-border);
  padding:11px 20px;
  font-family:var(--mono);font-size:9px;color:var(--t3);
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(7,10,24,0.6);
  backdrop-filter:blur(16px);
}}

.overlay{{
  display:none;position:fixed;inset:0;
  background:rgba(0,0,0,.72);
  backdrop-filter:blur(20px) saturate(120%);
  -webkit-backdrop-filter:blur(20px) saturate(120%);
  z-index:999;align-items:center;justify-content:center;
}}
.overlay.on{{display:flex;}}
.modal{{
  background:linear-gradient(145deg,rgba(18,22,44,0.96) 0%,rgba(12,16,34,0.98) 100%);
  border:1px solid var(--glass-border2);
  border-radius:var(--r-xl);
  padding:28px;max-width:420px;width:90%;
  box-shadow:0 40px 80px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.04),inset 0 1px 0 rgba(255,255,255,.07);
  position:relative;
  animation:popIn .24s cubic-bezier(.34,1.4,.64,1);
}}
@keyframes popIn{{
  from{{transform:scale(.9) translateY(12px);opacity:0}}
  to{{transform:scale(1) translateY(0);opacity:1}}
}}
.modal-close{{
  position:absolute;top:14px;right:16px;
  background:var(--glass-light);
  border:1px solid var(--glass-border);
  border-radius:7px;width:26px;height:26px;
  font-size:15px;color:var(--t2);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:background var(--dur),color var(--dur);
}}
.modal-close:hover{{background:var(--glass-mid);color:var(--t0);}}
.modal-ticker{{
  font-family:var(--mono);font-size:30px;font-weight:700;
  margin-bottom:3px;line-height:1;
  filter:drop-shadow(0 0 12px currentColor);
}}
.modal-name{{font-size:12px;color:var(--t2);margin-bottom:22px;}}
.modal-banner{{
  border-radius:9px;padding:10px 14px;margin-bottom:14px;
  font-size:11px;line-height:1.6;display:none;
  backdrop-filter:blur(8px);
}}
.modal-banner.on{{display:block;}}
.modal-banner.warn{{
  background:rgba(255,87,87,.08);
  border:1px solid rgba(255,87,87,.25);color:#ff7575;
}}
.modal-banner.info{{
  background:rgba(255,159,67,.07);
  border:1px solid rgba(255,159,67,.22);color:#ffb347;
}}
.modal-row{{
  display:flex;justify-content:space-between;align-items:center;
  padding:9px 0;border-bottom:1px solid var(--glass-border);
  font-size:12px;
}}
.modal-row:last-of-type{{border-bottom:none;}}
.modal-key{{
  color:var(--t2);font-size:9.5px;
  text-transform:uppercase;letter-spacing:.7px;font-weight:600;
}}
.modal-val{{
  color:var(--t0);font-family:var(--mono);
  font-size:11.5px;font-weight:600;
}}
.modal-val.secondary{{color:var(--t1);font-size:11px;font-weight:400;}}
.modal-source-row{{
  display:flex;justify-content:space-between;
  padding:9px 0;border-bottom:1px solid var(--glass-border);gap:14px;
}}
.modal-source-col{{display:flex;flex-direction:column;gap:4px;flex:1;}}
.modal-source-label{{
  color:var(--t2);font-size:9px;
  text-transform:uppercase;letter-spacing:.7px;font-weight:600;
}}
.modal-source-date{{
  font-family:var(--mono);font-size:12px;font-weight:600;color:var(--t0);
}}
.modal-source-date.conflict{{color:var(--conflict);}}
.modal-ir-link{{
  display:inline-flex;align-items:center;gap:7px;
  margin-top:18px;
  font-family:var(--mono);font-size:10px;font-weight:600;
  color:var(--accent);text-decoration:none;
  border:1px solid rgba(91,156,246,.22);
  border-radius:9px;padding:9px 14px;width:100%;
  justify-content:center;
  background:rgba(91,156,246,.05);
  backdrop-filter:blur(8px);
  transition:background var(--dur),border-color var(--dur),box-shadow var(--dur);
}}
.modal-ir-link:hover{{
  background:rgba(91,156,246,.1);
  border-color:rgba(91,156,246,.45);
  box-shadow:0 0 20px rgba(91,156,246,.12);
}}

/* ── Mobile ── */
@media (max-width: 768px) {{
  .sidebar {{ width: 0; border-right-color: transparent; }}
  .sidebar-toggle {{ }}
  .topbar {{ padding: 0 12px; height: 48px; gap: 8px; }}
  .page-title {{ font-size: 11.5px; }}
  .topbar-meta {{ display: none; }}
  .vdiv {{ display: none; }}
  .tstat {{ padding: 4px 8px; }}
  .tstat-num {{ font-size: 12px; }}
  .tstat-lbl {{ font-size: 6.5px; }}
  .timingbar {{ flex-direction: column; align-items: flex-start; gap: 6px; padding: 8px 12px; }}
  .search-bar {{ padding: 7px 12px; }}
  .search-input {{ width: 160px; }}
  .cgrid {{
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 2px;
    padding: 3px;
  }}
  .dcell {{ min-height: 64px; padding: 5px 3px 4px; }}
  .dno {{ font-size: 8px; }}
  .chip {{
    font-size: 7.5px;
    padding: 2px 4px;
    border-radius: 4px;
  }}
  .evbadge {{ font-size: 6px; padding: 1px 3px; }}
  .dname {{ font-size: 7px; padding: 3px 0; }}
  .pw-grid {{ grid-template-columns: 1fr; gap: 4px; }}
  .pw-panel {{ margin: 12px 10px 0; }}
  .main {{ padding: 12px 10px 24px; }}
  .mblock {{ margin-bottom: 18px; }}
  .ubox {{ margin: 0 10px 24px; }}
  .modal {{ padding: 20px 16px; }}
  .modal-ticker {{ font-size: 24px; }}
  .search-bar {{ top: 48px; }}
}}

@media (max-width: 480px) {{
  .cgrid {{ grid-template-columns: 1fr; }}
  .dcell.empty {{ display: none; }}
  .dcell.wknd:not(.has-e) {{ display: none; }}
  .topbar-right {{ gap: 6px; }}
  .tstat-lbl {{ display: none; }}
}}
</style>
</head>
<body>
<div class="page-wrap">

<aside class="sidebar" id="sidebar">
  <div class="sidebar-head">
    <span class="sidebar-title">Sectors</span>
  </div>
  <div class="sidebar-body">{sidebar_html}</div>
</aside>

<div class="content">

<header class="topbar">
  <div class="topbar-left">
    <button class="sidebar-toggle open" id="sidebarToggle"
            onclick="toggleSidebar()" title="Toggle sectors">&#8249;</button>
    <span class="title-dot"></span>
    <span class="page-title">Earnings Calendar</span>
    <span class="vdiv"></span>
    <span class="topbar-meta">Consumer &amp; Retail · {ts}</span>
  </div>
  <div class="topbar-right">
    <div class="tstat">
      <span class="tstat-num" style="color:var(--accent)">{nf}</span>
      <span class="tstat-lbl">Dates Found</span>
    </div>
    <div class="tstat">
      <span class="tstat-num" style="color:var(--t2)">{nu}</span>
      <span class="tstat-lbl">Unannounced</span>
    </div>
    <div class="tstat">
      <span class="tstat-num" style="color:var(--conflict)">{nm}</span>
      <span class="tstat-lbl">Mismatches</span>
    </div>
  </div>
</header>

<div class="timingbar">
  <span class="key-label">Key</span>
  <span class="tpill pre">{BMO_SVG_KEY}&nbsp;BMO</span>
  <span class="key-desc">Before market open</span>
  <span class="key-sep">·</span>
  <span class="tpill aft">{AMC_SVG_KEY}&nbsp;AMC</span>
  <span class="key-desc">After market close</span>
  <span class="key-sep">·</span>
  <span class="tpill unc">? Unconfirmed</span>
  <span class="key-desc">Yahoo only</span>
  <span class="key-sep">·</span>
  <span class="tpill mis">! Conflict</span>
  <span class="key-desc">Sources disagree</span>
  <span class="key-sep">·</span>
  <span class="key-desc" style="color:var(--t3)">Click any ticker for details</span>
  <div class="event-legend">
    <span class="evleg-label">Events</span>
    <span class="evleg-item"><span class="evleg-dot holiday"></span>Federal Holiday</span>
    <span class="evleg-item"><span class="evleg-dot retail"></span>Retail / Consumer Event</span>
    <span class="evleg-item"><span class="evleg-dot closed"></span>Market Closed</span>
  </div>
</div>

<div class="search-bar">
  <div class="search-wrap">
    <span class="search-icon">⌕</span>
    <input class="search-input" id="searchInput" type="text"
           placeholder="Search ticker…" autocomplete="off" spellcheck="false">
    <button class="search-clear" id="searchClear" onclick="clearSearch()">×</button>
  </div>
  <span class="search-hint" id="searchHint"></span>
</div>

{pw_html}

<main class="main">{cal}</main>

{uhtml}

<footer class="footer">
  <span>Neil J Kanatt · NASDAQ API + Yahoo Finance</span>
  <span id="refreshLabel">Next refresh at 4 AM &amp; 10 PM ET · {ts}</span>
</footer>

</div>
</div>

<div class="overlay" id="overlay" onclick="closeModal(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeModal()">×</button>
    <div class="modal-ticker" id="mTicker"></div>
    <div class="modal-name"   id="mName"></div>
    <div class="modal-banner warn" id="mMismatch">
      ⚠ Date conflict — NASDAQ and Yahoo show different dates. Verify before acting.
    </div>
    <div class="modal-banner info" id="mUnconf">
      ❗ Unconfirmed — sourced from Yahoo Finance only. Not yet on NASDAQ.
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

let sidebarOpen = true;
function toggleSidebar() {{
  sidebarOpen = !sidebarOpen;
  document.getElementById('sidebar').classList.toggle('collapsed', !sidebarOpen);
  document.getElementById('sidebarToggle').classList.toggle('open', sidebarOpen);
}}

function toggleSector(safe) {{
  const t = document.getElementById('tickers-' + safe);
  const a = document.getElementById('arrow-'   + safe);
  const open = t.classList.contains('open');
  t.classList.toggle('open', !open);
  a.classList.toggle('open', !open);
}}

let pwOpen = false;
function togglePriorWeek() {{
  pwOpen = !pwOpen;
  document.getElementById('pwBody').classList.toggle('open', pwOpen);
  document.getElementById('pwChevron').classList.toggle('open', pwOpen);
  document.getElementById('pwToggleLabel').textContent = pwOpen ? 'Hide' : 'Show';
}}

function scheduleSmartRefresh() {{
  const now = new Date();
  const fmt = new Intl.DateTimeFormat('en-US', {{
    timeZone:'America/New_York',
    hour:'numeric', minute:'numeric', second:'numeric', hour12:false
  }});
  const p   = fmt.formatToParts(now);
  const h   = parseInt(p.find(x => x.type==='hour').value);
  const m   = parseInt(p.find(x => x.type==='minute').value);
  const s   = parseInt(p.find(x => x.type==='second').value);
  const sec = h*3600 + m*60 + s;
  let minDiff = Infinity;
  for (const t of [4*3600, 22*3600]) {{
    let d = t - sec; if (d <= 0) d += 86400;
    if (d < minDiff) minDiff = d;
  }}
  const next = new Date(now.getTime() + minDiff*1000);
  const lbl  = next.toLocaleTimeString('en-US', {{
    timeZone:'America/New_York', hour:'numeric', minute:'2-digit', hour12:true
  }});
  const el = document.getElementById('refreshLabel');
  if (el) el.textContent = 'Next refresh at ' + lbl + ' ET · {ts}';
  setTimeout(() => location.reload(), minDiff*1000);
}}
scheduleSmartRefresh();

const searchInput = document.getElementById('searchInput');
const searchClear = document.getElementById('searchClear');
const searchHint  = document.getElementById('searchHint');
searchInput.addEventListener('input', function() {{
  const q = this.value.trim().toUpperCase();
  searchClear.classList.toggle('on', q.length > 0);
  applySearch(q);
}});
function clearSearch() {{
  searchInput.value = '';
  searchClear.classList.remove('on');
  searchHint.textContent = '';
  applySearch('');
}}
function applySearch(q) {{
  const chips  = document.querySelectorAll('.chip');
  const uchips = document.querySelectorAll('.uchip');
  if (!q) {{
    chips.forEach(c  => c.classList.remove('dimmed'));
    uchips.forEach(c => c.classList.remove('dimmed'));
    searchHint.textContent = ''; return;
  }}
  let found = 0;
  chips.forEach(c => {{
    const match = c.dataset.ticker && c.dataset.ticker.toUpperCase().includes(q);
    c.classList.toggle('dimmed', !match); if (match) found++;
  }});
  uchips.forEach(c => {{
    const match = c.dataset.ticker && c.dataset.ticker.toUpperCase().includes(q);
    c.classList.toggle('dimmed', !match); if (match) found++;
  }});
  searchHint.textContent = found
    ? found + ' result' + (found > 1 ? 's' : '')
    : 'No results';
}}

function showCard(ticker,name,sector,timing,nasdaqDate,color,source,yahooDate,mismatch,confirmed,irUrl) {{
  document.getElementById('mTicker').textContent = ticker;
  document.getElementById('mTicker').style.color = color;
  document.getElementById('mName').textContent   = name;
  document.getElementById('mSector').textContent = sector;
  const nd = document.getElementById('mNasdaqDate');
  const yd = document.getElementById('mYahooDate');
  nd.textContent = (!confirmed || nasdaqDate === 'TBD') ? 'Not on NASDAQ' : nasdaqDate;
  yd.textContent = (yahooDate && yahooDate !== 'N/A')   ? yahooDate       : 'Not available';
  nd.classList.toggle('conflict', mismatch);
  yd.classList.toggle('conflict', mismatch);
  document.getElementById('mTiming').textContent =
    timing === 'BMO' ? 'Before Market Open' :
    timing === 'AMC' ? 'After Market Close'  :
    timing === 'TBD' ? 'Not yet confirmed'   : 'Unconfirmed';
  document.getElementById('mSource').textContent = source;
  document.getElementById('mMismatch').classList.toggle('on', mismatch);
  document.getElementById('mUnconf').classList.toggle('on', !confirmed && nasdaqDate !== 'TBD');
  document.getElementById('mIRLink').href = irUrl || ('https://finance.yahoo.com/quote/' + ticker);
  document.getElementById('overlay').classList.add('on');
}}
function closeModal(e) {{
  if (!e || e.target === document.getElementById('overlay'))
    document.getElementById('overlay').classList.remove('on');
}}
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') document.getElementById('overlay').classList.remove('on');
}});
</script>
</body>
</html>"""
    return html

# ── RUN ──
df, generated_at = run_fetch()
html = build_html(df, generated_at)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done — index.html written")
