
# Save DataFrame to pickle file
import pandas as pd
from sklearn.preprocessing import LabelEncoder

random_state = 42




def save_dataframe_to_pickle(df, file_path):
    """
    Save a pandas DataFrame to a pickle file
    
    Args:
        df (pandas.DataFrame): DataFrame to save
        file_path (str): Path where the pickle file will be saved
    """
    try:
        df.to_pickle(file_path)
        print(f"DataFrame successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving DataFrame: {e}")

# Read DataFrame from pickle file
def read_dataframe_from_pickle(file_path):
    """
    Read a pandas DataFrame from a pickle file
    
    Args:
        file_path (str): Path to the pickle file
        
    Returns:
        pandas.DataFrame: DataFrame loaded from the pickle file
    """
    try:
        df = pd.read_pickle(file_path)
        print(f"DataFrame successfully loaded from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading DataFrame: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    
def collect_relevant_data(gene_exp_df_bkp:pd.DataFrame ,label_df_bkp:pd.DataFrame ):
    gene_exp_df = gene_exp_df_bkp.copy()
    label_df = label_df_bkp.copy()
    relevant_df = gene_exp_df.loc[label_df.case_id.tolist()] # filetering out the available_subset 
    label_df.set_index(label_df["case_id"],inplace=True,drop=True)
    sorted_labels = label_df["tumour_site"].sort_index()
    sorted_gene_exp_df = relevant_df.sort_index()
    del gene_exp_df,label_df
    return sorted_gene_exp_df,sorted_labels

def remove_low_frequency_labels(label_df, threshold, column_name="tumour_site"):
    # Handle DataFrame input
    if isinstance(label_df, pd.DataFrame):
        if column_name is None:
            raise ValueError("column_name must be specified when input is a DataFrame")
        labels = label_df[column_name]
    else:
        labels = label_df
    
    # Count label frequencies and filter
    value_counts = labels.value_counts()
    high_freq_labels = value_counts[value_counts > threshold].index
    
    # Apply filtering
    mask = labels.isin(high_freq_labels)
    filtered = labels[mask]
    
    # Return same type as input
    if isinstance(label_df, pd.DataFrame):
        return label_df[mask]
    return filtered

def encode_labels(label_series):
    # Initialize the encoder
    label_encoder = LabelEncoder()
    # Fit and transform the labels
    encoded_labels = label_encoder.fit_transform(label_series)
    return encoded_labels, label_encoder

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))