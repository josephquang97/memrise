# memrise
Memrise Upload Auto with TTS Local

### Required Library

```
python -m pip install pyttsx3
python -m pip install pydantic
python -m pip install requests
```

## How to use the `pydantic`

Let create new a file *json* with the following content:

`myjson.json`
```json
{"courses": [{"id": 6131624, "name": "Dummy", "slug": "dummy", "url": "/course/6131624/dummy/", "description": "", "photo": "https://static.memrise.com/garden/img/placeholders/course-4.png", "photo_small": "https://static.memrise.com/garden/img/placeholders/course-4.png", "photo_large": "https://static.memrise.com/garden/img/placeholders/course-4.png", "num_things": 3, "num_levels": 2, "num_learners": 1, "source": {"id": 474, "slug": "vietnamese", "name": "Vietnamese", "photo": "https://static.memrise.com/uploads/category_photos/vietnamese.png", "parent_id": 614, "index": 966, "language_code": "vi"}, "target": {"id": 6, "slug": "english", "name": "English", "photo": "https://static.memrise.com/uploads/category_photos/en.png", "parent_id": 578, "index": 1051, "language_code": "en"}, "learned": 0, "review": 0, "ignored": 0, "ltm": 0, "difficult": 0, "category": {"name": "English", "photo": "https://static.memrise.com/uploads/category_photos/en.png"}, "next_session": {"recommendation_id": "3d0d34b4-41f1-454b-a019-150d67787e87", "next_session": {"session_type": "learn", "is_enabled": true, "counter": 0, "url": "/aprender/learn?course_id=6131624?recommendation_id=3d0d34b4-41f1-454b-a019-150d67787e87", "is_pro": false}, "selector": [], "is_unlocked": false}, "percent_complete": 0}], "to_review_total": 0, "has_more_courses": true}
```

#### The json file has 3 major informations:

- courses : this informations has list datatype
- to_review_total : has the integer type
- has_more_courses : has the boolean type

Therefore, we will implement a class with as the following


```python
import pydantic
import json


class MyCourse(pydantic.BaseModel):
    courses: list
    to_review_total: int
    has_more_courses: bool
    
if __name__ == "__main__":
    with open('myjson.json') as file:
        data = json.load(file) # convert to dictionary
        mycourse: MyCourse = MyCourse(**data)
    
    # Now figure it out
    # First information
    print('First information:',mycourse.courses)
    # Second information
    print('Second information:',mycourse.to_review_total)
    # Final information
    print('Final information:',mycourse.has_more_courses)
```

    First information: [{'id': 6131624, 'name': 'Dummy', 'slug': 'dummy', 'url': '/course/6131624/dummy/', 'description': '', 'photo': 'https://static.memrise.com/garden/img/placeholders/course-4.png', 'photo_small': 'https://static.memrise.com/garden/img/placeholders/course-4.png', 'photo_large': 'https://static.memrise.com/garden/img/placeholders/course-4.png', 'num_things': 3, 'num_levels': 2, 'num_learners': 1, 'source': {'id': 474, 'slug': 'vietnamese', 'name': 'Vietnamese', 'photo': 'https://static.memrise.com/uploads/category_photos/vietnamese.png', 'parent_id': 614, 'index': 966, 'language_code': 'vi'}, 'target': {'id': 6, 'slug': 'english', 'name': 'English', 'photo': 'https://static.memrise.com/uploads/category_photos/en.png', 'parent_id': 578, 'index': 1051, 'language_code': 'en'}, 'learned': 0, 'review': 0, 'ignored': 0, 'ltm': 0, 'difficult': 0, 'category': {'name': 'English', 'photo': 'https://static.memrise.com/uploads/category_photos/en.png'}, 'next_session': {'recommendation_id': '3d0d34b4-41f1-454b-a019-150d67787e87', 'next_session': {'session_type': 'learn', 'is_enabled': True, 'counter': 0, 'url': '/aprender/learn?course_id=6131624?recommendation_id=3d0d34b4-41f1-454b-a019-150d67787e87', 'is_pro': False}, 'selector': [], 'is_unlocked': False}, 'percent_complete': 0}]
    Second information: 0
    Final information: True
    

#### More details :
As we can see that the *courses* information is a list of the course which has many informations inside. So, we can build the class *course* with the new schema as the following program:


