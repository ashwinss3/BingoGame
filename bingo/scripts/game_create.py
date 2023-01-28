from bingo.models import GameOptions

game_options = [
    {"name": "Haaland is the Top Point Scorer this Season", "description": "Haaland finishes the season with most points this FPL Season"},
    {"name": "Top Scoring Midfielder scores 220+ points", "description": "The Midfielder with most points finishes with 220 or more points"},
    {"name": "Top Scoring Defender Scores 220+ points", "description": "The Defender with most points finishes with 220 or more points"},
    {"name": "Top Scoring GK Scores 180+ points", "description": "The Goalkeeper with most points finishes with 180 or more points"},
    {"name": "Haaland the Hauler - Most points in a Season ever", "description": "Haaland becomes the player to score the most points in an FPL Season. The record is currently held by Salah (303 Points)"},
    {"name": "Reliable Trippier - Breaks Robertson's points record", "description": "Trippier breaks the record for most points by a defender in a season. It is currently held by Robertson (213 points)"},
    {"name": "Captain Fantastic - Haaland Scores 45+ Goals", "description": "Haaland finishes the Season with 45 or More goals in the Premier League"},
    {"name": "Newcastle finishes in the Top 4", "description": "Newcastle Finishes in the Top 4 this season."},
    {"name": "Rashford breaks his personal best for most points in a Season(177 points)", "description": "Rashford continues his form and breaks his points record for a Season. His current record in 177 points."},
    {"name": "Kane scores more than 242 Points(His Personal Best)", "description": "Harry Kane Scores more than 242 points and breaks his personal record for most FPL points in a season."},
    {"name": "Arsenal wins the League", "description": "Arsenal wins the Premier League "},
    {"name": "City Overtakes Arsenal to win the League", "description": "Manchester City overtakes Arsenal and wins the League"},
    {"name": "Defensive Castle - Newcastle Finishes with Least Goals Conceded", "description": "Newcastle maintains their defensive form and finishes the Season with Least Goals conceded among all the teams."},
    {"name": "Century of Goals - Team Finishes with 100+ Goals", "description": "Any team finishes with 100 or more goals this season."},
    {"name": "Top Scoring Defender outscores Top Scoring Midfielder", "description": "Top Scoring Defender scores more points that top scoring Midfielder"},
    {"name": "Most CS - Ramsdale overtakes Pope", "description": "Ramsdale overtakes Pope and finishes the Season with most Clean Sheets"},
    {"name": "AGUEROOO - PL winner is decided on final matchday", "description": "The Premier League winner is not decided until the final Match day"},
    {"name": "Relegation Battle Goes till Final Matchday", "description": "Relegated teams are not decided until the final Match day"},
    {"name": "Spending Misfortune - Chelsea misses out European spots", "description": "The new players doesn't help and Chelsea misses out on Major European Spots."},
    {"name": "Klopp's Comeback - Liverpool Finishes in Top 5", "description": "Liverpool finishes in the Top 5 at the end of the Season"},
    {"name": "Mitoma Magic - Finishes with 150+ points", "description": "Mitoma finishes with 150 or more points"},
    {"name": "Old Favourites - TAA outscores Robertson", "description": "TAA finishes the season with more points than Robertson"},
    {"name": "De Bruyne's Delivery - KDB finishes Season with most assists", "description": "KDB finishes the Season with Most Assists"},
    {"name": "The Axe Falls again - Another manager fired", "description": "Another manager gets fired before the end of season"},
    {"name": "Bench Fodder Finishes with 130+ Points", "description": "A Bench Fodder scores 120 or more points in the Season",
     "condition": "To be considered as Bench Fodder, Intial Price of the player: 4.0m max for GK/Def, 5.0m max for Mid/Att"},
    {"name": "Nketiah Finishes among Top 5 Forwards", "description": "Nketiah finishes the FPL season among the Top 5 forwards with highest points this season."},
    {"name": "Budget Forwards Battle - Mitrovic Outscores Toney", "description": "Mitrovic finishes the season with more points than Toney."},
    {"name": "Premium Mid Battle - Salah outscores KDB", "description": "Salah scores more points than KDB by the end of Season"},
    {"name": "Arsenal Mid Battle - Saka Outscores Odegaard",
     "description": "Saka finishes with more points than Odegaard"},
    {"name": "Winner scores 2900+ points",
     "description": "FPL Overall Winner scores 2900 or more points"},
    {"name": "Foden Outscores Mahrez - Pep Strikes Again",
     "description": "Foden finishes with more points than Mahrez by end of Season."},
    {"name": "FREE SPACE", "description": "FREE SPACE"},
]

def create_options(game_id, option_list=None):
    if not option_list:
        option_list = game_options
    batch_size = 100
    objs = [GameOptions(**i, game_id=game_id) for i in option_list]

    GameOptions.objects.bulk_create(objs, batch_size)
