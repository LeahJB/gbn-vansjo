def bayes_net_predict(rfile_fpath, sd_fpath, year, chla_prev_summer, colour_prev_summer,
                      tp_prev_summer, wind_speed, rain, sigma):
    """ Make predictions given the evidence provided based on a pre-fitted
        Bayesian network. This function is just a thin "wrapper" around the
        R function named 'bayes_net_predict' in 'bayes_net_utils.R'.
        See also bayes_net_predict_operational.

        NOTE: 'bayes_net_utils.R' must be in the same folder as this file.

    Args:
        rfile_fpath:       Str. Filepath to fitted BNLearn network object (.rds file)
        sd_fpath:          Str. Filepath to csv containing standard deviation info from fitted BN
        year:              Int. Year for prediction
        chla_prevSummer:   Float. Chl-a measured from the previous summer  (mg/l)
        colour_prevSummer: Float. Colour measured from the previous summer (mg Pt/l)
        TP_prevSummer:     Float. Total P measured from the previous summer (mg/l)
        wind_speed:        Float. Predicted wind speed for season of interest (m/s)
        rain:              Float. Predicted precipitation for season of interest (mm)
        sigma:             Float. Standard deviation of the box cox transformed observations

    Returns:
        Dataframe with columns 'year', 'node', 'threshold', 'prob_below_threshold',
       'prob_above_threshold', 'expected_value', 'sd' (standard deviation)
    """
    import pandas as pd
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter

    # Load R script
    ro.r.source('bayes_net_utils.R')

    # Call R function with user-specified evidence
    res = ro.r['bayes_net_predict'](rfile_fpath, sd_fpath, year,
                                    chla_prev_summer, colour_prev_summer,
                                    tp_prev_summer, wind_speed, rain, sigma)

    # Convert back to Pandas df
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(res)

    # Add 'year' to results as unique identifier
    df['year'] = int(year)
    df.reset_index(drop=True, inplace=True)

    # Add predicted WFD class
    df['WFD_class'] = df[['threshold', 'expected_value']].apply(lambda x: discretize([x.threshold], x.expected_value), axis=1)

    return df


def bayes_net_predict_nomet(rfile_fpath, sd_fpath, year, chla_prev_summer,
                            colour_prev_summer, tp_prev_summer, sigma):
    """ Make predictions given the evidence provided based on a pre-fitted
        Bayesian network with no met nodes
        This function is just a thin "wrapper" around the R function named
        'bayes_net_predict_nomet' in 'bayes_net_utils.R'.
        See also bayes_net_predict_operational.

        NOTE: 'bayes_net_utils.R' must be in the same folder as this file.

    Args:
        rfile_fpath:       Str. Filepath to fitted BNLearn network object (.rds file)
        sd_fpath:          Str. Filepath to csv with standard deviations from fitted BN
        year:              Int. Year for prediction
        chla_prevSummer:   Float. Chl-a measured from the previous summer  (mg/l)
        colour_prevSummer: Float. Colour measured from the previous summer (mg Pt/l)
        TP_prevSummer:     Float. Total P measured from the previous summer (mg/l)
        sigma:             Float. Standard deviation of the box cox transformed observations

    Returns:
        Dataframe with columns 'year', 'node', 'threshold', 'prob_below_threshold',
       'prob_above_threshold', 'expected_value', 'sd' (standard deviation)
    """
    import pandas as pd
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter

    # Load R script
    ro.r.source('bayes_net_utils.R')

    # Call R function with user-specified evidence
    res = ro.r['bayes_net_predict_nomet'](rfile_fpath, sd_fpath, year,
                                          chla_prev_summer, colour_prev_summer,
                                          tp_prev_summer, sigma)

    # Convert back to Pandas df
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(res)

    # Add 'year' to results as unique identifier
    df['year'] = int(year)
    df.reset_index(drop=True, inplace=True)

    # Add predicted WFD class
    df['WFD_class'] = df[['threshold', 'expected_value']].apply(lambda x: discretize([x.threshold], x.expected_value), axis=1)

    return df


def bayes_net_predict_operational(rfile_fpath, year, chla_prev_summer, colour_prev_summer,
                                  tp_prev_summer, sigma):
    """ Make predictions given the evidence provided based on the pre-fitted
        Bayesian network.
        This function is just a thin "wrapper" around the R function named
        'bayes_net_predict_operational' in 'bayes_net_utils.R'.

        Very similar to bayes_net_predict, but:
        - Drop met nodes for operational forecast
        - Only forecast for TP, colour and cyano (not chla)).
        - Remove standard deviations which were in bayes_net_predict function

        NOTE: 'bayes_net_utils.R' must be in the same folder as this file.

    Args:
        rfile_fpath:       Str. Filepath to fitted BNLearn network object (.rds file)
        year:              Int. Year for prediction
        chla_prevSummer:   Float. Chl-a measured from the previous summer  (mg/l)
        colour_prevSummer: Float. Colour measured from the previous summer (mg Pt/l)
        TP_prevSummer:     Float. Total P measured from the previous summer (mg/l)
        sigma:             Float. Standard deviation of the box cox transformed observations

    Returns:
        Dataframe with columns 'year', 'node', 'threshold', 'prob_below_threshold',
       'prob_above_threshold', 'expected_value'
    """
    import pandas as pd
    import rpy2.robjects as ro
    from rpy2.robjects.packages import importr
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter

    # Load R script
    ro.r.source('bayes_net_utils.R')

    # Call R function with user-specified evidence
    res = ro.r['bayes_net_predict_operational'](rfile_fpath, year, chla_prev_summer,
                                                colour_prev_summer,
                                                tp_prev_summer, sigma)

    # Convert back to Pandas df
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(res)

    # Add 'year' to results as unique identifier
    df['year'] = int(year)
    df.reset_index(drop=True, inplace=True)

    # Add predicted WFD class
    df['WFD_class'] = df[['threshold','expected_value']].apply(lambda x: discretize([x.threshold], x.expected_value), axis=1)

    return df


