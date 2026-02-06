import requests
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import xml.etree.ElementTree as ET

# Dictionary mapping channel IDs to channel names
channel_names = {
    "ae-canada/4311": "A&E",
    "abc-wabc-new-york-ny/1769": "ABC (WABC)",
    "addik-tv/2033": "Addik",
    "adult-swim-east/607": "Adult Swim",
    "amc-eastern-feed-hd/6219": "AMC",
    "bbc-america-east/615": "BBC America",
    "bbc-news-north-america/527": "BBC World News HD",
    "bnn-bloomberg/294": "BNN Bloomberg",
    "bravo-canada/160": "Bravo",
    "canal-d/108": "Canal D",
    "canal-vie/307": "Canal Vie",
    "cartoon-network-canada-east/162": "Cartoon Network",
    "cbs-wbz-boston-ma/134": "CBS (WBZ)",
    "chch-hamilton-on/43": "CHCH",
    "city-montreal-qc/1171": "Citytv Montreal",
    "city-toronto-on/42": "Citytv Toronto",
    "cnn/70": "CNN",
    "cp24-cablepulse-24/321": "CP24",
    "crave1-east/72": "Crave 1",
    "crave2-east/86": "Crave 2",
    "crave3-east/85": "Crave 3",
    "crave4/320": "Crave 4",
    "ctv-comedy-east/159": "CTV Comedy",
    "ctv-drama/59": "CTV Drama",
    "ctv-life/309": "CTV Life",
    "ctv-montreal-cfcf-qc/50": "CTV Montreal",
    "ctv-nature-canada/1188": "CTV Nature",
    "ctv-news-channel/416": "CTV News Channel",
    "ctv-scifi/153": "CTV Sci-Fi",
    "ctv-speed-hd/3887": "CTV Speed",
    "ctv-cfto-toronto-on/39": "CTV Toronto",
    "ctv-wild-canada/472": "CTV Wild",
    "ctv2-barrie-on-ckvr/14229": "CTV2 Barrie",
    "ctv2-london-on/139": "CTV London",
    "ctv2-chrodt43-ottawa-on/13791": "CTV2 Ottawa",
    "destination-america/2074": "Destination America",
    "discovery-channel-canada-rogers/38127": "Discovery",
    "disney-channel-canada-east/16682": "Disney Channel",
    "dtour/11143": "DTour",
    "e-canada/295": "E!",
    "flavour-network/169": "Flavour Network",
    "food-network-canada-rogers/38125": "Food Network",
    "fox-wnyw-new-york-ny-hd/4557": "FOX (WNYW)",
    "fox-news/1083": "FOX News",
    "fox-sports-1/668": "FOX Sports 1",
    "fox-sports-2/2114": "FOX Sports 2",
    "fx-networks-canada/10026": "FX",
    "fxx-canada/13400": "FXX",
    "global-ckmi-quebec-hd/6437": "Global Montreal",
    "global-ciiidt41-toronto/13585": "Global Toronto",
    "hgtv-canada-rogers/38126": "HGTV",
    "history-canada-east/164": "History",
    "home-network/167": "Home Network",
    "rdi-news/8": "ICI RDI",
    "ici-cbft-montreal-qc/196": "ICI Télé Montreal", 
    "ici-television-cfhddt-montreal-qc/11385": "ICI Télévision",
    "independent-film-channel-us/1966": "IFC",
    "investigation-discovery-canada-rogers/38128": "Investigation Discovery",
    "ion-eastern-feed-hd/8534": "ION Television East HD",
    "law-crime-network/32823": "Law and Crime",
    "lifetime-network-us-eastern-feed/654": "Lifetime",
    "lifetime-tv-canada/1148": "Lifetime Canada",
    "lifetime-movies-hd-east/4723": "LMN",
    "logo-east/2091": "Logo",
    "love-nature-4k/33687": "Love Nature",
    "max/306": "MAX",
    "meteomedia-montreal/5942": "Meteo Media Montreal",
    "mlb-network/6178": "MLB Network",
    "moremax-eastern-hd/7097": "Cinema Hits",
    "motor-trend-hd/12597": "MotorTrend HD",
    "msnbc-usa/655": "MSNBC",
    "mtv-usa-eastern-feed/656": "MTV",
    "nasa-4k/33492": "NASA",
    "national-geographic-wild/7537": "Nat Geo WILD",
    "national-geographic-us-hd-eastern/4436": "National Geographic",
    "nba-tv-usa/3116": "NBA TV",
    "newsmax-tv/16818": "Newsmax TV",
    "nfl-network/3349": "NFL Network",
    "nfl-redzone/6921": "NFL Red Zone",
    "nhl-network-usa/14156": "NHL Network",
    "nick-jr-hd/11444": "Nick Jr.",
    "nickelodeon-usa-east-feed/658": "Nickelodeon East",
    "nicktoons-hd-east/11445": "Nicktoons",
    "omni-east/31930": "OMNI East",
    "omni2/613": "OMNI 2 Toronto",
    "ontario-legislature/417": "Ontario Legislature",
    "outdoor-channel-us/1086": "Outdoor Channel",
    "oprah-winfrey-network-usa-eastern/1159": "OWN",
    "oxygen-eastern-feed/659": "Oxygen True Crime",
    "pbs-wnet-new-york-ny/1774": "PBS 13 (WNET) New York",
    "planete-hd/6765": "Planete+",
    "qub/7616": "QUB",
    "reelzchannel/4175": "ReelzChannel",
    "retro-tv-wxnyld4-new-york-ny/16446": "Retro TV",
    "science-hd/5828": "Science",
    "scripps-news-wpxntv7-new-york-ny/37059": "Scripps",
    "sec-network/13711": "SEC Network",
    "paramount-with-showtime-eastern-feed/665": "Showtime (E)",
    "showtime-2-eastern/1387": "SHOWTIME 2",
    "sportsnet-360/336": "Sportsnet 360",
    "starz-eastern/583": "STARZ East",
    "sundancetv-usa-east-hd/8264": "SundanceTV HD",
    "super-channel-vault/4835": "Superchannel Vault",
    "syfy-eastern-feed/596": "SYFY",
    "tbs-east/61": "TBS",
    "temoin/9109": "Temoin",
    "turner-classic-movies-canada/2847": "TCM",
    "teennick-eastern/1954": "TeenNick",
    "telemundo-east-hd/33284": "Telemundo East",
    "telemundo-wkaq-san-juan-pr/6172": "Telemundo San Juan",
    "the-tennis-channel/2269": "Tennis Channel",
    "wpix-new-york-superstation/63": "The CW (WPIX New York)",
    "tmc-hd-eastern/4352": "The Movie Channel East",
    "the-weather-channel/1526": "The Weather Channel",
    "tlc-usa-eastern/5005": "TLC",
    "tnt-eastern-feed/347": "TNT",
    "travel-us-east/662": "Travel Channel",
    "trutv-usa-eastern/333": "truTV",
    "tv-one-hd/7082": "TV One HD",
    "universal-kids-hd/8835": "Universal Kids",
    "univision-eastern-feed-hd/8136": "Univision East",
    "usa-network-east-feed/640": "USA Network",
    "us-armenia-kmrzdt5-los-angeles-ca/18634": "USArmenia",
    "vh1-eastern-feed/663": "VH1",
    "vice/624": "VICE",
    "w-wtn-east/64": "W Network",
    "abc-wabc-new-york-ny/1769": "WABC (New York) ABC East",
    "cbs-wcbs-new-york-ny/1766": "WCBS (New York) CBS East",
    "we-hd/6220": "WE tv",
    "weather-network/419": "Weather Network",
    "wild-tv/2976": "Wild TV",
    "nbc-wnbc-new-york-ny/1767": "WNBC (New York) NBC East",
    "fox-wnyw-new-york-ny-hd/4557": "WNYW (New York) FOX East",
    "wsbk-tv38-boston/58": "WSBK",
    "pbs-kcpt-kansas-city-mo/2711": "KCPT PBS",
    "cbs-kctv-kansas-city-mo/2431": "KCTV CBS",
    "cw-kcwe-kansas-city-mo/2715": "KCWE CW",
    "cbs-khqa-quincy-mo/4972": "KHQA CBS",
    "abc-kmbc-kansas-city-mo-hd/8877": "KMBC ABC",
    "metv-kmbctv2-kansas-city-mo/7267": "KMBC MeTV",
    "bounce-kmcitv2-kansas-city-mo/15588": "KMCI Bounce TV",
    "court-tv-kmcitv3-kansas-city-mo/15589": "KMCI Court TV",
    "kmci-38-the-spot-kansas-city-mo-hd/7272": "KMCI The Spot",
    "abc-kmiz-columbia-mo/2722": "KMIZ ABC",
    "metv-kmiz2-columbia-mo/10288": "KMIZ MeTV",
    "mnt-kmizdt3-columbia-mo/13173": "KMIZ MY Network",
    "pbs-kmos-warrensburg-mo/2719": "KMOS PBS",
    "ctn-kfdr-jefferson-city-mo/8010": "KNLJ CTN",
    "cw-komutv3-columbia-mo/8011": "KOMU CW",
    "nbc-komu-columbia-mo/2721": "KOMU NBC",
    "ion-kpxe-kansas-city-mo/2714": "KPXE ION",
    "fox-kqfx-columbia-mo/5012": "KQFX FOX",
    "cbs-krcg-jefferson-mo-hd/6301": "KRCG CBS",
    "charge-krcg3-jefferson-city-mo/15268": "KRCG Charge!",
    "comet-tv-krcg2-jefferson-city-mo/15267": "KRCG Comet",
    "tbd-tv-krcg4-jefferson-mo/20030": "KRCG TBD",
    "grit-tv-kshbtv2-kansas-city-mi/10994": "KSHB Grit",
    "laff-kshbtv3-kansas-city-mo/15591": "KSHB Laff",
    "nbc-kshb-kansas-city-mo-hd/6625": "KSHB NBC",
    "mnt-ksmo-kansas-city-mo-hd/6944": "KSMO My Network",
    "abc-ktvo-kirskville-mo/5922": "KTVO ABC",
    "cbs-ktvodt2-kirskville-mo/11542": "KTVO CBS",
    "comet-tv-ktvo3-ottumwa-ia/18392": "KTVO Comet",
    "cw-kyou4-ottumwa-ia/18307": "KYOU CW",
    "fox-kyou-ottumwa-ia/5037": "KYOU FOX",
    "grit-tv-kyoutv5-ottumwa-ia/34617": "KYOU GRIT",
    "nbc-kyoudt2-ottumwa-ia/33140": "KYOU NBC",
    "antenna-wdaftv2-kansas-city-mo/10568": "WDAF Antenna",
    "fox-wdaf-kansas-city-mo/2451": "WDAF FOX",
    "nbc-wgem-quincy-il/5135": "WGEM NBC",
    "abc-wolo-columbia-sc/1098": "ABC (WOLO)",
    "bein-sport-usa/10853": "beIN Sports",
    "bet-gospel/6191": "BET Gospel",
    "bet-jams/2113": "BET Jams",
    "bet-soul/3229": "BET Soul",
    "bounce-network/14312": "Bounce",
    "cspan/648": "C-SPAN",
    "cbs-wbz-boston-ma/134": "CBS (WBZ)",
    "cheddar-news/33695": "Cheddar News",
    "cmt-music/2288": "CMT Music",
    "fox-wfxt-boston-ma-hd/3657": "FOX (WFXT)",
    "fox-weather/37620": "FOX Weather",
    "gettv/11258": "getTV",
    "grit-network/14377": "Grit",
    "ion-plus-wgpxtv5-greensboro-nc/12243": "ION Plus",
    "laff-network/20169": "Laff",
    "magnolia-network-canada/2034": "Magnolia Network",
    "metv-network/16325": "MeTV",
    "metv-toons-wjlp2-new-jersey/15178": "MeTV Toons",
    "mgm-east/7609": "MGM+",
    "mgm-drivein/11487": "MGM+ Drive-In",
    "mgm-hits-east/11485": "MGM+ Hits",
    "mgm-marquee/11486": "MGM+ Marquee",
    "mtv-classic-east/2093": "MTV Classic",
    "mtv-live/6080": "MTV Live",
    "mtv-2-east/1515": "MTV2",
    "mtv-u/2701": "mTvU",
    "nbc-wmaq-chicago-il/1831": "NBC (WMAQ)",
    "newsnation-eastern-feed/65": "NewsNation",
    "nfl-redzone/6921": "NFL RedZone",
    "nickmusic/2112": "NickMusic",
    "paramount-network-usa-eastern-feed/1030": "Paramount Network",
    "pbs-mpt-maryland-public-broadcasting/1636": "PBS (MPT)",
    "create-wmpt2-annapolis-md/5545": "PBS Create",
    "pbs-kids-wkle4-lexington-ky/32103": "PBS Kids",
    "pop-east/10165": "Pop",
    "revolt-tv/11301": "Revolt",
    "showtime-extreme-eastern/1615": "Showtime Extreme",
    "showtime-next-hd-eastern/7109": "Showtime Next",
    "showtime-women-eastern/2273": "Showtime Women",
    "smile/5275": "Smile",
    "sony-movies/17063": "Sony Movies",
    "starz-comedy-eastern/4223": "Starz Comedy",
    "starz-edge-hd-eastern/7089": "Starz Edge",
    "starz-encore-eastern/667": "Starz Encore",
    "starz-encore-action-eastern/2078": "Starz Encore Action",
    "starz-encore-classic-eastern/2080": "Starz Encore Classic",
    "starz-encore-westerns-eastern/1959": "Starz Encore Westerns",
    "tbd-tv/31478": "TBD.",
    "tsn1/11": "TSN1",
    "tsn2/4294": "TSN2",
    "tsn3/13719": "TSN3",
    "tsn4/279": "TSN4",
    "tsn5/278": "TSN5",
    "tv-land-eastern/1252": "TV Land",
    "tva-sports/9823": "TVA Sports",
    "wgn-chicago-local/1915": "WGN 9",
    "yes-network/1953": "Yes Network"

    # Add more channel IDs and names as needed
}

