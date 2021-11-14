import os
from time import time
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import re


def parse(url):
    # It computes the parsing of the searched elements
    soup = BeautifulSoup(open(url), features="lxml")
    # Calling the function that parse the anime title
    animeTitle = filterName(soup)
    # Initialize the vector in wich results of the parsing will be placed
    ret_values = [animeTitle]
    # It computes the parsing of all elements into a span tag
    res_span = span_analysis(soup)
    # To respect the specified order in which the .tsv file has to be build we have to place
    # the animeUsers field between the other returned from span_analysis so we have implemented these 2 for loops
    for i in range(6):
        ret_values.append(res_span[i])
    ret_values.append(users(soup))
    for i in range(6, len(res_span)):
        ret_values.append(res_span[i])
    # Append all the other computed fields in the return list
    ret_values.append(synopsis(soup))
    ret_values.append(related_anime(soup))
    ret_values.append(characters(soup))
    ret_values.append(voices(soup))
    ret_values.append(staff(soup))
    ret_values.append(parse_url(soup))
    return ret_values

def analyse_dir(index):
    ''' It calls the parsing function on each file that belongs to the given directory (with directory index in [1,383]) '''
    
    # It takes the directory index, each directory in named with page_i and contains 50 html anime pages
    page = "/content/drive/My Drive/ADM-HW3/HW3/pages/page"+str(index)+"/"
    directory_list = os.listdir(page)
    for file in directory_list:
        # It takes the index of the anime
        file_index = re.split('_|\.', file)[1]
        r = parse(page+file)
        write_Tsv(r, file_index)


def write_Tsv(arr, ind):
    # Write a .tsv file for each anime, the file's name is index.tsv where index is that of the anime
    header = ['animeTitle', 'animeType', 'animeNumEpisode', 'releaseDate', 'endDate', 'animeNumMembers', 'animeScore', 'animeUsers',
              'animeRank', 'animePopularity', 'animeDescription', 'animeRelated', 'animeCharacters', 'animeVoices', 'animeStaff', 'animeUrl']
    filename = '/content/drive/My Drive/ADM-HW3/HW3/tsvFiles/anime_' + ind + '.tsv'
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)
        writer.writerow(arr)


def filterName(soup):
    # It finds the title of the html page
    result = soup.find("title").string.lstrip().rstrip()
    return result


def span_analysis(soup):
    # It returns all the searched elements that are inside a span tag
    animeType = ""
    animeNumEpisode = ""
    aired = ""
    animeNumMembers = -1
    animeScore = -1.0
    animeRank = -1
    animePopularity = -1
    release = ""
    end = ""
    results = soup.find_all("span", class_="dark_text")
    for r in results:
        stringa = r.get_text()
        if animeType == "" and "Type" in stringa:
            animeType = anime_type(r)
        if animeNumEpisode == "" and "Episodes" in stringa:
            tmp = r.parent.text.split()[1]
            animeNumEpisode = int(tmp) if tmp != "Unknown" else None
        if aired == "" and "Aired" in stringa:
            # The function invoked return a list with at most 2 dates, we have to split them in release and end date
            aired = dates(r)
            release = aired[0]
            end = aired[1]
        if animeNumMembers == -1 and "Members" in stringa:
            animeNumMembers = number_members(r)
        if animeScore == -1.0 and "Score:" in stringa:  # Aggiunto -1
            animeScore = score(r)
        if animeRank == -1 and "Ranked" in stringa:
            animeRank = rank(r)
        if animePopularity == -1 and "Popularity" in stringa:
            animePopularity = popularity(r)
    # We place all the results in an array to return
    array = [animeType, animeNumEpisode, release, end, animeNumMembers,
             animeScore, animeRank, animePopularity]
    return array


def anime_type(r):
    # It finds the anime type
    return r.find_next('a').contents[0].lstrip().rstrip()


def dates(r):
    # It computes the start and end date of an anime and when it doesn't have an end, it returns an empty string
    times = r.parent.text.split()
    if "to" in times:
        # 'to' in times -> we have the end date
        to_ind = times.index("to")
        return parse_dates(times[1:to_ind], times[to_ind + 1:])
    elif "Not" in times:
        # Id dates are not available we return a list on None
        return [None, None]
    else:
        # We only have the starting date
        return parse_dates(times[1:])


def parse_dates(start, end=[]):
    ''' 
    Based on the length of the date this function understand what fields make up
    the date and parse there with the correct format type
    '''
    
    if len(start) == 1:
        # We have only the year
        start = datetime.strptime(start[0], '%Y')
    elif len(start) == 2:
        # We have only year and month
        start = datetime.strptime(" ".join(start), '%b %Y')
    elif len(start) == 3:
        # We have all the three fields
        start = datetime.strptime(" ".join(start), '%b %d, %Y')

    if len(end) == 1 and end[0] != "?":
        # If end date is '?' means that the anime is still in production
        end = datetime.strptime(end[0], '%Y')
    elif len(end) == 2:
        end = datetime.strptime(" ".join(end), '%b %Y')
    elif len(end) == 3:
        end = datetime.strptime(" ".join(end), '%b %d, %Y')
    else:
        # If we don't have an end date we don't parse anything
        end = ""
    return [start, end]


