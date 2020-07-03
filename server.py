from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
from album import Album
import album

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# http -f POST localhost:8080/albums/ year=2001 artist=Test genre=rap album=test1

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

  
engine = sa.create_engine(DB_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()


@route("/albums/<artist>")
def albums(artist):
    artist= artist.title() # Приводим первую букву в названии артиста к заглавной

    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        nr_albums = str(len(album_names))
        result = "Всего найдено {} альбомов группы {}:<br><br>".format(nr_albums, artist)
        result += "<br>".join(album_names)
    return result


@route("/albums/", method="POST")
@route("/albums", method="POST")
def save_album():
            
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")
    
    # Проверяем тип данных в поле year
    try:
        year = int(year)   
    except ValueError:
        print("Год выпуска альбома должен состоять из целых чисел, вы ввели: ", year)
    new_album = album.save(year, artist, genre, album_name)
    result = "Альбом #{} успешно сохранен".format(new_album.id)    
    return result



if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)