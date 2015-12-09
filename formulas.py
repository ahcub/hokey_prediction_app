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
    multiplication_result = raw_data.get('S/Z') * raw_data.get('RÚS')
    result_df = DataFrame({'Name': raw_data.get('Jméno'), 'Team': raw_data.get('Tým'),
                           'Probability': multiplication_result})

    result_dict = {}

    for team, indexes in result_df.groupby('Team').groups.items():
        result_dict[team] = result_df.loc[indexes, ['Name', 'Probability']].set_index('Name').to_dict()['Probability']

    return result_dict


@FormulasRegistry.register_formula
def match_based_probabilities(raw_data):
    probability = ((raw_data.get('games_scored') / raw_data.get('games_played')) *
                   raw_data.get('current_zero_result_streak')) * 100.0

    result_df = DataFrame({'Name': raw_data.get('Jméno'), 'Team': raw_data.get('Tým'),
                           'Probability': probability})

    result_dict = {}

    for team, indexes in result_df.groupby('Team').groups.items():
        result_dict[team] = result_df.loc[indexes, ['Name', 'Probability']].set_index('Name').to_dict()['Probability']

    print(result_dict)
    return result_dict
