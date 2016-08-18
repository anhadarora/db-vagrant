##'Simple Forum' and 'Swiss System Tournament' PostgreSQL DB running on Vagrant VM.

### INSTALLATION

To install and run Vagrant with configured VM:
[Install and setup Vagrant VM](https://udacity.atlassian.net/wiki/display/BENDH/Vagrant+VM+Installation)

---

### RUNNING TOURNAMENT

At `/vagrant/tournament/` there is a **`Single Tournament`** and **`Multiple Tournament`** (extras) project.

To run a **`Single Tournament`** test:
- go to `/vagrant/tournament/`
- run `psql`
- in psql run `\i tournament.sql`
- run `python tournament_test.py`

To run a **`Multiple Tournament`** test:
- go to `/vagrant/tournament/`
- run `psql`
- in psql run `\i multiple_tournaments.sql`
- run `python multiple_tournaments_test.py`

>**OBS: The 'Multiple Tournament' is for the project extras:**

>1. *Support more than one tournament in the database, so matches do not have to be deleted between tournaments.*
>2. *Prevent rematches between players.*
>3. *Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.*