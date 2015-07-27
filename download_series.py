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

SERIES = 'http://watch-series-tv.to/serie/'
HOMEPAGE = 'http://watch-series-tv.to'
EPISODE_STRING = '/episode/'
GORILLAVID_STRING = 'download_link_gorillavid.in'
CALE_LINK = '/open/cale/'
GORILLAVID_URL = 'http://gorillavid.in/'


def main():
    """ Downlaods complete series from watchseries
    """

    prefix = os.path.abspath('.')
    series_name = create_series_name()
    names_filename = prefix + '/names_' + series_name + '.txt'
    links_filename = prefix + '/links_' + series_name + '.txt'
    real_url = create_url(SERIES, series_name)
    if (not os.path.isfile(links_filename)
            or os.path.isfile(links_filename)
            and not created_today(links_filename)
            or not os.path.isfile(names_filename)
            or os.path.isfile(names_filename)
            and not created_today(names_filename)):
        watch_series_series_page = urllib2.urlopen(real_url)
        series_link = watch_series_series_page.readlines()
        watch_series_series_page.close()

        episodes_list_links = create_list_episodes_links(series_link,
                names_filename)

        gorillavid_list_links = create_gorillavid_links_list(
                episodes_list_links)

        create_download_links(gorillavid_list_links,
                links_filename)

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
        links = links_file.readlines()
    # print links

    with open(names_filename, 'r') as names_file:
        names = names_file.readlines()
    # print names

    for i in range(len(links)):
        start_pos = names[i].find('/', 8) + 1
        start_pos = names[i].find('/', start_pos) + 1
        end_pos = names[i].find('.', start_pos)
        filename = names[i][start_pos: end_pos]

        # print filename

        pos = links[i].find('video')
        start_pos = links[i].find('.', pos)
        end_pos = links[i].find('\\', start_pos)

        fileformat = links[i][start_pos: end_pos]
        # print fileformat
        # print links[i][:-1]


        string = 'wget -c ' + links[i][:-1] + ' -O ' + filename + fileformat
        print string
        os.system(string)

    # for i in range(len(downloadable_links)):
    #     start_pos = episodes_list_links[i].find('/', 8) + 1
    #     start_pos = episodes_list_links[i].find('/', start_pos) + 1
    #     end_pos = episodes_list_links[i].find('.', start_pos)
    #     filename = episodes_list_links[i][start_pos: end_pos]


    #     # pos = downloadable_links[i].find('video')
    #     # start_pos = downloadable_links[i].find('.', pos)
    #     # fileformat = downloadable_links[i][start_pos:]
    #     pos = links[i].find('video')
    #     start_pos = links[i].find('.', pos)
    #     fileformat = links[i][start_pos:]



    #     string = 'wget ' + links[i] + ' -O ' + filename+ fileformat
    #     os.system(string)


def create_download_links(episodes_list_links, links_filename):
    """ Create download links

    :episodes_list_links: list of links
    :returns: list of downloadaable links

    """
    links = []
    downloadable_links = []
    for i in range(len(episodes_list_links)):
        start_pos = episodes_list_links[i].find('/', 8) + 1
        value = episodes_list_links[i][start_pos: ]
        url = GORILLAVID_URL + 'embed-' + value + '-960x480.html'
        print url
        links.append(url)


    for i in range(len(links)):
        webpage = urllib2.urlopen(links[i])
        webpage_text = webpage.read()
        webpage.close()

        initial_pos = webpage_text.find('file:')
        start_pos = webpage_text.find('http', initial_pos)
        end_pos = webpage_text.find('"', start_pos)
        url = webpage_text[start_pos: end_pos]
        print url
        downloadable_links.append(url)

    with open(links_filename, 'w') as links_file:
        for elem in downloadable_links:
            links_file.write(elem)
            links_file.write('\n')

    return downloadable_links



def create_gorillavid_links_list(episodes_list_links):
    """ creates list of gorillavid links

    :episodes_list_links: list
    :returns: list

    """
    intermediate_links = []
    for i in range(len(episodes_list_links)):

        # open link
        intermediate_webpage = urllib2.urlopen(episodes_list_links[i])
        intermediate_webpage_text = intermediate_webpage.read()
        intermediate_webpage.close()

        # for i in range(len(intermediate_webpage_text)):
            # print i
        # print intermediate_webpage_text
        # ignore first gorillavid link because it's normally not a complete epis
        pos = intermediate_webpage_text.find(GORILLAVID_STRING)
        if pos != -1:
            pos = intermediate_webpage_text.find(GORILLAVID_STRING, pos + 1)
            if pos != -1:
                start_pos = intermediate_webpage_text.find(CALE_LINK, pos)
                end_pos = intermediate_webpage_text.find('"', start_pos)
                link = intermediate_webpage_text[start_pos:end_pos]
                # print link
                intermediate_links.append(create_url(HOMEPAGE, link))


    # print links
    for elem in intermediate_links:
        print elem

    links = []
    for i in range(len(intermediate_links)):

        intermediate_webpage = urllib2.urlopen(intermediate_links[i])
        intermediate_webpage_text = intermediate_webpage.read()
        intermediate_webpage.close()

        start_pos = intermediate_webpage_text.find(GORILLAVID_URL)
        end_pos = intermediate_webpage_text.find('"', start_pos)
        link = intermediate_webpage_text[start_pos:end_pos]
        links.append(link)

    for elem in links:
        print elem
    return links


def create_list_episodes_links(series_link, names_filename):
    """ creates list of episodes links

    :first_link: data
    :returns: data

    """
    links = set()
    for i in range(len(series_link)):
        pos = series_link[i].find(EPISODE_STRING)
        while pos != -1:
            end_pos = series_link[i].find('"', pos)
            link = series_link[i][pos :end_pos]
            links.add(create_url(HOMEPAGE, link))
            pos = series_link[i].find(EPISODE_STRING, end_pos)
    for elem in sorted(links):
        print elem

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
    for i in range(1, len(sys.argv[1:]) + 1):
        if i != len(sys.argv[1:]):
            name += sys.argv[i] + '_'
        else:
            name += sys.argv[i]
    name = name.lower()
    return name



def create_url(prefix, url):
    """ Creates url from series name

    :url: series name string
    :returns: url string

    """
    # appending name to the prefix url
    url = prefix + url
    return url


if __name__ == '__main__':
    main()

