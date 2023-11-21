import pandas as pd 


def resample_time_series(data_frame:pd.DataFrame, value_column:str, time_column:str, time_window:str='D'):
    """
    Resample a time series DataFrame based on the desired time window.

    Parameters:
    - data_frame (pd.DataFrame): DataFrame containing the time series data.
    - time_column (str): Name of the column containing time information.
    - value_column (str): Name of the column containing the values.
    - time_window (str): Pandas offset alias for the desired time window
                        ('D' for daily, 'W' for weekly, 'M' for monthly, etc.).

    Returns:
    - pd.DataFrame: Resampled time series DataFrame.
    """

    df = data_frame.copy()

    # # Ensure the time column is in datetime format
    df[time_column] = pd.to_datetime(df[time_column])

    # # Set the time column as the DataFrame index
    df.set_index(time_column, inplace=True)

    # Resample the time series based on the specified time window
    if time_window == 'D':
        resampled_df = df[value_column]
        resampled_df.reset_index(inplace=True)
        return resampled_df
    
    resampled_df = df[value_column].resample(time_window).sum()

    # Convert the index to a column named 'date' and reset the index
    resampled_df = pd.DataFrame(resampled_df)
    resampled_df.reset_index(inplace=True)

    return resampled_df 

