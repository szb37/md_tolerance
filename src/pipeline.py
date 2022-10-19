from src.data_processing import get_all_data, make_value_list, filter_data, make_df, process_df
import src.folders as folders
import pandas as pd
import numpy as np
import json
import os


# Adjustable parameters
first_MD_days = 10 # as defined in protocol
nr_guesses_threshold = 1 # corresponds to keep all data; legacy parameter
include_PL=False

# Read data
with open(os.path.join(folders.safety_vault_dir, 'tolerance.json')) as json_file:
    data = json.load(json_file)


def get_data(first_MD_days=first_MD_days, nr_guesses_threshold=nr_guesses_threshold, include_PL=include_PL, plot=False, return_keys=False):
    # Data processing
    all_guess_data_sorted = get_all_data(data, first_MD_days, include_PL=include_PL)
    filtered_data = filter_data(all_guess_data_sorted, nr_guesses_threshold)
    if plot:
        plot_data(filtered_data, include_PL)
    if return_keys:
        return get_filtered_keys(filtered_data)
    return filtered_data


def get_filtered_keys(filtered_data):
    k = make_value_list(filtered_data, 'key')
    return k


def plot_data(filtered_data, include_PL):
    # Data plotting
    p = make_value_list(filtered_data, 'correct_guess_probability')
    n = make_value_list(filtered_data, 'nr_guesses')
    k = make_value_list(filtered_data, 'key')
    if include_PL:
        bar_plot(k, p, 'Correct Guess Probability', xtitle='Nr days since last MD', ytitle='p')
    else:
        bar_plot(k, p, 'Correct MD Guess Probability', xtitle='Nr days since last MD', ytitle='p')
    bar_plot(k, n, 'Number of Guesses', xtitle='Nr days since last MD', ytitle='n')


def get_df_data(first_MD_days=first_MD_days, filter_list=None):
    # Turn data into df to prepare for analysis
    return make_df(data, first_MD_days, filter_list)


def prepare_df_data(first_MD_days=first_MD_days, nr_guesses_threshold=None, save_csv=False):
    # Prepare csv for data analysis
    if nr_guesses_threshold:
        filter_list = get_data(first_MD_days=first_MD_days, nr_guesses_threshold=nr_guesses_threshold, return_keys=True)
        df = get_df_data(first_MD_days, filter_list)
        df_dose = process_df(df, (save_csv, 'data/guess_dose_data_filtered.csv'))
    else:
        df = get_df_data(first_MD_days)
        df_dose = process_df(df, (save_csv, 'data/guess_dose_data.csv'))
    return df_dose