def fetch_with_retry(url, headers, cookies, retries=10, delay=2):
    """
    Fetch a URL and retry if the response status is not 200 or on exceptions.
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
            if response.status_code == 200:
                return response
            # else:
            #     print(f"Attempt {attempt}/{retries} failed: Status {response.status_code} - {url}")
        except Exception as e:
            # print(f"Attempt {attempt}/{retries} exception: {e} - {url}")
            pass  # <--- add this line so Python has a statement in the except block
        # random sleep to avoid hammering the server
        time.sleep(delay + random.uniform(2, 4))
    return None

def get_cisession_with_timezone(tz="America/New_York", retries=5, delay=3):
    """
    Create a session with TVPassport and set the timezone.
    Retries until status_code == 200 or retries are exhausted.
    """
    session = requests.Session()
    session.get("https://www.tvpassport.com/", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    })

    payload = {"timezone": tz}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tvpassport.com/my-passport/dashboard"
    }

    for attempt in range(1, retries + 1):
        try:
            response = session.post(
                "https://www.tvpassport.com/my-passport/dashboard/save_timezone",
                data=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200 and "cisession" in session.cookies:
                return session, session.cookies["cisession"]

        except requests.exceptions.RequestException:
            pass

        time.sleep(delay)

    return None, None


# 🔹 Get cisession once here (outside function)
session, cisession = get_cisession_with_timezone("America/New_York")


def scrape_tv_programming(channel_id, date):
    url = f"https://www.tvpassport.com/tv-listings/stations/{channel_id}/{date}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }

    # use the cisession cookie we got above
    cookies = {"cisession": cisession} if cisession else {}

    # use the retry function
    response = fetch_with_retry(url, headers, cookies, retries=10, delay=2)
    
    if response is None:
        return []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        programming_items = soup.select(".station-listings .list-group-item")

        programming_data = []

        for item in programming_items:
            start_time = parse_start(item)
            duration = parse_duration(item)
            end_time = start_time + timedelta(minutes=duration)
            title = parse_title(item)
            sub_title = parse_sub_title(item)
            description = parse_description(item)
            icon = parse_icon(item)
            category = parse_category(item)
            rating = parse_rating(item)
            actors = parse_actors(item)
            guest = parse_guest(item)
            director = parse_director(item)

            programming_data.append({
                "title": title,
                "sub_title": sub_title,
                "description": description,
                "icon": icon,
                "category": category,
                "rating": rating,
                "actors": actors,
                "guest": guest,
                "director": director,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "channel_id": channel_id
            })

        return programming_data
    else:
        return None

def parse_description(item):
    return item.get("data-description")

def parse_icon(item):
    return item.get("data-showpicture")

def parse_title(item):
    show_name = item.get("data-showname")
    episode_title = item.get("data-episodetitle")
    if show_name == "Movie":
        return episode_title
    else:
        return show_name

def parse_sub_title(item):
    return item.get("data-episodetitle")

def parse_category(item):
    showtype = item.get("data-showtype")
    return showtype.split(", ") if showtype else []

def parse_actors(item):
    cast = item.get("data-cast")
    return cast.split(", ") if cast else []

def parse_director(item):
    director = item.get("data-director")
    return director.split(", ") if director else []

def parse_guest(item):
    guest = item.get("data-guest")
    return guest.split(", ") if guest else []

def parse_rating(item):
    rating = item.get("data-rating")
    return {"system": "MPA", "value": rating.replace("TV", "TV-")} if rating else None

def parse_start(item):
    time_str = item.get("data-st")
    if time_str:
        return pytz.timezone("America/New_York").localize(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    else:
        return None

def parse_duration(item):
    duration_str = item.get("data-duration")
    return int(duration_str) if duration_str else None

def prettify(elem, level=0):
    """Add indentation to the XML element."""
    indent = "\n" + level * "    "  # Four spaces for each level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for subelem in elem:
            prettify(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent

def format_timezone_aware_datetime(dt):
    if dt.tzinfo is None:
        return dt.strftime("%Y%m%d%H%M%S")
    else:
        return dt.strftime("%Y%m%d%H%M%S %z")


def create_xml(programs):
    root = ET.Element("tv")
    
    # Add channel information for each channel
    for channel_id, channel_programs in programs.items():
        channel_elem = ET.SubElement(root, "channel")
        channel_elem.set("id", channel_names[channel_id])
        display_name_elem = ET.SubElement(channel_elem, "display-name")
        display_name_elem.set("lang", "en")
        display_name_elem.text = channel_names[channel_id]
    
    # Add program information under each channel
    for channel_id, channel_programs in programs.items():
        for program in channel_programs:
            start_time = format_timezone_aware_datetime(program["start_time"])
            end_time = format_timezone_aware_datetime(program["end_time"])
            program_elem = ET.SubElement(root, "programme")
            program_elem.set("start", start_time)
            program_elem.set("stop", end_time)
            program_elem.set("channel", channel_names.get(channel_id, "Unknown"))
    
            title_elem = ET.SubElement(program_elem, "title")
            title_elem.text = program["title"]
    
            desc_elem = ET.SubElement(program_elem, "desc")
            desc_elem.text = program["description"]
    
            # Add other elements as needed
    
    # Apply indentation
    prettify(root)
    
    # ✅ Use ElementTree.write() instead of tostring()
    import io
    tree = ET.ElementTree(root)
    buf = io.BytesIO()
    tree.write(buf, encoding="utf-8", xml_declaration=True)
    return buf.getvalue().decode("utf-8")



# Example usage
channel_ids = [
    "ae-canada/4311",
    "acc-network/33964",
    "amc-eastern-feed-hd/6219",
    "american-heroes-channel/2035",
    "animal-planet-us-east/645",
    "bbc-america-east/615",
    "bbc-news-north-america/527",
    "bet-eastern-feed/323",
    "bet-her/6837",
    "big-ten-network/4499",
    "bloomberg-tv-usa-hd/6790",
    "boomerang/2268",
    "bravo-usa-eastern-feed/646",
    "bravo-canada/160",
    "buzzr-tv-wwortv3-new-york-ny/10750",
    "cartoon-network-usa-hd-eastern/6917",
    "cbs-sports-network-usa/3115",
    "stadium-wlnytv3-riverhead-ny/34537",
    "chch-hamilton-on/43",
    "cinemax-eastern-feed/632",
    "cinepop-hd/9156",
    "cmt-canada/120",
    "cnbc-usa/201",
    "cnn/70",
    "cnn-international-north-america/3008",
    "comedy-central-us-eastern-feed/647",
    "comet-tv-wphltv4-philadelphiapa/10279",
    "court-tv-network/33650",
    "the-cooking-channel/4226",
    "cp24-cablepulse-24/321",
    "crime-investigation-network-usa-hd/6216",
    "cspan/648",
    "cspan-2/1050",
    "ctv-life/309",
    "ctv-nature-canada/1188",
    "ctv-speed-hd/3887",
    "ctv2-chrodt43-ottawa-on/13791",
    "ctv2-toronto-on/36",
    "destination-america/2074",
    "discovery-channel-us-eastern-feed/649",
    "discovery-family-channel/4225",
    "discovery-life-channel/1273",
    "disney-eastern-feed/595",
    "disney-junior-usa-hd-east/10523",
    "disney-xd-usa-eastern-feed/1053",
    "dtour/11143",
    "e-entertainment-usa-eastern-feed/617",
    "e-canada/295",
    "espn/594",
    "espn2/650",
    "espn-news/1527",
    "espn-u/3331",
    "flavour-network/169",
    "food-network-usa-eastern-feed/1054",
    "fox-business/4656",
    "fox-news/1083",
    "fox-sports-1/668",
    "fox-sports-2/2114",
    "freeform-east-feed/1011",
    "fuse-tv-hd-eastern/6221",
    "fx-networks-east-coast-hd/6111",
    "fx-movie-channel/1308",
    "fxx-usa-eastern/1952",
    "fyi-usa-hd-eastern/6211",
    "game-hd/14465",
    "golf-channel-canada/9900",
    "game-show-network-east/329",
    "hallmark-channel-hd-eastern/6213",
    "hallmark-family/32480",
    "hallmark-mystery-eastern/4453",
    "hbo-2-eastern-feed-hd/6313",
    "hbo-comedy-east/629",
    "hbo-eastern-feed/614",
    "hbo-family-eastern-feed/628",
    "hbo-signature-hbo-3-eastern-hd/7099",
    "hbo-zone-hd-east/7102",
    "hgtv-usa-eastern-feed/623",
    "hgtv-canada-rogers/38126",
    "history-2-canada/461",
    "history-canada-east/164",
    "history-channel-us-hd-east/4660",
    "hln/425",
    "home-network/167",
    "rdi-news/8",
    "independent-film-channel-us/1966",
    "investigation-discovery-usa-eastern/2090",
    "ion-eastern-feed-hd/8534",
    "law-crime-network/32823",
    "lifetime-network-us-eastern-feed/654",
    "lifetime-movies-hd-east/4723",
    "lifetime-tv-canada/1148",
    "logo-east/2091",
    "love-nature-4k/33687",
    "max/306",
    "meteomedia-montreal/5942",
    "mlb-network/6178",
    "moremax-eastern-hd/7097",
    "motor-trend-hd/12597",
    "msnbc-usa/655",
    "mtv-usa-eastern-feed/656",
    "nasa-4k/33492",
    "national-geographic-wild/7537",
    "national-geographic-us-hd-eastern/4436",
    "nba-tv-usa/3116",
    "newsmax-tv/16818",
    "nfl-network/3349",
    "nfl-redzone/6921",
    "nhl-network-usa/14156",
    "nick-jr-hd/11444",
    "nickelodeon-usa-east-feed/658",
    "nicktoons-hd-east/11445",
    "omni-east/31930",
    "omni2/613",
    "ontario-legislature/417",
    "outdoor-channel-us/1086",
    "oprah-winfrey-network-usa-eastern/1159",
    "oxygen-eastern-feed/659",
    "pbs-wnet-new-york-ny/1774",
    "planete-hd/6765",
    "qub/7616",
    "reelzchannel/4175",
    "retro-tv-wxnyld4-new-york-ny/16446",
    "science-hd/5828",
    "scripps-news-wpxntv7-new-york-ny/37059",
    "sec-network/13711",
    "paramount-with-showtime-eastern-feed/665",
    "showtime-2-eastern/1387",
    "sportsnet-360/336",
    "starz-eastern/583",
    "sundancetv-usa-east-hd/8264",
    "super-channel-vault/4835",
    "syfy-eastern-feed/596",
    "tbs-east/61",
    "turner-classic-movies-canada/2847",
    "teennick-eastern/1954",
    "telemundo-east-hd/33284",
    "telemundo-wkaq-san-juan-pr/6172",
    "temoin/9109",
    "the-tennis-channel/2269",
    "wpix-new-york-superstation/63",
    "tmc-hd-eastern/4352",
    "the-weather-channel/1526",
    "tlc-usa-eastern/5005",
    "tnt-eastern-feed/347",
    "travel-us-east/662",
    "trutv-usa-eastern/333",
    "tv-one-hd/7082",
    "universal-kids-hd/8835",
    "univision-eastern-feed-hd/8136",
    "usa-network-east-feed/640",
    "us-armenia-kmrzdt5-los-angeles-ca/18634",
    "vh1-eastern-feed/663",
    "vice/624",
    "w-wtn-east/64",
    "abc-wabc-new-york-ny/1769",
    "cbs-wcbs-new-york-ny/1766",
    "we-hd/6220",
    "weather-network/419",
    "wild-tv/2976",
    "nbc-wnbc-new-york-ny/1767",
    "fox-wnyw-new-york-ny-hd/4557",
    "wsbk-tv38-boston/58",
    "pbs-kcpt-kansas-city-mo/2711",
    "cbs-kctv-kansas-city-mo/2431",
    "cw-kcwe-kansas-city-mo/2715",
    "cbs-khqa-quincy-mo/4972",
    "abc-kmbc-kansas-city-mo-hd/8877",
    "metv-kmbctv2-kansas-city-mo/7267",
    "bounce-kmcitv2-kansas-city-mo/15588",
    "court-tv-kmcitv3-kansas-city-mo/15589",
    "kmci-38-the-spot-kansas-city-mo-hd/7272",
    "abc-kmiz-columbia-mo/2722",
    "metv-kmiz2-columbia-mo/10288",
    "mnt-kmizdt3-columbia-mo/13173",
    "pbs-kmos-warrensburg-mo/2719",
    "ctn-kfdr-jefferson-city-mo/8010",
    "cw-komutv3-columbia-mo/8011",
    "nbc-komu-columbia-mo/2721",
    "ion-kpxe-kansas-city-mo/2714",
    "fox-kqfx-columbia-mo/5012",
    "cbs-krcg-jefferson-mo-hd/6301",
    "charge-krcg3-jefferson-city-mo/15268",
    "comet-tv-krcg2-jefferson-city-mo/15267",
    "tbd-tv-krcg4-jefferson-mo/20030",
    "grit-tv-kshbtv2-kansas-city-mi/10994",
    "laff-kshbtv3-kansas-city-mo/15591",
    "nbc-kshb-kansas-city-mo-hd/6625",
    "mnt-ksmo-kansas-city-mo-hd/6944",
    "abc-ktvo-kirskville-mo/5922",
    "cbs-ktvodt2-kirskville-mo/11542",
    "comet-tv-ktvo3-ottumwa-ia/18392",
    "cw-kyou4-ottumwa-ia/18307",
    "fox-kyou-ottumwa-ia/5037",
    "grit-tv-kyoutv5-ottumwa-ia/34617",
    "nbc-kyoudt2-ottumwa-ia/33140",
    "antenna-wdaftv2-kansas-city-mo/10568",
    "fox-wdaf-kansas-city-mo/2451",
    "nbc-wgem-quincy-il/5135",
    "abc-wolo-columbia-sc/1098",
    "bein-sport-usa/10853",
    "bet-gospel/6191",
    "bet-jams/2113",
    "bet-soul/3229",
    "bounce-network/14312",
    "cspan/648",
    "cbs-wbz-boston-ma/134",
    "cheddar-news/33695",
    "cmt-music/2288",
    "fox-wfxt-boston-ma-hd/3657",
    "fox-weather/37620",
    "gettv/11258",
    "grit-network/14377",
    "ion-plus-wgpxtv5-greensboro-nc/12243",
    "laff-network/20169",
    "magnolia-network-canada/2034",
    "metv-network/16325",
    "metv-toons-wjlp2-new-jersey/15178",
    "mgm-east/7609",
    "mgm-drivein/11487",
    "mgm-hits-east/11485",
    "mgm-marquee/11486",
    "mtv-classic-east/2093",
    "mtv-live/6080",
    "mtv-2-east/1515",
    "mtv-u/2701",
    "nbc-wmaq-chicago-il/1831",
    "newsnation-eastern-feed/65",
    "nfl-redzone/6921",
    "nickmusic/2112",
    "paramount-network-usa-eastern-feed/1030",
    "pbs-mpt-maryland-public-broadcasting/1636",
    "create-wmpt2-annapolis-md/5545",
    "pbs-kids-wkle4-lexington-ky/32103",
    "pop-east/10165",
    "revolt-tv/11301",
    "showtime-extreme-eastern/1615",
    "showtime-next-hd-eastern/7109",
    "showtime-women-eastern/2273",
    "smile/5275",
    "sony-movies/17063",
    "starz-comedy-eastern/4223",
    "starz-edge-hd-eastern/7089",
    "starz-encore-eastern/667",
    "starz-encore-action-eastern/2078",
    "starz-encore-classic-eastern/2080",
    "starz-encore-westerns-eastern/1959",
    "tbd-tv/31478",
    "tsn1/11",
    "tsn2/4294",
    "tsn3/13719",
    "tsn4/279",
    "tsn5/278",
    "tv-land-eastern/1252",
    "tva-sports/9823",
    "wgn-chicago-local/1915",
    "yes-network/1953"
]


# Calculate today's date and the dates for the next two days
dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(4)]

all_programs = {}
for channel_id in channel_ids:
    program_data = []
    for date in dates:
        program_data_for_date = scrape_tv_programming(channel_id, date)
        if program_data_for_date:
            program_data.extend(program_data_for_date)

    if program_data:
        all_programs[channel_id] = program_data

if all_programs:
    channel_names_list = list(channel_names.keys())  # Get the channel IDs in the correct order
    channel_programs = {}
    for channel_id in channel_names_list:
        channel_programs[channel_id] = [
            {
                "title": program["title"],
                "sub_title": program["sub_title"],
                "description": program["description"],
                "icon": program["icon"],
                "category": program["category"],
                "rating": program["rating"],
                "actors": program["actors"],
                "guest": program["guest"],
                "director": program["director"],
                "start_time": pytz.timezone("America/New_York").localize(datetime.strptime(program["start_time"], "%Y-%m-%d %H:%M:%S")),
                "end_time": pytz.timezone("America/New_York").localize(datetime.strptime(program["end_time"], "%Y-%m-%d %H:%M:%S")),
                "channel_id": program["channel_id"]
            } for program in all_programs[channel_id]
        ]

    # Print the XML content
    xml_content = create_xml(channel_programs)  # Generate XML content
    print(xml_content)  # Print the XML content
