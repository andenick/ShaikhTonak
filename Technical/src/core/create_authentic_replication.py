# This script creates an authentic replication of Shaikh & Tonak's Table 5.4.
# It loads the raw, incomplete data, cleans it, and merges it into a single file.
# No interpolation or artificial data generation is performed.

import pandas as pd
import numpy as np

def clean_and_merge_sources():
    """Loads, cleans, and merges the two source files for Table 5.4."""
    
    # --- Part 1: 1958-1973 ---
    part1_path = 'data/extracted_tables/book_tables/table_p36_camelot[page]_0.csv'
    df1 = pd.read_csv(part1_path, index_col=0)
    
    # The last row is gK, but is unnamed. Let's name it.
    df1 = df1.rename(index={df1.index[-2]: 'gK'})

    # The value for 'u' in 1973 is 0.0, which is a missing value.
    df1.loc['u', '1973'] = np.nan

    # --- Part 2: 1974-1989 ---
    part2_path = 'data/extracted_tables/book_tables/table_p37_camelot[page]_0.csv'
    df2_raw = pd.read_csv(part2_path, index_col=0)

    # The columns are years 1974-1989, as per the README
    years_part2 = [str(y) for y in range(1974, 1990)]
    df2_raw.columns = years_part2

    # --- Merge --- 
    # Combine the two dataframes, aligning on the variable names (index)
    df_authentic = pd.concat([df1, df2_raw], axis=1, sort=True)

    # Reorder columns to be chronological
    all_years = [str(y) for y in range(1958, 1990)]
    df_authentic = df_authentic.reindex(columns=all_years)

    # Save the authentic, raw-merged data
    output_path = 'src/analysis/replication/output/table_5_4_authentic_raw_merged.csv'
    df_authentic.to_csv(output_path)
    
    print(f"Successfully created authentic raw merged data at: {output_path}")
    return df_authentic

if __name__ == '__main__':
    clean_and_merge_sources()