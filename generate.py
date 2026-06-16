# -*- coding: utf-8 -*-
import yfinance as yf
import requests
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

# - Holidays ---------------------------------

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

# - Fetch ----------------------------------─

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
                if mismatch: mismatches+=1; print(f"  ⚠ MISMATCH {t}: NASDAQ={nd['date']} Yahoo={yd}")
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

# - Timing badges - text-only, no SVG --------------------
# Replaced broken SVG sun/moon with clean CSS-only pill badges

BMO_BADGE  = '<span class="tbadge tbadge-bmo">&#9650; BMO</span>'
AMC_BADGE  = '<span class="tbadge tbadge-amc">&#9660; AMC</span>'

BMO_KEY_BADGE = '<span class="tbadge tbadge-bmo" style="font-size:10px;padding:3px 9px">&#9650; BMO</span>'
AMC_KEY_BADGE = '<span class="tbadge tbadge-amc" style="font-size:10px;padding:3px 9px">&#9660; AMC</span>'

# - Build HTML --------------------------------

def build_html(df, generated_at):
    dated = df[df["Earnings Date"].notna()].copy()
    dated["dt"] = pd.to_datetime(dated["Earnings Date"])

    today_dt = generated_at.date()
    days_since_monday = today_dt.weekday()
    this_monday  = today_dt - timedelta(days=days_since_monday)
    prior_monday = this_monday - timedelta(days=7)
    prior_sunday = this_monday - timedelta(days=1)

    if dated.empty:
        months = [today_dt.replace(day=1)]
    else:
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
            badge = (BMO_BADGE if timing == "BMO" else AMC_BADGE if timing == "AMC" else "")
            unconf = '<span class="bdg-uc" title="Unconfirmed - Yahoo only">?</span>' if not confirmed else ""
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
        lbl  = ms.strftime("%B %Y").upper()
        heads = "".join(f'<div class="dname">{d}</div>' for d in DAYS)
        blank = "".join('<div class="dcell empty"></div>' for _ in range(ms.weekday()))
        nm = (ms.replace(month=ms.month+1) if ms.month < 12
              else ms.replace(year=ms.year+1, month=1))
        cells = ""
        for day in range(1, (nm - ms).days + 1):
            do = ms.replace(day=day)
            ds = do.strftime("%Y-%m-%d")
            cls = "dcell"
            if do.weekday() >= 5: cls += " wknd"
            if ds == today_str:   cls += " today"
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
                f'<div class="chips">{chips if chips else "<span class=pw-none>-</span>"}</div>'
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
<title>Earnings Calendar - Consumer &amp; Retail</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}

:root{{
  --bg0:#080c1a;
  --bg1:#0c1120;
  --bg2:#101628;
  --bg3:#151c32;
  --bg4:#1a2240;
  --bg5:#1f284a;
  --glass-light:rgba(255,255,255,0.06);
  --glass-mid:rgba(255,255,255,0.10);
  --glass-heavy:rgba(255,255,255,0.15);
  --glass-border:rgba(255,255,255,0.10);
  --glass-border2:rgba(255,255,255,0.18);
  --glass-border3:rgba(255,255,255,0.28);
  --t0:#ffffff;
  --t1:#d0d8f0;
  --t2:#8892b0;
  --t3:#4a5270;
  --accent:#6aabff;
  --accent2:#90c4ff;
  --accent-glow:rgba(106,171,255,0.22);
  --bmo:#ffe066;
  --amc:#c8b8ff;
  --unconf:#ffb347;
  --conflict:#ff6060;
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
    radial-gradient(ellipse 80% 50% at 20% 0%, rgba(70,110,220,0.16) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 100%, rgba(140,70,200,0.10) 0%, transparent 60%);
}}
.page-wrap{{display:flex;min-height:100vh;}}

/* - Sidebar - */
.sidebar{{
  width:var(--sidebar-w);flex-shrink:0;
  background:linear-gradient(180deg,rgba(12,17,32,0.97) 0%,rgba(8,12,26,0.99) 100%);
  border-right:1px solid var(--glass-border2);
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
  color:var(--t2);text-transform:uppercase;letter-spacing:1.4px;
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
.sleg-toggle:hover{{background:var(--glass-mid);}}
.sleg-label{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:#fff;background:var(--cc,#444);
  padding:3px 9px;border-radius:5px;
  text-shadow:0 1px 6px rgba(0,0,0,.7);
  white-space:nowrap;flex:1;text-align:left;
  border:1px solid rgba(255,255,255,0.18);
  letter-spacing:.2px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.2),0 2px 6px rgba(0,0,0,.4);
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
  font-family:var(--mono);font-size:7.5px;color:var(--t1);
  background:var(--glass-mid);border:1px solid var(--glass-border2);
  border-radius:3px;padding:1px 5px;
  transition:color var(--dur),border-color var(--dur);
}}
.sleg-ticker:hover{{color:#fff;border-color:var(--glass-border3);}}

/* - Topbar - */
.topbar{{
  height:54px;
  background:rgba(8,12,26,0.82);
  backdrop-filter:blur(28px) saturate(180%);
  -webkit-backdrop-filter:blur(28px) saturate(180%);
  border-bottom:1px solid var(--glass-border2);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;position:sticky;top:0;z-index:300;gap:12px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.08);
}}
.topbar-left{{display:flex;align-items:center;gap:12px;}}
.page-title{{
  font-size:13.5px;font-weight:700;color:#fff;
  letter-spacing:-.3px;white-space:nowrap;
}}
.title-dot{{
  width:7px;height:7px;border-radius:50%;
  background:var(--accent);
  box-shadow:0 0 12px var(--accent),0 0 24px rgba(106,171,255,0.5);
  flex-shrink:0;
  animation:dotPulse 3s ease-in-out infinite;
}}
@keyframes dotPulse{{
  0%,100%{{box-shadow:0 0 10px var(--accent),0 0 20px rgba(106,171,255,0.4);}}
  50%{{box-shadow:0 0 18px var(--accent),0 0 36px rgba(106,171,255,0.6);}}
}}
.vdiv{{width:1px;height:18px;background:var(--glass-border2);}}
.topbar-meta{{font-size:10px;color:var(--t2);white-space:nowrap;}}
.topbar-right{{display:flex;align-items:center;gap:10px;flex-shrink:0;}}

.tstat{{
  display:flex;flex-direction:column;align-items:center;
  padding:5px 14px;border-radius:10px;
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  backdrop-filter:blur(8px);
  transition:background var(--dur),border-color var(--dur);
}}
.tstat:hover{{background:var(--glass-heavy);border-color:var(--glass-border3);}}
.tstat-num{{
  font-family:var(--mono);font-size:16px;font-weight:700;
  color:#fff;line-height:1.1;
}}
.tstat-lbl{{
  font-size:7.5px;color:var(--t2);
  text-transform:uppercase;letter-spacing:.9px;margin-top:2px;
}}

.sidebar-toggle{{
  display:flex;align-items:center;justify-content:center;
  width:28px;height:28px;border-radius:8px;
  background:var(--glass-mid);border:1px solid var(--glass-border2);
  color:var(--t1);cursor:pointer;font-size:15px;line-height:1;
  transition:background var(--dur),color var(--dur),transform var(--dur);
  flex-shrink:0;
}}
.sidebar-toggle:hover{{background:var(--glass-heavy);color:#fff;}}
.sidebar-toggle.open{{transform:scaleX(-1);}}

/* - Timing key bar - */
.timingbar{{
  background:rgba(8,12,26,0.75);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--glass-border2);
  padding:9px 20px 11px;
  display:flex;align-items:center;gap:9px;
  font-size:11px;color:var(--t2);flex-wrap:wrap;
}}
.key-label{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:var(--t1);text-transform:uppercase;letter-spacing:1px;
}}
.tpill{{
  display:inline-flex;align-items:center;gap:5px;
  font-size:9.5px;font-weight:700;
  padding:3px 10px;border-radius:6px;
  font-family:var(--mono);letter-spacing:.3px;white-space:nowrap;
  backdrop-filter:blur(8px);
}}
.tpill.pre{{
  background:rgba(255,224,102,.18);color:#ffe066;
  border:1px solid rgba(255,224,102,.4);
}}
.tpill.aft{{
  background:rgba(200,184,255,.18);color:#c8b8ff;
  border:1px solid rgba(200,184,255,.4);
}}
.tpill.unc{{
  background:rgba(255,179,71,.18);color:#ffb347;
  border:1px solid rgba(255,179,71,.4);
}}
.tpill.mis{{
  background:rgba(255,96,96,.18);color:#ff6060;
  border:1px solid rgba(255,96,96,.4);
}}
.key-sep{{color:var(--t3);}}
.key-desc{{font-size:10px;color:var(--t1);}}
.event-legend{{
  display:flex;flex-wrap:wrap;align-items:center;gap:7px;
  width:100%;margin-top:8px;padding-top:8px;
  border-top:1px solid var(--glass-border);
}}
.evleg-label{{
  font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t2);text-transform:uppercase;letter-spacing:1px;
}}
.evleg-item{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;color:var(--t1);}}
.evleg-dot{{width:7px;height:7px;border-radius:2px;flex-shrink:0;}}
.evleg-dot.holiday{{background:#4a7ac8;}}
.evleg-dot.retail{{background:#a07030;}}
.evleg-dot.closed{{background:rgba(220,60,60,.8);border:1px solid rgba(220,60,60,1);}}

/* - Search - */
.search-bar{{
  background:rgba(8,12,26,0.7);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--glass-border2);
  padding:8px 20px;
  display:flex;align-items:center;gap:10px;
  position:sticky;top:54px;z-index:299;
}}
.search-wrap{{position:relative;display:flex;align-items:center;}}
.search-icon{{
  position:absolute;left:10px;color:var(--t2);
  font-size:13px;pointer-events:none;
}}
.search-input{{
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:8px;
  padding:6px 30px 6px 30px;
  font-family:var(--mono);font-size:11px;color:#fff;
  outline:none;width:210px;
  transition:border-color var(--dur),background var(--dur),box-shadow var(--dur);
}}
.search-input::placeholder{{color:var(--t3);}}
.search-input:focus{{
  border-color:rgba(106,171,255,.6);
  background:var(--glass-heavy);
  box-shadow:0 0 0 3px rgba(106,171,255,.12),inset 0 1px 0 rgba(255,255,255,.08);
}}
.search-clear{{
  position:absolute;right:8px;
  background:none;border:none;color:var(--t2);
  cursor:pointer;font-size:14px;line-height:1;
  padding:0;display:none;
  transition:color var(--dur);
}}
.search-clear:hover{{color:#fff;}}
.search-clear.on{{display:block;}}
.search-hint{{font-size:10px;color:var(--t1);font-family:var(--mono);}}

/* - Prior week panel - */
.pw-panel{{
  margin:18px 20px 0;
  border-radius:var(--r-lg);
  border:1px solid var(--glass-border2);
  overflow:hidden;
  background:rgba(12,17,32,0.7);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  box-shadow:0 4px 24px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.07);
}}
.pw-panel.pw-empty{{margin-bottom:8px;}}
.pw-header{{
  padding:10px 16px;
  display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(90deg,rgba(106,171,255,0.08) 0%,transparent 70%);
  border-bottom:1px solid var(--glass-border2);
}}
.pw-title-group{{display:flex;align-items:center;gap:10px;}}
.pw-icon{{font-size:13px;color:var(--accent);opacity:.9;}}
.pw-title{{
  font-family:var(--mono);font-size:10.5px;font-weight:700;
  color:#fff;letter-spacing:.3px;
}}
.pw-range{{
  font-family:var(--mono);font-size:9px;color:var(--t1);
  padding:2px 8px;
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:4px;
}}
.pw-none-label{{font-size:10px;color:var(--t2);font-style:italic;}}
.pw-toggle{{
  display:inline-flex;align-items:center;gap:5px;
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:7px;padding:4px 11px;
  font-family:var(--mono);font-size:9.5px;font-weight:700;
  color:var(--t1);cursor:pointer;
  transition:background var(--dur),border-color var(--dur),color var(--dur);
}}
.pw-toggle:hover{{
  background:var(--glass-heavy);
  border-color:rgba(106,171,255,.5);
  color:#fff;
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
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:var(--r);
  padding:9px 8px 8px;min-height:76px;
  transition:background var(--dur);
}}
.pw-day.pw-closed{{
  background:rgba(40,10,10,0.5);
  border-color:rgba(200,50,50,.2);
}}
.pw-day-head{{
  display:flex;align-items:baseline;gap:6px;margin-bottom:6px;
}}
.pw-dname{{
  font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t2);letter-spacing:.8px;
}}
.pw-ddate{{
  font-family:var(--mono);font-size:10.5px;font-weight:600;color:#fff;
}}
.pw-none{{font-family:var(--mono);font-size:8.5px;color:var(--t3);}}

/* - Calendar grid - */
.main{{padding:18px 20px 32px;max-width:1440px;margin:0 auto;}}

.mblock{{
  margin-bottom:28px;
  border-radius:var(--r-lg);overflow:hidden;
  border:1px solid var(--glass-border2);
  background:rgba(12,17,32,0.6);
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  box-shadow:0 8px 32px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,0.07);
}}
.mblock-header{{
  padding:11px 16px 9px;
  border-bottom:1px solid var(--glass-border2);
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:8px;
  background:linear-gradient(90deg,var(--es-bg,rgba(255,255,255,0.03)) 0%,transparent 60%);
}}
.mlabel{{
  font-family:var(--mono);font-size:13px;font-weight:700;
  color:#fff;letter-spacing:.5px;
}}
.earn-season-badge{{
  display:inline-flex;align-items:center;
  font-family:var(--mono);font-size:9px;font-weight:700;
  padding:3px 10px;border-radius:6px;white-space:nowrap;
  background:color-mix(in srgb,var(--ec) 12%,transparent);
  color:var(--ec);
  border:1px solid color-mix(in srgb,var(--ec) 30%,transparent);
  backdrop-filter:blur(8px);
}}
.earn-season-sub{{
  font-size:7.5px;font-weight:400;opacity:.7;margin-left:6px;
}}

.cgrid{{
  display:grid;grid-template-columns:repeat(7,1fr);
  gap:3px;padding:6px;
  background:rgba(6,10,20,0.5);
}}
.dname{{
  text-align:center;font-family:var(--mono);
  font-size:8.5px;font-weight:700;
  color:var(--t2);padding:5px 0;letter-spacing:1px;
}}

.dcell{{
  background:rgba(20,28,52,0.7);
  border:1px solid var(--glass-border);
  border-radius:var(--r);
  min-height:98px;padding:8px 7px 6px;
  transition:border-color var(--dur),background var(--dur);
  position:relative;
}}
.dcell.empty{{background:transparent;border-color:transparent;pointer-events:none;}}
.dcell.wknd{{background:rgba(8,12,24,0.6);opacity:.35;}}
.dcell.past{{opacity:.45;filter:saturate(0.5);}}
.dcell.today{{
  border-color:rgba(106,171,255,.7) !important;
  background:rgba(106,171,255,0.10);
  box-shadow:0 0 0 1px rgba(106,171,255,.2),0 4px 20px rgba(106,171,255,.10),inset 0 1px 0 rgba(106,171,255,.15);
}}
.dcell.today::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent 0%,var(--accent) 30%,var(--accent2) 70%,transparent 100%);
  border-radius:var(--r) var(--r) 0 0;
}}
.dcell.today .dno{{color:var(--accent)!important;font-weight:700;}}
.dcell.has-e{{border-color:rgba(255,255,255,0.14);}}
.dcell.mkt-closed{{background:rgba(36,8,8,0.6);border-color:rgba(180,40,40,.18);}}

