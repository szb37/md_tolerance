import pandas as pd
import numpy as np

# Functions for data processing
include_PL=False

####### Helper functions #######
def schedule_to_list(schedule):
    """Turns a schedule (dictionary) into a list"""

    schedule_list = list()
    weeks = ['week1', 'week2', 'week3', 'week4']
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    for week in weeks:
        if week in schedule.keys():
            for day in days:
                if day in schedule[week].keys():
                    schedule_list.append(schedule[week][day])
                else:
                    schedule_list.append('NC')
        else:
            schedule_list += ['NC']*7

    return schedule_list

def get_days(schedule_list, drug):
    """Returns a list of indexes when drug occured in schedule_list"""

    days = list()

    for day, s in enumerate(schedule_list):
        if s == drug:
            days.append(day)

    return days

def get_days_since_last_MD(days, days_type, first_MD_days=7, MD_days=None):
    """Finds nr of days since last MD using the MD_days list"""

    days_since_last_MD = list()

    if days_type == 'MD':
        for i, day in enumerate(days):
            if i == 0:
                days_since_last_MD.append(first_MD_days)
            else:
                days_since_last_MD.append(day-days[i-1])
    elif days_type == 'PL':
        if MD_days is not None and len(MD_days) > 0:
            for day in days:
                # filter MD_days by <day and take max
                MD_days_before = list(filter(lambda x: x < day, MD_days))
                if len(MD_days_before) == 0:
                    continue
                MD_day_before = max(MD_days_before)
                days_since_last_MD.append(day-MD_day_before)

    return days_since_last_MD

def get_guess_corrects(guesses_list, days, drug):
    """Returns a list of booleans indicating if guess was correct
       for all days"""

    guess_corrects = list()

    for day in days:
        guessed_correctly = guesses_list[day] == drug
        guess_corrects.append(guessed_correctly)

    return guess_corrects

def get_participant_data(data, first_MD_days, include_PL=include_PL, full=False):
    """Returns a list of tuples, where each tuple indicateds the correctness
       of guess and the nr of days since last MD for each time the
       participant MD"""

    capsules_list = schedule_to_list(data['capsules'])
    guesses_list = schedule_to_list(data['guesses'])

    MD_days = get_days(capsules_list, 'MD')
    PL_days = get_days(capsules_list, 'PL')
    days_since_last_MD = get_days_since_last_MD(MD_days, 'MD', first_MD_days=first_MD_days)
    PL_days_since_last_MD = get_days_since_last_MD(PL_days, 'PL', MD_days=MD_days)

    guess_corrects = get_guess_corrects(guesses_list, MD_days, 'MD')
    PL_guess_corrects = get_guess_corrects(guesses_list, PL_days, 'PL')

    if full:
        # TODO: if include_PL then add it to data
        n = len(guess_corrects)
        id_list = [data['id']]*n
        drug_list = [data['drug']]*n
        drug_category_list = [data['drug_category']]*n
        dose_list = [data['dose']]*n
        nr_MD = list(range(n))
        participant_data = list(zip(id_list, drug_list, drug_category_list, dose_list, guess_corrects, days_since_last_MD, MD_days, nr_MD))
        participant_data = [list(t) for t in participant_data]
    else:
        if include_PL:
            guess_corrects += PL_guess_corrects
            days_since_last_MD += PL_days_since_last_MD
        participant_data = list(zip(guess_corrects, days_since_last_MD))

    return participant_data

def convert_dose(dose, category):
    # convert shroom dosage to LSD dosage
    # 0.1g of dried mushroom ~4.6µg LSD (Szigeti et al., 2021)
    if category == 1:
        return dose
    elif category == 2:
        return (dose*4.6)/100000
    else:
        return np.nan

def factor(var):
    # make categorical values
    var_set = set(var)
    var_set = {x: y for x, y in [pair for pair in zip(var_set, range(len(var_set)))]}
    return [var_set[x] for x in var]


