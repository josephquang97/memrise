from PyMemAPI import __version__
from PyMemAPI import Memrise, SQLite, Course
from PyMemAPI.exception import LoginError
import unittest
import io

def test_version():
    assert __version__ == "0.1.0"


# Test Memrise features
class TestMemrise(unittest.TestCase):
    def test_login_fail(self):
        with self.assertRaises(LoginError):
            cli = Memrise()
            cli.login('testingerror','nopassword')

    def test_login_success(self):
        cli = Memrise()
        self.assertTrue(cli.login('dummy_user','testing2022'))

    def test_select_course(self):
        cli = Memrise()
        cli.login('dummy_user','testing2022')
        mock_stdin('1')
        course = cli.select_course()
        self.assertEqual(course.name,"Testing Course")

# Unit test for Course

# @dataclass
# class Client:
#     username: str = field(init=False)
#     password: str = field(init=False)
#     session: requests.Session = requests.Session()

# 	def login(self, username, password): ...
# 	def courses(self): ...
# 	def get(self, path: str, params: Optional[Dict[str, Any]] = None): ...
# 	def post(
#         self,
#         path: str,
#         payload: Dict[str, Any],
#         headers: Dict[str, str],
#         files: Optional[Dict[str, Tuple[str, bytes, str]]] = None,
#     ) -> requests.Response: ...


# @dataclass
# class Word:
#     id: int
#     text: str
#     audio_col: int
#     audio_count: int
#     client: Client

#     def upload_audio(self, audio: Any): ...
#     def remove_audio(self) -> int: ...

# @dataclass
# class Level:
# 	client: Client
# 	schema: LevelSchema
# 	id: int
# 	name: str

# 	def __post_init__(self):
# 		self.id = self.schema.id
# 		self.name = self.schema.title

#     def __init__(self, client: Client, schema: LevelSchema):
#         self.client = client
#         self.schema = schema
#         self.id = self.schema.id
#         self.name = self.schema.title

#     def get_words(self) -> List[Word]: ...

# 	def __parse_words(self, data: Dict[str, Any]) -> List[Word]: ...

# @dataclass
# class Course:
#     def __init__(self, client: Client, schema: CourseSchema):
#         self.client = client
#         self.schema = schema
#         self.id = schema.id
#         self.name = schema.name
#         self.source_lang = schema.source.language_code
#         self.target_lang = schema.target.language_code

#     def levels(self) -> List[Level]: ...
# @pytest.mark.parametrize(
#     "text, language, expected",
#     [
#         ("hello", "am", "həˈloʊ"),
#         ("hello", "br", "hɛˈləʊ"),
#         ("tomato", "am", "təˈmeɪˌtoʊ"),
#         ("tomato", "br", "təˈmɑːtəʊ"),
#     ],
# )
# def test_get_IPA(text, language, expected):
#     assert get_IPA(text, language) == expected


# @pytest.mark.parametrize(
#     "bulk, language, expected",
#     [
#         (["university", "tomato"], "am", ["ˌjunəˈvɜrsəti", "təˈmeɪˌtoʊ"]),
#         (["university", "tomato"], "br", ["ˌjuːnɪˈvɜːsɪti", "təˈmɑːtəʊ"]),
#     ],
# )
# def test_get_IPAs(bulk, language, expected):
#     assert get_IPAs(bulk, language) == expected
