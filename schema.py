import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Optional, Any, Dict, Tuple
from pydantic import BaseModel, HttpUrl
from dataclasses import dataclass, field
from memrise import transUntilDone
from text2ipa import get_IPAs
from pathlib import Path
import requests, json, logging, re, pyttsx3, tempfile, sqlite3


URL = "https://app.memrise.com"
UPLOAD_PATH = "/ajax/thing/cell/upload_file/"
DELETE_PATH = "/ajax/thing/column/delete_from/"
# COURSE = "https://app.memrise.com/v1.17/courses/{course_id}/"
# LEVEL = "https://app.memrise.com/v1.17/courses/{course_id}/levels/"
LANGUAGE = {
    "en-gb": [
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
    ],
    "en": [
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0",
    ],
    "fr": [
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR-FR_HORTENSE_11.0",
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_V110_FR-FR_PAUL_11.0",
    ],
    "jp": [
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_HARUKA_11.0",
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_JA-JP_ICHIRO_11.0",
    ],
}

TAG_XML = """<set xml=true><VOICE REQUIRED="NAME={name}"><rate speed="{speed}" ><silence msec="100"/>{text}<silence msec="100"/>"""
CUSTOM = {
    "en": [
        # 'VW Bridget',
        "VW Julie",
        # 'VW Kate',
        "VW Paul",
    ],
    "jp": ["VW Misaki"],
}


class InvalidSeperateElement(Exception):
    """Language is not supported ERROR"""

    def __init__(self, sep: str, message: str):
        self._sep = sep
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return f"sep = {self._sep} : {self._message}"


class UnSupportLanguage(Exception):
    """Language is not supported ERROR"""

    def __init__(self, language: str, message: str):
        self._language = language
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return f"Language {self._language} : {self._message}"


class LoginError(Exception):
    ...


class AddLevelError(Exception):
    """Add Level Exception Handle"""

    def __init__(self, id: str, message: str):
        self._id = id
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return f"Course ID {self._id} : {self._message}"


class AddBulkError(Exception):
    """Add Bulk Exception Handle"""

    def __init__(self, id: str, message: str):
        self._id = id
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return f"Add Bulk Error Item ID {self._id}: {self._message}"


class ConnectionError(Exception):
    ...


class JSONParseError(Exception):
    ...


class InputOutOfRange(Exception):
    """Exception raised for errors in the input option which's out of range.

    Attributes:
        input value -- the number input option
        message -- explanation of the error
    """

    def __init__(self, option: int, message: str):
        self.option = option
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Input value: {self.option} -> {self.message}"


def concat(words: str):
    mywords = re.findall("\\w+", words.lower())
    retstr = ""
    for myword in mywords:
        retstr += myword[0].upper() + myword[1:]
    return retstr


def custom_audio(language: str, text: str) -> None:
    if language not in CUSTOM.keys():
        raise UnSupportLanguage(language=language, message="Not support.")
    else:
        voices: List[str] = CUSTOM[language]

    for voice in voices:
        vname = voice.replace(" ", "")
        filename = concat(text)
        Path(f"./custom/{vname}/").mkdir(parents=True, exist_ok=True)
        with open(f"./custom/{vname}/{filename}.txt", "w") as fp:
            fp.seek(0)
            fp.write(TAG_XML.format(name=voice, speed=-2, text=text))


class Category(BaseModel):
    name: str
    photo: HttpUrl


class Language(BaseModel):
    """Memrise course language."""

    id: int
    slug: str
    name: str
    photo: HttpUrl
    parent_id: int
    index: int
    language_code: str


class CourseSchema(BaseModel):
    """Memrise course schema."""

    id: int
    name: str
    slug: str
    url: str
    description: str
    photo: HttpUrl
    photo_small: HttpUrl
    photo_large: HttpUrl
    num_things: int
    num_levels: int
    num_learners: int
    source: Language
    target: Language
    learned: int
    review: int
    ignored: int
    ltm: int
    difficult: int
    category: Category
    percent_complete: int


