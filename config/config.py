from enum import Enum
import os


db_file = "config/database.vdb"

rel_path = "bet_num.txt"
abs = os.path.join(script_dir, rel_path)

f = open(os.path.join(script_dir, 'bet_num.txt'), 'r', encoding='utf-8')
sumBet = int(f.read())
f.close()#кол-во необходимых заявок

#price = '10'

class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_CITY = "1"
