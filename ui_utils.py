from operator import itemgetter

from PyQt4 import QtGui

WINDOW_WIDTH = 450
WINDOW_HEIGHT = 550

TABLE_HEIGHT = 400
TABLE_WIDTH = 300


def teams_combo_box(teams_names):
    combo_box = QtGui.QComboBox()
    for team_name in teams_names:
        combo_box.addItem(team_name)
    return combo_box


def make_table(data):
    table = QtGui.QTableWidget()

    table.resize(TABLE_HEIGHT, TABLE_WIDTH)
    table.setColumnCount(2)

    table.setHorizontalHeaderLabels(('Name', 'Probability'))

    sorted_data = [(name, possibility) for name, possibility in data.items()]
    sorted_data.sort(key=itemgetter(1), reverse=True)
    for index, (name, possibility) in enumerate(sorted_data):
        table.insertRow(index)
        table.setItem(index, 0, QtGui.QTableWidgetItem(name))
        table.setItem(index, 1, QtGui.QTableWidgetItem('%.2f %%' % possibility))

    return table


def construct_tabs(data):
    tabs = QtGui.QTabWidget()
    for tab_name, teams_data in data.items():
        tab = QtGui.QWidget()
        tab_layout = QtGui.QGridLayout()
        for index, (team_name, players_probabilities) in enumerate(teams_data.items()):
            tab_layout.addWidget(QtGui.QLabel(team_name), 0, index)
            table = make_table(players_probabilities)
            tab_layout.addWidget(table, 1, index)
        tab.setLayout(tab_layout)
        tabs.addTab(tab, tab_name)
    return tabs
