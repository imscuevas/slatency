import pandas as pd
import numpy as np
import argparse
import json
import sys # For sys.exit

def calculate_derived_timings(df):
    """
    Calculates derived timing metrics in milliseconds and adds them as new columns.
    Assumes input columns from the DataFrame are already in milliseconds.
    """
    # Time to connect = connectTime_ms - namelookupTime_ms
    if 'connectTime_ms' in df.columns and 'namelookupTime_ms' in df.columns:
        df['time_to_connect_ms'] = df['connectTime_ms'] - df['namelookupTime_ms']
        # Ensure non-negative, as namelookup can sometimes be slightly larger due to resolution or system effects
        df.loc[df['time_to_connect_ms'] < 0, 'time_to_connect_ms'] = 0.0


    # Time to TLS = appconnectTime_ms - connectTime_ms
    # appconnectTime_ms is 0 for HTTP or if SSL negotiation didn't happen/complete
    if 'appconnectTime_ms' in df.columns and 'connectTime_ms' in df.columns:
        df['time_to_tls_ms'] = df['appconnectTime_ms'] - df['connectTime_ms']
        df.loc[df['appconnectTime_ms'] == 0, 'time_to_tls_ms'] = 0.0 # If no appconnect, TLS time is 0
        df.loc[df['time_to_tls_ms'] < 0, 'time_to_tls_ms'] = 0.0


    # Time to first byte setup (TTFB setup) = pretransferTime_ms - (appconnectTime_ms or connectTime_ms)
    if 'pretransferTime_ms' in df.columns:
        base_for_ttfb_setup_ms = np.where(df['appconnectTime_ms'] > 0, df['appconnectTime_ms'], df.get('connectTime_ms', 0.0))
        df['ttfb_setup_ms'] = df['pretransferTime_ms'] - base_for_ttfb_setup_ms
        df.loc[df['ttfb_setup_ms'] < 0, 'ttfb_setup_ms'] = 0.0


    # Server processing time = startTransferTime_ms - pretransferTime_ms
    if 'startTransferTime_ms' in df.columns and 'pretransferTime_ms' in df.columns:
        df['server_processing_ms'] = df['startTransferTime_ms'] - df['pretransferTime_ms']
        df.loc[df['server_processing_ms'] < 0, 'server_processing_ms'] = 0.0

    # Response download time = totalTime_ms - startTransferTime_ms
    if 'totalTime_ms' in df.columns and 'startTransferTime_ms' in df.columns:
        df['response_download_ms'] = df['totalTime_ms'] - df['startTransferTime_ms']
        df.loc[df['response_download_ms'] < 0, 'response_download_ms'] = 0.0

    return df

def print_statistics(series, metric_name):
    """Prints common statistics for a pandas Series."""
    if series.empty or series.isnull().all():
        print(f"  No valid data for {metric_name} to calculate statistics.")
        return
    
    # Ensure series is numeric and drop NaNs for calculations
    numeric_series = pd.to_numeric(series, errors='coerce').dropna()
    if numeric_series.empty:
        print(f"  No numeric data for {metric_name} after coercion.")
        return

    print(f"  {metric_name}:")
    print(f"    Count:  {numeric_series.count()}")
    print(f"    Mean:   {numeric_series.mean():.3f} ms")
    print(f"    Median: {numeric_series.median():.3f} ms")
    print(f"    StdDev: {numeric_series.std():.3f} ms")
    print(f"    Min:    {numeric_series.min():.3f} ms")
    print(f"    Max:    {numeric_series.max():.3f} ms")
    print(f"    P50:    {numeric_series.quantile(0.50):.3f} ms (Median)")
    print(f"    P90:    {numeric_series.quantile(0.90):.3f} ms")
    print(f"    P95:    {numeric_series.quantile(0.95):.3f} ms")
    print(f"    P99:    {numeric_series.quantile(0.99):.3f} ms")