def number_members(r):
    # It parses the number of members removing the ',' that separate the number (e.g. 1,360 becomes 1360)
    animeNumMembers = r.parent.text.split()[1]
    result = animeNumMembers.replace(',', '')
    return int(result)


def score(r):
    # It parses the score of the anime
    animeScore = r.parent.text.split()[1]
    return float(animeScore) if animeScore != "N/A" else None


def users(soup):
    # It parses the number of users of the anime
    result = soup.find_all(
            'div', attrs={"data-title": "score"})
    result = result[0]['data-user']
    result = result.split()[0]
    print(result)
    result = result.replace(',', '')
    # If we have '-' we return None because it means that we do not have a users number
    return int(result) if result != '-' else None


def rank(r):
    # It parses the rank of the anime
    result = r.parent.text.split()[1]
    if result != "N/A":
        # If there is a rank we remove the first character that is '#'
        return int(result[1:])
    else:
        # If there is not rank we return None
        return None


def popularity(r):
    # It parses the popularity of the anime
    return int(r.parent.text.split()[1][1:])


def synopsis(soup):
    # It parses the synopsis of the anime also making some processing on the string
    arr = soup.find('p', itemprop="description")
    arr = ' '.join(str(x) for x in arr)
    # Replace <br> tag, '\n' and '\t' with blak space and multiple blank spaces with only one of them
    arr = arr.replace('<br/>', ' ')
    arr = arr.replace('\n', ' ')
    arr = arr.replace('\t', ' ')
    arr = arr.replace('  ', ' ')
    # It removes whitespace from the beginning and end of the string
    return arr.lstrip().rstrip()


def related_anime(soup):
    # It returns related anime with hyperlinks and that are uniques
    r_vec = []
    r_sect = soup.find('h2', text=re.compile(r'Related Anime'))
    if r_sect == None:
        # If there aren't related animes it returns an empty list
        return r_vec
    find_table = r_sect.find_next('table')
    rows = find_table.find_all('tr')
    for i in rows:
        table_data = i.find_all('td')
        for el in table_data:
            a = el.find('a')
            if a != None and a.get('href') != '' and a.get('href') != None:
                r_vec.append(a.text.rstrip().lstrip())
    # The set cast ensures uniques values
    return list(set(r_vec))


def characters(soup):
    # It returns the list of characters
    c_vec = []
    c_sect = soup.find('h2', text=re.compile(r'Characters & Voice Actors'))
    find_div = c_sect.find_next('div')
    find_table = find_div.find_all('table')
    for t in find_table:
        rows = t.find_all('tr')
        for i in rows:
            table_data = i.find_all('td')
            character = table_data[1].text.rstrip().lstrip()
            tmp = character.split('\n ')
            c_vec.append(tmp[0])
    # It removes '' from the list
    c_vec = list(filter(('').__ne__, c_vec))
    return c_vec


def voices(soup):
    # It returns the list of voices, as above
    v_vec = []
    v_sect = soup.find('h2', text=re.compile(r'Characters & Voice Actors'))
    find_div = v_sect.find_next('div')
    find_table = find_div.find_all('table')
    for t in find_table:
        rows = t.find_all('tr')
        for i in rows:
            table_data = i.find_all('td')
            voice = table_data[0].text.rstrip().lstrip()
            tmp = voice.split('\n ')
            v_vec.append(tmp[0])
    v_vec = list(set(v_vec))
    if '' in v_vec:
        v_vec.remove('')
    return v_vec


def staff(soup):
    # It returns the list of characters
    s_vec = []
    s_sect = soup.find('h2', text=re.compile(r'Staff'))
    find_div = s_sect.find_next(
        'div', attrs={"class": "detail-characters-list"})
    if find_div == None:
        return s_vec
    find_table = find_div.find_all('table')
    for t in find_table:
        rows = t.find_all('tr')
        for i in rows:
            table_data = i.find_all('td')
            member = table_data[1].text.rstrip().lstrip()
            tmp = member.split('\n ')
            # It adds to the list that will be returnes a list composed of the name of the person in the staff and its role
            s_vec.append([tmp[0], tmp[len(tmp)-1].lstrip()])
    return s_vec


def parse_url(soup):
    # It parses the url of the html anime page
    return soup.find('meta', attrs={"property": "og:url"}).attrs['content']
