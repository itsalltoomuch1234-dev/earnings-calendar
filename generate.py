# -*- coding: utf-8 -*-
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
    "CPB":"Campbell's Company","SJM":"J.M. Smucker",
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
    "UAA":  "https://about.underarmour.com/en/investors/press-releases--events---presentations.html",
    "AEO":  "https://investors.ae.com/investor-home/default.aspx",
    "ANF":  "https://corporate.abercrombie.com/investors",
    "VFC":  "https://www.vfc.com/investors",
    "GAP":  "https://investors.gapinc.com/Investor-Relation/default.aspx",
    "BIRK": "https://www.birkenstock-holding.com/",
    "LEVI": "https://investors.levistrauss.com/home/default.aspx",
    "ONON": "https://investors.on-running.com/home/default.aspx",
    "LULU": "https://corporate.lululemon.com/investors",
    "DECK": "https://ir.deckers.com/",
    "NKE":  "https://investors.nike.com",
    "DLTR": "https://corporate.dollartree.com/investors",
    "DG":   "https://investor.dollargeneral.com",
    "ROST": "https://investors.rossstores.com",
    "TJX":  "https://investor.tjx.com/",
    "GOOS": "https://investors.canadagoose.com",
    "COTY": "https://investors.coty.com",
    "CPRI": "https://capriholdings.com/",
    "ELF":  "https://investor.elfbeauty.com/stock-and-financial/events-and-presentations",
    "ULTA": "https://www.ulta.com/investor",
    "RL":   "https://corporate.ralphlauren.com/investor-relations",
    "TPR":  "https://www.tapestry.com/investors/",
    "EL":   "https://www.elcompanies.com/en/investors",
    "KSS":  "https://investors.kohls.com/overview/default.aspx",
    "BBWI": "https://www.bbwinc.com/investors",
    "M":    "https://www.macysinc.com/investors/",
    "ACI":  "https://www.albertsonscompanies.com/investors/overview/default.aspx",
    "BBY":  "https://investors.bestbuy.com",
    "KR":   "https://ir.kroger.com",
    "TGT":  "https://corporate.target.com/investors",
    "LOW":  "https://corporate.lowes.com/investors",
    "HD":   "https://ir.homedepot.com",
    "COST": "https://investor.costco.com",
    "WMT":  "https://stock.walmart.com",
    "NCLH": "https://www.nclhltd.com/investors",
    "RCL":  "https://www.rclinvestor.com/",
    "CCL":  "https://www.carnivalcorp.com/investors/",
    "TAP":  "https://ir.molsoncoors.com/overview/default.aspx",
    "BF-B": "https://investors.brown-forman.com",
    "STZ":  "https://ir.cbrands.com/",
    "KDP":  "https://investors.keurigdrpepper.com",
    "PEP":  "https://www.pepsico.com/investors",
    "KO":   "https://investors.coca-colacompany.com",
    "BYND": "https://investors.beyondmeat.com",
    "LW":   "https://www.lambweston.com/en/investors.html",
    "CAG":  "https://www.conagrabrands.com/investor-relations",
    "CPB":  "https://investor.thecampbellscompany.com/",
    "SJM":  "https://investors.jmsmucker.com",
    "MKC":  "https://ir.mccormick.com/",
    "HRL":  "https://investors.hormelfoods.com",
    "GIS":  "https://investors.generalmills.com/home/default.aspx",
    "IFF":  "https://ir.iff.com",
    "KHC":  "https://ir.kraftheinzcompany.com",
    "HSY":  "https://www.thehersheycompany.com/en_us/investors.html",
    "MDLZ": "https://ir.mondelezinternational.com",
    "NWL":  "https://ir.newellbrands.com",
    "CLX":  "https://investors.thecloroxcompany.com/overview/default.aspx",
    "CHD":  "https://investor.churchdwight.com/overview/default.aspx",
    "KMB":  "https://www.investor.kimberly-clark.com/",
    "CL":   "https://investor.colgatepalmolive.com/",
    "PG":   "https://www.pginvestor.com/overview/default.aspx",
    "MO":   "https://www.altria.com/Investors/at-a-glance",
    "PM":   "https://www.pmi.com/investor-relations/overview",
    "MAT":  "https://investors.mattel.com/overview/default.aspx",
    "HAS":  "https://investor.hasbro.com",
    "DPZ":  "https://ir.dominos.com",
    "DRI":  "https://investor.darden.com/home/default.aspx",
    "QSR":  "https://www.rbi.com/English/investors/investor-home/default.aspx",
    "CMG":  "https://ir.chipotle.com",
    "YUM":  "https://investors.yum.com/corporateprofile/default.aspx",
    "SBUX": "https://investor.starbucks.com/ir-home/default.aspx",
    "MCD":  "https://corporate.mcdonalds.com/corpmcd/investors.html",
    "SFD":  "https://investors.smithfieldfoods.com/",
    "TSN":  "https://ir.tyson.com/investor-home/default.aspx",
    "SYY":  "https://investors.sysco.com/",
    "CART": "https://investors.instacart.com/",
    "DASH": "https://ir.doordash.com/overview/default.aspx",
    "FRT":  "https://www.federalrealty.com/investors/overview/",
    "REG":  "https://investors.regencycenters.com/",
    "KIM":  "https://investors.kimcorealty.com/",
    "SPG":  "https://simonpg.gcs-web.com/news-events/stockholder-events",
    "MAS":  "https://investor.masco.com/overview/default.aspx",
    "BALL": "https://investors.ball.com/",
    "TSCO": "https://ir.tractorsupply.com/investor-relations/overview/default.aspx",
    "AMCR": "https://www.amcor.com/investors",
    "ROL":  "https://www.rollins.com/investors",
    "CTAS": "https://www.cintas.com/investors/",
    "IP":   "https://www.internationalpaper.com/investors",
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
                if r.status_code==429: print(f"  Rate limited {ds} - waiting 15s"); time.sleep(15); continue
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
    print(f"EARNINGS CALENDAR REFRESH - {today.strftime('%B %d, %Y %I:%M %p ET')}")
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
                if mismatch: mismatches+=1; print(f"  MISMATCH {t}: NASDAQ={nd['date']} Yahoo={yd}")
                rows.append({"Sector":sector,"Ticker":t,"Earnings Date":nd["date"],"Timing":nd["timing"],
                             "Source":"NASDAQ","Yahoo Date":yd or "N/A","Mismatch":mismatch,"Confirmed":True})
            elif yd:
                rows.append({"Sector":sector,"Ticker":t,"Earnings Date":yd,"Timing":None,
                             "Source":"Yahoo Finance","Yahoo Date":yd,"Mismatch":False,"Confirmed":False})
            else:
                rows.append({"Sector":sector,"Ticker":t,"Earnings Date":None,"Timing":None,
                             "Source":"-","Yahoo Date":"N/A","Mismatch":False,"Confirmed":False})
    df=pd.DataFrame(rows)
    print(f"DONE: {df['Earnings Date'].notna().sum()} dates · {df['Earnings Date'].isna().sum()} unannounced · {mismatches} mismatches")
    return df,today

