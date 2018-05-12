# PyChat
A chat tool coded in Python.

First, you need to have installed in your server:
- Python 3.x
  - psycopg2: Python module to connect to PSQL
- PostgreSQL

You run tables.sql in order to create the tables in PostgreSQL. The main.py file is kept running in server, while the user.py is executed in client side.

The database has only two tables:
- rooms: id, name, password
- users: id, id_room, name, ip, port

When the user connect to server, he sends his name, the name of the room he's trying to connect to and the room's password (we call this the 'login request').
The main.py checks in rooms table whether the room exists and the password is correct. Then main.py search in users table for the users already connected to room and return to user a list of IPs and ports, so he can connect to them directly, using the module socket (standard library). NO MESSAGE IS SENT TO SERVER (THEN NO MESSAGE IS KEPT IN SERVER). THE COMMUNICATION IS ONLY P2P. The purpose of server is to keep up-to-date the address of users. The rooms are considered, in fact, the right to access a specific list of user addresses.

Sometimes, the address of a user may change (connection to internet interrupted or router rebooted IP), so every five minutes the users send to server a new login request. In case any message fails to be delivered, the user may do it too.
