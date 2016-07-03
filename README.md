Synopsis
========
This project uses a database to run a swiss-style tournament where no players are eliminated and the most competitive matches possible are generated.


How to Run
==========
Follow these steps in the terminal:

>psql  
>\i tournament.sql  
>\q  
>python tournament_test.py  


Files
=====
tournament.sql - contains sql for creating the tables  
tournament.py - a python file that uses the psycopg2 API to interact with the database  
tournament_test.py - a file provided to me that tests tournament.py to check my work  