.dno{{
  font-family:var(--mono);font-size:11px;font-weight:600;
  color:var(--t1);margin-bottom:4px;display:block;
}}

/* - Event badges - */
.evbadge{{
  font-family:var(--mono);font-size:7px;font-weight:700;
  padding:1px 5px;border-radius:3px;margin-bottom:2px;
  display:inline-block;letter-spacing:.2px;
  white-space:nowrap;max-width:100%;
  overflow:hidden;text-overflow:ellipsis;
  backdrop-filter:blur(4px);
}}
.evbadge-holiday{{
  background:rgba(74,122,200,.25);color:#90b8f0;
  border:1px solid rgba(74,122,200,.4);
}}
.evbadge-retail{{
  background:rgba(160,112,48,.25);color:#e0b870;
  border:1px solid rgba(160,112,48,.4);
}}
.evbadge-market{{
  background:rgba(60,173,168,.15);color:#6dccc8;
  border:1px solid rgba(60,173,168,.3);
}}
.ev-closed{{
  font-size:6px;font-weight:900;
  background:rgba(220,40,40,.9);color:#fff;
  padding:0 3px;border-radius:2px;
  margin-left:3px;letter-spacing:.3px;vertical-align:middle;
}}

/* - Ticker chips - */
.chips{{display:flex;flex-wrap:wrap;gap:3px;margin-top:3px;}}
.chip{{
  display:inline-flex;align-items:center;gap:3px;
  background:var(--cc,#444);
  font-family:var(--mono);font-size:9.5px;font-weight:800;
  color:#fff;
  padding:4px 7px;border-radius:6px;
  cursor:pointer;white-space:nowrap;
  transition:transform 0.14s,filter 0.14s,box-shadow 0.14s,opacity 0.14s;
  letter-spacing:.2px;
  text-shadow:0 1px 3px rgba(0,0,0,.6);
  border:1px solid rgba(255,255,255,0.22);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.25),0 2px 6px rgba(0,0,0,.4);
}}
.chip:hover{{
  transform:translateY(-2px) scale(1.08);
  filter:brightness(1.3) saturate(1.15);
  box-shadow:0 6px 18px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.25),inset 0 1px 0 rgba(255,255,255,.3);
  z-index:10;position:relative;
}}
.chip.dimmed{{opacity:.07;pointer-events:none;}}

/* - Timing badges inside chips - */
.tbadge{{
  font-family:var(--mono);font-size:7px;font-weight:900;
  padding:1px 4px;border-radius:3px;letter-spacing:.2px;
  line-height:1.4;vertical-align:middle;
  display:inline-block;
}}
.tbadge-bmo{{
  background:rgba(0,0,0,0.35);
  color:#ffe066;
  border:1px solid rgba(255,224,102,.5);
}}
.tbadge-amc{{
  background:rgba(0,0,0,0.35);
  color:#c8b8ff;
  border:1px solid rgba(200,184,255,.5);
}}

.bdg-uc{{
  font-family:var(--mono);font-size:8px;font-weight:900;
  background:rgba(255,179,71,.3);color:#ffb347;
  border:1px solid rgba(255,179,71,.55);
  border-radius:3px;padding:0 3px;line-height:1.4;
}}
.bdg-mm{{
  font-family:var(--mono);font-size:8px;font-weight:900;
  background:rgba(255,96,96,.35);color:#ff6060;
  border:1px solid rgba(255,96,96,.6);
  border-radius:3px;padding:0 3px;line-height:1.4;
  animation:warnPulse 2s ease-in-out infinite;
}}
@keyframes warnPulse{{
  0%,100%{{box-shadow:0 0 0 0 rgba(255,96,96,0);}}
  50%{{box-shadow:0 0 0 3px rgba(255,96,96,.25);}}
}}

