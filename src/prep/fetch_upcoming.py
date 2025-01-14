import requests, csv, pandas
from upcoming_match import UpcomingMatch
from helper import Helper 

class FetchUpcoming:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.helper = Helper()

    def append_to_csv(self, matches, csv_filename):
        with open(csv_filename, mode='w', newline='') as csv_file:
            fieldnames = ['start_time', 'home_team', 'away_team']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Check if the file is empty, if so write the header
            if csv_file.tell() == 0:
                writer.writeheader()

            for match in matches:  
                if 'Women' not in match.competition_name and 'Int. Friendly Games W' not in match.competition_name:        
                    writer.writerow({
                        'start_time': match.start_time,
                        'home_team': match.home_team,
                        'away_team': match.away_team
                    })

    def __call__(self, sport_id='14'):
        url = f"https://api.betika.com/v1/uo/matches?limit=1000&tab=2&sub_type_id=162&sport_id={sport_id}&sort_id=2&period_id=-1&esports=false&is_srl=false&page=1"

        matches_data = self.helper.fetch_data(url)['data']
        matches = [UpcomingMatch(match) for match in matches_data]

        if matches:
            self.append_to_csv(matches, self.csv_filename)
