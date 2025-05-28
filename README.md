# CSV Date Remover

A Python script to delete rows from CSV files within a specified datetime range. This tool is useful for data cleaning, removing outliers, or filtering time-series data.

## Features

- **Flexible datetime parsing** - Supports multiple common datetime formats
- **Safe operations** - Dry run mode and automatic backup options
- **Format specification** - Tell the script exactly what datetime format your data uses
- **Comprehensive validation** - Checks files, columns, and date formats before processing
- **Detailed feedback** - Shows statistics about what's being deleted
- **Command-line interface** - Easy to use and integrate into workflows

## Installation

### Prerequisites
- Python 3.6+
- pandas library

### Install dependencies
```bash
pip install pandas
```

## Usage

### Basic Syntax
```bash
python datetime_row_deleter.py <input_file> -c <datetime_column> -s <start_date> -e <end_date> [options]
```

### Required Arguments
- `input_file` - Path to your CSV file
- `-c, --datetime-column` - Name of the column containing datetime values
- `-s, --start-date` - Start of the deletion range (inclusive)
- `-e, --end-date` - End of the deletion range (inclusive)

### Optional Arguments
- `-o, --output-file` - Output file path (default: overwrites input file)
- `-f, --format` - Specify the exact datetime format of your data
- `--dry-run` - Preview what would be deleted without actually deleting
- `--backup` - Create a backup of the original file before modification
- `-h, --help` - Show help message

## Examples

### Basic Usage
Delete all rows between January 1, 2023 and January 31, 2023:
```bash
python datetime_row_deleter.py data.csv -c timestamp -s "2023-01-01" -e "2023-01-31"
```

### Specify Custom Format
If your datetime column uses a specific format, specify it with `-f`:
```bash
python datetime_row_deleter.py data.csv -c date_column -s "01-01-2023" -e "31-01-2023" -f "%d-%m-%Y"
```

### Time-based Deletion
Delete rows within a specific time window:
```bash
python datetime_row_deleter.py data.csv -c datetime -s "2023-01-01 10:00:00" -e "2023-01-01 15:00:00"
```

### Safe Operations
Use dry run to preview changes:
```bash
python datetime_row_deleter.py data.csv -c timestamp -s "2023-01-01" -e "2023-01-31" --dry-run
```

Create backup before deletion:
```bash
python datetime_row_deleter.py data.csv -c timestamp -s "2023-01-01" -e "2023-01-31" --backup
```

### Save to Different File
Keep original file unchanged:
```bash
python datetime_row_deleter.py data.csv -c timestamp -s "2023-01-01" -e "2023-01-31" -o cleaned_data.csv
```

## Supported Datetime Formats

The script automatically detects these common formats:

| Format | Example |
|--------|---------|
| `%Y-%m-%d %H:%M:%S` | 2023-01-15 14:30:00 |
| `%Y-%m-%d %H:%M` | 2023-01-15 14:30 |
| `%Y-%m-%d` | 2023-01-15 |
| `%m/%d/%Y %H:%M:%S` | 01/15/2023 14:30:00 |
| `%m/%d/%Y %H:%M` | 01/15/2023 14:30 |
| `%m/%d/%Y` | 01/15/2023 |
| `%d/%m/%Y %H:%M:%S` | 15/01/2023 14:30:00 |
| `%d/%m/%Y %H:%M` | 15/01/2023 14:30 |
| `%d/%m/%Y` | 15/01/2023 |
| `%Y-%m-%dT%H:%M:%S` | 2023-01-15T14:30:00 |
| `%Y-%m-%dT%H:%M:%SZ` | 2023-01-15T14:30:00Z |

### Custom Format Specification

If your data uses a different format, specify it with the `-f` flag using Python's strftime codes:

```bash
# For format like "Jan 15, 2023"
python datetime_row_deleter.py data.csv -c date -s "Jan 01, 2023" -e "Jan 31, 2023" -f "%b %d, %Y"

# For format like "2023.01.15-14:30"
python datetime_row_deleter.py data.csv -c timestamp -s "2023.01.01-00:00" -e "2023.01.31-23:59" -f "%Y.%m.%d-%H:%M"
```

## Common Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2023 |
| `%y` | 2-digit year | 23 |
| `%m` | Month (01-12) | 01 |
| `%B` | Full month name | January |
| `%b` | Abbreviated month | Jan |
| `%d` | Day of month (01-31) | 15 |
| `%H` | Hour (00-23) | 14 |
| `%I` | Hour (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%p` | AM/PM | PM |

## Error Handling

The script includes comprehensive error handling for:
- **File not found** - Checks if input file exists
- **Invalid columns** - Verifies datetime column exists in the DataFrame
- **Date parsing errors** - Validates datetime format and provides helpful error messages
- **Invalid date ranges** - Ensures start date is before end date
- **Data type issues** - Automatically converts datetime columns if needed

## Output Information

The script provides detailed information about the operation:
- Number of rows in original DataFrame
- Datetime range of the existing data
- Number of rows being deleted
- Number of remaining rows
- Confirmation of output file location

### Example Output
```
Loading data from sales_data.csv...
Loaded DataFrame with 10000 rows and 5 columns
Data datetime range: 2022-12-01 00:00:00 to 2024-02-28 23:59:59
Deleting 1250 rows between 2023-01-01 00:00:00 and 2023-01-31 23:59:59
Filtered data saved to sales_data.csv
Final DataFrame: 8750 rows, 5 columns
Rows deleted: 1250
```

## Best Practices

1. **Always use dry run first** - Preview changes with `--dry-run` before actual deletion
2. **Create backups** - Use `--backup` for important data files
3. **Specify output file** - Use `-o` to avoid overwriting original data
4. **Check datetime ranges** - The script shows your data's datetime range to help with range selection
5. **Use specific formats** - If auto-detection fails, specify format with `-f`

## Troubleshooting

### Common Issues

**"Column not found" error:**
- Check column names in your CSV file
- Column names are case-sensitive
- Use quotes if column names have spaces: `-c "Date Time"`

**"Unable to parse datetime" error:**
- Check the format of your datetime values
- Use `-f` to specify the exact format
- Ensure start and end dates match your data's format

**"No rows deleted" result:**
- Verify your date range includes data from your file
- Check that your datetime format matches the data
- The script shows your data's date range for reference

## License

This script is provided as-is for educational and practical use. Feel free to modify and distribute according to your needs.