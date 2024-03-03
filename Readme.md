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


<!---
Sep 18:

Added user, Game List page, Game Details page, 
League List page, League Standings page,

Added login/logout, etc.

Need to add login restrictions for endpoints.


TODOs :

USer Game Page

Todo: 

Add game week standing.

Add league standings.



TODOS:

Optimize Django DB Queries

if possible in dropdown show unselected options in green and selcted one in red

gmail login



Add how to play and scoring system. (link in homescreen)


Auto join user in the main leage if the form submitted is correct

debug as false



Use PL apps color - i.e purple

Reset password flow

Check CSS for Sign up page

Test login on mobile, faced csrf issue

Host postgres


Post game deadline, dont allow to save, and dont allow to change choices in UI as well

Create a countdown 
-->