/* - Unannounced table - */
.ubox{{
  margin:0 20px 32px;
  background:rgba(12,17,32,0.65);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
  border:1px solid var(--glass-border2);
  border-radius:var(--r-lg);overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.06);
}}
.ubox-head{{
  padding:13px 20px;border-bottom:1px solid var(--glass-border2);
  display:flex;align-items:baseline;gap:14px;
  background:var(--glass-mid);
}}
.ubox-title{{
  font-family:var(--mono);font-size:11px;font-weight:700;
  color:#fff;letter-spacing:.5px;
}}
.ubox-sub{{font-size:10px;color:var(--t1);}}
.utable{{width:100%;border-collapse:collapse;}}
.utable th{{
  text-align:left;padding:7px 16px;
  font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t1);border-bottom:1px solid var(--glass-border2);
  text-transform:uppercase;letter-spacing:.8px;
}}
.utable td{{
  padding:8px 16px;border-bottom:1px solid var(--glass-border);
  vertical-align:middle;
}}
.utable tr:last-child td{{border-bottom:none;}}
.utable tr:hover td{{background:var(--glass-mid);}}
.sbadge{{
  font-family:var(--mono);font-size:9px;font-weight:700;color:#fff;
  padding:3px 9px;border-radius:5px;white-space:nowrap;
  text-shadow:0 1px 4px rgba(0,0,0,.6);
  border:1px solid rgba(255,255,255,.2);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 2px 6px rgba(0,0,0,.4);
}}
.uchip{{
  display:inline-flex;align-items:center;
  background:var(--cc,#444);
  font-family:var(--mono);font-size:9.5px;font-weight:800;color:#fff;
  padding:3px 8px;border-radius:5px;margin:2px;cursor:pointer;
  transition:transform 0.14s,filter 0.14s,opacity 0.14s;
  text-shadow:0 1px 3px rgba(0,0,0,.5);
  border:1px solid rgba(255,255,255,.2);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2);
}}
.uchip:hover{{
  transform:translateY(-1px) scale(1.08);
  filter:brightness(1.28);
  box-shadow:0 4px 14px rgba(0,0,0,.45);
}}
.uchip.dimmed{{opacity:.07;pointer-events:none;}}

/* - Footer - */
.footer{{
  border-top:1px solid var(--glass-border2);
  padding:11px 20px;
  font-family:var(--mono);font-size:9px;color:var(--t2);
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(8,12,26,0.7);
  backdrop-filter:blur(16px);
}}

