from getpass import getpass
from schema import SQLite, Memrise
import logging

PATH = "C:\\Users\\JosephQuang\\Desktop\\ELSA\\"
FILE = "Innovation.db"


if __name__ == "__main__":
    # Enter username and password here
    __username__ = input('Enter username: ')
    __password__ = getpass('Enter password: ')
    user = Memrise()
    user.login(__username__, __password__)
    course = user.select_course()
    # df = pd.read_csv('vocabulary.csv',encoding='utf-16',sep='\t', header=None)
    db = SQLite(f"{PATH}{FILE}")
    df_topic = db.select_local_topic()  # id | topic
    for idx in range(df_topic.shape[0]):
        bulk = db.topic_to_bulk(int(df_topic[0][idx]))
        status = course.add_level_with_bulk(df_topic[1][idx], bulk, "tab")
        if status:
            logging.warning(f"Successful to add level {df_topic[0][idx]}")
            db.switch_status(str(df_topic[0][idx]))
        else:
            logging.warning(f"Failed to add level {df_topic[0][idx]}")
    db.close()