def main():
    parser = argparse.ArgumentParser(description="Analyze latency data from a JSON file.")
    parser.add_argument("input_file", type=str, nargs='?', default="results.json",
                        help="Path to the JSON input file (default: results.json).")
    
    args = parser.parse_args()
    input_file_path = args.input_file

    try:
        # Load the JSON data using pandas.read_json for direct DataFrame creation
        df = pd.read_json(input_file_path)
        print(f"Data loaded successfully from '{input_file_path}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        # This can happen if JSON is malformed or empty
        print(f"Error reading JSON file '{input_file_path}': {e}")
        print("The file might be empty or not a valid JSON array of objects.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_file_path}': {e}")
        sys.exit(1)

    if df.empty:
        print("The JSON file was empty or contained no data. Exiting.")
        sys.exit(0)

    print("\n--- DataFrame Info ---")
    df.info(verbose=True, show_counts=True)

    print("\n--- Initial Data Head ---")
    print(df.head())

    # --- Analysis of Successful Requests ---
    print("\n--- Analysis of Successful Requests (HTTP 2xx/3xx) ---")
    # Base conditions for a successful request based on http_code
    success_conditions = (
        df['http_code'].notna() & 
        (df['http_code'] >= 200) & 
        (df['http_code'] < 400)
    )
    # If the 'error' column exists, a successful request must also have a null value in this column.
    # If the 'error' column doesn't exist, it implies no errors were logged in this field for any request.
    if 'error' in df.columns:
        success_conditions &= df['error'].isnull()
    
    successful_df = df[success_conditions].copy()


    successful_df = df[success_conditions].copy() # Use .copy() to avoid SettingWithCopyWarning

    if successful_df.empty:
        print("No successful requests found in the data for detailed statistical analysis.")
    else:
        print(f"\nFound {len(successful_df)} successful requests out of {len(df)} total entries.")

        # Define the base timing columns (now in milliseconds from JSON)
        base_time_cols_ms = ['queueTime_ms', 'namelookupTime_ms', 'connectTime_ms',
                             'appconnectTime_ms', 'pretransferTime_ms',
                             'startTransferTime_ms', 'totalTime_ms', 'redirectTime_ms']
        
        # Ensure all expected base time columns exist, if not, print a warning (they should exist if main.py ran correctly)
        for col_ms in base_time_cols_ms:
            if col_ms not in successful_df.columns:
                print(f"Warning: Column {col_ms} not found in successful_df.")

        # Calculate derived timing metrics
        successful_df = calculate_derived_timings(successful_df)

        print("\n--- Statistics for Successful Requests (Times in Milliseconds) ---")
        
        # Print stats for base timings in milliseconds
        for metric_ms in base_time_cols_ms:
            if metric_ms in successful_df.columns:
                print_statistics(successful_df[metric_ms], metric_ms)
        
        # Print stats for derived timings in milliseconds
        derived_metrics_ms = ['time_to_connect_ms', 'time_to_tls_ms', 'ttfb_setup_ms',
                              'server_processing_ms', 'response_download_ms']
        for metric_ms in derived_metrics_ms:
            if metric_ms in successful_df.columns:
                print_statistics(successful_df[metric_ms], metric_ms)
            else:
                print(f"  Metric {metric} not calculated or not available.")
        
        print("\n--- Successful Requests DataFrame Head (with calculated milliseconds) ---")
        display_cols = base_time_cols_ms + derived_metrics_ms
        # Filter display_cols to only those present in successful_df to avoid KeyError
        display_cols = [col for col in display_cols if col in successful_df.columns]
        print(successful_df[display_cols].head())


    # --- Analysis of Errors ---
    print("\n--- Analysis of Errors ---")
    # Base condition for an error: http_code is not in the 200-399 range or is NaN.
    # Note: http_code should always exist as per main.py logic (value or -1).
    error_http_conditions = ~(
        df['http_code'].notna() &
        (df['http_code'] >= 200) & 
        (df['http_code'] < 400)
    )

    if 'error' in df.columns:
        # If 'error' column exists, an error is also when df['error'] is not null.
        error_conditions = error_http_conditions | df['error'].notna()
    else:
        # If 'error' column doesn't exist, errors are determined solely by http_code.
        error_conditions = error_http_conditions

    error_df = df[error_conditions].copy()

    if error_df.empty:
        print("No errors found in the data.")
    else:
        print(f"\nFound {len(error_df)} entries with errors or non-successful HTTP codes.")
        print("\nError Summary:")
        if 'error' in error_df.columns and not error_df['error'].dropna().empty:
            print(error_df['error'].value_counts())
        if 'http_code' in error_df.columns:
            print("\nHTTP Code Counts for Errors/Non-Successful:")
            print(error_df['http_code'].value_counts())
        
        print("\n--- Error DataFrame Head ---")
        print(error_df.head())

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()