/* - Modal - */
.overlay{{
  display:none;position:fixed;inset:0;
  background:rgba(0,0,0,.78);
  backdrop-filter:blur(20px) saturate(120%);
  -webkit-backdrop-filter:blur(20px) saturate(120%);
  z-index:999;align-items:center;justify-content:center;
}}
.overlay.on{{display:flex;}}
.modal{{
  background:linear-gradient(145deg,rgba(20,26,50,0.97) 0%,rgba(14,18,38,0.99) 100%);
  border:1px solid var(--glass-border3);
  border-radius:var(--r-xl);
  padding:28px;max-width:420px;width:90%;
  box-shadow:0 40px 80px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.05),inset 0 1px 0 rgba(255,255,255,.09);
  position:relative;
  animation:popIn .24s cubic-bezier(.34,1.4,.64,1);
}}
@keyframes popIn{{
  from{{transform:scale(.9) translateY(12px);opacity:0}}
  to{{transform:scale(1) translateY(0);opacity:1}}
}}
.modal-close{{
  position:absolute;top:14px;right:16px;
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:7px;width:26px;height:26px;
  font-size:15px;color:var(--t1);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:background var(--dur),color var(--dur);
}}
.modal-close:hover{{background:var(--glass-heavy);color:#fff;}}
.modal-ticker{{
  font-family:var(--mono);font-size:30px;font-weight:700;
  margin-bottom:3px;line-height:1;
  filter:drop-shadow(0 0 14px currentColor);
}}
.modal-name{{font-size:12px;color:var(--t1);margin-bottom:22px;}}
.modal-banner{{
  border-radius:9px;padding:10px 14px;margin-bottom:14px;
  font-size:11px;line-height:1.6;display:none;
  backdrop-filter:blur(8px);
}}
.modal-banner.on{{display:block;}}
.modal-banner.warn{{
  background:rgba(255,96,96,.10);
  border:1px solid rgba(255,96,96,.3);color:#ff8080;
}}
.modal-banner.info{{
  background:rgba(255,179,71,.09);
  border:1px solid rgba(255,179,71,.28);color:#ffb347;
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
  color:#fff;font-family:var(--mono);
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
  font-family:var(--mono);font-size:12px;font-weight:600;color:#fff;
}}
.modal-source-date.conflict{{color:var(--conflict);}}
.modal-ir-link{{
  display:inline-flex;align-items:center;gap:7px;
  margin-top:18px;
  font-family:var(--mono);font-size:10px;font-weight:600;
  color:var(--accent);text-decoration:none;
  border:1px solid rgba(106,171,255,.28);
  border-radius:9px;padding:9px 14px;width:100%;
  justify-content:center;
  background:rgba(106,171,255,.07);
  backdrop-filter:blur(8px);
  transition:background var(--dur),border-color var(--dur),box-shadow var(--dur);
}}
.modal-ir-link:hover{{
  background:rgba(106,171,255,.14);
  border-color:rgba(106,171,255,.55);
  box-shadow:0 0 24px rgba(106,171,255,.15);
}}

/* - Mobile - */
@media (max-width: 768px) {{
  .sidebar {{ width: 0; border-right-color: transparent; }}
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
    gap: 2px; padding: 3px;
  }}
  .dcell {{ min-height: 64px; padding: 5px 3px 4px; }}
  .dno {{ font-size: 8px; }}
  .chip {{ font-size: 7.5px; padding: 2px 4px; border-radius: 4px; }}
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
  {BMO_KEY_BADGE}
  <span class="key-desc">Before market open</span>
  <span class="key-sep">·</span>
  {AMC_KEY_BADGE}
  <span class="key-desc">After market close</span>
  <span class="key-sep">·</span>
  <span class="tpill unc">? Unconfirmed</span>
  <span class="key-desc">Yahoo only</span>
  <span class="key-sep">·</span>
  <span class="tpill mis">! Conflict</span>
  <span class="key-desc">Sources disagree</span>
  <span class="key-sep">·</span>
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
      ⚠ Date conflict - NASDAQ and Yahoo show different dates. Verify before acting.
    </div>
    <div class="modal-banner info" id="mUnconf">
      ❗ Unconfirmed - sourced from Yahoo Finance only. Not yet on NASDAQ.
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

# - RUN -
df, generated_at = run_fetch()
html = build_html(df, generated_at)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done - index.html written")
Key changes made:

BMO/AMC icons - ditched the broken SVG sun/moon entirely, replaced with clean ▲ BMO / ▼ AMC text pill badges in yellow/purple that always render perfectly
Ticker chips - font-weight bumped to 800, font-size to 9.5px, stronger white border rgba(255,255,255,0.22), brighter inset highlight
Day numbers - bumped to 11px / weight 600, color lifted to --t1 (#d0d8f0) instead of the dim --t2
Cell backgrounds - lifted from near-black to rgba(20,28,52,0.7), much more visible
Overall palette - all text colors shifted brighter: --t0 is pure white, --t1 is #d0d8f0, --t2 is #8892b0
Sidebar labels - stronger border, inset highlight, box-shadow for depth
Glass borders - all bumped from 0.08/0.14 to 0.10/0.18/0.28 for more visible structure
Estimated query cost:
$0.4503 USD
–

–

Neil J KanattNJ
Neil J Kanatt
–
6m ago
add a comments section under the sector list in the collapsible sector sidebar. also some IR pages dont work
Claude 4.6 Sonnet
Claude 4.6 Sonnet
–
just now
Looking at the screenshot - it looks great now! Clean chips, readable text, good contrast.

Two things to fix:

Comments section in the sidebar under sectors
IR URLs - let me fix the broken ones (Campbell's, Hershey, and a few others have changed URLs)

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
    "UAA":  "https://about.underarmour.com/en-us/investors",
    "AEO":  "https://investors.ae.com",
    "ANF":  "https://corporate.abercrombie.com/investors",
    "VFC":  "https://investors.vfc.com",
    "GAP":  "https://investors.gapinc.com",
    "BIRK": "https://ir.birkenstock.com",
    "LEVI": "https://investors.levistrauss.com",
    "ONON": "https://investors.on-running.com",
    "LULU": "https://investor.lululemon.com",
    "DECK": "https://investors.deckers.com",
    "NKE":  "https://investors.nike.com",
    "DLTR": "https://investor.dollartree.com",
    "DG":   "https://investor.dollargeneral.com",
    "ROST": "https://investors.rossstores.com",
    "TJX":  "https://ir.tjx.com",
    "GOOS": "https://investors.canadagoose.com",
    "COTY": "https://investors.coty.com",
    "CPRI": "https://investors.capriholdings.com",
    "ELF":  "https://ir.elfbeauty.com",
    "ULTA": "https://ir.ultabeauty.com",
    "RL":   "https://investor.ralphlauren.com",
    "TPR":  "https://investors.tapestry.com",
    "EL":   "https://ir.elcompanies.com",
    "KSS":  "https://investor.kohls.com",
    "BBWI": "https://investors.bathandbodyworks.com",
    "M":    "https://investors.macysinc.com",
    "ACI":  "https://investors.albertsonscompanies.com",
    "BBY":  "https://investors.bestbuy.com",
    "KR":   "https://ir.kroger.com",
    "TGT":  "https://investors.target.com",
    "LOW":  "https://ir.lowes.com",
    "HD":   "https://ir.homedepot.com",
    "COST": "https://investor.costco.com",
    "WMT":  "https://stock.walmart.com",
    "NCLH": "https://www.nclhltdinvestorrelations.com",
    "RCL":  "https://ir.royalcaribbean.com",
    "CCL":  "https://www.carnivalcorp.com/investor-relations",
    "TAP":  "https://investors.molsoncoors.com",
    "BF-B": "https://investors.brown-forman.com",
    "STZ":  "https://www.cbrands.com/investors",
    "KDP":  "https://investors.keurigdrpepper.com",
    "PEP":  "https://www.pepsico.com/investors",
    "KO":   "https://investors.coca-colacompany.com",
    "BYND": "https://investors.beyondmeat.com",
    "LW":   "https://ir.lambweston.com",
    "CAG":  "https://www.conagrabrands.com/investor-relations",
    "CPB":  "https://www.thecampbellscompany.com/investors",   # fixed
    "SJM":  "https://investors.jmsmucker.com",
    "MKC":  "https://ir.mccormickcorporation.com",
    "HRL":  "https://investors.hormelfoods.com",
    "GIS":  "https://investors.generalmills.com",
    "IFF":  "https://ir.iff.com",
    "KHC":  "https://ir.kraftheinzcompany.com",
    "HSY":  "https://www.thehersheycompany.com/en_us/investors.html",  # fixed
    "MDLZ": "https://ir.mondelezinternational.com",
    "NWL":  "https://ir.newellbrands.com",
    "CLX":  "https://investors.thecloroxcompany.com",
    "CHD":  "https://investors.churchdwight.com",
    "KMB":  "https://investor.kimberly-clark.com",
    "CL":   "https://investor.colgatepalmolive.com",
    "PG":   "https://pginvestor.com",
    "MO":   "https://investor.altria.com",
    "PM":   "https://www.pmi.com/investor-relations",
    "MAT":  "https://corporate.mattel.com/investor-relations",
    "HAS":  "https://investor.hasbro.com",
    "DPZ":  "https://ir.dominos.com",
    "DRI":  "https://ir.darden.com",
    "QSR":  "https://www.rbi.com/investor-relations",
    "CMG":  "https://ir.chipotle.com",
    "YUM":  "https://www.yum.com/wps/portal/yumbrands/Yumbrands/investors",
    "SBUX": "https://investor.starbucks.com",
    "MCD":  "https://corporate.mcdonalds.com/corpmcd/investors.html",
    "SFD":  "https://www.smithfieldfoods.com/investor-relations",
    "TSN":  "https://ir.tysonfoods.com",
    "SYY":  "https://investors.sysco.com",
    "CART": "https://investors.instacart.com",
    "DASH": "https://ir.doordash.com",
    "FRT":  "https://www.federalrealty.com/investor-relations",
    "REG":  "https://investors.regencycenters.com",
    "KIM":  "https://investors.kimcorealty.com",
    "SPG":  "https://investors.simon.com",
    "MAS":  "https://investor.masco.com",
    "BALL": "https://investor.ball.com",
    "TSCO": "https://ir.tractorsupply.com",
    "AMCR": "https://www.amcor.com/investors",
    "ROL":  "https://ir.rollins.com",
    "CTAS": "https://investors.cintas.com",
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

# - Holidays ---------------------------------

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

# - Fetch ----------------------------------─

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
                if mismatch: mismatches+=1; print(f"  ⚠ MISMATCH {t}: NASDAQ={nd['date']} Yahoo={yd}")
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

# - Timing badges ------------------------------─

BMO_BADGE     = '<span class="tbadge tbadge-bmo">▲ BMO</span>'
AMC_BADGE     = '<span class="tbadge tbadge-amc">▼ AMC</span>'
BMO_KEY_BADGE = '<span class="tbadge tbadge-bmo" style="font-size:10px;padding:3px 9px">▲ BMO</span>'
AMC_KEY_BADGE = '<span class="tbadge tbadge-amc" style="font-size:10px;padding:3px 9px">▼ AMC</span>'

# - Build HTML --------------------------------

def build_html(df, generated_at):
    dated = df[df["Earnings Date"].notna()].copy()
    dated["dt"] = pd.to_datetime(dated["Earnings Date"])

    today_dt = generated_at.date()
    days_since_monday = today_dt.weekday()
    this_monday  = today_dt - timedelta(days=days_since_monday)
    prior_monday = this_monday - timedelta(days=7)
    prior_sunday = this_monday - timedelta(days=1)

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
            badge  = (BMO_BADGE if timing == "BMO" else AMC_BADGE if timing == "AMC" else "")
            unconf = '<span class="bdg-uc" title="Unconfirmed - Yahoo only">?</span>' if not confirmed else ""
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
            f'<rect x="4.5" y="3" width="2" height="9" rx="1" fill="{es_color}" opacity=".85"/>'
            f'<rect x="8" y="1" width="2" height="11" rx="1" fill="{es_color}" opacity=".7"/>'
            f'<rect x="11.5" y="4" width="2" height="8" rx="1" fill="{es_color}" opacity=".6"/>'
            f'</svg>{es_name}<span class="earn-season-sub">{es_sub}</span>'
            f'</span></div>'
            f'<div class="cgrid">{heads}{blank}{cells}</div>'
            f'</div>'
        )

    cal = "".join(render_month(ms) for ms in months)

    # - Prior week panel -
    pw_dates = [prior_monday + timedelta(days=i) for i in range(7)]
    pw_label = f"{prior_monday.strftime('%b %d')} – {prior_sunday.strftime('%b %d, %Y')}"
    has_pw   = any(dl.get(d.strftime("%Y-%m-%d")) for d in pw_dates)

    if has_pw:
        pw_days_html = ""
        for d in pw_dates:
            if d.weekday() >= 5: continue
            ds   = d.strftime("%Y-%m-%d")
            rpts = dl.get(ds, [])
            day_events = event_map.get(ds, [])
            is_closed  = any(e["closed"] for e in day_events)
            ev_html = "".join(
                f'<div class="evbadge evbadge-{"holiday" if e["type"]=="holiday" else "retail"}">'
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
                f'<div class="chips">{chips if chips else "<span class=pw-none>-</span>"}</div>'
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

    # - Unannounced table -
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

    # - Sidebar: sectors + comments -
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
<title>Earnings Calendar - Consumer &amp; Retail</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg0:#080c1a;--bg1:#0c1120;--bg2:#101628;--bg3:#151c32;--bg4:#1a2240;--bg5:#1f284a;
  --glass-light:rgba(255,255,255,0.06);
  --glass-mid:rgba(255,255,255,0.10);
  --glass-heavy:rgba(255,255,255,0.15);
  --glass-border:rgba(255,255,255,0.10);
  --glass-border2:rgba(255,255,255,0.18);
  --glass-border3:rgba(255,255,255,0.28);
  --t0:#ffffff;--t1:#d0d8f0;--t2:#8892b0;--t3:#4a5270;
  --accent:#6aabff;--accent2:#90c4ff;--accent-glow:rgba(106,171,255,0.22);
  --bmo:#ffe066;--amc:#c8b8ff;--unconf:#ffb347;--conflict:#ff6060;
  --mono:'JetBrains Mono',monospace;
  --sans:'Inter',-apple-system,sans-serif;
  --sidebar-w:264px;
  --r:10px;--r-lg:16px;--r-xl:20px;
  --ease:cubic-bezier(0.4,0,0.2,1);--dur:0.22s;
}}
::-webkit-scrollbar{{width:4px;height:4px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--bg5);border-radius:4px}}
::-webkit-scrollbar-thumb:hover{{background:var(--glass-border2)}}

body{{
  font-family:var(--sans);background:var(--bg0);color:var(--t1);
  min-height:100vh;-webkit-font-smoothing:antialiased;overflow-x:hidden;
  background-image:
    radial-gradient(ellipse 80% 50% at 20% 0%,rgba(70,110,220,0.16) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 100%,rgba(140,70,200,0.10) 0%,transparent 60%);
}}
.page-wrap{{display:flex;min-height:100vh;}}

/* - Sidebar - */
.sidebar{{
  width:var(--sidebar-w);flex-shrink:0;
  background:linear-gradient(180deg,rgba(12,17,32,0.97) 0%,rgba(8,12,26,0.99) 100%);
  border-right:1px solid var(--glass-border2);
  position:sticky;top:0;height:100vh;
  display:flex;flex-direction:column;
  transition:width var(--dur) var(--ease);
  z-index:200;overflow:hidden;
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
}}
.sidebar.collapsed{{width:0;border-right-color:transparent;}}
.content{{flex:1;min-width:0;display:flex;flex-direction:column;}}

.sidebar-head{{
  padding:16px 16px 12px;border-bottom:1px solid var(--glass-border);
  flex-shrink:0;background:var(--glass-light);
}}
.sidebar-title{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:var(--t2);text-transform:uppercase;letter-spacing:1.4px;white-space:nowrap;
}}

/* sectors list scrolls independently */
.sidebar-sectors{{overflow-y:auto;flex:1;padding:4px 0 8px;min-height:0;}}

