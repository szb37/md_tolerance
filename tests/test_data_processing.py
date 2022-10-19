# TODO: make files importable from top level (might have to add __init__.py)
import sys
sys.path.append('/sbmd_tolerance')

import data_processing


# data used for tests

first_MD_days_range = range(10)

participant1 = {
    'id': 'xxxx1',
    'capsules': {
        'week1': {'mon': 'MD', 'tue': 'MD', 'wed': 'MD', 'thu': 'MD', 'fri': 'MD', 'sat': 'MD'},
        'week2': {'mon': 'MD', 'tue': 'MD', 'wed': 'MD', 'thu': 'MD', 'fri': 'MD', 'sat': 'MD'}
    },
    'guesses': {
        'week1': {'mon': 'MD', 'tue': 'MD', 'wed': 'MD', 'thu': 'MD', 'fri': 'MD', 'sat': 'MD'},
        'week2': {'mon': 'MD', 'tue': 'MD', 'wed': 'MD', 'thu': 'MD', 'fri': 'MD', 'sat': 'MD'},
    },
    'drug': 'LSD',
    'drug_category': 1,
    'dose': 9.0
}
participant1_true = {
    'capsules_list': ['MD']*6 + ['NC'] + ['MD']*6 + ['NC']*15,
    'guesses_list': ['MD']*6 + ['NC'] + ['MD']*6 + ['NC']*15,
    'MD_days': [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12],
    'days_since_last_MD': lambda x: [x] + [1]*5 + [2] + [1]*5,
    'guess_corrects': [True]*12,
    'participant_data': lambda x: [(True, x)] + [(True, 1)]*5 + [(True, 2)] + [(True, 1)]*5
}

participant2 = {
    'id': 'xxxx2',
    'capsules': {
        'week1': {'mon': 'PL', 'tue': 'PL', 'wed': 'NC', 'thu': 'PL', 'fri': 'PL', 'sat': 'PL'},
        'week2': {'mon': 'PL', 'tue': 'PL', 'wed': 'PL', 'thu': 'PL', 'fri': 'NC', 'sat': 'PL'}
    },
    'guesses': {
        'week1': {'mon': 'PL', 'tue': 'MD', 'wed': 'NC', 'thu': 'MD', 'fri': 'MD', 'sat': 'MD'},
        'week2': {'mon': 'MD', 'tue': 'MD', 'wed': 'MD', 'thu': 'MD', 'fri': 'NC', 'sat': 'MD'},
    },
    'drug': '1p-LSD',
    'drug_category': 1,
    'dose': 8.0
}
participant2_true = {
    'capsules_list': ['PL']*2 + ['NC'] + ['PL']*3 + ['NC'] + ['PL']*4 + ['NC', 'PL'] + ['NC']*15,
    'guesses_list': ['PL', 'MD', 'NC'] + ['MD']*3 + ['NC'] + ['MD']*4 + ['NC', 'MD'] + ['NC']*15,
    'MD_days': [],
    'days_since_last_MD': lambda x: [],
    'guess_corrects': [],
    'participant_data': lambda x: []
}

participant3 = {
    'id': 'xxxx3',
    'capsules': {
        'week1': {'mon': 'NC', 'tue': 'MD', 'wed': 'PL', 'thu': 'MD', 'fri': 'PL', 'sat': 'PL'},
        'week2': {'mon': 'PL', 'tue': 'MD', 'wed': 'NC', 'thu': 'PL', 'fri': 'PL', 'sat': 'PL'}
    },
    'guesses': {
        'week1': {'mon': 'NC', 'tue': 'MD', 'wed': 'MD', 'thu': 'PL', 'fri': 'PL', 'sat': 'PL'},
        'week2': {'mon': 'MD', 'tue': 'PL', 'wed': 'NC', 'thu': 'MD', 'fri': 'MD', 'sat': 'MD'},
    },
    'drug': 'LSD',
    'drug_category': 1,
    'dose': 10.0
}
participant3_true = {
    'capsules_list': ['NC', 'MD', 'PL', 'MD', 'PL', 'PL', 'NC'] + ['PL', 'MD', 'NC'] + ['PL']*3 + ['NC']*15,
    'guesses_list': ['NC'] + ['MD']*2 + ['PL']*3 + ['NC'] + ['MD', 'PL', 'NC'] + ['MD']*3 + ['NC']*15,
    'MD_days': [1, 3, 8],
    'days_since_last_MD': lambda x: [x] + [2, 5],
    'guess_corrects': [True, False, False],
    'participant_data': lambda x: [(True, x), (False, 2), (False, 5)]
}

