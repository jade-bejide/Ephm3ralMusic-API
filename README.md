# Ephm3ralMusic-API
![Contributors](https://img.shields.io/github/contributors/jade-bejide/Ephm3ralMusic-API?style=plastic)
![Forks](https://img.shields.io/github/forks/jade-bejide/Ephm3ralMusic-API)
![Stars](https://img.shields.io/github/stars/jade-bejide/Ephm3ralMusic-API)
![Licence](https://img.shields.io/github/license/jade-bejide/Ephm3ralMusic-API)
![Issues](https://img.shields.io/github/issues/jade-bejide/Ephm3ralMusic-API)


This is the Ephm3ralMusic-API, a Python REST-API built using FastAPI and pydantic to provide developers with key data to build music applications. This API is the main 
endpoint for the upcoming Ephm3ral Music web application and is also freely available to all developers worldwide.

## Features
<ul>
 <li>Type Safety using <a href="https://docs.python.org/3/library/typing.html" target="_blank">typing</a>.
  <li>Real time updation of stats for individual applications</li>
</ul>

## Technology Stack
* Language: Python
* Environment: Fly.io
* Framework: FastAPI
* Database: MySQL

## Get Started
*This project is not fully production ready*
<br />
The API endpoint can be accessed via <a href="https://ephm3ral-music.fly.dev/" target="_blank">this webpage</a>.

### Example Code
#### Python

```python
import requests
from pprint import pprint

#fetch all albums
albums_response = requests.get("https://ephm3ral-music.fly.dev/albums")

albums = albums_response.json()

pprint(albums)
```

#### JavaScript

```javascript
const artistAlbums = `https://ephm3ral-music.fly.dev/artist/5/albums`;

//fetch albums by a specific artist
let response = fetch(artistAlbums)
		.then(response => response.json())
		.then(data => console.log(data))
		.catch(error => console.log(error));
```

## Documentation
### Artists

Get all artists (default limit of 10)
<br />
```https://ephm3ral-music.fly.dev/artists```

Get an artist by id
<br />
```https://ephm3ral-music.fly.dev/artist/{id}```

### Songs

Get all songs (default limit of 10)
<br />
```https://ephm3ral-music.fly.dev/songs```

Get all songs by a specific artis, by id
<br />
```https://ephm3ral-music.fly.dev/artist/{id}/songs```

### Albums

Get all albums (default limit of 10)
<br />
```https://ephm3ral-music.fly.dev/albums```

Get all albums by a specific artist, by id
<br />
```https://ephm3ral-music.fly.dev/artist/{id}/albums```

## Example Usages
<ul>
  <li> Music Recommender Systems </li>
  <li> Leaderboard Apps </li>
  <li> Social Media Platforms </li>
 </ul>