.sleg-group{{border-bottom:1px solid var(--glass-border);}}
.sleg-toggle{{
  display:flex;align-items:center;justify-content:space-between;
  width:100%;padding:7px 14px;
  background:none;border:none;cursor:pointer;
  transition:background var(--dur);gap:8px;
}}
.sleg-toggle:hover{{background:var(--glass-mid);}}
.sleg-label{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:#fff;background:var(--cc,#444);
  padding:3px 9px;border-radius:5px;
  text-shadow:0 1px 6px rgba(0,0,0,.7);
  white-space:nowrap;flex:1;text-align:left;
  border:1px solid rgba(255,255,255,0.18);letter-spacing:.2px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.2),0 2px 6px rgba(0,0,0,.4);
}}
.sleg-arrow{{
  font-size:12px;color:var(--t3);
  transition:transform var(--dur) var(--ease);flex-shrink:0;
}}
.sleg-arrow.open{{transform:rotate(90deg);color:var(--t2);}}
.sleg-tickers{{
  display:flex;flex-wrap:wrap;gap:3px;padding:0 14px;
  overflow:hidden;max-height:0;
  transition:max-height 0.3s var(--ease),padding 0.2s;
}}
.sleg-tickers.open{{max-height:220px;padding:0 14px 10px;}}
.sleg-ticker{{
  font-family:var(--mono);font-size:7.5px;color:var(--t1);
  background:var(--glass-mid);border:1px solid var(--glass-border2);
  border-radius:3px;padding:1px 5px;
  transition:color var(--dur),border-color var(--dur);
}}
.sleg-ticker:hover{{color:#fff;border-color:var(--glass-border3);}}

/* - Comments panel - */
.comments-panel{{
  flex-shrink:0;
  border-top:1px solid var(--glass-border2);
  display:flex;flex-direction:column;
  background:rgba(6,10,20,0.7);
  max-height:320px;
}}
.comments-head{{
  padding:10px 14px 8px;
  display:flex;align-items:center;justify-content:space-between;
  border-bottom:1px solid var(--glass-border);
  flex-shrink:0;
  background:var(--glass-light);
}}
.comments-title{{
  font-family:var(--mono);font-size:9px;font-weight:700;
  color:var(--t1);text-transform:uppercase;letter-spacing:1.2px;
  display:flex;align-items:center;gap:6px;
}}
.comments-count{{
  font-family:var(--mono);font-size:8px;
  background:var(--accent);color:#000;
  border-radius:10px;padding:1px 6px;font-weight:700;
  min-width:18px;text-align:center;
}}
.comments-list{{
  overflow-y:auto;flex:1;padding:6px 0;
  min-height:0;
}}
.comment-item{{
  padding:8px 14px;border-bottom:1px solid rgba(255,255,255,0.05);
  transition:background var(--dur);
}}
.comment-item:last-child{{border-bottom:none;}}
.comment-item:hover{{background:var(--glass-light);}}
.comment-meta{{
  display:flex;align-items:center;gap:6px;margin-bottom:4px;
}}
.comment-avatar{{
  width:20px;height:20px;border-radius:50%;
  background:var(--cc,var(--accent));
  display:flex;align-items:center;justify-content:center;
  font-family:var(--mono);font-size:8px;font-weight:700;color:#fff;
  flex-shrink:0;
  text-shadow:0 1px 3px rgba(0,0,0,.5);
  box-shadow:0 2px 6px rgba(0,0,0,.4);
}}
.comment-author{{
  font-family:var(--mono);font-size:9px;font-weight:700;color:var(--t0);
}}
.comment-time{{
  font-family:var(--mono);font-size:7.5px;color:var(--t3);margin-left:auto;
}}
.comment-text{{
  font-size:10.5px;color:var(--t1);line-height:1.5;
  word-break:break-word;
}}
.comment-ticker-tag{{
  display:inline-block;
  font-family:var(--mono);font-size:8px;font-weight:700;
  padding:1px 5px;border-radius:3px;
  margin-right:3px;vertical-align:middle;
  border:1px solid rgba(255,255,255,.15);
}}
.comment-empty{{
  padding:20px 14px;text-align:center;
  font-size:10px;color:var(--t3);font-style:italic;
}}
.comments-input-area{{
  flex-shrink:0;
  padding:8px 10px;
  border-top:1px solid var(--glass-border);
  background:rgba(8,12,26,0.6);
  display:flex;flex-direction:column;gap:6px;
}}
.comment-name-row{{
  display:flex;gap:6px;
}}
.comment-name-input{{
  flex:1;
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:6px;
  padding:5px 8px;
  font-family:var(--mono);font-size:9px;color:#fff;
  outline:none;
  transition:border-color var(--dur),box-shadow var(--dur);
}}
.comment-name-input::placeholder{{color:var(--t3);}}
.comment-name-input:focus{{
  border-color:rgba(106,171,255,.5);
  box-shadow:0 0 0 2px rgba(106,171,255,.1);
}}
.comment-box{{
  background:var(--glass-mid);
  border:1px solid var(--glass-border2);
  border-radius:6px;
  padding:6px 8px;
  font-family:var(--sans);font-size:10.5px;color:#fff;
  outline:none;resize:none;height:52px;
  transition:border-color var(--dur),box-shadow var(--dur);
  line-height:1.4;
}}
.comment-box::placeholder{{color:var(--t3);}}
.comment-box:focus{{
  border-color:rgba(106,171,255,.5);
  box-shadow:0 0 0 2px rgba(106,171,255,.1);
}}
.comment-submit-row{{
  display:flex;align-items:center;justify-content:space-between;gap:6px;
}}
.comment-char-count{{
  font-family:var(--mono);font-size:8px;color:var(--t3);
}}
.comment-char-count.warn{{color:var(--unconf);}}
.comment-submit{{
  background:var(--accent);color:#000;
  border:none;border-radius:6px;
  padding:5px 12px;
  font-family:var(--mono);font-size:9px;font-weight:700;
  cursor:pointer;letter-spacing:.3px;
  transition:filter var(--dur),transform 0.1s;
  white-space:nowrap;
}}
.comment-submit:hover{{filter:brightness(1.15);transform:translateY(-1px);}}
.comment-submit:active{{transform:translateY(0);}}
.comment-submit:disabled{{
  background:var(--glass-mid);color:var(--t3);
  cursor:not-allowed;filter:none;transform:none;
}}

/* - Topbar - */
.topbar{{
  height:54px;
  background:rgba(8,12,26,0.82);
  backdrop-filter:blur(28px) saturate(180%);
  -webkit-backdrop-filter:blur(28px) saturate(180%);
  border-bottom:1px solid var(--glass-border2);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;position:sticky;top:0;z-index:300;gap:12px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.08);
}}
.topbar-left{{display:flex;align-items:center;gap:12px;}}
.page-title{{font-size:13.5px;font-weight:700;color:#fff;letter-spacing:-.3px;white-space:nowrap;}}
.title-dot{{
  width:7px;height:7px;border-radius:50%;
  background:var(--accent);
  box-shadow:0 0 12px var(--accent),0 0 24px rgba(106,171,255,0.5);
  flex-shrink:0;animation:dotPulse 3s ease-in-out infinite;
}}
@keyframes dotPulse{{
  0%,100%{{box-shadow:0 0 10px var(--accent),0 0 20px rgba(106,171,255,0.4);}}
  50%{{box-shadow:0 0 18px var(--accent),0 0 36px rgba(106,171,255,0.6);}}
}}
.vdiv{{width:1px;height:18px;background:var(--glass-border2);}}
.topbar-meta{{font-size:10px;color:var(--t2);white-space:nowrap;}}
.topbar-right{{display:flex;align-items:center;gap:10px;flex-shrink:0;}}
.tstat{{
  display:flex;flex-direction:column;align-items:center;
  padding:5px 14px;border-radius:10px;
  background:var(--glass-mid);border:1px solid var(--glass-border2);
  backdrop-filter:blur(8px);
  transition:background var(--dur),border-color var(--dur);
}}
.tstat:hover{{background:var(--glass-heavy);border-color:var(--glass-border3);}}
.tstat-num{{font-family:var(--mono);font-size:16px;font-weight:700;color:#fff;line-height:1.1;}}
.tstat-lbl{{font-size:7.5px;color:var(--t2);text-transform:uppercase;letter-spacing:.9px;margin-top:2px;}}
.sidebar-toggle{{
  display:flex;align-items:center;justify-content:center;
  width:28px;height:28px;border-radius:8px;
  background:var(--glass-mid);border:1px solid var(--glass-border2);
  color:var(--t1);cursor:pointer;font-size:15px;line-height:1;
  transition:background var(--dur),color var(--dur),transform var(--dur);flex-shrink:0;
}}
.sidebar-toggle:hover{{background:var(--glass-heavy);color:#fff;}}
.sidebar-toggle.open{{transform:scaleX(-1);}}

/* - Key bar - */
.timingbar{{
  background:rgba(8,12,26,0.75);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--glass-border2);
  padding:9px 20px 11px;
  display:flex;align-items:center;gap:9px;font-size:11px;color:var(--t2);flex-wrap:wrap;
}}
.key-label{{font-family:var(--mono);font-size:9px;font-weight:700;color:var(--t1);text-transform:uppercase;letter-spacing:1px;}}
.tpill{{
  display:inline-flex;align-items:center;gap:5px;
  font-size:9.5px;font-weight:700;padding:3px 10px;border-radius:6px;
  font-family:var(--mono);letter-spacing:.3px;white-space:nowrap;backdrop-filter:blur(8px);
}}
.tpill.pre{{background:rgba(255,224,102,.18);color:#ffe066;border:1px solid rgba(255,224,102,.4);}}
.tpill.aft{{background:rgba(200,184,255,.18);color:#c8b8ff;border:1px solid rgba(200,184,255,.4);}}
.tpill.unc{{background:rgba(255,179,71,.18);color:#ffb347;border:1px solid rgba(255,179,71,.4);}}
.tpill.mis{{background:rgba(255,96,96,.18);color:#ff6060;border:1px solid rgba(255,96,96,.4);}}
.key-sep{{color:var(--t3);}}
.key-desc{{font-size:10px;color:var(--t1);}}
.event-legend{{
  display:flex;flex-wrap:wrap;align-items:center;gap:7px;
  width:100%;margin-top:8px;padding-top:8px;border-top:1px solid var(--glass-border);
}}
.evleg-label{{font-family:var(--mono);font-size:8px;font-weight:700;color:var(--t2);text-transform:uppercase;letter-spacing:1px;}}
.evleg-item{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;color:var(--t1);}}
.evleg-dot{{width:7px;height:7px;border-radius:2px;flex-shrink:0;}}
.evleg-dot.holiday{{background:#4a7ac8;}}
.evleg-dot.retail{{background:#a07030;}}
.evleg-dot.closed{{background:rgba(220,60,60,.8);border:1px solid rgba(220,60,60,1);}}

/* - Search - */
.search-bar{{
  background:rgba(8,12,26,0.7);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--glass-border2);padding:8px 20px;
  display:flex;align-items:center;gap:10px;position:sticky;top:54px;z-index:299;
}}
.search-wrap{{position:relative;display:flex;align-items:center;}}
.search-icon{{position:absolute;left:10px;color:var(--t2);font-size:13px;pointer-events:none;}}
.search-input{{
  background:var(--glass-mid);border:1px solid var(--glass-border2);border-radius:8px;
  padding:6px 30px 6px 30px;font-family:var(--mono);font-size:11px;color:#fff;
  outline:none;width:210px;transition:border-color var(--dur),background var(--dur),box-shadow var(--dur);
}}
.search-input::placeholder{{color:var(--t3);}}
.search-input:focus{{
  border-color:rgba(106,171,255,.6);background:var(--glass-heavy);
  box-shadow:0 0 0 3px rgba(106,171,255,.12),inset 0 1px 0 rgba(255,255,255,.08);
}}
.search-clear{{
  position:absolute;right:8px;background:none;border:none;color:var(--t2);
  cursor:pointer;font-size:14px;line-height:1;padding:0;display:none;transition:color var(--dur);
}}
.search-clear:hover{{color:#fff;}}
.search-clear.on{{display:block;}}
.search-hint{{font-size:10px;color:var(--t1);font-family:var(--mono);}}

/* - Prior week - */
.pw-panel{{
  margin:18px 20px 0;border-radius:var(--r-lg);border:1px solid var(--glass-border2);
  overflow:hidden;background:rgba(12,17,32,0.7);backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);box-shadow:0 4px 24px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.07);
}}
.pw-panel.pw-empty{{margin-bottom:8px;}}
.pw-header{{
  padding:10px 16px;display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(90deg,rgba(106,171,255,0.08) 0%,transparent 70%);
  border-bottom:1px solid var(--glass-border2);
}}
.pw-title-group{{display:flex;align-items:center;gap:10px;}}
.pw-icon{{font-size:13px;color:var(--accent);opacity:.9;}}
.pw-title{{font-family:var(--mono);font-size:10.5px;font-weight:700;color:#fff;letter-spacing:.3px;}}
.pw-range{{
  font-family:var(--mono);font-size:9px;color:var(--t1);
  padding:2px 8px;background:var(--glass-mid);border:1px solid var(--glass-border2);border-radius:4px;
}}
.pw-none-label{{font-size:10px;color:var(--t2);font-style:italic;}}
.pw-toggle{{
  display:inline-flex;align-items:center;gap:5px;background:var(--glass-mid);
  border:1px solid var(--glass-border2);border-radius:7px;padding:4px 11px;
  font-family:var(--mono);font-size:9.5px;font-weight:700;color:var(--t1);cursor:pointer;
  transition:background var(--dur),border-color var(--dur),color var(--dur);
}}
.pw-toggle:hover{{background:var(--glass-heavy);border-color:rgba(106,171,255,.5);color:#fff;}}
.pw-chevron{{font-size:13px;line-height:1;transition:transform var(--dur) var(--ease);display:inline-block;}}
.pw-chevron.open{{transform:rotate(90deg);}}
.pw-body{{max-height:0;overflow:hidden;transition:max-height 0.38s var(--ease);}}
.pw-body.open{{max-height:620px;}}
.pw-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;padding:10px;}}
.pw-day{{
  background:var(--glass-mid);border:1px solid var(--glass-border2);
  border-radius:var(--r);padding:9px 8px 8px;min-height:76px;transition:background var(--dur);
}}
.pw-day.pw-closed{{background:rgba(40,10,10,0.5);border-color:rgba(200,50,50,.2);}}
.pw-day-head{{display:flex;align-items:baseline;gap:6px;margin-bottom:6px;}}
.pw-dname{{font-family:var(--mono);font-size:8px;font-weight:700;color:var(--t2);letter-spacing:.8px;}}
.pw-ddate{{font-family:var(--mono);font-size:10.5px;font-weight:600;color:#fff;}}
.pw-none{{font-family:var(--mono);font-size:8.5px;color:var(--t3);}}

/* - Calendar - */
.main{{padding:18px 20px 32px;max-width:1440px;margin:0 auto;}}
.mblock{{
  margin-bottom:28px;border-radius:var(--r-lg);overflow:hidden;
  border:1px solid var(--glass-border2);background:rgba(12,17,32,0.6);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  box-shadow:0 8px 32px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,0.07);
}}
.mblock-header{{
  padding:11px 16px 9px;border-bottom:1px solid var(--glass-border2);
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;
  background:linear-gradient(90deg,var(--es-bg,rgba(255,255,255,0.03)) 0%,transparent 60%);
}}
.mlabel{{font-family:var(--mono);font-size:13px;font-weight:700;color:#fff;letter-spacing:.5px;}}
.earn-season-badge{{
  display:inline-flex;align-items:center;font-family:var(--mono);font-size:9px;font-weight:700;
  padding:3px 10px;border-radius:6px;white-space:nowrap;
  background:color-mix(in srgb,var(--ec) 12%,transparent);color:var(--ec);
  border:1px solid color-mix(in srgb,var(--ec) 30%,transparent);backdrop-filter:blur(8px);
}}
.earn-season-sub{{font-size:7.5px;font-weight:400;opacity:.7;margin-left:6px;}}
.cgrid{{
  display:grid;grid-template-columns:repeat(7,1fr);gap:3px;padding:6px;
  background:rgba(6,10,20,0.5);
}}
.dname{{text-align:center;font-family:var(--mono);font-size:8.5px;font-weight:700;color:var(--t2);padding:5px 0;letter-spacing:1px;}}
.dcell{{
  background:rgba(20,28,52,0.7);border:1px solid var(--glass-border);
  border-radius:var(--r);min-height:98px;padding:8px 7px 6px;
  transition:border-color var(--dur),background var(--dur);position:relative;
}}
.dcell.empty{{background:transparent;border-color:transparent;pointer-events:none;}}
.dcell.wknd{{background:rgba(8,12,24,0.6);opacity:.35;}}
.dcell.past{{opacity:.45;filter:saturate(0.5);}}
.dcell.today{{
  border-color:rgba(106,171,255,.7)!important;background:rgba(106,171,255,0.10);
  box-shadow:0 0 0 1px rgba(106,171,255,.2),0 4px 20px rgba(106,171,255,.10),inset 0 1px 0 rgba(106,171,255,.15);
}}
.dcell.today::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent 0%,var(--accent) 30%,var(--accent2) 70%,transparent 100%);
  border-radius:var(--r) var(--r) 0 0;
}}
.dcell.today .dno{{color:var(--accent)!important;font-weight:700;}}
.dcell.has-e{{border-color:rgba(255,255,255,0.14);}}
.dcell.mkt-closed{{background:rgba(36,8,8,0.6);border-color:rgba(180,40,40,.18);}}
.dno{{font-family:var(--mono);font-size:11px;font-weight:600;color:var(--t1);margin-bottom:4px;display:block;}}
.evbadge{{
  font-family:var(--mono);font-size:7px;font-weight:700;padding:1px 5px;border-radius:3px;
  margin-bottom:2px;display:inline-block;letter-spacing:.2px;white-space:nowrap;
  max-width:100%;overflow:hidden;text-overflow:ellipsis;backdrop-filter:blur(4px);
}}
.evbadge-holiday{{background:rgba(74,122,200,.25);color:#90b8f0;border:1px solid rgba(74,122,200,.4);}}
.evbadge-retail{{background:rgba(160,112,48,.25);color:#e0b870;border:1px solid rgba(160,112,48,.4);}}
.ev-closed{{
  font-size:6px;font-weight:900;background:rgba(220,40,40,.9);color:#fff;
  padding:0 3px;border-radius:2px;margin-left:3px;letter-spacing:.3px;vertical-align:middle;
}}
.chips{{display:flex;flex-wrap:wrap;gap:3px;margin-top:3px;}}
.chip{{
  display:inline-flex;align-items:center;gap:3px;
  background:var(--cc,#444);font-family:var(--mono);font-size:9.5px;font-weight:800;
  color:#fff;padding:4px 7px;border-radius:6px;cursor:pointer;white-space:nowrap;
  transition:transform 0.14s,filter 0.14s,box-shadow 0.14s,opacity 0.14s;letter-spacing:.2px;
  text-shadow:0 1px 3px rgba(0,0,0,.6);border:1px solid rgba(255,255,255,0.22);
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.25),0 2px 6px rgba(0,0,0,.4);
}}
.chip:hover{{
  transform:translateY(-2px) scale(1.08);filter:brightness(1.3) saturate(1.15);
  box-shadow:0 6px 18px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.25),inset 0 1px 0 rgba(255,255,255,.3);
  z-index:10;position:relative;
}}
.chip.dimmed{{opacity:.07;pointer-events:none;}}
.tbadge{{
  font-family:var(--mono);font-size:7px;font-weight:900;padding:1px 4px;border-radius:3px;
  letter-spacing:.2px;line-height:1.4;vertical-align:middle;display:inline-block;
}}
.tbadge-bmo{{background:rgba(0,0,0,0.35);color:#ffe066;border:1px solid rgba(255,224,102,.5);}}
.tbadge-amc{{background:rgba(0,0,0,0.35);color:#c8b8ff;border:1px solid rgba(200,184,255,.5);}}
.bdg-uc{{
  font-family:var(--mono);font-size:8px;font-weight:900;
  background:rgba(255,179,71,.3);color:#ffb347;border:1px solid rgba(255,179,71,.55);
  border-radius:3px;padding:0 3px;line-height:1.4;
}}
.bdg-mm{{
  font-family:var(--mono);font-size:8px;font-weight:900;
  background:rgba(255,96,96,.35);color:#ff6060;border:1px solid rgba(255,96,96,.6);
  border-radius:3px;padding:0 3px;line-height:1.4;
  animation:warnPulse 2s ease-in-out infinite;
}}
@keyframes warnPulse{{
  0%,100%{{box-shadow:0 0 0 0 rgba(255,96,96,0);}}
  50%{{box-shadow:0 0 0 3px rgba(255,96,96,.25);}}
}}

/* - Unannounced - */
.ubox{{
  margin:0 20px 32px;background:rgba(12,17,32,0.65);backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);border:1px solid var(--glass-border2);
  border-radius:var(--r-lg);overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.06);
}}
.ubox-head{{
  padding:13px 20px;border-bottom:1px solid var(--glass-border2);
  display:flex;align-items:baseline;gap:14px;background:var(--glass-mid);
}}
.ubox-title{{font-family:var(--mono);font-size:11px;font-weight:700;color:#fff;letter-spacing:.5px;}}
.ubox-sub{{font-size:10px;color:var(--t1);}}
.utable{{width:100%;border-collapse:collapse;}}
.utable th{{
  text-align:left;padding:7px 16px;font-family:var(--mono);font-size:8px;font-weight:700;
  color:var(--t1);border-bottom:1px solid var(--glass-border2);text-transform:uppercase;letter-spacing:.8px;
}}
.utable td{{padding:8px 16px;border-bottom:1px solid var(--glass-border);vertical-align:middle;}}
.utable tr:last-child td{{border-bottom:none;}}
.utable tr:hover td{{background:var(--glass-mid);}}
.sbadge{{
  font-family:var(--mono);font-size:9px;font-weight:700;color:#fff;
  padding:3px 9px;border-radius:5px;white-space:nowrap;
  text-shadow:0 1px 4px rgba(0,0,0,.6);border:1px solid rgba(255,255,255,.2);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 2px 6px rgba(0,0,0,.4);
}}
.uchip{{
  display:inline-flex;align-items:center;background:var(--cc,#444);
  font-family:var(--mono);font-size:9.5px;font-weight:800;color:#fff;
  padding:3px 8px;border-radius:5px;margin:2px;cursor:pointer;
  transition:transform 0.14s,filter 0.14s,opacity 0.14s;
  text-shadow:0 1px 3px rgba(0,0,0,.5);border:1px solid rgba(255,255,255,.2);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.2);
}}
.uchip:hover{{transform:translateY(-1px) scale(1.08);filter:brightness(1.28);box-shadow:0 4px 14px rgba(0,0,0,.45);}}
.uchip.dimmed{{opacity:.07;pointer-events:none;}}

/* - Footer - */
.footer{{
  border-top:1px solid var(--glass-border2);padding:11px 20px;
  font-family:var(--mono);font-size:9px;color:var(--t2);
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(8,12,26,0.7);backdrop-filter:blur(16px);
}}

/* - Modal - */
.overlay{{
  display:none;position:fixed;inset:0;background:rgba(0,0,0,.78);
  backdrop-filter:blur(20px) saturate(120%);-webkit-backdrop-filter:blur(20px) saturate(120%);
  z-index:999;align-items:center;justify-content:center;
}}
.overlay.on{{display:flex;}}
.modal{{
  background:linear-gradient(145deg,rgba(20,26,50,0.97) 0%,rgba(14,18,38,0.99) 100%);
  border:1px solid var(--glass-border3);border-radius:var(--r-xl);
  padding:28px;max-width:420px;width:90%;
  box-shadow:0 40px 80px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.05),inset 0 1px 0 rgba(255,255,255,.09);
  position:relative;animation:popIn .24s cubic-bezier(.34,1.4,.64,1);
}}
@keyframes popIn{{from{{transform:scale(.9) translateY(12px);opacity:0}}to{{transform:scale(1) translateY(0);opacity:1}}}}
.modal-close{{
  position:absolute;top:14px;right:16px;background:var(--glass-mid);
  border:1px solid var(--glass-border2);border-radius:7px;width:26px;height:26px;
  font-size:15px;color:var(--t1);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  transition:background var(--dur),color var(--dur);
}}
.modal-close:hover{{background:var(--glass-heavy);color:#fff;}}
.modal-ticker{{font-family:var(--mono);font-size:30px;font-weight:700;margin-bottom:3px;line-height:1;filter:drop-shadow(0 0 14px currentColor);}}
.modal-name{{font-size:12px;color:var(--t1);margin-bottom:22px;}}
.modal-banner{{border-radius:9px;padding:10px 14px;margin-bottom:14px;font-size:11px;line-height:1.6;display:none;backdrop-filter:blur(8px);}}
.modal-banner.on{{display:block;}}
.modal-banner.warn{{background:rgba(255,96,96,.10);border:1px solid rgba(255,96,96,.3);color:#ff8080;}}
.modal-banner.info{{background:rgba(255,179,71,.09);border:1px solid rgba(255,179,71,.28);color:#ffb347;}}
.modal-row{{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid var(--glass-border);font-size:12px;}}
.modal-row:last-of-type{{border-bottom:none;}}
.modal-key{{color:var(--t2);font-size:9.5px;text-transform:uppercase;letter-spacing:.7px;font-weight:600;}}
.modal-val{{color:#fff;font-family:var(--mono);font-size:11.5px;font-weight:600;}}
.modal-val.secondary{{color:var(--t1);font-size:11px;font-weight:400;}}
.modal-source-row{{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--glass-border);gap:14px;}}
.modal-source-col{{display:flex;flex-direction:column;gap:4px;flex:1;}}
.modal-source-label{{color:var(--t2);font-size:9px;text-transform:uppercase;letter-spacing:.7px;font-weight:600;}}
.modal-source-date{{font-family:var(--mono);font-size:12px;font-weight:600;color:#fff;}}
.modal-source-date.conflict{{color:var(--conflict);}}
.modal-ir-link{{
  display:inline-flex;align-items:center;gap:7px;margin-top:18px;
  font-family:var(--mono);font-size:10px;font-weight:600;color:var(--accent);text-decoration:none;
  border:1px solid rgba(106,171,255,.28);border-radius:9px;padding:9px 14px;width:100%;
  justify-content:center;background:rgba(106,171,255,.07);backdrop-filter:blur(8px);
  transition:background var(--dur),border-color var(--dur),box-shadow var(--dur);
}}
.modal-ir-link:hover{{background:rgba(106,171,255,.14);border-color:rgba(106,171,255,.55);box-shadow:0 0 24px rgba(106,171,255,.15);}}

/* - Mobile - */
@media(max-width:768px){{
  .sidebar{{width:0;border-right-color:transparent;}}
  .topbar{{padding:0 12px;height:48px;gap:8px;}}
  .page-title{{font-size:11.5px;}}
  .topbar-meta,.vdiv{{display:none;}}
  .tstat{{padding:4px 8px;}}
  .tstat-num{{font-size:12px;}}
  .tstat-lbl{{font-size:6.5px;}}
  .timingbar{{flex-direction:column;align-items:flex-start;gap:6px;padding:8px 12px;}}
  .search-bar{{padding:7px 12px;top:48px;}}
  .search-input{{width:160px;}}
  .cgrid{{grid-template-columns:repeat(7,minmax(0,1fr));gap:2px;padding:3px;}}
  .dcell{{min-height:64px;padding:5px 3px 4px;}}
  .dno{{font-size:8px;}}
  .chip{{font-size:7.5px;padding:2px 4px;border-radius:4px;}}
  .evbadge{{font-size:6px;padding:1px 3px;}}
  .dname{{font-size:7px;padding:3px 0;}}
  .pw-grid{{grid-template-columns:1fr;gap:4px;}}
  .pw-panel{{margin:12px 10px 0;}}
  .main{{padding:12px 10px 24px;}}
  .mblock{{margin-bottom:18px;}}
  .ubox{{margin:0 10px 24px;}}
  .modal{{padding:20px 16px;}}
  .modal-ticker{{font-size:24px;}}
}}
@media(max-width:480px){{
  .cgrid{{grid-template-columns:1fr;}}
  .dcell.empty,.dcell.wknd:not(.has-e){{display:none;}}
  .topbar-right{{gap:6px;}}
  .tstat-lbl{{display:none;}}
}}
</style>
</head>
<body>
<div class="page-wrap">

<!-- - Sidebar - -->
<aside class="sidebar" id="sidebar">
  <div class="sidebar-head">
    <span class="sidebar-title">Sectors</span>
  </div>
  <div class="sidebar-sectors">{sidebar_html}</div>

  <!-- Comments panel -->
  <div class="comments-panel">
    <div class="comments-head">
      <span class="comments-title">
        Notes
        <span class="comments-count" id="commentCount">0</span>
      </span>
    </div>
    <div class="comments-list" id="commentsList">
      <div class="comment-empty" id="commentsEmpty">No notes yet. Add one below.</div>
    </div>
    <div class="comments-input-area">
      <div class="comment-name-row">
        <input class="comment-name-input" id="commentName" type="text"
               placeholder="Your name…" maxlength="20" autocomplete="off">
      </div>
      <textarea class="comment-box" id="commentBox"
                placeholder="Add a note… (e.g. NKE beat est, watching WMT)"
                maxlength="280"></textarea>
      <div class="comment-submit-row">
        <span class="comment-char-count" id="charCount">0 / 280</span>
        <button class="comment-submit" id="commentSubmit" onclick="submitComment()" disabled>Post</button>
      </div>
    </div>
  </div>
</aside>

<div class="content">

<header class="topbar">
  <div class="topbar-left">
    <button class="sidebar-toggle open" id="sidebarToggle"
            onclick="toggleSidebar()" title="Toggle sidebar">&#8249;</button>
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
  {BMO_KEY_BADGE}
  <span class="key-desc">Before market open</span>
  <span class="key-sep">·</span>
  {AMC_KEY_BADGE}
  <span class="key-desc">After market close</span>
  <span class="key-sep">·</span>
  <span class="tpill unc">? Unconfirmed</span>
  <span class="key-desc">Yahoo only</span>
  <span class="key-sep">·</span>
  <span class="tpill mis">! Conflict</span>
  <span class="key-desc">Sources disagree</span>
  <span class="key-sep">·</span>
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

<!-- Modal -->
<div class="overlay" id="overlay" onclick="closeModal(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeModal()">×</button>
    <div class="modal-ticker" id="mTicker"></div>
    <div class="modal-name"   id="mName"></div>
    <div class="modal-banner warn" id="mMismatch">
      ⚠ Date conflict - NASDAQ and Yahoo show different dates. Verify before acting.
    </div>
    <div class="modal-banner info" id="mUnconf">
      ❗ Unconfirmed - sourced from Yahoo Finance only. Not yet on NASDAQ.
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

// - Sidebar toggle -
let sidebarOpen = true;
function toggleSidebar() {{
  sidebarOpen = !sidebarOpen;
  document.getElementById('sidebar').classList.toggle('collapsed', !sidebarOpen);
  document.getElementById('sidebarToggle').classList.toggle('open', sidebarOpen);
}}

// - Sector expand -
function toggleSector(safe) {{
  const t = document.getElementById('tickers-' + safe);
  const a = document.getElementById('arrow-'   + safe);
  const open = t.classList.contains('open');
  t.classList.toggle('open', !open);
  a.classList.toggle('open', !open);
}}

// - Prior week -
let pwOpen = false;
function togglePriorWeek() {{
  pwOpen = !pwOpen;
  document.getElementById('pwBody').classList.toggle('open', pwOpen);
  document.getElementById('pwChevron').classList.toggle('open', pwOpen);
  document.getElementById('pwToggleLabel').textContent = pwOpen ? 'Hide' : 'Show';
}}

// - Auto refresh -
function scheduleSmartRefresh() {{
  const now = new Date();
  const fmt = new Intl.DateTimeFormat('en-US',{{
    timeZone:'America/New_York',hour:'numeric',minute:'numeric',second:'numeric',hour12:false
  }});
  const p   = fmt.formatToParts(now);
  const h   = parseInt(p.find(x=>x.type==='hour').value);
  const m   = parseInt(p.find(x=>x.type==='minute').value);
  const s   = parseInt(p.find(x=>x.type==='second').value);
  const sec = h*3600+m*60+s;
  let minDiff=Infinity;
  for(const t of [4*3600,22*3600]){{let d=t-sec;if(d<=0)d+=86400;if(d<minDiff)minDiff=d;}}
  const next=new Date(now.getTime()+minDiff*1000);
  const lbl=next.toLocaleTimeString('en-US',{{timeZone:'America/New_York',hour:'numeric',minute:'2-digit',hour12:true}});
  const el=document.getElementById('refreshLabel');
  if(el)el.textContent='Next refresh at '+lbl+' ET · {ts}';
  setTimeout(()=>location.reload(),minDiff*1000);
}}
scheduleSmartRefresh();

// - Search -
const searchInput=document.getElementById('searchInput');
const searchClear=document.getElementById('searchClear');
const searchHint =document.getElementById('searchHint');
searchInput.addEventListener('input',function(){{
  const q=this.value.trim().toUpperCase();
  searchClear.classList.toggle('on',q.length>0);
  applySearch(q);
}});
function clearSearch(){{
  searchInput.value='';searchClear.classList.remove('on');
  searchHint.textContent='';applySearch('');
}}
function applySearch(q){{
  const chips=document.querySelectorAll('.chip');
  const uchips=document.querySelectorAll('.uchip');
  if(!q){{chips.forEach(c=>c.classList.remove('dimmed'));uchips.forEach(c=>c.classList.remove('dimmed'));searchHint.textContent='';return;}}
  let found=0;
  chips.forEach(c=>{{const match=c.dataset.ticker&&c.dataset.ticker.toUpperCase().includes(q);c.classList.toggle('dimmed',!match);if(match)found++;}});
  uchips.forEach(c=>{{const match=c.dataset.ticker&&c.dataset.ticker.toUpperCase().includes(q);c.classList.toggle('dimmed',!match);if(match)found++;}});
  searchHint.textContent=found?found+' result'+(found>1?'s':''):'No results';
}}

// - Modal -
function showCard(ticker,name,sector,timing,nasdaqDate,color,source,yahooDate,mismatch,confirmed,irUrl){{
  document.getElementById('mTicker').textContent=ticker;
  document.getElementById('mTicker').style.color=color;
  document.getElementById('mName').textContent=name;
  document.getElementById('mSector').textContent=sector;
  const nd=document.getElementById('mNasdaqDate');
  const yd=document.getElementById('mYahooDate');
  nd.textContent=(!confirmed||nasdaqDate==='TBD')?'Not on NASDAQ':nasdaqDate;
  yd.textContent=(yahooDate&&yahooDate!=='N/A')?yahooDate:'Not available';
  nd.classList.toggle('conflict',mismatch);
  yd.classList.toggle('conflict',mismatch);
  document.getElementById('mTiming').textContent=
    timing==='BMO'?'Before Market Open':timing==='AMC'?'After Market Close':timing==='TBD'?'Not yet confirmed':'Unconfirmed';
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
document.addEventListener('keydown',e=>{{if(e.key==='Escape')document.getElementById('overlay').classList.remove('on');}});

// - Comments -
const STORAGE_KEY = 'earnings_cal_comments_v1';
let comments = [];

function loadComments() {{
  try {{ comments = JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }} catch {{ comments = []; }}
  renderComments();
}}

function saveComments() {{
  try {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(comments.slice(-200))); }} catch {{}}
}}

function renderComments() {{
  const list  = document.getElementById('commentsList');
  const empty = document.getElementById('commentsEmpty');
  const count = document.getElementById('commentCount');
  count.textContent = comments.length;
  if (!comments.length) {{
    empty.style.display = 'block';
    // remove all comment items
    list.querySelectorAll('.comment-item').forEach(el => el.remove());
    return;
  }}
  empty.style.display = 'none';
  list.querySelectorAll('.comment-item').forEach(el => el.remove());
  // render newest first
  [...comments].reverse().forEach((c, i) => {{
    const idx   = comments.length - 1 - i;
    const el    = document.createElement('div');
    el.className = 'comment-item';
    const initials = (c.author || '?').slice(0,2).toUpperCase();
    // pick a stable color from author name
    const hue = [...(c.author||'A')].reduce((a,ch)=>a+ch.charCodeAt(0),0) % 360;
    const col = `hsl(${{hue}},55%,48%)`;
    el.innerHTML = `
      <div class="comment-meta">
        <div class="comment-avatar" style="--cc:${{col}}">${{initials}}</div>
        <span class="comment-author">${{escHtml(c.author||'Anonymous')}}</span>
        <span class="comment-time">${{formatAge(c.ts)}}</span>
        <button onclick="deleteComment(${{idx}})" title="Delete"
          style="background:none;border:none;color:var(--t3);cursor:pointer;font-size:11px;
                 margin-left:4px;padding:0 2px;line-height:1;transition:color .15s"
          onmouseover="this.style.color='var(--conflict)'"
          onmouseout="this.style.color='var(--t3)'">✕</button>
      </div>
      <div class="comment-text">${{formatText(c.text)}}</div>`;
    list.appendChild(el);
  }});
  list.scrollTop = 0;
}}

function escHtml(s) {{
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
          .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}}

function formatText(raw) {{
  // highlight $TICKER or plain ticker references
  const escaped = escHtml(raw);
  return escaped.replace(/\\$?([A-Z]{{2,5}})(?=[^a-z]|$)/g, (m, sym) => {{
    if (COMPANY_NAMES[sym]) {{
      const col = Object.entries(SECTORS).find(([,v])=>v.includes(sym));
      const c   = col ? SECTOR_COLORS[col[0]] : 'var(--accent)';
      return `<span class="comment-ticker-tag" style="background:${{c}}20;color:${{c}};border-color:${{c}}44">${{sym}}</span>`;
    }}
    return m;
  }});
}}

function formatAge(ts) {{
  const diff = Date.now() - ts;
  const m = Math.floor(diff/60000);
  if (m < 1)  return 'just now';
  if (m < 60) return m + 'm ago';
  const h = Math.floor(m/60);
  if (h < 24) return h + 'h ago';
  return Math.floor(h/24) + 'd ago';
}}

function deleteComment(idx) {{
  comments.splice(idx, 1);
  saveComments();
  renderComments();
}}

function submitComment() {{
  const nameEl = document.getElementById('commentName');
  const boxEl  = document.getElementById('commentBox');
  const text   = boxEl.value.trim();
  const author = nameEl.value.trim() || 'Anonymous';
  if (!text) return;
  comments.push({{ author, text, ts: Date.now() }});
  saveComments();
  boxEl.value = '';
  updateCharCount();
  renderComments();
}}

function updateCharCount() {{
  const box   = document.getElementById('commentBox');
  const count = document.getElementById('charCount');
  const btn   = document.getElementById('commentSubmit');
  const len   = box.value.length;
  count.textContent = len + ' / 280';
  count.classList.toggle('warn', len > 240);
  btn.disabled = len === 0;
}}

document.getElementById('commentBox').addEventListener('input', updateCharCount);
document.getElementById('commentBox').addEventListener('keydown', function(e) {{
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) submitComment();
}});

// refresh age labels every 60s
setInterval(() => renderComments(), 60000);
loadComments();
</script>
</body>
</html>"""
    return html

# - RUN -
df, generated_at = run_fetch()
html = build_html(df, generated_at)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done - index.html written")
