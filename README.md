# Memrise API

<p align="center"><img src="https://github.com/josephquang97/memrise/actions/workflows/test.yml/badge.svg"><a href="https://codecov.io/github/josephquang97/memrise/commit/8abed823b295beb7ecda8b564df2b81905fb81ad"><img src = "https://codecov.io/gh/josephquang97/memrise/branch/main/graphs/badge.svg?branch=main"></a></p>

## Installation

```
python -m pip install PyMemAPI
```

## Major Features

- API Memrise with some actions such as create new level, add bulk, rename level, ...
- Automaticially generate the audio and upload to Memrise
- Automaticially translate, get the International Phonetics Alphabet from database and sync with Memrise

## Documentations

The library have 3 main classes `Memrise`, `Course` and `SQLite`.

### Memrise

Memrise object will control your connection to Memrise. It's required your username and password to take permissions. And then it'll grant the necessary permission for the further process.

```python
class Memrise:
    username: str = field(init=False)
    password: str = field(init=False)
    session: requests.Session = requests.Session()
	
	def login(self, username, password) -> bool: ...
	def courses(self) -> List[Course]: ...
	def get(self, path: str, params: Optional[Dict[str, Any]] = None): ...
	def post(
        self,
        path: str,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        files: Optional[Dict[str, Tuple[str, bytes, str]]] = None,
    ) -> requests.Response: ...

    def select_course(self) -> Course: ...
```

### Course


### SQLite


