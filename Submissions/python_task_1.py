import pandas as pd

#creating dataframe of dataset-1
df = pd.read_csv('G:\mapup_task\MapUp-Data-Assessment-F\datasets\dataset-1.csv')
#creating dataframe of dataset-2
dfs = pd.read_csv('G:\mapup_task\MapUp-Data-Assessment-F\datasets\dataset-2.csv')

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
   
   
    """Creates a spreadsheet-style pivot table as a DataFrame Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively."""
    car_matrix_df = df.pivot_table(index='id_1', columns='id_2', values='car', aggfunc='first', fill_value=0)
    #setting the diagonal values to zero
    for column in car_matrix_df.columns :
        car_matrix_df.loc[column, column] = 0
    return car_matrix_df

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    
    #creates new column as car_types where distinguishes the car types based on range mentioned
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=('low', 'medium', 'high'), right=False)
    #counts car_types 
    count_types = df['car_type'].value_counts().to_dict()
    #sorts the data
    count_types = dict(sorted(count_types.items()))
    return count_types

def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    #calculate mean value with help of aggregate function mean()
    mean_value = df['bus'].mean()
    #creates list based on the condition given that value should be greater than twice of mean
    indexes = df[df['bus'] > 2 * mean_value].index.tolist()
    #sorts the list
    indexes.sort()
    return indexes
   
def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    
    #split the data with help of groupby function by the 'route' column and then calculating the mean of the 'truck' column for each group
    data_of_truck = df.groupby('route')['truck'].mean().reset_index()
    #storing values greater than 7 only
    data_of_truck= data_of_truck[data_of_truck['truck'] > 7]
    #converting dataframe to list and sorting it
    list_sorted_routes = sorted(data_of_truck['route'].tolist())
    return list_sorted_routes

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    #taking matrix from function one
    car_matrix = generate_car_matrix(df)
    #using lambda function to calculate the condition given
    matrix = car_matrix.applymap(lambda var : var * 0.75 if var > 20 else var * 1.25)
    matrix = matrix.round(1)
    return matrix

def time_check(dfs) :
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
   
    #combining the start date and time into new column start_DateTime
    dfs['start_DateTime'] = pd.to_datetime(dfs['startDay'].astype(str) + ' ' + dfs['startTime'].astype(str),errors = 'coerce')
    #combining the end date and time into new column end_DateTime
    dfs['end_DateTime'] = pd.to_datetime(dfs['endDay'].astype(str) + ' ' + dfs['endTime'].astype(str),errors = 'coerce')
    #using lambda function to determine if the maximum time difference between 'end_DateTime' and 'start_DateTime' is at least 7 days, and if the start and end times cover a full 24-hour period from midnight to 11:59:59 PM.
    #grouping based on id and id_2
    check_time = dfs.groupby(['id', 'id_2']).apply(lambda check1: (
      (check1['end_DateTime'].max() - check1['start_DateTime'].min()).total_seconds()>= 7 * 24 * 3600 and
        check1['start_DateTime'].min().time() == pd.Timestamp('00:00:00').time() and
        check1['end_DateTime'].max().time() == pd.Timestamp('23:59:59').time()
    ))
    return check_time
    