def classification_error(obs, pred):
    """
    Calculate classification error, the proportion of time the model predicted
    the class correctly

    Input:
        obs: series of observed classes, numeric format
        pred: series of predicted classes (aligned to obs), numeric format
    Output:
        Classification error (float)
    """
    import pandas as pd
    import numpy as np

    assert len(obs) == len(pred), "observed and predicted series have different lengths"

    # Were observed and predictions in the same class? 'right' col is a boolean,
    # 1=Yes the same, 0=no different
    right = np.where((obs == pred), 1, 0)

    classification_error = 1 - (right.sum() / len(right))

    return classification_error


def daily_to_summer_season(daily_df, agg_method_dict, replace_zero_with_NaN_li=[],
                           return_just_summer=True):
    """
    Take a dataframe with daily frequency data, and aggregate it to seasonal
    (6 monthly), just picking results for the summer (May-Oct) season.
    Input:
    - dataframe of daily data
    - dictionary of aggregation method functions
      (e.g. np.nansum, with a key for each column in daily_df)
      - replace_zero_with_NaN_list: list of column names to replace zeros with NaNs
    - return_just_summer (default True): return seasonally-aggregated data just for
      the 6 month growing season ('summer'), or also for the winter 6 months?

    Returns: dataframe of seasonally-aggregated data
    """
    import pandas as pd
    import numpy as np

    # Turn off "Setting with copy" warning, which is returning a false positive
    pd.options.mode.chained_assignment = None  # default='warn'

    # Drop any dictionary keys that aren't needed
    for key in list(agg_method_dict.keys()):
        if key not in daily_df.columns:
            del agg_method_dict[key]

    # Resample ('Q' for quarterly, '-month' for month to end in). If season
    # function changes, need to change this too
    # Returned df: winter values are stored against the year that corresponds
    # to the second half of the winter (e.g. Nov 99-Apr 2000 stored as 2000).
    # The shift is needed because otherwise the last day of the period
    # (corresponding to the label) is omitted. Checked manually and right.
    season_df = daily_df.shift(periods=-1).resample('2Q-Apr', closed='left').agg(agg_method_dict)

    # np.nansum isn't working as I expected, with sums of 0 when all values
    # are NaN. Replace these with NaNs.
    for col in replace_zero_with_NaN_li:
        season_df.loc[season_df[col] == 0.0, col] = np.NaN

    # Remove frequncy info from index so plotting works right
    season_df.index.freq = None

    # Add season info to the dataframe, i.e. a column with either "summer"
    # or "winter"
    def season(x):
        """Input month number, and return the season it corresponds to
        """
        if x in [11, 12, 1, 2, 3, 4]:
            return 'wint'
        else:
            return 'summ'

    season_df['Season'] = season_df.index.month.map(season)

    if return_just_summer is True:
        # Remove winter rows (a bit long-winded, but works)
        summer_df = season_df.loc[season_df['Season'] == 'summ']
        summer_df.drop('Season', axis=1, inplace=True)

        # Reindex
        summer_df['year'] = summer_df.index.year
        summer_df.set_index('year', inplace=True)

        return summer_df

    else:
        return season_df


def discretize(thresholds, value):
    """
    Function to compare a number to a list of thresholds and categorise accordingly.
    E.g. to apply row-wise down a df to convert from continuous to categorical data.
    Input:
        thresholds: list of class boundaries that define classes of interest
        value: float to be compared to the thresholds

    Returns: class the value lies in. Classes are defined in factor_li_dict
    within function according to number of thresholds
    (max 2 class boundaries (thresholds) supported at present)

    e.g. of usage:
    # E.g. 1:
    bound_dict = {'TP':[29.5]}
    for col in continuous_df.columns:
        disc_df[col] = continuous_df[col].apply(lambda x: discretize(bound_dict['TP'], x))
    # E.g. 2:
    df['WFD_class'] = df[['threshold','expected_value']].apply(lambda x: discretize([x.threshold], x.expected_value), axis=1)
    """
    import numpy as np

    if np.isnan(value):
        return np.NaN

    factor_li_dict = {2: [0, 1],
                      3: [0, 1, 2]}

    n_classes = len(thresholds) + 1

    for i, boundary in enumerate(thresholds):

        if value < boundary:
            return factor_li_dict[n_classes][i]
            break  # Break out of loop

        # If we're up to the last class boundary, and the value is bigger than it,
        # value is in the uppermost class
        if i + 1 == len(thresholds) and value >= boundary:
            return factor_li_dict[n_classes][i+1]