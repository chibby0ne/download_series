#!/usr/bin/env python
# encoding: utf-8

"""
Filename: download_series.py
Author: Antonio Gutierrez
Email: chibby0ne@gmail.com
Github: https://github.com/chibby0ne
Created: 13/07/2015
Description: downloads series from website
"""


import os
import urllib2
import sys
import time
import base64


SERIES_STRING = '/serie/'
HOMEPAGE = 'http://thewatchseries.to'
EPISODE_STRING = '<a href="/episode/'
GORILLAVID_STRING = 'download_link_gorillavid.in'
DACLIPS_STRING = 'download_link_daclips.in'
MOVPOD_STRING = 'download_link_movpod.in'

DOMAINS = [ GORILLAVID_STRING, DACLIPS_STRING, MOVPOD_STRING ]

## vodlocker also works because the file: string is left in the main page

def main():
    """ Downloads complete series from watchseries.
    """

    prefix = os.path.abspath('.')
    series_name, seasons = get_input()
    # series_name = create_series_name()
    # seasons = get_seasons()
    names_filename = prefix + '/names_' + series_name + '.txt'
    links_filename = prefix + '/links_' + series_name + '.txt'
    real_url = HOMEPAGE + SERIES_STRING + series_name

    """ Create download links if there isn't a links file or there is one but
    wasn't created the day the script is running, or there isn't a name file
    or there is one but wasn't created the day the script is running
    """
    if (not os.path.isfile(links_filename)
            or os.path.isfile(links_filename)
            and not created_today(links_filename)
            or not os.path.isfile(names_filename)
            or os.path.isfile(names_filename)
            and not created_today(names_filename)):
        watch_series_series_page = urllib2.urlopen(real_url)
        series_link = watch_series_series_page.readlines()
        watch_series_series_page.close()

        print "Creating list of episodes links..."
        episodes_list_links = create_list_episodes_links(series_link,
                names_filename)

        print "Creating list of video hosters' links..."
        gorillavid_list_links = create_gorillavid_links_list(
                episodes_list_links)

        print "Creating download links..."
        create_download_links(gorillavid_list_links,
                links_filename)

    print "Downloading.."
    download_all_links(links_filename, names_filename)

def created_today(filename):
    """ Returns true if file was created today, otherwise false

    filename: string
    return: boolean

    """
    file_time = os.path.getmtime(filename)
    time_struct = time.localtime(file_time)
    today_date = time.localtime()

    if (time_struct.tm_year == today_date.tm_year
            and time_struct.tm_mon == today_date.tm_mon
            and time_struct.tm_mday == today_date.tm_mday):
        return True
    return False

def download_all_links(links_filename, names_filename):
    """ Downloads all links from links_filename ands names them according to
    names_filename

    :links_filename: string
    :names_filename: string

    """
    with open(links_filename, 'r') as links_file:
        links = links_file.read().split('\n')
    links = links[:-1]

    with open(names_filename, 'r') as names_file:
        names = names_file.read().split('\n')
    names = names[:-1]

    files_in_dir= os.listdir(".")

    for i in range(len(links)):
        try:
            # getting filename
            start_pos = names[i].rfind('/') + 1
            end_pos = names[i].find('.', start_pos)
            filename = names[i][start_pos : end_pos]

            # getting extension
            start_pos = links[i].rfind('.') + 1
            fileformat = links[i][start_pos :]

            # avoid downloading same file if there's one with another extension
            if filename + ".mp4" not in files_in_dir or filename + ".flv" not in files_in_dir:
                string = 'wget -c ' + links[i] + ' -O "' + filename + '.' + fileformat + '"'
                # print string
                os.system(string)
                # if (os.stat(filename + '.' + fileformat)[7] < 10000):
                #     retry_download_another_videohoster();
        except KeyboardInterrupt:
            sys.exit(1)

