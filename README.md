# anime-checker.py
A python script to automatically check whether my favorite animes have been updated and notify me by email

by Eason Chang <eason@easonchang.com>

## Description
You should run this script with **python3**.

This script does a one-time check.

This script contains **2 config files**:

- **.env**        : stores environment variables of my email addresses and 
                    password.
- **animes.json** : stores a list of my favorite animes, including title,
                    website url, and current episode number.
## Installation

### 1. Edit your own .env: 
Replace your own email addresses and password in **.env-example**, and rename it to **.env**

### 2. Edit your own animes list in animes.json:
Add your own animes in **animes-example.json** (should follow the format), and rename it to **animes.json**

### 3. Change script file mode:
Add execute permission to **anime-checker.py**
```
chmod a+x /path/to/your/anime-checker.py
```

### 4. Set this script as a scheduled job using crontab:
```
crontab -e
```
Add this line at the buttom of the file (execute every 30 minutes):
```
*/30 * * * * /path/to/your/anime-checker.py
```
