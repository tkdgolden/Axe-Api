# Capstone 2
Multi-layered web application to host and store data for axe throwing tournaments and leagues.

## Docker
spins up instances of each application layer

## Database
PostgreSQL
![Screenshot (27)](https://github.com/tkdgolden/Axe-Api/assets/93563260/8a1155e7-a9bf-4bfb-9956-ab6e51881713)

## Database Management Layer
psycopg2 to perform SQL statements
Flask application to handle server routing to different endpoints that run processes in the database management layer.

## Web Application Layer / USER FLOWS
React web application with two portals (Player and Judge, described below) and navigation between the two via the Navbar at the top of the page with login and logout buttons
### Player View
without logging in, various statistics are displayed
Sidebar for navigation to different statistics views: 
- overall stats (default page) with players averages (by discipline will be a further study, right now set to the default of hatchet)
- stats by season with players averages and rankings for a given season
- tournament stats FURTHER STUDY PLACEHOLDER
- player search (imperfect searches will be FURTHER STUDY, right now can only accomodate searches that return exactly one player) displays a single player's overall stats
### Judge View
when a judge logs in, they are able to create and edit the necessary tables in the database in order to store all information needed to run a league
the navbar gives an extra option of registering new judges
two columns of options: season and tournament (FURTHER STUDY)
- season
- - the most recent season is displayed on top of the page for easy access
  - an option to go to a form to create a new season
  - an option to select an older season

once a season is selected, there are options regarding players:
- checking in a player (so that matches including players who are absent for the given week are not cluttering up the page)
- enrolling an existing player (these are players that already exist from previous seasons)
- a form to register a new player

there are also options regarding "laps" (each week of a season is called a lap):
- score an existing lap (you may select a lap that has already been created)
- start a new lap (automatically set to be the current lap)

when a lap is selected, and players checked in, a table with the available matches will appear below
- each grid on the table corresponds to two players a player will not play themselves, so these appear black
- matches that have been completed are green and cannot be clicked (players may not face off twice in one lap)
- matches that have not been completed are blue and can be clicked to begin that match

once a match is selected, a page for scoring that match is displayed
- most fields begin as hidden to control the flow of the match
- which color bullseye to aim for is kept secret until that throw has begun
- player scores cannot be recorded before the bullseye color has been announced
- only one player may score the "quick point" by throwing faster than their opponent
- the next throw may not begin until scores have been entered for each player (a quickpoint is optional)
- once all throws scores have been recorded, the option to submit reveals
- note handling of tiebreakers is FURTHER STUDY
- after submission, the page should return to the correct season and lap for selecting another match

# Step 1
please see initial_project_ideas.md
# Step 2
please see project_proposal.md
# Step 3
please see the schema diagram picture at the top of this page, as well as the db directory, and server directory, please acknowledge that everything related to tournaments is a FURTHER STUDY, and is in the structure as a placeholder, please acknowledge that different disciplines are FURTHER STUDY, and this is included in the structure as a placeholder
# Step 4
please see the webapp directory, please note, all pages related to tournaments are PLACEHOLDER FOR FURTHER STUDY, please note, alternative disciplines and handling ties are FURTHER STUDY, but references to these abilities exist as PLACEHOLDERS
# Step 5
please see the webapp directory, please note, all pages related to tournaments are PLACEHOLDER FOR FURTHER STUDY, please note, alternative disciplines and handling ties are FURTHER STUDY, but references to these abilities exist as PLACEHOLDERS