class CourseList(BaseModel):
    courses: List[CourseSchema]
    to_review_total: int
    has_more_courses: bool


class EditLevel(BaseModel):
    """Learnable is present for vocabulary"""

    success: bool
    rendered: str


class LevelSchema(BaseModel):
    """Level schema"""

    id: int
    index: int
    kind: int
    title: str
    pool_id: int
    course_id: int
    learnable_ids: List[int]


class LevelList(BaseModel):
    """List of level schema"""

    levels: List[LevelSchema]
    version: str


@dataclass
class Client:
    username: str = field(init=False)
    password: str = field(init=False)
    session: requests.Session = requests.Session()

    def login(self, username, password):
        try:
            res = self.session.get(f"{URL}/login/", timeout=30)
        except requests.RequestException as e:
            raise LoginError(f"LoginError with message: {e}")

        payload = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": res.cookies["csrftoken"],
        }

        try:
            response = self.session.post(
                f"{URL}/login/",
                data=payload,
                headers={"Referer": f"{URL}/login/"},
                timeout=30,
            )
        except requests.RequestException as e:
            print(e)
            exit()

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if res.status_code == 403:
                raise LoginError(f"Authentication failed: {e}")
            else:
                raise LoginError(f"Unexpected response during login: {e}")

    def courses(self):
        """Retrieve the courses to which the logged in user has edit permissions."""
        all_courses: List[Course] = []
        has_more_courses = True
        offset = 0
        while has_more_courses:
            data = self.get(
                "/ajax/courses/dashboard/",
                params={
                    "courses_filter": "teaching",
                    "get_review_count": "false",
                    "offset": offset,
                    "limit": 8,
                },
            )
            course_list = CourseList(**data)
            has_more_courses = course_list.has_more_courses
            offset += 9
            all_courses.extend(Course(self, schema) for schema in course_list.courses)
        return all_courses

    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        try:
            response = self.session.get(
                f"{URL}{path}",
                params=params,
                timeout=10,
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Get request failed: {e}")

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise ConnectionError(f"Unexpected response for a GET request: {e}")

        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            raise JSONParseError(f"Invalid JSON response for a GET request: {e}")

        return data

    def post(
        self,
        path: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        files: Optional[Dict[str, Tuple[str, bytes, str]]] = None,
    ) -> requests.Response:
        """Send POST request. Each POST request is NEED a CSRF TOKEN."""
        payload["csrfmiddlewaretoken"] = self.session.cookies["csrftoken"]
        try:
            response = self.session.post(
                f"{URL}{path}",
                files=files,
                headers=headers,
                data=payload,
                timeout=20,
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"POST request failed': {e}")

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print(response.content)
            raise ConnectionError(f"Unexpected response to a POST request': {e}")
            # pass

        return response


@dataclass
class Word:
    id: int
    text: str
    audio_col: int
    audio_count: int
    client: Client

    def upload_audio(self, audio: Any):
        if isinstance(audio, str):
            with open(audio, "rb") as fp:
                files = {"f": ("audio.mp3", fp.read(), "audio/mp3")}
        elif isinstance(audio, bytes):
            files = {"f": ("audio.mp3", audio, "audio/mp3")}
        else:
            raise TypeError(f"Expected 'str' or 'bytes', but {type(audio)}")

        payload = {
            "thing_id": self.id,
            "cell_id": self.audio_col,
            "cell_type": "column",
        }

        self.client.post(
            path=UPLOAD_PATH,
            files=files,
            headers={"Referer": "https://app.memrise.com/course"},
            payload=payload,
        )

    def remove_audio(self) -> int:
        """Remove all audio from a learnable."""
        for file_id in range(1, self.audio_count + 1):
            payload = {
                "thing_id": self.id,
                "column_key": self.audio_col,
                "cell_type": "column",
                "file_id": file_id,
            }
            try:
                self.client.post(
                    path=DELETE_PATH,
                    headers={"Referer": "https://app.memrise.com/course"},
                    payload=payload,
                )
            except ConnectionError as e:
                print(f"Failed to remove audio audio file ID {file_id}: {e}")
                continue

            self.audio_count -= 1
        return self.audio_count


class Level:
    def __init__(self, client: Client, schema: LevelSchema):
        self.client = client
        self.schema = schema
        self.id = self.schema.id
        self.name = self.schema.title

    def get_words(self) -> List[Word]:
        """Retrieve learnables in a level."""
        data = self.client.get(f"/ajax/level/editing_html/?level_id={self.id}")
        return self.__parse_words(data)

    def __parse_words(self, data: Dict[str, Any]) -> List[Word]:
        """Parse learnables (words) from Memrise API response."""
        level: EditLevel = EditLevel(**data)
        learnables: List[Word] = []

        # from lxml import html
        # tree = html.fromstring(level.rendered)
        # learnables_html = tree.xpath("//tr[contains(@class, 'thing')]")
        # for learnable in learnables_html:
        #     learnable_id = learnable.attrib["data-thing-id"]
        #     try:
        #         learnable_text = learnable.xpath("td[2]/div/div/text()")[0]
        #         column_number = learnable.xpath("td[contains(@class, 'audio')]/@data-key")[0]
        #     except IndexError:
        #         logging.warning("Failed to parse learnable id %s", learnable_id)
        #         continue
        #     audio_count = len(
        #         learnable.xpath(
        #             "td[contains(@class, 'audio')]/div/div[contains(@class, 'dropdown-menu')]/div"
        #         )
        #     )
        # ---------------------------------------------------------------------------------------
        soup = BeautifulSoup(level.rendered, "html.parser")
        tags = soup("tr", {"class": "thing"})
        column_number = soup.find("th", {"class": "column audio"})["data-key"]
        for tag in tags:
            item = tag.get("data-thing-id")
            if item is not None:
                learnable_id = item
                learnable_text = tag.text.split("\n")[2].strip()
                numbers = re.findall("\\d+", tag.text)
                try:
                    audio_count = int(numbers[-1])
                except IndexError as e:
                    audio_count = 0
                    print(f"Word `{learnable_text}`: 0 audios")
                    pass
            # Using the others instead ---------------------------------------------------------------
            learnables.append(
                Word(
                    client=self.client,
                    id=learnable_id,
                    text=learnable_text,
                    audio_col=column_number,
                    audio_count=audio_count,
                )
            )

        return learnables


class Course:
    def __init__(self, client: Client, schema: CourseSchema):
        self.client = client
        self.schema = schema
        self.id = schema.id
        self.name = schema.name
        self.source_lang = schema.source.language_code
        self.target_lang = schema.target.language_code

    def levels(self) -> List[Level]:
        """Retrieve course's levels."""
        data = self.client.get(f"/v1.17/courses/{self.id}/levels/")
        level_list = LevelList(**data)
        return [Level(self.client, schema) for schema in level_list.levels]

    def delete_level(self, level_id) -> None:
        data = {"level_id": f"{level_id}"}
        headers = {"Referer": f"https://app.memrise.com/course/{self.id}/edit/"}
        self.client.post("/ajax/level/delete/", payload=data, headers=headers)

    def set_level_title(
        self, level_id: str, new_val: str, headers: Dict[str, str]
    ) -> requests.Response:
        payload = {"level_id": f"{level_id}", "new_val": new_val}
        response = self.client.post(
            "/ajax/level/set_title/", payload=payload, headers=headers
        )
        # Validation status change name
        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            raise JSONParseError(f"Invalid JSON response for a GET request: {e}")
        else:
            status = data["success"]
            if status == False:
                logging.warning(f"Failed to rename the level {level_id}")
        return response

    def add_bulk(
        self, level_id: str, bulk: str, sep: str, headers: Dict[str, str]
    ) -> bool:
        """Add bulk for the level."""

        payload = {
            "word_delimiter": sep,
            "data": bulk,
            "level_id": level_id,
        }
        response = self.client.post(
            "/ajax/level/add_things_in_bulk/", payload=payload, headers=headers
        )
        # Validation status:
        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            raise JSONParseError(f"Invalid JSON response for a GET request: {e}")
        else:
            status = data["success"]
            if status == False:
                raise AddBulkError(id=level_id, message="Failed to Add Bulk.")
        return status

    def add_level(self) -> Tuple[str, Dict[str, str]]:
        """Add a new level in the course."""
        # Get the pool_id
        res = self.client.session.get(f"{URL}/course/{self.id}/any/edit/")
        soup = BeautifulSoup(res.content, "html.parser")
        tag = soup.find("div", {"class": "level collapsed"})
        data = {
            "course_id": f"{self.id}",
            "kind": "things",
            "pool_id": tag["data-pool-id"],
        }
        headers = {"Referer": f"{res.url}"}
        response = self.client.post("/ajax/level/add/", payload=data, headers=headers)

        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            raise AddLevelError(
                id=self.id,
                message=f"Invalid JSON response for a adding level request: {e}",
            )
        else:
            level_id = data["redirect_url"].split("_")[-1]

        return level_id, headers

    def add_level_with_bulk(self, name: str, bulk: str, sep: str) -> bool:
        """Add new level with bulk data."""
        # Validation for seperate parameter must be comma or tab
        if sep not in ["\t", ","]:
            raise InvalidSeperateElement(
                sep=sep, message="seperate paramater must be tab or comma."
            )
        else:
            word_delimiter = "tab" if sep == "\t" else "comma"
        # Part1: Add new level
        level_id, headers = self.add_level()

        # Part2: Rename the level title
        response = self.set_level_title(level_id, name, headers)

        # Part3: Add bulk request
        try:
            status = self.add_bulk(level_id, bulk, word_delimiter, headers)
        except ConnectionError as e:
            status = False
            self.delete_level(level_id)
            logging.warning(f"Failed to add level with bulk {level_id}: {e}")
        return status

    def update_audio(self, language: str, speed: int = 170, custom: bool = False):
        if language not in LANGUAGE.keys():
            raise UnSupportLanguage(
                language=language,
                message="Not support. Please download the new packages.",
            )
        else:
            voices: List[str] = LANGUAGE[language]
            __number_audio_you_wish__ = len(voices)
        # ---------------------------------------------
        mod = pyttsx3.init()
        mod.setProperty("rate", speed)
        for voice in voices:
            mod.setProperty("voice", voice)
            levels = self.levels()
            tempFolder = tempfile.TemporaryDirectory()
            for level in levels:
                print(f"Retriveing the level name `{level.name}`")
                words = level.get_words()
                for idx in range(len(words)):
                    if words[idx].audio_count >= __number_audio_you_wish__:
                        continue
                    filename = concat(words[idx].text)
                    if custom:
                        voices: List[str] = CUSTOM[language]
                        for voice in voices:
                            vname = voice.replace(" ", "")
                            words[idx].upload_audio(f"./custom/{vname}/{filename}.mp3")
                    else:
                        mod.save_to_file(
                            words[idx].text,
                            f"{tempFolder.name}/{idx:02}_{filename}.mp3",
                        )
                        mod.runAndWait()
                        words[idx].upload_audio(
                            f"{tempFolder.name}/{idx:02}_{filename}.mp3"
                        )


@dataclass
class Memrise(Client):
    def select_course(self):
        courses = self.courses()
        print("All courses: ")
        for indx in range(1, 1 + len(courses)):
            print(f"{indx}. {courses[indx-1].name}")
        choice = input("Make your choice: ")
        try:
            indx_choice = int(choice)
        except ValueError as e:
            raise ValueError(f"Input error with message: {e}")

        if indx_choice not in range(1, 1 + len(courses)):
            raise InputOutOfRange(
                indx_choice, f"Your choice out of range [1,{len(courses)}]"
            )
        return courses[indx_choice - 1]


INSERT_STATEMENT = (
    """INSERT INTO "sentense" ("sentense", "meaning", "topic") VALUES (?, ?, ?);"""
)
SELECT_NULL_MEANING = """SELECT "sentense" FROM sentense WHERE meaning is NULL;"""
SELECT_NULL_IPA = """SELECT "sentense" FROM sentense WHERE ipa is NULL;"""
UPDATE_MEANING = """UPDATE sentense SET meaning = ? WHERE sentense = ? ;"""
UPDATE_IPA = """UPDATE sentense SET ipa = ? WHERE sentense = ? ;"""
TOPIC_LOCAL = """SELECT id, name FROM topic WHERE status = 'local';"""
TOPIC_STREAM = """SELECT id, name FROM topic WHERE status = 'stream';"""
SENS_IN_TOPIC = (
    """SELECT "sentense", "meaning", "ipa" FROM "sentense" WHERE topic_id = ? ;"""
)
UPDATE_STATUS = """UPDATE topic SET status = 'stream' WHERE id = ? ;"""


@dataclass
class SQLite:
    filename: str
    conn: sqlite3.Connection = field(init=False)
    cur: sqlite3.Cursor = field(init=False)

    def __post_init__(self):
        self.conn = sqlite3.Connection(self.filename)
        self.cur = self.conn.cursor()

    def update_trans(self, src: str, dest: str):
        """Translation automatiacilly"""
        self.cur.execute(SELECT_NULL_MEANING)
        df = pd.DataFrame(self.cur.fetchall())
        bulk = transUntilDone(
            [item.lower() for item in list(df[0])], src=src, dest=dest, sep="\n\r"
        )

        for idx in range(len(bulk)):
            self.cur.execute(UPDATE_MEANING, (bulk[idx], df[0][idx]))

        self.conn.commit()

    def switch_status(self, topic_id: str):
        """Switch the status of the specific topic by id."""
        self.cur.execute(UPDATE_STATUS, (topic_id,))
        self.conn.commit()

    def update_ipas(self):
        """Convert and Update text to Internatioanl Phonetic Aplabets automaticially."""
        self.cur.execute(SELECT_NULL_IPA)
        df = pd.DataFrame(self.cur.fetchall())
        bulk = get_IPAs(list(df[0]), "am")

        for idx in range(len(bulk)):
            self.cur.execute(UPDATE_IPA, (bulk[idx], df[0][idx]))

        self.conn.commit()

    def select_local_topic(self) -> pd.DataFrame:
        """Select all local topics."""
        self.cur.execute(TOPIC_LOCAL)
        __df = pd.DataFrame(self.cur.fetchall())
        return __df

    def topic_to_bulk(
        self, topic_id: int, sep="\t", custom: bool = False, language: str = ""
    ) -> str:
        """Convert the content of topic to bulk text."""
        bulk: str = ""
        df = self.__select_sentense_in_topic(topic_id)
        for idx in range(df.shape[0]):
            __learable: str = df[0][idx]
            __meaning: str = df[1][idx]
            __ipa: str = df[2][idx]
            if custom:
                if language == "":
                    raise Exception("Missing language parameter.")
                custom_audio(language, __learable.lower())
            bulk += f"{__learable}{sep}{__meaning}{sep}{__ipa}\n"
        return bulk

    def __select_sentense_in_topic(self, topic_id: int) -> pd.DataFrame:
        """Local method: Select a specific topic by id."""
        self.cur.execute(SENS_IN_TOPIC, (topic_id,))
        __df = pd.DataFrame(self.cur.fetchall())
        return __df

    def close(self):
        """Close the database."""
        self.cur.close()
        self.conn.commit()
        self.conn.close()
