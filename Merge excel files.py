import os
import pandas as pd

folder_path = '/Users/luisguinea/Documents/Pruebas/Investigacion de compositores para Peermusic'

# Function to read all Excel files from the folder
def read_excel_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]
    return [os.path.join(folder_path, f) for f in files]

# Function to merge data from multiple Excel files
def merge_excel_files(file_paths):
    artist_details_df = pd.DataFrame()
    albums_df = pd.DataFrame()

    for file_path in file_paths:
        try:
            df = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            if 'Artist Details' in df:
                artist_details_sheet = df['Artist Details']
                artist_details_sheet['SourceFile'] = os.path.basename(file_path)
                artist_details_df = pd.concat([artist_details_df, artist_details_sheet], ignore_index=True)
            if 'Albums' in df:
                albums_sheet = df['Albums']
                albums_sheet['SourceFile'] = os.path.basename(file_path)
                # Add the "Artist" column by removing "_Spotify_Data" from the file name
                albums_sheet['Artist'] = os.path.basename(file_path).replace('_Spotify_Data', '').replace('.xlsx', '').replace('.xls', '')
                # Reorder columns to put "Artist" first
                columns = ['Artist'] + [col for col in albums_sheet.columns if col != 'Artist']
                albums_sheet = albums_sheet[columns]
                albums_df = pd.concat([albums_df, albums_sheet], ignore_index=True)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    return artist_details_df, albums_df

# Main function to execute the merging process
def main():
    excel_files = read_excel_files(folder_path)
    if not excel_files:
        print('No Excel files found in the specified folder.')
        return

    artist_details_df, albums_df = merge_excel_files(excel_files)
    output_file_path = os.path.join(folder_path, 'merged.xlsx')

    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        artist_details_df.to_excel(writer, sheet_name='Artist Details', index=False)
        albums_df.to_excel(writer, sheet_name='Albums', index=False)

    print(f'Merged Excel file created at: {output_file_path}')

if __name__ == "__main__":
    main()