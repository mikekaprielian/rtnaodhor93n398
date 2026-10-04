import requests
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import xml.etree.ElementTree as ET

# Dictionary mapping channel IDs to channel names
channel_names = {
    "bounce-network/14312": "Bounce",
    "bravo-usa-eastern-feed/646": "Bravo",
    "charge/15228": "CHARGE!",
    "cinemax-eastern-feed/632": "Cinemax",
    "cinemax-action-eastern-hd/7094": "Cinemax Action",
    "cinemax-classics-eastern/636": "Cinemax Classics",
    "cinemax-hits-eastern-hd/7097": "Cinemax Hits",
    "comet-tv/16811": "Comet",
    "court-tv-network/33650": "Court TV",
    "discovery-turbo-usa/2143": "Discovery Turbo",
    "hbo-hd-eastern-feed/627": "HBO",
    "hbo-comedy-hd-east/7105": "HBO Comedy",
    "hbo-drama-hbo-3-eastern-hd/7099": "HBO Drama",
    "hbo-hits-eastern-feed-hd/6313": "HBO Hits",
    "hbo-latino-hbo-7-hd-eastern/7096": "HBO Latino",
    "hbo-movies-east/630": "HBO Movies",
    "hbo-west/6424": "HBO West",
    "ion-eastern-feed/1274": "ION",
    "ion-mystery-kftrdt3-ontario-ca/16533": "ION Mystery",
    "law-crime-network/32823": "Law & Crime",
    "love-nature/3907": "Love Nature",
    "metv-network/16325": "MeTV",
    "metv-toons-wjlp2-new-jersey/15178": "MeTV Toons",
    "mgm-east/7609": "MGM+",
    "mgm-drivein/11487": "MGM+ Drive In",
    "mgm-hits-east/11485": "MGM+ Hits",
    "mgm-marquee-hd/11616": "MGM+ Marquee",
    "reelzchannel/4175": "REELZ Channel",
    "roar/39566": "Roar",
    "screenpix/34659": "Screenpix",  
    "screenpix-action/34660": "Screenpix Action",
    "screenpix-westerns/34661": "Screenpix Westerns",
    "scripps-news/5999": "Scripps News",
    "sundancetv-usa-east-hd/8264": "Sundance TV",
    "the-nest/14118": "The Nest",
    "telemundo-wneu-manchester-ma-hd/9350": "Telemundo (WNEU)"

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
    p_tags = item.find_all("p")
    if len(p_tags) >= 2:
        return p_tags[1].get_text(strip=True)
    elif len(p_tags) == 1:
        return p_tags[0].get_text(strip=True)
    return item.get("data-description")

def parse_icon(item):
    return item.get("data-showpicture")

def parse_title(item):
    show_name = item.get("data-showname")
    episode_title = item.get("data-episodetitle")

    if show_name == "Movie":
        return episode_title
    elif show_name == "Cinéma":
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
    "bounce-network/14312",
    "bravo-usa-eastern-feed/646",
    "charge/15228",
    "cinemax-eastern-feed/632",
    "cinemax-action-eastern-hd/7094",
    "cinemax-classics-eastern/636",
    "cinemax-hits-eastern-hd/7097",
    "comet-tv/16811",
    "court-tv-network/33650",
    "discovery-turbo-usa/2143",
    "hbo-hd-eastern-feed/627",
    "hbo-comedy-hd-east/7105",
    "hbo-drama-hbo-3-eastern-hd/7099",
    "hbo-hits-eastern-feed-hd/6313",
    "hbo-latino-hbo-7-hd-eastern/7096",
    "hbo-movies-east/630",
    "hbo-west/6424",
    "ion-eastern-feed/1274",
    "ion-mystery-kftrdt3-ontario-ca/16533",
    "law-crime-network/32823",
    "love-nature/3907",
    "metv-network/16325",
    "metv-toons-wjlp2-new-jersey/15178",
    "mgm-east/7609",
    "mgm-drivein/11487",
    "mgm-hits-east/11485",
    "mgm-marquee-hd/11616",
    "reelzchannel/4175",
    "roar/39566",
    "screenpix/34659",  
    "screenpix-action/34660",
    "screenpix-westerns/34661",
    "scripps-news/5999",
    "sundancetv-usa-east-hd/8264",
    "the-nest/14118",
    "telemundo-wneu-manchester-ma-hd/9350"
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
