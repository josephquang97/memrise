import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")
voice = voices[3]

# languages = engine.getProperty("languages")
ENGINE = pyttsx3.init()
VOICES = ENGINE.getProperty("voices")


def info_voice():
    for idx in range(len(VOICES)):
        print(f"{idx+1}. {VOICES[idx].name}")


info_voice()