def create_download_links(episodes_list_links, links_filename):
    """ Create download links

    :episodes_list_links: list of links
    :returns: list of downloadable links

    """

    """
    Create embed link using format knowledge of the links (i.e: every embed
    link follows the same format)
    """
    links = []
    downloadable_links = []
    for i in range(len(episodes_list_links)):
        start_pos = episodes_list_links[i].rfind('/') + 1
        value = episodes_list_links[i][start_pos: ]

        domain = episodes_list_links[i][len('http://') : episodes_list_links[i].rfind('.')]

        url = 'http://' + domain + '.in/embed-' + value + '-960x480.html'
        links.append(url)

    """
    Find the raw files' url, save them in the links_file and return list of them
    """
    for i in range(len(links)):
        # print links[i]
        webpage = urllib2.urlopen(links[i])
        webpage_text = webpage.read()
        webpage.close()

        initial_pos = webpage_text.find('file:')
        start_pos = webpage_text.find('http', initial_pos)
        end_pos = webpage_text.find('"', start_pos)
        url = webpage_text[start_pos: end_pos]
        # print url
        downloadable_links.append(url)

    with open(links_filename, 'w') as links_file:
        for elem in downloadable_links:
            links_file.write(elem)
            links_file.write('\n')

    return downloadable_links

def create_gorillavid_links_list(episodes_list_links):
    """ creates list of gorillavid links

    :episodes_list_links: list of strings
    :returns: list of strings

    """

    """ Navigate to each episode page and look for the second gorillavid link
    and get that link
    """
    links = []
    for i in range(len(episodes_list_links)):

        intermediate_webpage = urllib2.urlopen(episodes_list_links[i])
        intermediate_webpage_text = intermediate_webpage.read()
        intermediate_webpage.close()

        found = False;
        index = 0
        while not found and index < len(DOMAINS):
            pos = intermediate_webpage_text.find(DOMAINS[index])
            if pos != -1:
                pos = intermediate_webpage_text.find(DOMAINS[index], pos + 1)
                if pos != -1:
                    found = True

                    """ get string for that gorillavid and attach it to the
                    homepage to build the next page's url
                    """
                    start_pos = intermediate_webpage_text.find('href="', pos)
                    end_pos = intermediate_webpage_text.find('"', start_pos +
                            len('href="'))
                    link = intermediate_webpage_text[start_pos + len('href="') :
                            end_pos]

                    """ Decode gorillavid url from this website's link
                    """
                    link = base64.b64decode(link[link.find("=") + 1 : ])
                    links.append(link)

            index = index + 1
    return links

def create_list_episodes_links(series_link, names_filename):
    """ creates list of episodes links

    :first_link: data
    :returns: data

    """
    links = set()
    for i in range(len(series_link)):
        pos = series_link[i].find(EPISODE_STRING)
        if pos != -1:
            end_pos = series_link[i].find('"', pos + len('<a href ="'))
            link = series_link[i][pos + len('<a href="') : end_pos]
            links.add(HOMEPAGE + link)
    with open(names_filename, 'w') as names_file:
        for elem in sorted(links):
            names_file.write(elem)
            names_file.write('\n')
    return sorted(links)

def create_series_name():
    """Creates series name from command line

    :returns: string

    """
    name = ''
    if len(sys.argv) == 1:
        name = os.path.basename(os.path.abspath('.'))
    else:
        for i in range(1, len(sys.argv[1:]) + 1):
            if i != len(sys.argv[1:]):
                name += sys.argv[i] + '_'
        else:
            name += sys.argv[i]
        name = name.lower()
    return name

def get_filesize(filename):
    """gets file size of filename in bytes

    :filename: string (file name)
    :returns: int (number of bytes)

    """
    return os.stat(filename)[6]

def get_input():
    """ parses command line parameters
    :returns: string series name
              string season number
    """
    name = ''
    if len(sys.argv) == 1:
        name = os.path.basename(os.path.abspath('.'))
        return name, 0
    else:
        name = ''
        season = []
        done = False
        i = 1
        while (i < len(sys.argv) and done == false):
            if sys.argv[i] == '-n':
                i += 1
                while (i < len(sys.argv) and sys.argv[i] != '-s'):
                    name += sys.argv[i] + '_'
                name = name[:-1] 
                name = name.lower()
            if sys.argv[i] == '-s':
                i += 1
                season = int(sys.argv[i])
                done = True  
        return name, season

if __name__ == '__main__':
    main()