####### Main functions #######
def get_all_data(data, first_MD_days, include_PL=include_PL):
    """Returns a dictionary with the keys representing the nr of days since
       last MD and the values being a dictionary with the following data:
       correct_guess_probability, nr_guesses, nr_correct_guesses"""

    # list of tuples (guess_correct: bool, nr_days_since_last_MD: int)
    # to gather all guess data from MD subjects
    all_dose_data = list()

    # dictionary with int keys representing nr days since last MD
    # and values being dictionary with data_keys
    all_guess_data_sorted = dict()
    data_keys = ['correct_guess_probability', 'nr_guesses', 'nr_correct_guesses']
    data_vals_init = [0., 0., 0.]

    # gather all participants data and add to all_dose_data list
    for participant_data in data:
        all_dose_data += get_participant_data(participant_data, first_MD_days, include_PL=include_PL)

    # maximum nr_days_since_last_MD of all participants
    max_break = max(all_dose_data, key = lambda i : i[1])[1]

    # populate all_guess_data_sorted with init vals
    for break_day in range(max_break+1):
        init_data_dict = dict(zip(data_keys, data_vals_init))
        all_guess_data_sorted[break_day] = init_data_dict

    # loop over all_dose_data and add to guesses
    for guess_correct, nr_days_since_last_MD in all_dose_data:
        all_guess_data_sorted[nr_days_since_last_MD]['nr_guesses'] += 1
        if guess_correct:
            all_guess_data_sorted[nr_days_since_last_MD]['nr_correct_guesses'] += 1

    # compute correct_guess_probability for each entry in all_dose_data_sorted
    for break_day in all_guess_data_sorted:
        nr_correct_guesses = all_guess_data_sorted[break_day]['nr_correct_guesses']
        nr_guesses = all_guess_data_sorted[break_day]['nr_guesses']
        if nr_guesses != 0:
            correct_guess_probability = nr_correct_guesses/nr_guesses
            all_guess_data_sorted[break_day]['correct_guess_probability'] = correct_guess_probability

    return all_guess_data_sorted

def make_value_list(guess_data, value):
    p_list = list()

    for key in guess_data:
        if value == 'key':
            p_list.append(key)
        else:
            p_list.append(guess_data[key][value])

    return p_list

def filter_data(data, nr_guesses_threshold):
    """Gets rid of values whose nr_guesses are below the threshold. Returns filtered data."""
    filtered_data = dict()

    for k in data:
        if data[k]['nr_guesses'] >= nr_guesses_threshold:
            filtered_data[k] = data[k]

    return filtered_data

def make_df(data, first_MD_days, filter_list):
    """Returns a pandas DataFrame with the following columns: id, isGuessCorrect,
       daysSinceLastMD, drug, drugCategory, dose, daysSinceStart"""

    all_dose_data = list()

    # gather all participants data and add to all_dose_data list
    for participant_data in data:
        all_dose_data += get_participant_data(participant_data, first_MD_days, full=True)

    df = pd.DataFrame(all_dose_data, columns=['id', 'drug', 'drugCategory', 'dose', 'isGuessCorrect', 'daysSinceLastMD', 'daysSinceStart', 'nrMD'])

    if filter_list:
        boolean_series = df['daysSinceLastMD'].isin(filter_list)
        df = df[boolean_series]

    return df

def process_df(df, save_csv=(False, None)):
    # pre-process dataframe and potentially save as csv

    acid_dose_list = list()
    for _, row in df.iterrows():
        new_dose = convert_dose(row['dose'], row['drugCategory'])
        acid_dose_list.append(new_dose)

    df['acidDose'] = acid_dose_list

    df['group'] = df[['id']].apply(factor)

    df['isGuessCorrectInt'] = [int(b) for b in list(df['isGuessCorrect'])]

    df_dose = df.dropna(inplace=False)

    if save_csv[0]:
        df_dose.to_csv(save_csv[1], index=False)

    return df_dose