participant4 = {
    'id': 'xxxx4',
    'capsules': {
        'week1': {'mon': 'PL', 'tue': 'PL', 'wed': 'PL', 'thu': 'PL', 'fri': 'PL', 'sat': 'PL'},
        'week2': {'mon': 'PL', 'tue': 'MD', 'wed': 'MD', 'thu': 'PL', 'fri': 'MD', 'sat': 'MD'}
    },
    'guesses': {
        'week1': {'mon': 'PL', 'tue': 'PL', 'wed': 'MD', 'thu': 'MD', 'fri': 'MD', 'sat': 'PL'},
        'week2': {'mon': 'MD', 'tue': 'MD', 'wed': 'MD', 'thu': 'MD', 'fri': 'PL', 'sat': 'PL'},
    },
    'drug': 'LSD',
    'drug_category': 1,
    'dose': 10.0
}
participant4_true = {
    'capsules_list': ['PL']*6 + ['NC'] + ['PL'] + ['MD']*2 + ['PL'] + ['MD']*2 + ['NC']*15,
    'guesses_list': ['PL']*2 + ['MD']*3 + ['PL'] + ['NC'] + ['MD']*4 + ['PL']*2 + ['NC']*15,
    'MD_days': [8, 9, 11, 12],
    'days_since_last_MD': lambda x: [x] + [1, 2, 1],
    'guess_corrects': [True, True, False, False],
    'participant_data': lambda x: [(True, x), (True, 1), (False, 2), (False, 1)]
}

data = [participant1, participant2, participant3, participant4]