BMO_BADGE     = '<span class="tbadge tbadge-bmo">&#9650; BMO</span>'
AMC_BADGE     = '<span class="tbadge tbadge-amc">&#9660; AMC</span>'
BMO_KEY_BADGE = '<span class="tbadge tbadge-bmo" style="font-size:10px;padding:3px 9px">&#9650; BMO</span>'
AMC_KEY_BADGE = '<span class="tbadge tbadge-amc" style="font-size:10px;padding:3px 9px">&#9660; AMC</span>'

def build_html(df, generated_at):
    dated = df[df["Earnings Date"].notna()].copy()
    dated["dt"] = pd.to_datetime(dated["Earnings Date"])

    today_dt = generated_at.date()
    days_since_monday = today_dt.weekday()
    prior_monday = today_dt - timedelta(days=days_since_monday + 7)

    if dated.empty:
        months = [today_dt.replace(day=1)]
    else:
        mn = min(dated["dt"].min().date().replace(day=1), prior_monday.replace(day=1))
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

    today_str = generated_at.strftime("%Y-%m-%d")
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
            badge  = (BMO_BADGE if timing == "BMO" else AMC_BADGE if timing == "AMC" else "")
            unconf = '<span class="bdg-uc" title="Unconfirmed">?</span>' if not confirmed else ""
            warn   = '<span class="bdg-mm" title="Date conflict">!</span>' if mismatch else ""
            chips += (
                f'<div class="chip s-{safe}" style="--cc:{col}" data-ticker="{ticker}" '
                f'onclick="showCard(\'{ticker}\',\'{cn}\',\'{st}\',\'{timing or "TBD"}\','
                f'\'{ds}\',\'{col}\',\'{source}\',\'{yd_safe}\','
                f'{str(mismatch).lower()},{str(confirmed).lower()},\'{ir_url}\')">'
                f'{ticker}{badge}{unconf}{warn}</div>'
            )
        return chips

    def render_month(ms):
        es_name, es_sub, es_color, es_bg = EARNINGS_SEASON_BY_MONTH[ms.month]
        lbl   = ms.strftime("%B %Y").upper()
        heads = "".join(f'<div class="dname">{d}</div>' for d in DAYS)
        blank = "".join('<div class="dcell empty"></div>' for _ in range(ms.weekday()))
        nm = (ms.replace(month=ms.month+1) if ms.month < 12
              else ms.replace(year=ms.year+1, month=1))
        cells = ""
        for day in range(1, (nm - ms).days + 1):
            do  = ms.replace(day=day)
            ds  = do.strftime("%Y-%m-%d")
            cls = "dcell"
            if do.weekday() >= 5: cls += " wknd"
            if ds == today_str:   cls += " today"
            if do < today_dt and ds != today_str: cls += " past"
            rpts = dl.get(ds, [])
            if rpts: cls += " has-e"
            day_events = event_map.get(ds, [])
            if any(e["closed"] for e in day_events): cls += " mkt-closed"
            ev_html = "".join(
                f'<div class="evbadge evbadge-{"holiday" if e["type"]=="holiday" else "retail"}">'
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
            f'<rect x="4.5" y="3" width="2" height="9" rx="1" fill="{es_color}" opacity="0.85"/>'
            f'<rect x="8" y="1" width="2" height="11" rx="1" fill="{es_color}" opacity="0.7"/>'
            f'<rect x="11.5" y="4" width="2" height="8" rx="1" fill="{es_color}" opacity="0.6"/>'
            f'</svg>{es_name}<span class="earn-season-sub">{es_sub}</span>'
            f'</span></div>'
            f'<div class="cgrid">{heads}{blank}{cells}</div>'
            f'</div>'
        )

    cal = "".join(render_month(ms) for ms in months)

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
                f'\'TBD\',\'TBD\',\'{col}\',\'-\',\'N/A\',false,false,'
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
    ir_json = json.dumps(IR_URLS)

    # ── Sidebar: each ticker is a link to its IR page ──────────────────────
    sidebar_html = ""
    for s in SECTORS:
        col  = SECTOR_COLORS[s]
        safe = s.replace(" ","_").replace("/","_").replace("&","_")
        tickers_html = ""
        for t in SECTORS[s]:
            ir = IR_URLS.get(t, f"https://finance.yahoo.com/quote/{t}")
            tickers_html += (
                f'<a class="sleg-ticker" href="{ir}" target="_blank" rel="noopener" '
                f'title="{COMPANY_NAMES.get(t, t)}">{t}</a>'
            )
        sidebar_html += (
            f'<div class="sleg-group">'
            f'<button class="sleg-toggle" onclick="toggleSector(\'{safe}\')" style="--cc:{col}">'
            f'<span class="sleg-dot" style="background:{col}"></span>'
            f'<span class="sleg-label">{s}</span>'
            f'<span class="sleg-arrow" id="arrow-{safe}">&#8250;</span>'
            f'</button>'
            f'<div class="sleg-tickers" id="tickers-{safe}">{tickers_html}</div>'
            f'</div>'
        )

    # ── Build the JS notes logic as a plain string (no f-string) ──────────
    # This avoids ALL brace-escaping issues with template literals
    notes_js = r"""
const STORAGE_KEY = 'earnings_cal_private_notes_v1';
let notes = [];

function loadNotes() {
  try { notes = JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
  catch(e) { notes = []; }
  renderNotes();
}

function saveNotes() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(notes)); }
  catch(e) {}
}

function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2,6);
}

function renderNotes() {
  const list = document.getElementById('notesList');
  if (!list) return;
  const val = document.getElementById('notesBox');
  if (notes.length > 0 && val) {
    // notes stored but we show them inline in the textarea on load
  }
  // We use a simple single textarea approach - load last note into box
  if (notes.length > 0 && val && val.value === '') {
    val.value = notes[0].text;
  }
}

function saveNote() {
  const box = document.getElementById('notesBox');
  if (!box) return;
  const text = box.value;
  if (text.trim() === '') {
    notes = [];
  } else {
    notes = [{ id: genId(), text: text, ts: Date.now() }];
  }
  saveNotes();
  // Flash the border briefly to confirm save
  box.style.borderColor = 'rgba(106,171,255,0.9)';
  setTimeout(function() { box.style.borderColor = ''; }, 600);
}

// Auto-save on every keystroke (debounced)
let saveTimer = null;
function onNotesInput() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNote, 800);
}

loadNotes();
"""

    # ── Auto-refresh JS (plain string, no f-string) ─────────────────────
    refresh_js = r"""
function scheduleSmartRefresh() {
  const targets = [4 * 3600, 22 * 3600]; // 4 AM and 10 PM ET in seconds-since-midnight
  const now = new Date();

  // Get current ET time components
  const etParts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/New_York',
    hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false
  }).formatToParts(now);

  const h = parseInt(etParts.find(x => x.type === 'hour').value);
  const m = parseInt(etParts.find(x => x.type === 'minute').value);
  const s = parseInt(etParts.find(x => x.type === 'second').value);
  const nowSec = h * 3600 + m * 60 + s;

  // Find the next target that hasn't passed yet today
  let minDiff = Infinity;
  for (const t of targets) {
    let diff = t - nowSec;
    if (diff <= 0) diff += 86400; // wrap to next day
    if (diff < minDiff) minDiff = diff;
  }

  // Update footer label
  const nextTime = new Date(now.getTime() + minDiff * 1000);
  const lbl = nextTime.toLocaleTimeString('en-US', {
    timeZone: 'America/New_York', hour: 'numeric', minute: '2-digit', hour12: true
  });
  const el = document.getElementById('refreshLabel');
  if (el) el.textContent = 'Next refresh at ' + lbl + ' ET';

  // Use a precise countdown that re-checks every second to avoid drift
  function tick() {
    const n = new Date();
    const ep = new Intl.DateTimeFormat('en-US', {
      timeZone: 'America/New_York',
      hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false
    }).formatToParts(n);
    const ch = parseInt(ep.find(x => x.type === 'hour').value);
    const cm = parseInt(ep.find(x => x.type === 'minute').value);
    const cs = parseInt(ep.find(x => x.type === 'second').value);
    const curSec = ch * 3600 + cm * 60 + cs;

    for (const t of targets) {
      // Fire if we are within 2 seconds of target (handles any drift)
      if (Math.abs(curSec - t) <= 2) {
        location.reload();
        return;
      }
    }
    setTimeout(tick, 1000);
  }
  setTimeout(tick, 1000);
}
scheduleSmartRefresh();
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Earnings Calendar - Consumer &amp; Retail</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg0:#080b18;--bg1:#0d1120;--bg2:#111628;--bg3:#151c30;--bg4:#1a2238;--bg5:#1f2942;
  /* Glass palette — brighter, more vivid */
  --glass-light:rgba(255,255,255,0.07);
  --glass-mid:rgba(255,255,255,0.12);
  --glass-heavy:rgba(255,255,255,0.20);
  --glass-border:rgba(255,255,255,0.14);
  --glass-border2:rgba(255,255,255,0.24);
  --glass-border3:rgba(255,255,255,0.38);
  --glass-shine:rgba(255,255,255,0.55);
  --t0:#ffffff;--t1:#dde6ff;--t2:#9aadd4;--t3:#4e5f88;
  --accent:#6aabff;--accent2:#93c8ff;--accent-glow:rgba(106,171,255,0.35);
  --bmo:#ffd740;--amc:#b8a4ff;--unconf:#ffaa33;--conflict:#ff5252;
  --mono:'JetBrains Mono',monospace;
  --sans:'Inter',-apple-system,sans-serif;
  --sidebar-w:240px;
  --r:10px;--r-lg:14px;--r-xl:18px;
  --ease:cubic-bezier(0.4,0,0.2,1);--dur:0.2s;
}}
::-webkit-scrollbar{{width:3px;height:3px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:rgba(255,255,255,0.18);border-radius:3px}}
::-webkit-scrollbar-thumb:hover{{background:rgba(255,255,255,0.32)}}

body{{
  font-family:var(--sans);background:var(--bg0);color:var(--t1);
  min-height:100vh;-webkit-font-smoothing:antialiased;overflow-x:hidden;
  background-image:
    radial-gradient(ellipse 90% 60% at 15% -10%,rgba(80,130,255,0.18) 0%,transparent 55%),
    radial-gradient(ellipse 70% 50% at 85% 110%,rgba(160,60,220,0.13) 0%,transparent 55%),
    radial-gradient(ellipse 50% 40% at 50% 50%,rgba(20,30,80,0.35) 0%,transparent 70%);
}}
.page-wrap{{display:flex;min-height:100vh;}}

/* ========== GLASS MIXIN (applied via classes) ========== */
.glass{{
  background:linear-gradient(135deg,rgba(255,255,255,0.10) 0%,rgba(255,255,255,0.04) 100%);
  backdrop-filter:blur(24px) saturate(160%);-webkit-backdrop-filter:blur(24px) saturate(160%);
  border:1px solid rgba(255,255,255,0.18);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.22),
    inset 0 -1px 0 rgba(0,0,0,0.15),
    0 8px 32px rgba(0,0,0,0.45),
    0 2px 8px rgba(0,0,0,0.25);
}}

/* ========== SIDEBAR ========== */
.sidebar{{
  width:var(--sidebar-w);flex-shrink:0;
  background:linear-gradient(180deg,
    rgba(12,16,36,0.97) 0%,
    rgba(8,11,24,1) 100%);
  border-right:1px solid rgba(255,255,255,0.14);
  position:sticky;top:0;height:100vh;
  display:flex;flex-direction:column;
  transition:width var(--dur) var(--ease);
  z-index:200;overflow:hidden;
  box-shadow:2px 0 24px rgba(0,0,0,0.5),inset -1px 0 0 rgba(255,255,255,0.06);
}}
.sidebar.collapsed{{width:0;border-right-color:transparent;}}
.content{{flex:1;min-width:0;display:flex;flex-direction:column;}}

.sidebar-head{{
  padding:14px 14px 10px;
  border-bottom:1px solid rgba(255,255,255,0.10);
  flex-shrink:0;
  background:linear-gradient(180deg,rgba(106,171,255,0.12) 0%,transparent 100%);
}}
.sidebar-title{{
  font-family:var(--mono);font-size:8.5px;font-weight:700;
  color:var(--accent);text-transform:uppercase;letter-spacing:2px;white-space:nowrap;
}}

.sidebar-sectors{{overflow-y:auto;flex:1;padding:4px 0;min-height:0;}}

.sleg-group{{border-bottom:1px solid rgba(255,255,255,0.06);}}
.sleg-toggle{{
  display:flex;align-items:center;gap:8px;
  width:100%;padding:7px 12px;background:none;border:none;cursor:pointer;
  transition:background var(--dur);
}}
.sleg-toggle:hover{{background:rgba(255,255,255,0.08);}}
.sleg-dot{{
  width:8px;height:8px;border-radius:50%;flex-shrink:0;
  box-shadow:0 0 6px currentColor;
}}
.sleg-label{{
  font-family:var(--mono);font-size:8.5px;font-weight:700;
  color:var(--t0);flex:1;text-align:left;letter-spacing:.3px;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;
}}
.sleg-arrow{{font-size:11px;color:var(--t3);transition:transform var(--dur) var(--ease);flex-shrink:0;}}
.sleg-arrow.open{{transform:rotate(90deg);color:var(--t2);}}
.sleg-tickers{{
  display:flex;flex-wrap:wrap;gap:3px;padding:0 12px;
  overflow:hidden;max-height:0;transition:max-height 0.3s var(--ease),padding 0.2s;
}}
.sleg-tickers.open{{max-height:200px;padding:0 12px 8px;}}

.sleg-ticker{{
  font-family:var(--mono);font-size:7.5px;color:var(--t1);
  background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
  border-radius:3px;padding:1px 5px;cursor:pointer;
  transition:color var(--dur),background var(--dur),border-color var(--dur);
  text-decoration:none;display:inline-block;
}}
.sleg-ticker:hover{{
  color:#fff;background:rgba(106,171,255,0.20);
  border-color:rgba(106,171,255,0.50);
}}

/* ========== NOTES PANEL ========== */
.notes-panel{{
  flex-shrink:0;
  display:flex;flex-direction:column;
  background:linear-gradient(180deg,rgba(10,13,30,0.98) 0%,rgba(6,8,20,1) 100%);
  border-top:1px solid rgba(255,255,255,0.12);
  padding:8px;
  gap:6px;
}}
.notes-box{{
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.14);
  border-radius:8px;
  padding:7px 9px;
  font-family:var(--sans);font-size:10px;color:#fff;
  outline:none;resize:none;
  height:110px;
  line-height:1.5;
  transition:border-color var(--dur),background var(--dur),box-shadow var(--dur);
  width:100%;
}}
.notes-box::placeholder{{color:var(--t3);font-style:italic;}}
.notes-box:focus{{
  border-color:rgba(106,171,255,0.55);
  background:rgba(255,255,255,0.09);
  box-shadow:0 0 0 3px rgba(106,171,255,0.10),inset 0 1px 0 rgba(255,255,255,0.08);
}}

/* ========== TOPBAR ========== */
.topbar{{
  height:52px;
  background:linear-gradient(90deg,rgba(12,16,34,0.96) 0%,rgba(8,11,26,0.96) 100%);
  backdrop-filter:blur(40px) saturate(200%);-webkit-backdrop-filter:blur(40px) saturate(200%);
  border-bottom:1px solid rgba(255,255,255,0.14);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 18px;position:sticky;top:0;z-index:300;gap:12px;
  box-shadow:
    0 1px 0 rgba(255,255,255,0.08),
    0 4px 24px rgba(0,0,0,0.6),
    inset 0 1px 0 rgba(255,255,255,0.10);
}}
.topbar-left{{display:flex;align-items:center;gap:10px;}}
.page-title{{font-size:13px;font-weight:700;color:#fff;letter-spacing:-.3px;white-space:nowrap;}}
.title-dot{{
  width:8px;height:8px;border-radius:50%;background:var(--accent);
  box-shadow:0 0 0 2px rgba(106,171,255,0.30),0 0 14px rgba(106,171,255,0.65);
  flex-shrink:0;animation:dotPulse 2.5s ease-in-out infinite;
}}
@keyframes dotPulse{{
  0%,100%{{box-shadow:0 0 0 2px rgba(106,171,255,0.18),0 0 8px rgba(106,171,255,0.45);}}
  50%{{box-shadow:0 0 0 4px rgba(106,171,255,0.32),0 0 22px rgba(106,171,255,0.80);}}
}}
.vdiv{{width:1px;height:16px;background:rgba(255,255,255,0.14);}}
.topbar-meta{{font-size:10px;color:var(--t2);white-space:nowrap;}}
.topbar-right{{display:flex;align-items:center;gap:8px;flex-shrink:0;}}

/* Glass stat pills */
.tstat{{
  display:flex;flex-direction:column;align-items:center;
  padding:5px 12px;border-radius:10px;
  background:linear-gradient(135deg,rgba(255,255,255,0.10) 0%,rgba(255,255,255,0.04) 100%);
  border:1px solid rgba(255,255,255,0.16);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.18),0 2px 8px rgba(0,0,0,0.35);
  transition:background var(--dur),border-color var(--dur),box-shadow var(--dur);
}}
.tstat:hover{{
  background:linear-gradient(135deg,rgba(255,255,255,0.16) 0%,rgba(255,255,255,0.08) 100%);
  border-color:rgba(255,255,255,0.28);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.28),0 4px 16px rgba(0,0,0,0.4);
}}
.tstat-num{{font-family:var(--mono);font-size:15px;font-weight:700;color:#fff;line-height:1.1;}}
.tstat-lbl{{font-size:7px;color:var(--t2);text-transform:uppercase;letter-spacing:.9px;margin-top:2px;}}
.sidebar-toggle{{
  display:flex;align-items:center;justify-content:center;
  width:28px;height:28px;border-radius:8px;
  background:linear-gradient(135deg,rgba(255,255,255,0.12) 0%,rgba(255,255,255,0.05) 100%);
  border:1px solid rgba(255,255,255,0.18);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.22),0 2px 6px rgba(0,0,0,0.3);
  color:var(--t1);cursor:pointer;font-size:16px;line-height:1;
  transition:background var(--dur),color var(--dur),box-shadow var(--dur);flex-shrink:0;
}}
.sidebar-toggle:hover{{
  background:linear-gradient(135deg,rgba(255,255,255,0.22) 0%,rgba(255,255,255,0.10) 100%);
  color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,0.35),0 4px 12px rgba(0,0,0,0.4);
}}

/* ========== KEY BAR ========== */
.timingbar{{
  background:linear-gradient(90deg,rgba(10,13,30,0.92) 0%,rgba(8,11,24,0.92) 100%);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,0.10);
  padding:8px 18px 10px;
  display:flex;align-items:center;gap:8px;
  font-size:11px;color:var(--t2);flex-wrap:wrap;
  box-shadow:0 2px 12px rgba(0,0,0,0.3);
}}
.key-label{{font-family:var(--mono);font-size:8.5px;font-weight:700;color:var(--t0);text-transform:uppercase;letter-spacing:1px;}}
.tpill{{
  display:inline-flex;align-items:center;gap:4px;font-size:9px;font-weight:700;
  padding:3px 9px;border-radius:6px;font-family:var(--mono);letter-spacing:.3px;white-space:nowrap;
  backdrop-filter:blur(8px);
}}
.tpill.pre{{background:rgba(255,215,64,.18);color:#ffd740;border:1px solid rgba(255,215,64,.40);box-shadow:0 0 8px rgba(255,215,64,.15);}}
.tpill.aft{{background:rgba(184,164,255,.18);color:#b8a4ff;border:1px solid rgba(184,164,255,.40);box-shadow:0 0 8px rgba(184,164,255,.15);}}
.tpill.unc{{background:rgba(255,170,51,.18);color:#ffaa33;border:1px solid rgba(255,170,51,.40);}}
.tpill.mis{{background:rgba(255,82,82,.18);color:#ff5252;border:1px solid rgba(255,82,82,.40);}}
.key-sep{{color:var(--t3);}}
.key-desc{{font-size:9.5px;color:var(--t1);}}
.event-legend{{
  display:flex;flex-wrap:wrap;align-items:center;gap:6px;
  width:100%;margin-top:7px;padding-top:7px;border-top:1px solid rgba(255,255,255,0.08);
}}
.evleg-label{{font-family:var(--mono);font-size:8px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:1px;}}
.evleg-item{{display:inline-flex;align-items:center;gap:4px;font-size:9px;color:var(--t1);}}
.evleg-dot{{width:7px;height:7px;border-radius:2px;flex-shrink:0;}}
.evleg-dot.holiday{{background:#4a7ac8;}}
.evleg-dot.retail{{background:#a07030;}}
.evleg-dot.closed{{background:rgba(220,60,60,.9);}}

/* ========== SEARCH ========== */
.search-bar{{
  background:linear-gradient(90deg,rgba(10,13,30,0.88) 0%,rgba(8,11,24,0.88) 100%);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,0.10);padding:7px 18px;
  display:flex;align-items:center;gap:10px;position:sticky;top:52px;z-index:299;
}}
.search-wrap{{position:relative;display:flex;align-items:center;}}
.search-icon{{position:absolute;left:9px;color:var(--t2);font-size:13px;pointer-events:none;}}
.search-input{{
  background:linear-gradient(135deg,rgba(255,255,255,0.09) 0%,rgba(255,255,255,0.04) 100%);
  border:1px solid rgba(255,255,255,0.16);border-radius:8px;
  padding:5px 28px 5px 28px;font-family:var(--mono);font-size:11px;color:#fff;
  outline:none;width:200px;
  backdrop-filter:blur(12px);
  transition:border-color var(--dur),background var(--dur),box-shadow var(--dur);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.12);
}}
.search-input::placeholder{{color:var(--t3);}}
.search-input:focus{{
  border-color:rgba(106,171,255,0.65);
  background:linear-gradient(135deg,rgba(106,171,255,0.12) 0%,rgba(255,255,255,0.06) 100%);
  box-shadow:0 0 0 3px rgba(106,171,255,0.14),inset 0 1px 0 rgba(255,255,255,0.18);
}}
.search-clear{{
  position:absolute;right:7px;background:none;border:none;color:var(--t2);
  cursor:pointer;font-size:14px;line-height:1;padding:0;display:none;transition:color var(--dur);
}}
.search-clear:hover{{color:#fff;}}
.search-clear.on{{display:block;}}
.search-hint{{font-size:10px;color:var(--t1);font-family:var(--mono);}}

/* ========== CALENDAR ========== */
.main{{padding:16px 18px 32px;max-width:1440px;margin:0 auto;}}
.mblock{{
  margin-bottom:24px;border-radius:var(--r-lg);overflow:hidden;
  border:1px solid rgba(255,255,255,0.13);
  background:linear-gradient(145deg,rgba(16,21,46,0.92) 0%,rgba(10,14,32,0.96) 100%);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  box-shadow:
    0 8px 32px rgba(0,0,0,0.55),
    0 2px 8px rgba(0,0,0,0.35),
    inset 0 1px 0 rgba(255,255,255,0.10),
    inset 0 -1px 0 rgba(0,0,0,0.20);
}}
.mblock-header{{
  padding:10px 14px 8px;border-bottom:1px solid rgba(255,255,255,0.10);
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;
  background:linear-gradient(90deg,var(--es-bg,rgba(255,255,255,0.03)) 0%,transparent 55%);
}}
.mlabel{{font-family:var(--mono);font-size:12px;font-weight:700;color:#fff;letter-spacing:.5px;}}
.earn-season-badge{{
  display:inline-flex;align-items:center;font-family:var(--mono);font-size:8.5px;font-weight:700;
  padding:3px 9px;border-radius:6px;white-space:nowrap;
  background:color-mix(in srgb,var(--ec) 16%,transparent);
  color:var(--ec);border:1px solid color-mix(in srgb,var(--ec) 36%,transparent);
  box-shadow:0 0 10px color-mix(in srgb,var(--ec) 20%,transparent);
}}
.earn-season-sub{{font-size:7px;font-weight:400;opacity:0.65;margin-left:5px;}}

.cgrid{{
  display:grid;grid-template-columns:repeat(7,1fr);gap:2px;padding:4px;
  background:rgba(4,6,16,0.75);
}}
.dname{{
  text-align:center;font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t2);padding:5px 0;letter-spacing:1.2px;
}}

/* Calendar cells — glass effect */
.dcell{{
  background:linear-gradient(145deg,rgba(22,30,64,0.85) 0%,rgba(14,20,48,0.92) 100%);
  border:1px solid rgba(255,255,255,0.09);
  border-radius:8px;min-height:100px;padding:7px 6px 5px;
  transition:border-color 0.15s,background 0.15s,box-shadow 0.15s;
  position:relative;overflow:hidden;
  backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);
}}
/* Subtle top-shine on each cell */
.dcell::before{{
  content:'';position:absolute;inset:0;
  background:linear-gradient(160deg,rgba(255,255,255,0.06) 0%,transparent 40%);
  pointer-events:none;border-radius:8px;
}}
.dcell.empty{{background:transparent;border-color:transparent;pointer-events:none;backdrop-filter:none;}}
.dcell.wknd{{background:rgba(6,8,20,0.72);opacity:0.42;}}
.dcell.past{{opacity:0.38;filter:saturate(0.40) brightness(0.78);}}
/* Today — vivid glass highlight */
.dcell.today{{
  border-color:rgba(106,171,255,0.75)!important;
  background:linear-gradient(145deg,rgba(106,171,255,0.14) 0%,rgba(40,70,180,0.20) 100%)!important;
  box-shadow:
    0 0 0 1px rgba(106,171,255,0.25),
    0 4px 20px rgba(106,171,255,0.18),
    inset 0 1px 0 rgba(106,171,255,0.30),
    inset 0 0 20px rgba(106,171,255,0.06)!important;
}}
.dcell.today::after{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent);
  border-radius:8px 8px 0 0;opacity:0.9;
}}
.dcell.today .dno{{color:var(--accent)!important;font-weight:700;text-shadow:0 0 8px rgba(106,171,255,0.6);}}
.dcell.has-e{{
  border-color:rgba(255,255,255,0.15);
  background:linear-gradient(145deg,rgba(26,36,76,0.92) 0%,rgba(16,24,58,0.97) 100%);
}}
.dcell.mkt-closed{{
  background:linear-gradient(145deg,rgba(50,12,12,0.85) 0%,rgba(30,6,6,0.95) 100%);
  border-color:rgba(200,50,50,.25);
}}
.dno{{
  font-family:var(--mono);font-size:10.5px;font-weight:600;
  color:rgba(220,230,255,0.82);margin-bottom:3px;display:block;
}}
.evbadge{{
  font-family:var(--mono);font-size:6.5px;font-weight:700;padding:1px 4px;border-radius:3px;
  margin-bottom:2px;display:inline-block;letter-spacing:.2px;white-space:nowrap;
  max-width:100%;overflow:hidden;text-overflow:ellipsis;
}}
.evbadge-holiday{{background:rgba(74,122,200,.35);color:#a0c4f8;border:1px solid rgba(74,122,200,.60);}}
.evbadge-retail{{background:rgba(160,112,48,.35);color:#f0c878;border:1px solid rgba(160,112,48,.60);}}
.ev-closed{{
  font-size:6px;font-weight:900;background:rgba(220,40,40,.92);color:#fff;
  padding:0 3px;border-radius:2px;margin-left:2px;letter-spacing:.3px;vertical-align:middle;
}}
.chips{{display:flex;flex-wrap:wrap;gap:3px;margin-top:3px;}}

/* ========== CHIPS — black text, vivid glass ========== */
.chip{{
  display:inline-flex;align-items:center;gap:2px;
  background:linear-gradient(135deg,
    color-mix(in srgb,var(--cc) 75%,#fff 25%) 0%,
    color-mix(in srgb,var(--cc) 90%,#fff 10%) 60%,
    var(--cc) 100%);
  font-family:var(--mono);font-size:9px;font-weight:800;
  color:#000;
  padding:4px 7px;border-radius:6px;cursor:pointer;white-space:nowrap;
  transition:transform 0.13s,filter 0.13s,box-shadow 0.13s,opacity 0.13s;
  letter-spacing:.2px;
  border:1px solid rgba(255,255,255,0.35);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.55),
    inset 0 -1px 0 rgba(0,0,0,0.15),
    0 2px 6px rgba(0,0,0,0.40);
}}
.chip:hover{{
  transform:translateY(-2px) scale(1.09);
  filter:brightness(1.20) saturate(1.10);
  box-shadow:
    0 6px 18px rgba(0,0,0,0.55),
    0 0 14px color-mix(in srgb,var(--cc) 50%,transparent),
    inset 0 1px 0 rgba(255,255,255,0.60);
  z-index:10;position:relative;
}}
.chip.dimmed{{opacity:0.06;pointer-events:none;}}

.tbadge{{
  font-family:var(--mono);font-size:6.5px;font-weight:900;
  padding:1px 3px;border-radius:3px;letter-spacing:.2px;line-height:1.4;
  vertical-align:middle;display:inline-block;
}}
.tbadge-bmo{{background:rgba(0,0,0,0.35);color:#ffd740;border:1px solid rgba(255,215,64,.55);}}
.tbadge-amc{{background:rgba(0,0,0,0.35);color:#b8a4ff;border:1px solid rgba(184,164,255,.55);}}
.bdg-uc{{
  font-family:var(--mono);font-size:7.5px;font-weight:900;
  background:rgba(255,170,51,.40);color:#ffaa33;border:1px solid rgba(255,170,51,.65);
  border-radius:3px;padding:0 3px;line-height:1.4;
}}
.bdg-mm{{
  font-family:var(--mono);font-size:7.5px;font-weight:900;
  background:rgba(255,82,82,.45);color:#ff5252;border:1px solid rgba(255,82,82,.75);
  border-radius:3px;padding:0 3px;line-height:1.4;
  animation:warnPulse 2s ease-in-out infinite;
}}
@keyframes warnPulse{{
  0%,100%{{box-shadow:0 0 0 0 rgba(255,82,82,0);}}
  50%{{box-shadow:0 0 0 3px rgba(255,82,82,.35);}}
}}

/* ========== UNANNOUNCED ========== */
.ubox{{
  margin:0 18px 32px;
  background:linear-gradient(145deg,rgba(16,21,46,0.92) 0%,rgba(10,14,32,0.96) 100%);
  border:1px solid rgba(255,255,255,0.13);
  border-radius:var(--r-lg);overflow:hidden;
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  box-shadow:0 8px 32px rgba(0,0,0,0.50),inset 0 1px 0 rgba(255,255,255,0.08);
}}
.ubox-head{{
  padding:12px 18px;border-bottom:1px solid rgba(255,255,255,0.10);
  display:flex;align-items:baseline;gap:12px;
  background:rgba(255,255,255,0.04);
}}
.ubox-title{{font-family:var(--mono);font-size:10.5px;font-weight:700;color:#fff;letter-spacing:.5px;}}
.ubox-sub{{font-size:9.5px;color:var(--t1);}}
.utable{{width:100%;border-collapse:collapse;}}
.utable th{{
  text-align:left;padding:6px 14px;font-family:var(--mono);font-size:7.5px;font-weight:700;
  color:var(--t1);border-bottom:1px solid rgba(255,255,255,0.09);text-transform:uppercase;letter-spacing:.8px;
}}
.utable td{{padding:7px 14px;border-bottom:1px solid rgba(255,255,255,0.06);vertical-align:middle;}}
.utable tr:last-child td{{border-bottom:none;}}
.utable tr:hover td{{background:rgba(255,255,255,0.04);}}
.sbadge{{
  font-family:var(--mono);font-size:8.5px;font-weight:700;color:#000;
  padding:3px 8px;border-radius:5px;white-space:nowrap;
  border:1px solid rgba(255,255,255,.22);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 6px rgba(0,0,0,.4);
}}
/* Unannounced chips — also black text */
.uchip{{
  display:inline-flex;align-items:center;
  background:linear-gradient(135deg,
    color-mix(in srgb,var(--cc) 75%,#fff 25%) 0%,
    var(--cc) 100%);
  font-family:var(--mono);font-size:9px;font-weight:800;color:#000;
  padding:3px 7px;border-radius:5px;margin:2px;cursor:pointer;
  transition:transform 0.13s,filter 0.13s,opacity 0.13s;
  border:1px solid rgba(255,255,255,.28);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.40);
}}
.uchip:hover{{transform:translateY(-1px) scale(1.08);filter:brightness(1.18);}}
.uchip.dimmed{{opacity:0.06;pointer-events:none;}}

/* ========== FOOTER ========== */
.footer{{
  border-top:1px solid rgba(255,255,255,0.10);padding:10px 18px;
  font-family:var(--mono);font-size:8.5px;color:var(--t2);
  display:flex;justify-content:space-between;align-items:center;
  background:linear-gradient(90deg,rgba(8,10,24,0.92) 0%,rgba(6,8,18,0.92) 100%);
  backdrop-filter:blur(12px);
}}

/* ========== MODAL ========== */
.overlay{{
  display:none;position:fixed;inset:0;
  background:rgba(0,0,0,0.85);
  backdrop-filter:blur(28px) saturate(130%);-webkit-backdrop-filter:blur(28px) saturate(130%);
  z-index:999;align-items:center;justify-content:center;
}}
.overlay.on{{display:flex;}}
.modal{{
  background:linear-gradient(145deg,rgba(22,30,64,0.98) 0%,rgba(14,18,48,0.99) 100%);
  border:1px solid rgba(255,255,255,0.22);border-radius:var(--r-xl);
  padding:26px;max-width:400px;width:90%;
  backdrop-filter:blur(40px) saturate(180%);-webkit-backdrop-filter:blur(40px) saturate(180%);
  box-shadow:
    0 40px 80px rgba(0,0,0,0.90),
    0 0 0 1px rgba(255,255,255,0.06),
    inset 0 1px 0 rgba(255,255,255,0.14),
    inset 0 -1px 0 rgba(0,0,0,0.20);
  position:relative;animation:popIn .22s cubic-bezier(.34,1.4,.64,1);
}}
@keyframes popIn{{from{{transform:scale(.88) translateY(14px);opacity:0}}to{{transform:scale(1) translateY(0);opacity:1}}}}
.modal-close{{
  position:absolute;top:12px;right:14px;
  background:linear-gradient(135deg,rgba(255,255,255,0.12) 0%,rgba(255,255,255,0.05) 100%);
  border:1px solid rgba(255,255,255,0.18);
  border-radius:6px;width:24px;height:24px;font-size:14px;color:var(--t1);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.20);
  transition:background var(--dur),color var(--dur);
}}
.modal-close:hover{{
  background:linear-gradient(135deg,rgba(255,255,255,0.22) 0%,rgba(255,255,255,0.10) 100%);
  color:#fff;
}}
.modal-ticker{{
  font-family:var(--mono);font-size:28px;font-weight:700;margin-bottom:3px;line-height:1;
  filter:drop-shadow(0 0 12px currentColor);
}}
.modal-name{{font-size:11.5px;color:var(--t1);margin-bottom:20px;}}
.modal-banner{{border-radius:8px;padding:9px 12px;margin-bottom:12px;font-size:10.5px;line-height:1.5;display:none;}}
.modal-banner.on{{display:block;}}
.modal-banner.warn{{background:rgba(255,82,82,.12);border:1px solid rgba(255,82,82,.32);color:#ff8080;}}
.modal-banner.info{{background:rgba(255,170,51,.10);border:1px solid rgba(255,170,51,.30);color:#ffaa33;}}
.modal-row{{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.08);font-size:11.5px;}}
.modal-row:last-of-type{{border-bottom:none;}}
.modal-key{{color:var(--t2);font-size:9px;text-transform:uppercase;letter-spacing:.7px;font-weight:600;}}
.modal-val{{color:#fff;font-family:var(--mono);font-size:11px;font-weight:600;}}
.modal-val.secondary{{color:var(--t1);font-size:10.5px;font-weight:400;}}
.modal-source-row{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.08);gap:12px;}}
.modal-source-col{{display:flex;flex-direction:column;gap:3px;flex:1;}}
.modal-source-label{{color:var(--t2);font-size:8.5px;text-transform:uppercase;letter-spacing:.7px;font-weight:600;}}
.modal-source-date{{font-family:var(--mono);font-size:11.5px;font-weight:600;color:#fff;}}
.modal-source-date.conflict{{color:var(--conflict);}}
.modal-ir-link{{
  display:inline-flex;align-items:center;gap:6px;margin-top:16px;
  font-family:var(--mono);font-size:9.5px;font-weight:600;color:var(--accent);text-decoration:none;
  border:1px solid rgba(106,171,255,.36);border-radius:9px;padding:9px 14px;width:100%;
  justify-content:center;
  background:linear-gradient(135deg,rgba(106,171,255,0.12) 0%,rgba(106,171,255,0.05) 100%);
  backdrop-filter:blur(8px);
  box-shadow:inset 0 1px 0 rgba(106,171,255,0.20);
  transition:background var(--dur),border-color var(--dur),box-shadow var(--dur);
}}
.modal-ir-link:hover{{
  background:linear-gradient(135deg,rgba(106,171,255,0.22) 0%,rgba(106,171,255,0.10) 100%);
  border-color:rgba(106,171,255,.65);
  box-shadow:0 0 20px rgba(106,171,255,.22),inset 0 1px 0 rgba(106,171,255,0.35);
}}

/* ========== MOBILE ========== */
@media(max-width:768px){{
  .sidebar{{width:0;border-right-color:transparent;}}
  .topbar{{padding:0 10px;height:46px;gap:6px;}}
  .page-title{{font-size:11px;}}
  .topbar-meta,.vdiv{{display:none;}}
  .tstat{{padding:3px 7px;}}
  .tstat-num{{font-size:12px;}}
  .tstat-lbl{{font-size:6px;}}
  .timingbar{{flex-direction:column;align-items:flex-start;gap:5px;padding:7px 10px;}}
  .search-bar{{padding:6px 10px;top:46px;}}
  .search-input{{width:150px;}}
  .cgrid{{grid-template-columns:repeat(7,minmax(0,1fr));gap:1px;padding:2px;}}
  .dcell{{min-height:60px;padding:4px 3px 3px;}}
  .dno{{font-size:7.5px;}}
  .chip{{font-size:7px;padding:2px 4px;border-radius:4px;}}
  .evbadge{{font-size:5.5px;padding:1px 2px;}}
  .dname{{font-size:7px;padding:3px 0;}}
  .main{{padding:10px 8px 20px;}}
  .mblock{{margin-bottom:14px;}}
  .ubox{{margin:0 8px 20px;}}
  .modal{{padding:18px 14px;}}
  .modal-ticker{{font-size:22px;}}
}}
</style>
</head>
<body>
<div class="page-wrap">

<!-- ===== SIDEBAR ===== -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-head">
    <span class="sidebar-title">&#11041; Sectors</span>
  </div>
  <div class="sidebar-sectors">{sidebar_html}</div>

  <!-- PLAIN NOTES BOX pinned to bottom -->
  <div class="notes-panel">
    <textarea class="notes-box" id="notesBox"
              placeholder="Private notes&#10;Auto-saved locally…"
              oninput="onNotesInput()"></textarea>
  </div>
</aside>

<div class="content">

<header class="topbar">
  <div class="topbar-left">
    <button class="sidebar-toggle" id="sidebarToggle"
            onclick="toggleSidebar()" title="Toggle sidebar">&#8801;</button>
    <span class="title-dot"></span>
    <span class="page-title">Earnings Calendar</span>
    <span class="vdiv"></span>
    <span class="topbar-meta">Consumer &amp; Retail &middot; {ts}</span>
  </div>
  <div class="topbar-right">
    <div class="tstat">
      <span class="tstat-num" style="color:#6aabff">{nf}</span>
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
  {BMO_KEY_BADGE}
  <span class="key-desc">Before market open</span>
  <span class="key-sep">&middot;</span>
  {AMC_KEY_BADGE}
  <span class="key-desc">After market close</span>
  <span class="key-sep">&middot;</span>
  <span class="tpill unc">? Unconfirmed</span>
  <span class="key-desc">Yahoo only</span>
  <span class="key-sep">&middot;</span>
  <span class="tpill mis">! Conflict</span>
  <span class="key-desc">Sources disagree</span>
  <span class="key-sep">&middot;</span>
  <span class="key-desc" style="color:var(--t2)">Click any ticker for details</span>
  <div class="event-legend">
    <span class="evleg-label">Events</span>
    <span class="evleg-item"><span class="evleg-dot holiday"></span>Federal Holiday</span>
    <span class="evleg-item"><span class="evleg-dot retail"></span>Retail / Consumer Event</span>
    <span class="evleg-item"><span class="evleg-dot closed"></span>Market Closed</span>
  </div>
</div>

<div class="search-bar">
  <div class="search-wrap">
    <span class="search-icon">&#8981;</span>
    <input class="search-input" id="searchInput" type="text"
           placeholder="Search ticker&#8230;" autocomplete="off" spellcheck="false">
    <button class="search-clear" id="searchClear" onclick="clearSearch()">&times;</button>
  </div>
  <span class="search-hint" id="searchHint"></span>
</div>

<main class="main">{cal}</main>
{uhtml}

<footer class="footer">
  <span>Neil J Kanatt &middot; NASDAQ API + Yahoo Finance</span>
  <span id="refreshLabel">Next refresh calculating&hellip;</span>
</footer>
</div>
</div>

<!-- MODAL -->
<div class="overlay" id="overlay" onclick="closeModal(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeModal()">&times;</button>
    <div class="modal-ticker" id="mTicker"></div>
    <div class="modal-name"   id="mName"></div>
    <div class="modal-banner warn" id="mMismatch">
      &#9888; Date conflict &mdash; NASDAQ and Yahoo show different dates.
    </div>
    <div class="modal-banner info" id="mUnconf">
      &#10069; Unconfirmed &mdash; sourced from Yahoo Finance only.
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
      &#8599; Investor Relations Page
    </a>
  </div>
</div>

<script>
const SECTORS       = {sj};
const SECTOR_COLORS = {cj};
const COMPANY_NAMES = {nj};
const IR_URLS_JS    = {ir_json};

// ── Sidebar toggle ──────────────────────────────────────────────────────────
let sidebarOpen = true;
function toggleSidebar() {{
  sidebarOpen = !sidebarOpen;
  document.getElementById('sidebar').classList.toggle('collapsed', !sidebarOpen);
}}

function toggleSector(safe) {{
  const t = document.getElementById('tickers-' + safe);
  const a = document.getElementById('arrow-'   + safe);
  const open = t.classList.contains('open');
  t.classList.toggle('open', !open);
  a.classList.toggle('open', !open);
}}

// ── Search ──────────────────────────────────────────────────────────────────
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
    searchHint.textContent = '';
    return;
  }}
  let found = 0;
  chips.forEach(c => {{
    const match = c.dataset.ticker && c.dataset.ticker.toUpperCase().includes(q);
    c.classList.toggle('dimmed', !match);
    if (match) found++;
  }});
  uchips.forEach(c => {{
    const match = c.dataset.ticker && c.dataset.ticker.toUpperCase().includes(q);
    c.classList.toggle('dimmed', !match);
    if (match) found++;
  }});
  searchHint.textContent = found ? found + ' result' + (found > 1 ? 's' : '') : 'No results';
}}

// ── Modal ───────────────────────────────────────────────────────────────────
function showCard(ticker, name, sector, timing, nasdaqDate, color, source, yahooDate, mismatch, confirmed, irUrl) {{
  document.getElementById('mTicker').textContent = ticker;
  document.getElementById('mTicker').style.color  = color;
  document.getElementById('mName').textContent    = name;
  document.getElementById('mSector').textContent  = sector;
  const nd = document.getElementById('mNasdaqDate');
  const yd = document.getElementById('mYahooDate');
  nd.textContent = (!confirmed || nasdaqDate === 'TBD') ? 'Not on NASDAQ' : nasdaqDate;
  yd.textContent = (yahooDate && yahooDate !== 'N/A')   ? yahooDate       : 'Not available';
  nd.classList.toggle('conflict', mismatch);
  yd.classList.toggle('conflict', mismatch);
  document.getElementById('mTiming').textContent =
    timing === 'BMO' ? 'Before Market Open' :
    timing === 'AMC' ? 'After Market Close' :
    timing === 'TBD' ? 'Not yet confirmed'  : 'Unconfirmed';
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

<!-- Notes + Refresh JS injected as plain strings (no f-string brace conflicts) -->
<script>
{notes_js}
</script>
<script>
{refresh_js}
</script>

</body>
</html>"""
    return html

df, generated_at = run_fetch()
html = build_html(df, generated_at)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done - index.html written")
