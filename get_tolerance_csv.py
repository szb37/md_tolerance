"""
:Author: Balazs Szigeti <szb37@pm.me>
:Copyright: 2021, DrugNerdsLab
:License: MIT
"""

from src.pipeline import prepare_df_data as prepare_df_data
import src.folders as folders
import pandas as pd
import os

first_MD_days=10
nr_guesses_threshold=1

def get_tolerance(first_MD_days=first_MD_days):
    """ Controller to produce and save tolerance CSV """

    df = get_guess_accuracy_csv(first_MD_days=first_MD_days, nr_guesses_threshold=nr_guesses_threshold)
    df = add_covariates(df=df)
    df = clean_df(df=df)

    df_lsd = df.loc[df.drug_cat==1]
    df_shroom = df.loc[df.drug_cat==2]

    df.to_csv(os.path.join(folders.data_dir, 'tolerance_all_md2.csv'), index=False)
    df_lsd.to_csv(os.path.join(folders.data_dir, 'tolerance_lsd_md2.csv'), index=False)
    df_shroom.to_csv(os.path.join(folders.data_dir, 'tolerance_shroom_md2.csv'), index=False)

def get_guess_accuracy_csv(first_MD_days, nr_guesses_threshold):
    """ Get accuracy CSV from Stefan's code for further processing """

    df = prepare_df_data(
        first_MD_days=first_MD_days,
        nr_guesses_threshold=nr_guesses_threshold)

    # Rename and reorder columns for better expressiveness
    df = df.rename({
        'id': 'trial_id_str',
        'group': 'trial_id_int',
        'drugCategory': 'drug_cat',
        'daysSinceLastMD': 'days_since_last',
        'daysSinceStart': 'days_since_start',
        'acidDose':'acid_dose',
        'nrMD': 'n_MD', }, axis=1)
    df_temp=df.reindex(columns=[
        'trial_id_str',
        'trial_id_int',
        'drug',
        'drug_cat',
        'dose',
        'acid_dose',
        'isGuessCorrect',
        'isGuessCorrectInt',
        'days_since_last',
        'days_since_start',
        'n_MD',
    ])
    df = df_temp
    del df_temp

    return df

def add_covariates(df):
    """Add baseline covariates from mcrds_covs """

    df_covs = pd.read_csv(os.path.join(folders.safety_vault_dir, 'mcrds_covs.csv'))
    #df = pd.read_csv(os.path.join(folders.data_dir, 'guess_accuracy_temp_stage1.csv'))

    # Add empty covariate columns
    df_temp = df.assign(age=None)
    df = df_temp; del df_temp

    df_temp = df.assign(sex=None)
    df = df_temp; del df_temp

    df_temp = df.assign(education=None)
    df = df_temp; del df_temp

    df_temp = df.assign(psy_past=None)
    df = df_temp; del df_temp

    df_temp = df.assign(psy_now=None)
    df = df_temp; del df_temp

    df_temp = df.assign(suggestibility=None)
    df = df_temp; del df_temp

    df_temp = df.assign(expectation=None)
    df = df_temp; del df_temp

    df_temp = df.assign(n_micro_months=None)
    df = df_temp; del df_temp

    df_temp = df.assign(n_macro_exp=None)
    df = df_temp; del df_temp

    # Assign covariate values from mcrds_covs.csv
    for index, row in df_covs.iterrows():

        df.loc[df.trial_id_str==row.trial_id, 'age'] = row.age
        df.loc[df.trial_id_str==row.trial_id, 'sex'] = row.sex
        df.loc[df.trial_id_str==row.trial_id, 'education'] = row.education
        df.loc[df.trial_id_str==row.trial_id, 'psy_past'] = row.psy_past
        df.loc[df.trial_id_str==row.trial_id, 'psy_now'] = row.psy_now
        df.loc[df.trial_id_str==row.trial_id, 'suggestibility'] = row.suggestibility
        df.loc[df.trial_id_str==row.trial_id, 'expectation'] = row.expectation
        df.loc[df.trial_id_str==row.trial_id, 'n_micro_months'] = row.n_micro_months
        df.loc[df.trial_id_str==row.trial_id, 'n_macro_exp'] = row.n_macro_exp

    return df

def clean_df(df):
    """ Clean DF for R processing """

    df.dropna(inplace=True)

    # Fix column types
    df['trial_id_str'] = df['trial_id_str'].astype('str')
    df['trial_id_int'] = df['trial_id_int'].astype('int')
    df['drug'] = df['drug'].astype('str')
    df['drug_cat'] = df['drug_cat'].astype('int')
    df['dose'] = df['dose'].astype('float')
    df['acid_dose'] = df['acid_dose'].astype('float')
    df['isGuessCorrect'] = df['isGuessCorrect'].astype('bool')
    df['isGuessCorrectInt'] = df['isGuessCorrectInt'].astype('int')
    df['days_since_last'] = df['days_since_last'].astype('int')
    df['days_since_start'] = df['days_since_start'].astype('int')
    df['n_MD'] = df['n_MD'].astype('int')
    df['age'] = df['age'].astype('int')
    df['sex'] = df['sex'].astype('str')
    df['suggestibility'] = df['suggestibility'].astype('int')
    df['expectation'] = df['expectation'].astype('float')
    df['n_micro_months'] = df['n_micro_months'].astype('int')
    df['n_macro_exp'] = df['n_macro_exp'].astype('int')

    return df

if __name__ == '__main__':
    get_tolerance()