all_guess_data_sorted_true = {
    0: {
        0: {'correct_guess_probability': 1.0, 'nr_guesses': 3.0, 'nr_correct_guesses': 3.0},
        1: {'correct_guess_probability': 11./12., 'nr_guesses': 12.0, 'nr_correct_guesses': 11.0},
        2: {'correct_guess_probability': 1./3., 'nr_guesses': 3.0, 'nr_correct_guesses': 1.0},
        3: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        4: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        5: {'correct_guess_probability': 0., 'nr_guesses': 1.0, 'nr_correct_guesses': 0.0}
    },
    1: {
        0: {'correct_guess_probability': 0.0, 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        1: {'correct_guess_probability': 14./15., 'nr_guesses': 15.0, 'nr_correct_guesses': 14.0},
        2: {'correct_guess_probability': 1./3., 'nr_guesses': 3.0, 'nr_correct_guesses': 1.0},
        3: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        4: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        5: {'correct_guess_probability': 0., 'nr_guesses': 1.0, 'nr_correct_guesses': 0.0}
    },
    2: {
        0: {'correct_guess_probability': 0.0, 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        1: {'correct_guess_probability': 11./12., 'nr_guesses': 12.0, 'nr_correct_guesses': 11.0},
        2: {'correct_guess_probability': 4./6., 'nr_guesses': 6.0, 'nr_correct_guesses': 4.0},
        3: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        4: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        5: {'correct_guess_probability': 0., 'nr_guesses': 1.0, 'nr_correct_guesses': 0.0}
    },
    3: {
        0: {'correct_guess_probability': 0.0, 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        1: {'correct_guess_probability': 11./12., 'nr_guesses': 12.0, 'nr_correct_guesses': 11.0},
        2: {'correct_guess_probability': 1./3., 'nr_guesses': 3.0, 'nr_correct_guesses': 1.0},
        3: {'correct_guess_probability': 1., 'nr_guesses': 3.0, 'nr_correct_guesses': 3.0},
        4: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        5: {'correct_guess_probability': 0., 'nr_guesses': 1.0, 'nr_correct_guesses': 0.0}
    },
    4: {
        0: {'correct_guess_probability': 0.0, 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        1: {'correct_guess_probability': 11./12., 'nr_guesses': 12.0, 'nr_correct_guesses': 11.0},
        2: {'correct_guess_probability': 1./3., 'nr_guesses': 3.0, 'nr_correct_guesses': 1.0},
        3: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        4: {'correct_guess_probability': 1., 'nr_guesses': 3.0, 'nr_correct_guesses': 3.0},
        5: {'correct_guess_probability': 0., 'nr_guesses': 1.0, 'nr_correct_guesses': 0.0}
    },
    5: {
        0: {'correct_guess_probability': 0.0, 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        1: {'correct_guess_probability': 11./12., 'nr_guesses': 12.0, 'nr_correct_guesses': 11.0},
        2: {'correct_guess_probability': 1./3., 'nr_guesses': 3.0, 'nr_correct_guesses': 1.0},
        3: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        4: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        5: {'correct_guess_probability': 3./4., 'nr_guesses': 4.0, 'nr_correct_guesses': 3.0}
    },
    6: {
        0: {'correct_guess_probability': 0.0, 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        1: {'correct_guess_probability': 11./12., 'nr_guesses': 12.0, 'nr_correct_guesses': 11.0},
        2: {'correct_guess_probability': 1./3., 'nr_guesses': 3.0, 'nr_correct_guesses': 1.0},
        3: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        4: {'correct_guess_probability': 0., 'nr_guesses': 0.0, 'nr_correct_guesses': 0.0},
        5: {'correct_guess_probability': 0., 'nr_guesses': 1.0, 'nr_correct_guesses': 0.0},
        6: {'correct_guess_probability': 1., 'nr_guesses': 3.0, 'nr_correct_guesses': 3.0}
    }
}

result_keys = ['correct_guess_probability', 'nr_guesses', 'nr_correct_guesses']

result_list_true0 = {
    'correct_guess_probability': [1., 11./12., 1./3., 0., 0., 0.],
    'nr_guesses': [3., 12., 3., 0., 0., 1.],
    'nr_correct_guesses': [3., 11., 1., 0., 0., 0.],
}


# class for running tests

class TestDataProcessing:
    def test_schedule_to_list(self):
        f = data_processing.schedule_to_list

        capsules_list1 = f(participant1['capsules'])
        capsules_list2 = f(participant2['capsules'])
        capsules_list3 = f(participant3['capsules'])
        capsules_list4 = f(participant4['capsules'])

        guesses_list1 = f(participant1['guesses'])
        guesses_list2 = f(participant2['guesses'])
        guesses_list3 = f(participant3['guesses'])
        guesses_list4 = f(participant4['guesses'])

        assert capsules_list1 == participant1_true['capsules_list']
        assert capsules_list2 == participant2_true['capsules_list']
        assert capsules_list3 == participant3_true['capsules_list']
        assert capsules_list4 == participant4_true['capsules_list']

        assert guesses_list1 == participant1_true['guesses_list']
        assert guesses_list2 == participant2_true['guesses_list']
        assert guesses_list3 == participant3_true['guesses_list']
        assert guesses_list4 == participant4_true['guesses_list']

    def test_get_MD_days(self):
        f = data_processing.get_MD_days

        MD_days1 = f(participant1_true['capsules_list'])
        MD_days2 = f(participant2_true['capsules_list'])
        MD_days3 = f(participant3_true['capsules_list'])
        MD_days4 = f(participant4_true['capsules_list'])

        assert MD_days1 == participant1_true['MD_days']
        assert MD_days2 == participant2_true['MD_days']
        assert MD_days3 == participant3_true['MD_days']
        assert MD_days4 == participant4_true['MD_days']

    def test_get_days_since_last_MD(self):
        f = data_processing.get_days_since_last_MD

        for first_MD_days in first_MD_days_range:
            days_since_last_MD1 = f(participant1_true['MD_days'], first_MD_days)
            days_since_last_MD2 = f(participant2_true['MD_days'], first_MD_days)
            days_since_last_MD3 = f(participant3_true['MD_days'], first_MD_days)
            days_since_last_MD4 = f(participant4_true['MD_days'], first_MD_days)

            assert days_since_last_MD1 == participant1_true['days_since_last_MD'](first_MD_days)
            assert days_since_last_MD2 == participant2_true['days_since_last_MD'](first_MD_days)
            assert days_since_last_MD3 == participant3_true['days_since_last_MD'](first_MD_days)
            assert days_since_last_MD4 == participant4_true['days_since_last_MD'](first_MD_days)

    def test_get_guess_corrects(self):
        f = data_processing.get_guess_corrects

        guess_corrects1 = f(participant1_true['guesses_list'], participant1_true['MD_days'])
        guess_corrects2 = f(participant2_true['guesses_list'], participant2_true['MD_days'])
        guess_corrects3 = f(participant3_true['guesses_list'], participant3_true['MD_days'])
        guess_corrects4 = f(participant4_true['guesses_list'], participant4_true['MD_days'])

        assert guess_corrects1 == participant1_true['guess_corrects']
        assert guess_corrects2 == participant2_true['guess_corrects']
        assert guess_corrects3 == participant3_true['guess_corrects']
        assert guess_corrects4 == participant4_true['guess_corrects']

    def test_get_participant_data(self):
        f = data_processing.get_participant_data
        
        for first_MD_days in first_MD_days_range:
            participant_data1 = f(participant1, first_MD_days)
            participant_data2 = f(participant2, first_MD_days)
            participant_data3 = f(participant3, first_MD_days)
            participant_data4 = f(participant4, first_MD_days)

            assert participant_data1 == participant1_true['participant_data'](first_MD_days)
            assert participant_data2 == participant2_true['participant_data'](first_MD_days)
            assert participant_data3 == participant3_true['participant_data'](first_MD_days)
            assert participant_data4 == participant4_true['participant_data'](first_MD_days)

    def test_get_all_data(self):
        f = data_processing.get_all_data
        
        for first_MD_days in range(7):
            all_guess_data_sorted = f(data, first_MD_days)

            assert all_guess_data_sorted == all_guess_data_sorted_true[first_MD_days]

    def test_make_value_list(self):
        f = data_processing.make_value_list

        # we only check first_MD_days = 0
        for key in result_keys:
            result_list = f(all_guess_data_sorted_true[0], key)

            assert result_list == result_list_true0[key]

