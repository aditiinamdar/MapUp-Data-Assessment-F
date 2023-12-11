import pandas as pd
import networkx as nx
import numpy as np
from datetime import time, timedelta
df = pd.read_csv('G:\mapup_task\MapUp-Data-Assessment-F\datasets\dataset-3.csv')

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    #Creates a graph to represent toll locations and distances
    distance_graph = nx.Graph()
    #add edges and weights to the graph based on the data
    for i, elrow in df.iterrows():
        distance_graph.add_edge(elrow['id_start'], elrow['id_end'], weight=elrow['distance'])
    #calculates the shortest path distances between toll locations with help of floyd warshall algorithm
    distance_matrix = nx.floyd_warshall_numpy(distance_graph)
    distance_matrix_df = pd.DataFrame(distance_matrix, index=distance_graph.nodes, columns=distance_graph.nodes)
    #setting the diagonal values to 0
    for column in distance_matrix_df.columns :
        distance_matrix_df.loc[column, column] = 0
    #creating the symmetric matrix such that value of aij = aji
    distance_symmetric_matrix_df = (distance_matrix_df + distance_matrix_df.T) / 2
    return distance_symmetric_matrix_df

#print(calculate_distance_matrix(df))


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    #declares empty list to store data from matrix
    datalist= []
    df2 = calculate_distance_matrix(df)
    #extracts 'id_start', 'id_end' from columns & index
    df2.columns = pd.to_numeric(df2.columns, errors='coerce')
    df2.index = pd.to_numeric(df2.index, errors='coerce')
    for id_start, elrow in df2.iterrows():
        #converts 'distance' column to numeric type
        elrow = pd.to_numeric(elrow, errors='coerce')
        #creates combinations
        for id_end, distance in elrow.iteritems():
            if pd.notna(distance) and id_start != id_end:
                datalist.append([id_start, id_end, distance])
    #create a new DataFrame
    unrolled_df = pd.DataFrame(datalist, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    df2 = unroll_distance_matrix(df)
    #extracts rows based on reference_id
    reference_value_rows = df2[df2['id_start'] == reference_id]
    #calculates the average distance for reference_id
    avg_distance = reference_value_rows['distance'].mean()
    #calculate the 10% threshold range (including ceiling and floor)
    threshold = df2[(df2['distance'] >= (avg_distance - (avg_distance * 0.1))) & (df2['distance'] <= (avg_distance + (avg_distance * 0.1)))]
    #unique values from 'id_start' column 
    result_values_df = threshold['id_start'].unique()
    #sorts the values
    result_values_df.sort()
    return result_values_df

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    #taking dataframe from the second function
    df2 = unroll_distance_matrix(df)
    #creates rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    #adds columns & calculates the toll rate
    for vehicle_type, rate in rate_coefficients.items():
        df2[vehicle_type] = df2['distance'] * rate
    return df2

def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df