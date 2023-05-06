import re
import os.path
import pandas as pd

def loop_to_CSV(input_string, csv_file=None):
    
    # Apply the subfunctions to the input string
    result1 = input_string
    result2 = scale_to_numeric(extract_tonality_from_str(input_string))
    

    new_row = pd.DataFrame({
        'Subfunction 1 Output': [result1],
        'Subfunction 2 Output': [result2],
    })

    # Check if a CSV file was provided
        # check if the CSV file already exists
    if csv_file:
        try:
            # if it does, read the existing data into a DataFrame
            existing_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            # if the file doesn't exist, create an empty DataFrame
            existing_data = pd.DataFrame()
        
        # concatenate the new row to the existing DataFrame
        combined_data = pd.concat([existing_data, new_row], ignore_index=True)
        
        # write the combined DataFrame to the CSV file
        combined_data.to_csv(csv_file, index=False)
    else:
        # if no CSV file is provided, simply print the new row
        csv_file = 'dataset.csv'
        new_row.to_csv(csv_file, index=False)
        print(f"CSV file created: {csv_file}")


def bars_to_seconds(num_bars, bpm):
    sec_per_beat = 60 / bpm
    beats_per_bar = 4
    sec_per_bar = sec_per_beat * beats_per_bar
    total_sec = num_bars * sec_per_bar
    return total_sec

def remove_whitespace(input_string):
    # Use the replace() method to remove all whitespace characters
    return input_string.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

def extract_tonality_from_str(string):
    if string[-4:] == '.wav' or string[:-4] == '.mp3':
        string = string[:-4]

    elements = string.split('_')
    regex = r'[A-G]{1}(#|b)?(\s)?(min|maj|min7|maj7|7|m|M|Min|Maj)?$'
    for element in elements:
        match = re.search(regex, element)
        if match:
            tonality = match.group(0)
            return remove_whitespace(tonality)
        
    return None

def scale_to_numeric(string):
    if string is None:
        return None
    
    tone_map = {
        'C': 0,
        'C#': 1,
        'Db': 1,
        'D': 2,
        'D#': 3,
        'Eb': 3,
        'E': 4,
        'F': 5,
        'F#': 6,
        'Gb': 6,
        'G': 7,
        'G#': 8,
        'Ab': 8,
        'A': 9,
        'A#': 10,
        'Bb': 10,
        'B': 11
    }

    if len(string) > 1:
        if string[1] == '#':
            root = tone_map[string[0:2]]
            string = string[2:]
            
        elif string[1] == 'b':
            root = tone_map[string[0:2]]
            string = string[2:]
        else:
            root = tone_map[string[0]]
            string = string[1:]
        
        if string == 'min' or string == 'm' or string == 'Min':
            return root + 3
        else:
            return root
        
    else:
        root = tone_map[string[0]]
        return root
    
def main():
    loop_name = 'OS_DRIP_166_Gm_Polyform_Analog_Chords_2.wav'
    print(extract_tonality_from_str(loop_name))
if __name__ == "__main__":
    main()
