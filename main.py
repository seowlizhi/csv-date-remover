#!/usr/bin/env python3
"""
Script to delete rows from a DataFrame within a specified datetime range.
Supports CSV files with datetime columns.
"""

import pandas as pd
import argparse
from datetime import datetime
import sys
import os

def parse_datetime(date_string, format):
    """
    Parse datetime string with multiple format support.
    
    Args:
        date_string (str): Date string to parse
        
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.strptime(date_string, format)
    except ValueError:
        print(f"Unable to parse datetime: {date_string}")


def delete_datetime_range(df, datetime_col, start_date, end_date, format):
    """
    Delete rows from DataFrame within the specified datetime range.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        datetime_col (str): Name of the datetime column
        start_date (datetime): Start of deletion range (inclusive)
        end_date (datetime): End of deletion range (inclusive)
        
    Returns:
        pd.DataFrame: DataFrame with rows deleted
    """
    # Convert datetime column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df[datetime_col]):
        df[datetime_col] = pd.to_datetime(df[datetime_col], format=format)
    
    # Create mask for rows to keep (outside the deletion range)
    mask = ~((df[datetime_col] >= start_date) & (df[datetime_col] <= end_date))
    
    # Count rows being deleted
    rows_to_delete = (~mask).sum()
    print(f"Deleting {rows_to_delete} rows between {start_date} and {end_date}")
    
    # Return filtered DataFrame
    return df[mask].copy()

def main():
    parser = argparse.ArgumentParser(
        description='Delete rows from a DataFrame within a specified datetime range',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script.py data.csv -c timestamp -s "2023-01-01" -e "2023-01-31"
  python script.py data.csv -c date_col -s "2023-01-01 10:00:00" -e "2023-01-01 15:00:00" -o cleaned_data.csv
  python script.py data.csv -c datetime -s "01/01/2023" -e "12/31/2023"
        """
    )
    
    parser.add_argument('input_file', 
                       help='Path to input CSV file')
    
    parser.add_argument('-c', '--datetime-column', 
                       required=True,
                       help='Name of the datetime column')
    
    parser.add_argument('-f', '--datetime-format', 
                       required=True,
                       help='Format of datetime')
    
    parser.add_argument('-s', '--start-date', 
                       required=True,
                       help='Start date/datetime for deletion range (inclusive)')
    
    parser.add_argument('-e', '--end-date', 
                       required=True,
                       help='End date/datetime for deletion range (inclusive)')
    
    parser.add_argument('-o', '--output-file', 
                       help='Path to output CSV file (default: overwrites input file)')
    
    parser.add_argument('--dry-run', 
                       action='store_true',
                       help='Show what would be deleted without actually deleting')
    
    parser.add_argument('--backup', 
                       action='store_true',
                       help='Create backup of original file before modification')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists("input/"+args.input_file):
        print(f"Error: Input file input/'{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Load DataFrame
        print(f"Loading data from input/{args.input_file}...")
        df = pd.read_csv("input/"+args.input_file)
        print(f"Loaded DataFrame with {len(df)} rows and {len(df.columns)} columns")
        
        # Check if datetime column exists
        if args.datetime_column not in df.columns:
            print(f"Error: Column '{args.datetime_column}' not found in DataFrame.", file=sys.stderr)
            print(f"Available columns: {list(df.columns)}", file=sys.stderr)
            sys.exit(1)
        
        # Parse datetime arguments
        try:
            start_date = parse_datetime(args.start_date, args.datetime_format)
            end_date = parse_datetime(args.end_date, args.datetime_format)
        except ValueError as e:
            print(f"Error parsing datetime: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Validate date range
        if start_date > end_date:
            print("Error: Start date must be before or equal to end date.", file=sys.stderr)
            sys.exit(1)
        
        # Show current datetime range in data
        df_temp = df.copy()
        df_temp[args.datetime_column] = pd.to_datetime(df_temp[args.datetime_column], format=args.datetime_format)
        min_date = df_temp[args.datetime_column].min()
        max_date = df_temp[args.datetime_column].max()
        print(f"Data datetime range: {min_date} to {max_date}")
        
        if args.dry_run:
            # Dry run - just show what would be deleted
            mask = ((df_temp[args.datetime_column] >= start_date) & 
                   (df_temp[args.datetime_column] <= end_date))
            rows_to_delete = mask.sum()
            print(f"DRY RUN: Would delete {rows_to_delete} rows between {start_date} and {end_date}")
            print(f"Remaining rows: {len(df) - rows_to_delete}")
            
            if rows_to_delete > 0:
                print("\nSample of rows that would be deleted:")
                sample_rows = df_temp[mask].head(5)
                print(sample_rows[args.datetime_column].to_string())
        else:
            # Create backup if requested
            if args.backup:
                backup_file = f"{args.input_file}.backup"
                df.to_csv(backup_file, index=False)
                print(f"Backup created: {backup_file}")
            
            # Delete rows
            df_filtered = delete_datetime_range(df, args.datetime_column, start_date, end_date, args.datetime_format)
            
            # Determine output file
            output_file = args.output_file if args.output_file else args.input_file
            
            # Save filtered DataFrame
            df_filtered.to_csv("results/"+output_file, index=False)
            print(f"Filtered data saved to results/{output_file}")
            print(f"Final DataFrame: {len(df_filtered)} rows, {len(df_filtered.columns)} columns")
            print(f"Rows deleted: {len(df) - len(df_filtered)}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()