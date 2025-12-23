import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import xml.etree.ElementTree as ET

# Dictionary mapping channel IDs to channel names
channel_names = {
    "ae-canada/4311": "A&E",
    "acc-network/33964": "ACC Network",
    "amc-canada/3822": "AMC",
    "american-heroes-channel/2035": "American Heroes Channel",
    "animal-planet-us-east/645": "Animal Planet",
    "bbc-america-east/615": "BBC America",
    "bbc-news-north-america/527": "BBC World News HD",
    "bet-eastern-feed/323": "BET",
    "bet-her/6837": "BET Her",
    "bloomberg-tv-usa-hd/6790": "Bloomberg TV",
    "boomerang/2268": "Boomerang",
    "bravo-usa-eastern-feed/646": "Bravo",
    "cartoon-network-usa-hd-eastern/6917": "Cartoon Network",
    "cbs-sports-network-usa/3115": "CBS Sports Network",
    "cinemax-eastern-feed/632": "Cinemax",
    "cnbc-usa/201": "CNBC",
    "cmt-canada/120": "CMT",
    "cnn/70": "CNN",
    "comedy-central-us-eastern-feed/647": "Comedy Central",
    "the-cooking-channel/4226": "Cooking Channel",
    "crime-investigation-network-usa-hd/6216": "Crime & Investigation HD",
    "cspan/648": "CSPAN",
    "cspan-2/1050": "CSPAN 2",
    "destination-america/2074": "Destination America",
    "discovery-channel-us-eastern-feed/649": "Discovery",
    "discovery-family-channel/4225": "Discovery Family Channel",
    "discovery-life-channel/1273": "Discovery Life",
    "disney-eastern-feed/595": "Disney Channel (East)",
    "disney-junior-usa-hd-east/10523": "Disney Junior",
    "disney-xd-usa-eastern-feed/1053": "Disney XD",
    "e-entertainment-usa-eastern-feed/617": "E!",
    "espn-news/1527": "ESPNews",
    "espn-u/3331": "ESPNU",
    "food-network-usa-eastern-feed/1054": "Food Network",
    "fox-business/4656": "Fox Business Network",
    "fox-news/1083": "FOX News Channel",
    "fox-sports-1/668": "FOX Sports 1",
    "fox-sports-2/2114": "FOX Sports 2",
    "freeform-east-feed/1011": "Freeform",
    "fuse-tv-hd-eastern/6221": "Fuse HD",
    "fx-networks-east-coast-hd/6111": "FX",
    "fx-movie-channel/1308": "FX Movie",
    "fxx-usa-eastern/1952": "FXX",
    "fyi-usa-hd-eastern/6211": "FYI",
    "golf-channel-canada/9900": "Golf Channel",
    "hallmark-channel-hd-eastern/6213": "Hallmark",
    "hallmark-family/32480": "Hallmark Drama HD",
    "hallmark-mystery-eastern/4453": "Hallmark Movies & Mysteries HD",
    "hbo-2-eastern-feed-hd/6313": "HBO 2 East",
    "hbo-comedy-east/629": "HBO Comedy HD",
    "hbo-eastern-feed/614": "HBO East",
    "hbo-family-eastern-feed/628": "HBO Family East",
    "hbo-signature-hbo-3-eastern-hd/7099": "HBO Signature",
    "hbo-zone-hd-east/7102": "HBO Zone HD",
    "hgtv-usa-eastern-feed/623": "HGTV",
    "history-channel-us-hd-east/4660": "History",
    "hln/425": "HLN",
    "independent-film-channel-us/1966": "IFC",
    "investigation-discovery-usa-eastern/2090": "Investigation Discovery",
    "ion-eastern-feed-hd/8534": "ION Television East HD",
    "lifetime-network-us-eastern-feed/654": "Lifetime",
    "lifetime-movies-hd-east/4723": "LMN",
    "logo-east/2091": "Logo",
    "mlb-network/6178": "MLB Network",
    "moremax-eastern-hd/7097": "Cinema Hits",
    "motor-trend-hd/12597": "MotorTrend HD",
    "msnbc-usa/655": "MSNBC",
    "mtv-usa-eastern-feed/656": "MTV",
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
    "outdoor-channel-us/1086": "Outdoor Channel",
    "oprah-winfrey-network-usa-eastern/1159": "OWN",
    "oxygen-eastern-feed/659": "Oxygen True Crime",
    "pbs-wnet-new-york-ny/1774": "PBS 13 (WNET) New York",
    "reelzchannel/4175": "ReelzChannel",
    "science-hd/5828": "Science",
    "showtime-eastern-feed/665": "Showtime (E)",
    "showtime-2-eastern/1387": "SHOWTIME 2",
    "starz-eastern/583": "STARZ East",
    "sundancetv-usa-east-hd/8264": "SundanceTV HD",
    "syfy-eastern-feed/596": "SYFY",
    "tbs-east/61": "TBS",
    "turner-classic-movies-canada/2847": "TCM",
    "teennick-eastern/1954": "TeenNick",
    "telemundo-east-hd/33284": "Telemundo East",
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
    "vh1-eastern-feed/663": "VH1",
    "vice/624": "VICE",
    "abc-wabc-new-york-ny/1769": "WABC (New York) ABC East",
    "cbs-wcbs-new-york-ny/1766": "WCBS (New York) CBS East",
    "we-hd/6220": "WE tv",
    "nbc-wnbc-new-york-ny/1767": "WNBC (New York) NBC East",
    "fox-wnyw-new-york-ny-hd/4557": "WNYW (New York) FOX East"

    # Add more channel IDs and names as needed
}

