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
    "cbc-cbmt-montreal-qc-hd/4022": "CBC",
    "cbc-news-network/74": "CBC News Network",
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
    "ctv2-london-on/139": "CTV2 London",
    "ctv2-chrodt43-ottawa-on/13791": "CTV2 Ottawa",
    "destination-america/2074": "Destination America",
    "discovery-channel-canada-rogers/38127": "Discovery",
    "disney-channel-canada-east/16682": "Disney Channel",
    "dtour/11143": "DTOUR",
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
    "investigation/11344": "Investigation",
    "investigation-discovery-canada-rogers/38128": "Investigation Discovery",
    "lcn/432": "LCN",
    "lifetime-tv-canada/1148": "Lifetime",
    "magnolia-network-canada-rogers/38129": "Magnolia Network",
    "much-music/73": "Much",
    "national-geographic-canada/475": "National Geographic",
    "nbc-wnbc-new-york-ny/1767": "NBC (WNBC)",
    "nosey-watl2-atlanta-ga/9601": "Nosey",
    "noovo-cfjp-montrealqc-hd/5940": "Noovo",
    "cjon-ntv-stjohn-nl/199": "NTV",
    "omni-east/31930": "OMNI East",
    "oxygen-true-crime-canada/1120": "Oxygen True Crime",
    "showcase-canada/62": "Showcase",
    "silver-screen-classics/2115": "Silver Screen Classics",
    "slice/60": "Slice",
    "sportsnet-360/336": "Sportsnet 360",
    "sportsnet-east/255": "Sportsnet East",
    "sportsnet-one/8249": "Sportsnet One",
    "sportsnet-ontario/254": "Sportsnet Ontario",
    "sportsnet-pacific/314": "Sportsnet Pacific",
    "sportsnet-west/252": "Sportsnet West",
    "sportsnet-world/4442": "Sportsnet World",
    "starz1-east/55": "STARZ 1",
    "starz2-east/438": "STARZ 2",
    "super-ecran/57": "Super Ecran 1",
    "super-ecran-2/362": "Super Ecran 2",
    "super-ecran-3/410": "Super Ecran 3",
    "super-ecran-4/411": "Super Ecran 4",
    "stingray-naturescape-hd/16122": "Stingray Naturescape",
    "telequebec-civm-montreal/1140": "Télé-Québec",
    "weather-network/419": "The Weather Network",
    "treehouse/163": "Treehouse",
    "tsn1/11": "TSN 1",
    "tsn2/4294": "TSN 2",
    "tsn3/13719": "TSN 3",
    "tsn4/279": "TSN 4",
    "tsn5/278": "TSN 5",
    "tva-sports/9823": "TVA Sports 1",
    "tva-sports-2/13777": "TVA Sports 2",
    "usa-network-can/16": "USA Network",
    "w-wtn-east/64": "W Network",
    "ytv-youth-television-east/15": "YTV",
    "z/344": "Z"

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
    "abc-wabc-new-york-ny/1769",
    "addik-tv/2033",
    "adult-swim-east/607",
    "amc-eastern-feed-hd/6219",
    "bbc-america-east/615",
    "bbc-news-north-america/527",
    "bnn-bloomberg/294",
    "bravo-canada/160",
    "canal-d/108",
    "canal-vie/307",
    "cartoon-network-canada-east/162",
    "cbc-cbmt-montreal-qc-hd/4022",
    "cbc-news-network/74",
    "cbs-wbz-boston-ma/134",
    "chch-hamilton-on/43",
    "city-montreal-qc/1171",
    "city-toronto-on/42",
    "cnn/70",
    "cp24-cablepulse-24/321",
    "crave1-east/72",
    "crave2-east/86",
    "crave3-east/85",
    "crave4/320",
    "ctv-comedy-east/159",
    "ctv-drama/59",
    "ctv-life/309",
    "ctv-montreal-cfcf-qc/50",
    "ctv-nature-canada/1188",
    "ctv-news-channel/416",
    "ctv-scifi/153",
    "ctv-speed-hd/3887",
    "ctv-cfto-toronto-on/39",
    "ctv-wild-canada/472",
    "ctv2-barrie-on-ckvr/14229",
    "ctv2-london-on/139",
    "ctv2-chrodt43-ottawa-on/13791",
    "destination-america/2074",
    "discovery-channel-canada-rogers/38127",
    "disney-channel-canada-east/16682",
    "dtour/11143",
    "e-canada/295",
    "flavour-network/169",
    "food-network-canada-rogers/38125",
    "fox-wnyw-new-york-ny-hd/4557",
    "fox-news/1083",
    "fox-sports-1/668",
    "fox-sports-2/2114",
    "fx-networks-canada/10026",
    "fxx-canada/13400",
    "global-ckmi-quebec-hd/6437",
    "global-ciiidt41-toronto/13585",
    "hgtv-canada-rogers/38126",
    "history-canada-east/164",
    "home-network/167",
    "rdi-news/8",
    "ici-cbft-montreal-qc/196", 
    "ici-television-cfhddt-montreal-qc/11385",
    "independent-film-channel-us/1966",
    "investigation/11344",
    "investigation-discovery-canada-rogers/38128",
    "lifetime-tv-canada/1148",
    "lcn/432",
    "magnolia-network-canada-rogers/38129",
    "much-music/73",
    "national-geographic-canada/475",
    "nbc-wnbc-new-york-ny/1767",
    "nosey-watl2-atlanta-ga/9601",
    "noovo-cfjp-montrealqc-hd/5940",
    "cjon-ntv-stjohn-nl/199",
    "omni-east/31930",
    "oxygen-true-crime-canada/1120",
    "showcase-canada/62",
    "silver-screen-classics/2115",
    "slice/60",
    "sportsnet-360/336",
    "sportsnet-east/255",
    "sportsnet-one/8249",
    "sportsnet-ontario/254",
    "sportsnet-pacific/314",
    "sportsnet-west/252",
    "sportsnet-world/4442",
    "starz1-east/55",
    "starz2-east/438",
    "super-ecran/57",
    "super-ecran-2/362",
    "super-ecran-3/410",
    "super-ecran-4/411",
    "stingray-naturescape-hd/16122",
    "telequebec-civm-montreal/1140",
    "weather-network/419",
    "treehouse/163",
    "tsn1/11",
    "tsn2/4294",
    "tsn3/13719",
    "tsn4/279",
    "tsn5/278",
    "tva-sports/9823",
    "tva-sports-2/13777",
    "usa-network-can/16",
    "w-wtn-east/64",
    "ytv-youth-television-east/15",
    "z/344"
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
