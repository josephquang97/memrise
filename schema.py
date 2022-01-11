import requests, json, logging, re
from bs4 import BeautifulSoup
from typing import List, Optional, Any, Dict, Tuple
from pydantic import BaseModel, HttpUrl
from dataclasses import dataclass, field


URL = "https://app.memrise.com"
UPLOAD_PATH = "/ajax/thing/cell/upload_file/"
DELETE_PATH = "/ajax/thing/column/delete_from/"
COURSE = "https://app.memrise.com/v1.17/courses/{course_id}/"
LEVEL = "https://app.memrise.com/v1.17/courses/{course_id}/levels/"


class LoginError(Exception):
    ...


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
            raise ConnectionError(f"Unexpected response to a POST request': {e}")

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
                    logging.warning(
                        f"Failed to parse learnable {learnable_id} with message: {e}"
                    )
                    audio_count = 0
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
