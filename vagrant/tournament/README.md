##'Swiss System Tournament' PostgreSQL DB

### RUNNING PROJECT

To run a **`Multiple Tournament`** test:
- first, in psql run `\i multiple_tournaments.sql`
- then, run `python multiple_tournaments_test.py`

>**OBS: Tests 11, 12 and 13 are for 'Multiple Tournament' extras:**

>1. *Support more than one tournament in the database, so matches do not have to be deleted between tournaments.*
>2. *Prevent rematches between players.*
>3. *Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.*