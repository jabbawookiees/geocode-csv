# Geocode CSV Script

This is a quick script to geocode CSV files. It uses Google's Geocode API, so that means you can only do 2500 per day.

This script is smart enough to continue where it last left off if you shut it down.

## Usage:

Have a list of addresses as a text  file, one address in each line. CSV format is accepted too, but only the first column will be used.

Run the script:

`python geocodecsv.py input.csv --output output.csv`

Output argument is optional with a default of output.csv. This will provide a result with seven columns:  
Address - The original address  
Latitude - Latitude provided by Google  
Longitude - Longitude provided by Google  
City - City provided by Google. Useful for a sanity check  
Country - Same as city  
Status - Can either be "OK", "No Results", or "Ignored"  
Raw Data - JSON format of Google's result

Ignoring addresses
If for some reason, your CSV has some clutter addresses that you want to have ignored, you can add the strings in the ignore list at the start of the script.


## Requirements

This uses the non-native Python libraries `geocoder` and `click`. Please install those :)