```python
import pydantic
import json
from typing import List

class course(pydantic.BaseModel):
    """course schema."""

    id: int
    name: str
    slug: str
    url: str
    description: str
    photo: str
    photo_small: str
    photo_large: str
    num_things: int
    num_levels: int
    num_learners: int
    source: dict
    target: dict
    learned: int
    review: int
    ignored: int
    ltm: int
    difficult: int
    category: dict
    percent_complete: int

class MyCourse(pydantic.BaseModel):
    courses: List[course]
    to_review_total: int
    has_more_courses: bool
    
if __name__ == "__main__":
    with open('myjson.json') as file:
        data = json.load(file) # convert to dictionary
        mycourse: MyCourse = MyCourse(**data)
    
    # Now figure it out
    # First information
    course = mycourse.courses[0]
    print('id:', course.id)
    print('name:', course.name)
    print('slug:', course.slug)
    print('url:', course.url)
    print('description:', course.description)
    print('photo:', course.photo)
    print('photo_small:', course.photo_small)
    print('photo_large:', course.photo_large)
    print('num_things:', course.num_things)
    print('num_levels:', course.num_levels)
    print('num_learners:', course.num_learners)

```

    id: 6131624
    name: Dummy
    slug: dummy
    url: /course/6131624/dummy/
    description: 
    photo: https://static.memrise.com/garden/img/placeholders/course-4.png
    photo_small: https://static.memrise.com/garden/img/placeholders/course-4.png
    photo_large: https://static.memrise.com/garden/img/placeholders/course-4.png
    num_things: 3
    num_levels: 2
    num_learners: 1
    

## Extract data from html type


```python
from bs4 import BeautifulSoup

class EditStatus(BaseModel):
    """Learnable is present for vocabulary"""
    success: bool
    rendered: str
    
class MyLevelSchema(BaseModel):
    """Level schema"""
    id: int
    index: int
    kind: int
    title: str
    pool_id: int
    course_id: int
    learnable_ids: List[int]

class MyListLevel(BaseModel):
    """List of level schema"""
    levels: List[MyLevelSchema]
    version: str
```


```python
with open('./myjsons/levels.json') as file:
    data = json.load(file)
    mydata: MyListLevel = MyListLevel(**data)
with open('./myjsons/editing_level.json') as file:
    data = json.load(file)
    mydata2: EditStatus = EditStatus(**data)
```


```python
mydata.levels[0].learnable_ids[1]
```




    20945127407874



### Extract with BeautifulSoup


```python
soup2 = BeautifulSoup(mydata2.rendered,'html.parser')
```


```python
with open('index.html','w',encoding='utf-8') as fp:
    fp.seek(0)
    fp.write(mydata2.rendered)
```


```python
# <th class="column audio" data-key="3" data-role="pool-column-header"><span class="txt">Audio</span>
# <i class="ico ico-edit ico-blue"></i></th>
# get data-key
tags = soup("th",{"class":"column audio"})
for tag in tags:
    print(tag["data-key"])
# Figure out the column which store audio
audio_col = soup.find("th",{"class":"column audio"})["data-key"]
print('Audio column:', audio_col)
```

    3
    Audio column: 3
    

### Figure out the word_id and the number of audio existing with relugar expression


```python
import re
tags = soup2("tr",{"class":"thing"})
for tag in tags:
    item = tag.get("data-thing-id")
    if item is not None:
        learnable_id = item
        learnable_text = tag.text.split('\n')[2].strip()
        try:
            audios = re.findall("\\d+",tag.text)
            audio_count = int(audios[-1])
        except IndexError as e:
            audio_count = 0
        print(f'{learnable_id} - {audio_count} audio files - {learnable_text}')
```

    319506819 - 2 audio files - she studied ALL night for her CHEMISTRY final.
    319506820 - 2 audio files - we WORKED for HOURS on our MATH assignment.
    319506821 - 2 audio files - he FORGOT to HAND in his ESSAY.
    319506822 - 2 audio files - she POINTED out a SILLY mistake I had MADE.
    319506823 - 2 audio files - that's your END OF YEAR project.
    

### Extract with the library `lxml`


```python
from lxml import html
tree = html.fromstring(mydata2.rendered)
```

### Find all the tag *`<tr>`* with the item *"thing"*

The characters **'//'** to inform that the tag *`<tr>`* is hide below the others tags


```python
learnables_html = tree.xpath("//tr[contains(@class, 'thing')]")
```


```python
for learnable in learnables_html:
    learnable_id = learnable.attrib["data-thing-id"]
    learnable_text = learnable.xpath("td[2]/div/div/text()")[0]
    column_number = learnable.xpath("td[contains(@class, 'audio')]/@data-key")[0]
    audio_count = learnable.xpath(
                    "td[contains(@class, 'audio')]/div/div[contains(@class, 'dropdown-menu')]/div"
                )
    print(f'{learnable_id} - {len(audio_count)} audio files - {learnable_text}')
print('Audio column:', column_number)
```

    319506819 - 2 audio files - she studied ALL night for her CHEMISTRY final.
    319506820 - 2 audio files - we WORKED for HOURS on our MATH assignment.
    319506821 - 2 audio files - he FORGOT to HAND in his ESSAY.
    319506822 - 2 audio files - she POINTED out a SILLY mistake I had MADE.
    319506823 - 2 audio files - that's your END OF YEAR project.
    Audio column: 4
    

### Explaining

The code below:
```python
learnable_text = learnable.xpath("td[2]/div/div/text()")[0]
```
Get the text inside of the tag `<div class="text">she studied ALL night for her CHEMISTRY final.</div>`
```xml
<td>
    <div class="text">
    <button><div class="text">Alts</div></button> Upload file here
        <div class="text">she studied ALL night for her CHEMISTRY final.</div>
    </div>
</td>
```
