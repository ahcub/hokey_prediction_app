from operator import attrgetter

from pandas import DataFrame


class FormulasRegistry:
    formulas = []

    @staticmethod
    def register_formula(formula_func):
        FormulasRegistry.formulas.append(formula_func)
        FormulasRegistry.formulas.sort(key=attrgetter('__name__'))
        return formula_func

    @staticmethod
    def get_processed_data_for_all_formulas(raw_data):
        result = []
        for formula_func in FormulasRegistry.formulas:
            result.append((formula_func.__name__, formula_func(raw_data)))
        return result


@FormulasRegistry.register_formula
def hits_count_mult_success_percent(raw_data):
    probability = raw_data.get('S/Z') * raw_data.get('RÚS')

    return data_to_return(raw_data, probability)


@FormulasRegistry.register_formula
def match_based_probabilities(raw_data):
    probability = ((raw_data.get('games_scored') / raw_data.get('games_played')) *
                   raw_data.get('current_zero_result_streak')) * 100.0

    return data_to_return(raw_data, probability)


def data_to_return(raw_data, probability):
    result_df = DataFrame({'Name': raw_data.get('Jméno'), 'Team': raw_data.get('Tým'),
                           'Probability': probability, 'tendency': raw_data.get('tendency')})
    result_dict = {}
    for team, indexes in result_df.groupby('Team').groups.items():
        team_data_dicts = result_df.loc[indexes, ['Name', 'Probability', 'tendency']].set_index('Name').to_dict()
        team_result_dict = {}
        for dict_name, dict_data in team_data_dicts.items():
            for key, val in dict_data.items():
                if key not in team_result_dict:
                    team_result_dict[key] = {}
                team_result_dict[key][dict_name] = val

        result_dict[team] = team_result_dict
    return result_dict

if __name__ == '__main__':
    print(FormulasRegistry.formulas)
