import sys
from PyQt4 import QtGui

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

team_1_label = ''
team_2_label = ''

table = None


def teams_combo_box(teams_names):
    combo_box = QtGui.QComboBox()
    for team_name in teams_names:
        combo_box.addItem(team_name)
    return combo_box


def make_table(data):
    table = QtGui.QTableWidget()

    table.setWindowTitle("QTableWidget Example @pythonspot.com")
    table.resize(400, 250)
    table.setColumnCount(2)

    table.setHorizontalHeaderLabels(('Name', 'Probability'))

    for index, (name, possibility) in enumerate(data.items()):
        table.insertRow(index)
        if index % 2:
            table.setItem(index, 0, QtGui.QTableWidgetItem(QtGui.QIcon(r'D:\GitHub\hockey_prediction_app\down.png'), name))
        else:

            table.setItem(index, 0, QtGui.QTableWidgetItem(name))
        table.setItem(index, 1, QtGui.QTableWidgetItem(str(possibility)))

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


def connect_btn_callback():
    print(team_1_label)
    print(team_2_label)
    row_index = table.rowCount()+1
    table.insertRow(row_index)
    table.setItem(row_index, 0, QtGui.QTableWidgetItem(team_1_label))


def team_1_selector_callback(text):
    global team_1_label
    team_1_label = text


def team_2_selector_callback(text):
    global team_2_label
    team_2_label = text


def main():
    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QWidget()

    main_layout = QtGui.QVBoxLayout()

    tabs = construct_tabs(data)
    main_layout.addWidget(tabs)

    teams_names = ['Team 1', 'Team 2']

    buttons_layout = QtGui.QGridLayout()
    team_1_selector = teams_combo_box(teams_names)
    team_2_selector = teams_combo_box(teams_names)
    team_1_selector.currentIndexChanged['QString'].connect(team_1_selector_callback)
    team_2_selector.currentIndexChanged['QString'].connect(team_2_selector_callback)

    buttons_layout.addWidget(team_1_selector, 0, 0)
    buttons_layout.addWidget(team_2_selector, 0, 1)


    main_layout.addLayout(buttons_layout)

    calculate_btn = QtGui.QPushButton('Calculate')
    calculate_btn.clicked.connect(connect_btn_callback)

    main_layout.addWidget(calculate_btn)


    # Set title and show
    main_window.setWindowTitle('Hockey probability app')
    main_window.setLayout(main_layout)
    main_window.show()

    tabs.setParent(None)
    main_layout.insertWidget(0, construct_tabs({'a': {}, 'b': {}}))
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
