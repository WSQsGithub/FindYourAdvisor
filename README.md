# Advisor Information Searcher

This Python script allows you to search for detailed information about academic advisors based on a provided list of advisor names and institutions. It pulls data from Google Scholar, including the advisor's name, profile URL, affiliation, and citation count, and stores this information in a CSV file.

## Features

- **Search by Name & Institution**: Search for advisors by name and optional institution.
- **Concurrent Searches**: Uses multiple threads to speed up the search process.
- **CSV Output**: Saves the information in a CSV file for easy use and sharing.

## Requirements

- Python 3.6+
- `requests`
- `beautifulsoup4`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/advisor-info-search.git
   ```

2. **Install dependencies:**

   Make sure you have Python 3.6+ installed, and then install the required packages with:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare the advisor list:**

   Copy the whole select element from the website and paste it here (use developer tools to copy the select element)
   
   Example format:

   ```html
   <select class="phdAdv form-control" name="applicant[advisor_ships_attributes][0][user_id]" id="applicant_advisor_ships_attributes_0_user_id"><option value="">-----</option>
        <option value="1">John Doe </option>
        <option value="2">Jane Smith</option>
    </select>
   ```

2. **Run the script:**

   Execute the script using:

   ```bash
   python get_researcgh_interests.py
   ```

   This will search for the professors and save the results in a CSV file named `professor_info.csv`.

## Output

The results will be saved in a CSV file with the following columns:

- **Name**: The advisor's name
- **Institution**: The advisor's affliation
- **Citation Count**: The advisor's institution
- **Research Interests**: The advisor's citation count (if available)
- **Scholar Link**: The URL to the advisor's Google Scholar profile


## Example CSV Output:

| Name         | Institution              | Citation Count | Research Interests | Scholar Link                          |
|--------------|--------------------------|----------------|--------------------|---------------------------------------|
| John Doe     | University of Example    | 1200           | AI, Machine Learning| https://scholar.google.com/citations/123456789 |
| Jane Smith   | Example Institute        | 1500           | Data Science, Big Data| https://scholar.google.com/citations/987654321 |

## Notes

- Google Scholar may block or limit requests if too many requests are made in a short time. This script uses a simple delay and threading to help manage this, but use it responsibly.
- Ensure that the institutions are spelled correctly for better results.
- Please double-check the contents for accuracy, as the search may not be entirely accurate.
