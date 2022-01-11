from schema import Memrise
from getpass import getpass
import pyttsx3, re, tempfile

ENGLISH_GB = (
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
)

ENGLISH = [
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
]

FRENCH = [
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_V110_FR-FR_PAUL_11.0",
]

JAPAN = [
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_ICHIRO_11.0",
]


def concat(words: str):
    mywords = re.findall("\\w+", words.lower())
    retstr = ""
    for myword in mywords:
        retstr += myword[0].upper() + myword[1:]
    return retstr


if __name__ == "__main__":
    # Enter username and password here
    __username__ = input("Enter username: ")
    __password__ = getpass("Enter password: ")
    __number_audio_you_wish__ = 2
    __voice__ = ENGLISH[1]
    __rate__ = 175  # Default is 200
    # ---------------------------------------------
    mod = pyttsx3.init()
    mod.setProperty("voice", __voice__)
    mod.setProperty("rate", __rate__)  # Default 200

    user = Memrise()
    user.login(__username__, __password__)
    course = user.select_course()
    levels = course.levels()
    tempFolder = tempfile.TemporaryDirectory()
    for level in levels:
        print(f"Retriveing the level name `{level.name}`")
        words = level.get_words()
        for idx in range(len(words)):
            if words[idx].audio_count >= __number_audio_you_wish__:
                continue
            filename = concat(words[idx].text)
            mod.save_to_file(
                words[idx].text, f"{tempFolder.name}/{idx:02}_{filename}.mp3"
            )
            mod.runAndWait()
            words[idx].upload_audio(f"{tempFolder.name}/{idx:02}_{filename}.mp3")
