import re
from urllib.parse import urljoin

import requests
from html_table_parser.parser import HTMLTableParser
from lxml.html import fromstring, tostring


def get_matches_info(site, url, headers):
    matches_info = []
    for match_url_path in get_hockey_matches(url, headers):
        html_page = get_match_html_page(site, match_url_path, headers)
        matches_info.append({
            'date': get_match_date(html_page),
            'players_scored': get_payers_scored(html_page),
            'match_players': get_match_players(html_page)
        })
    return matches_info


def get_hockey_matches(url, headers):
    request_result = requests.get(url, headers=headers)
    html_page = fromstring(request_result.content)
    matches_table = html_page.find_class('preview m-b-30')
    for matches_group in matches_table:
        for match_info in matches_group.findall('tbody/tr'):
            pattern = re.compile(r'"(\\/\w+\\/\d+)"')
            match = pattern.search(match_info.attrib['onclick']).group().replace('\\', '')
            yield match


def get_match_html_page(site, match_url_path, headers):
    request_result = requests.get(urljoin(site, match_url_path), headers=headers)
    return fromstring(request_result.content)


def get_match_date(html_page):
    found_elements = html_page.find_class('col-100 heading')
    for el in found_elements:
        for li_element in el.findall('ul/li'):
            pattern = re.compile(r'(\d+\.\d+\.\d+)')
            search_result = pattern.search(li_element.text_content())
            if search_result is not None:
                return search_result.group()


def get_payers_scored(html_page):
    score_tables = html_page.find_class('table-last-right')

    players_scored = set()
    for table in score_tables:
        for redundant_el in table.find_class('row-plus-minus'):
            redundant_el.getparent().remove(redundant_el)
        table_string = tostring(table, encoding='utf-8')
        table_parser = HTMLTableParser()
        table_parser.feed(table_string.decode('utf-8'))
        for row in table_parser.tables[0][1:]:
            players_scored.add(extract_player_name(row[2]))

    return players_scored


def extract_player_name(player_info, cut_last_element=True):
    player_name_els = player_info.split()
    if cut_last_element:
        player_name_els = player_name_els[:-1]
    processed_player_name_els = [name_el.lower().capitalize() for name_el in player_name_els]
    return ' '.join(processed_player_name_els)


def get_match_players(html_page):
    match_players = set()
    players_tables_containers = html_page.find_class('col-soupisky-home') + html_page.find_class('col-soupisky-visitor')
    for tables_container in players_tables_containers:
        for table in tables_container.findall('table'):
            table_string = tostring(table, encoding='utf-8')
            table_parser = HTMLTableParser()
            table_parser.feed(table_string.decode('utf-8'))
            for row in table_parser.tables[0][1:]:
                if row[0]:
                    match_players.add(extract_player_name(row[2], cut_last_element=False))
    return match_players
