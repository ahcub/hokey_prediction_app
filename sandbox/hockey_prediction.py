import re

from html_table_parser.parser import HTMLTableParser
from lxml.html import fromstring, tostring
from pandas import DataFrame
from numpy import array
import pandas as pd

from data_utils import get_matches_info, get_players_data_from_matches_stats

data = {
    'hits_count_mult_success_percent': {
        'Team1':
            {
                'Dominik Kubalík': 61.5429,
                'Viktor Hübl': 55.9860,
                'Rostislav Olesz': 79.9362,
            },
        'Team2':
            {
                'Nicholas Johnson': 58.3758,
                'Jakub Valský': 55.5128,
                'Marcel Haščák': 50.0100,
            }
    },
    'match_based_stat': {
        'Team1':
            {
                'Dominik Kubalík': 61.5429,
                'Viktor Hübl': 55.9860,
                'Rostislav Olesz': 79.9362,
            },
        'Team2':
            {
                'Nicholas Johnson': 58.3758,
                'Jakub Valský': 55.5128,
                'Marcel Haščák': 50.0100,
            }
    }
}
if __name__ == '__main__':
    a = 'http://www.hokej.cz/tipsport-extraliga/zapasy?matchList-view-displayAll=1&matchList-filter-season=2015&matchList-filter-competition=5574'

    import requests

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,en;q=0.8,uk;q=0.6,ru;q=0.4",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Cookie": "__gfp_64b=V7olMB1z1eHHz1PITzwE5Wc4548gu8NNKiDuhHfpYB3.J7; popupShown=true; scrollingDivDisabled=true; ibbid=BBID-01-01228999950496682; _gat=1; __utmt=1; __utmt_trac2=1; PHPSESSID=f84tqsoduqpjj3cc4gvjrrsjn0; nette-browser=anoda2xp6a; _ga=GA1.2.509669587.1449483158; __utma=47860542.509669587.1449483158.1449670439.1449676216.19; __utmb=47860542.12.10.1449676216; __utmc=47860542; __utmz=47860542.1449483158.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
"Host": "www.hokej.cz",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",}


    df = get_players_data_from_matches_stats(a, headers)
    print(df.to_dict())
    # print(df)
    # with open(r'D:\GitHub\hockey_prediction_app\sandbox\table_example.html', encoding='utf-8') as file_:
    #     s = file_.read()
    #     p = HTMLTableParser()
    #     p.feed(s)
    #     table_set = array([table[1:] for table_group in p.tables for table in table_group])
    #     df2 = DataFrame(table_set[1:], columns=table_set[0])
    #     df2 = df2.convert_objects(convert_numeric=True)
    #     multiplication_result = df2.get('S/Z') * df2.get('RÚS')
    #     df3 = DataFrame({'Name': df2.get('Jméno'), 'Team': df2.get('Tým'), 'Probability': multiplication_result})
    #
    # result_df = df.merge(df3, left_index=True, right_on='Name')
    #
    # print(result_df)
    # print(result_df.get('Name'))
    # print(result_df.get('Team'))


    # r = requests.get(a, headers=headers)
    #
    # # print(r.content)
    # doc = fromstring(r.content)
    # c = doc.find_class('col-soupisky-home') + doc.find_class('col-soupisky-visitor')
    #
    # for el in c:
    #     for table in el.findall('table'):
    #         table_string = tostring(table, encoding='utf-8')
    #         p = HTMLTableParser()
    #         decoded_str = table_string.decode('utf-8')
    #         # print(decoded_str)
    #         p.feed(decoded_str)
    #         for row in p.tables[0][1:]:
    #             if row[0]:
    #                 print(extract_player_name(row[2], cut_last_element=False))
    #         print('=' * 40)

    # for el in c:
    #     for sub_el in el.findall('ul/li'):
    #         pattern = re.compile(r'(\d+\.\d+\.\d+)')
    #         search_result = pattern.search(sub_el.text_content())
    #         if search_result is not None:
    #             print(search_result.group())
    #
    #
    #     p = HTMLTableParser()
    #     p.feed(table_string.decode('utf-8'))
    #     print(p.tables)
    #
    # for table_set in p.tables:
    #     for table in table_set[1:]:
    #         scoring_probability = float(table[7]) * float(table[-1])
    #         if scoring_probability > 15.0:
    #             a = '%s %f | %s %f' % (table[1], scoring_probability, table[1], scoring_probability)
    #             print(a)

    # with open('example.html', encoding='utf-8') as file_:
    #     s = file_.read()
    #     p = HTMLTableParser()
    #     p.feed(s)
    #     table_set = array([table[1:] for table_group in p.tables for table in table_group])
    #
    #     df = DataFrame(table_set[1:], columns=table_set[0])
    #     df = df.convert_objects(convert_numeric=True)
    #     # for team in df.get('Tým').unique():
    #     #     print(team)
    #     multiplication_result = df.get('S/Z') * df.get('RÚS')
    #     result_df = DataFrame({'Name': df.get('Jméno'), 'Team': df.get('Tým'), 'Probability':multiplication_result})
    #     for team, indexes in result_df.groupby('Team').groups.items():
    #         print(result_df.loc[indexes, ['Name', 'Probability']].set_index('Name').to_dict()['Probability'])
        # for table_set in p.tables:
        #     for table in table_set[1:]:
        #         scoring_probability = float(table[7]) * float(table[-1])
        #         if scoring_probability > 50.0:
        #
        #             a = '%20s %3.4f | %20s %3.4f' %(table[1], scoring_probability, table[1], scoring_probability)
        #             print(a)
