from PyMemAPI import Memrise
from getpass import getpass

FILE = "course.db"


def choose_course():
    # Enter username and password here
    __username__ = input("Enter username: ")
    __password__ = getpass("Enter password: ")

    # Sign in Memrise
    user = Memrise()
    user.login(__username__, __password__)

    # Choose the course
    course = user.select_course()
    return course


if __name__ == "__main__":
    course = choose_course()
    # levels = course.levels()
    # for level in levels:
    #     words = level.get_words()
    #     for word in words:
    #         while word.audio_count > 0:
    #             word.remove_audio()
    course.update_audio("en", custom=True)

# if __name__ == "__main__":
# #     # course = choose_course()

# #     # Read the database find the new levels
#     db = SQLite(f"./course/{FILE}")

# #     # Select the local topics
#     df_topic = db.select_local_topic()

# #     # Retrieval all topics to convert to bulk
# #     # And then connect to MEMRISE add bulk to new level for each topic
#     for idx in range(df_topic.shape[0]):
#         sep = "\t"
# #         # Get topic id & name
#         topic_id = int(df_topic[0][idx])
#         topic_name = df_topic[1][idx]
# #         # Streaming data
#         bulk = db.topic_to_bulk(topic_id, sep, custom=True, language="en")
#         # status = course.add_level_with_bulk(topic_name, bulk, sep)
#         # Validate the status
#         # if status:
#         #     logging.Logger(f"Successful to add level {topic_id}")
#         #     db.switch_status(str(df_topic[0][idx]))
#         # else:
#         #     logging.warning(f"Failed to add level {topic_id}")
#     # Close the database
#     db.close()

#     # Update the audio for each levels
#     # course.update_audio("en", custom=True)