def scrape_tv_programming(channel_id, date):
    url = f"https://www.tvpassport.com/tv-listings/stations/{channel_id}/{date}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
    cookies = {
        "cisession": "d86212bfc9056dc4f9b43c43e4139a5f11f2f719"
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    
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
                "channel_id": channel_id  # Add channel_id to the dictionary
            })

        return programming_data
    else:
        print("Failed to retrieve programming data. Status code:", response.status_code)
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
    
    # Convert tree to XML string
    xml_string = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode()
    
    return xml_string


# Example usage
channel_ids = [
    "ae-canada/4311",
    "acc-network/33964",
    "amc-canada/3822",
    "american-heroes-channel/2035",
    "animal-planet-us-east/645",
    "bbc-america-east/615",
    "bbc-news-north-america/527",
    "bet-eastern-feed/323",
    "bet-her/6837",
    "bloomberg-tv-usa-hd/6790",
    "boomerang/2268",
    "bravo-usa-eastern-feed/646",
    "cartoon-network-usa-hd-eastern/6917",
    "cbs-sports-network-usa/3115",
    "cinemax-eastern-feed/632",
    "cmt-canada/120",
    "cnbc-usa/201",
    "cnn/70",
    "comedy-central-us-eastern-feed/647",
    "the-cooking-channel/4226",
    "crime-investigation-network-usa-hd/6216",
    "cspan/648",
    "cspan-2/1050",
    "destination-america/2074",
    "discovery-channel-us-eastern-feed/649",
    "discovery-family-channel/4225",
    "discovery-life-channel/1273",
    "disney-eastern-feed/595",
    "disney-junior-usa-hd-east/10523",
    "disney-xd-usa-eastern-feed/1053",
    "e-entertainment-usa-eastern-feed/617",
    "espn-news/1527",
    "espn-u/3331",
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
    "golf-channel-canada/9900",
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
    "history-channel-us-hd-east/4660",
    "hln/425",
    "independent-film-channel-us/1966",
    "investigation-discovery-usa-eastern/2090",
    "ion-eastern-feed-hd/8534",
    "lifetime-network-us-eastern-feed/654",
    "lifetime-movies-hd-east/4723",
    "logo-east/2091",
    "mlb-network/6178",
    "moremax-eastern-hd/7097",
    "motor-trend-hd/12597",
    "msnbc-usa/655",
    "mtv-usa-eastern-feed/656",
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
    "outdoor-channel-us/1086",
    "oprah-winfrey-network-usa-eastern/1159",
    "oxygen-eastern-feed/659",
    "pbs-wnet-new-york-ny/1774",
    "reelzchannel/4175",
    "science-hd/5828",
    "showtime-eastern-feed/665",
    "showtime-2-eastern/1387",
    "starz-eastern/583",
    "sundancetv-usa-east-hd/8264",
    "syfy-eastern-feed/596",
    "tbs-east/61",
    "turner-classic-movies-canada/2847",
    "teennick-eastern/1954",
    "telemundo-east-hd/33284",
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
    "vh1-eastern-feed/663",
    "vice/624",
    "abc-wabc-new-york-ny/1769",
    "cbs-wcbs-new-york-ny/1766",
    "we-hd/6220",
    "nbc-wnbc-new-york-ny/1767",
    "fox-wnyw-new-york-ny-hd/4557"
]


# Calculate today's date and the dates for the next two days
dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]

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
