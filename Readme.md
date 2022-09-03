# Django FPL Bingo Game

An FPL BINGO Game



Steps:
1. Create a Django Server with a Static HTML
2. Create a PAGE where Admin can create a BINGO GAME and add options.
3. Create a page where USER can select and Save their Bingo options for a GAME.
4. An ENDPoint to update the GAME options.
5. Calculate the score of the users


Models:
1. League - id, game_ids (one to many)
1. Game - id, name, choices, end_time,
2. Options - id, name, is_done,
3. UserGame - game_id, user_id, user_choices, score
4. User - name, user_id, password, reddit_user_name
6. League Standings - league_id, user_id, score, position, prev_position.
7. UserChoices - TO store choice of user for a game

Choices can be stored in a single array.Calculation can be done based by using formula based on positions