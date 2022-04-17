from datetime import datetime
from uuid import uuid4

from bson.objectid import ObjectId
from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.database.connect import db
from app.schema.response import music as music_resp
from app.schema.entity.file import AudioFile
from app.schema.entity.music import Music, MusicFile, MusicInDB
from app.schema.response.common import RequestMetadata, ResponseMetadata

from app.utils.time import elapsed, time2str

router = APIRouter()


@router.post(
    "/music",
    tags=["Music"]
)
async def upload_music(
    music_name: str,
    singer_name: str,
    music_file: UploadFile
):
    request_time = datetime.now()
    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data={
            "music_name": music_name,
            "singer_name": singer_name,
            "music_file": music_file.filename,
        },
    )

    request_time = datetime.now()
    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data={
            "music_name": music_name,
            "singer_name": singer_name,
            "music_file": music_file.filename,
        },
    )

    # file validation
    # binary = await music_file.read()
    # audio_file = AudioFile(binary, content_type=music_file.content_type)

    # save file in minIO
    # path = await audio_file.save(music_file.filename)
    # path = "/music/12842lalsdfa.wav"

    # save data in DB
    metadata = MusicFile(
        name=music_file.filename,
        # path=path,
        # **audio_file.metadata,
    )
    fileDB = db.file
    file_id = fileDB.insert_one(metadata.dict()).inserted_id
    music = MusicInDB(
        name=music_name,
        singer=singer_name,
        play_total=0,
        file_id=file_id,
    )
    musicDB = db.music
    musicDB.insert_one(music.dict())

    response_time = datetime.now()
    response_metadata = ResponseMetadata(
        request_time=time2str(request_time),
        response_time=time2str(response_time),
        elapsed_time=elapsed(request_time, response_time),
    )
    response = music_resp.UploadMusicResponse(
        request_metadata=request_metadata,
        response_metadata=response_metadata,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(response),
    )

################################################################################


@router.get(
    "/music",
    tags=["Music"]
)
async def get_music_info(
    music_name: str,
    singer_name: str
):
    request_time = datetime.now()
    request_data = dict(music_name=music_name)
    if singer_name:
        request_data.update(dict(singer_name=singer_name))
    request_metadata = RequestMetadata(
        request_id=str(uuid4()),
        request_data=request_data,
    )

    # get music info from mongoDB
    fileDB = db.musicFile
    musicDB = db.music

    music_data = musicDB.find_one(
        {
            "musicName": music_name,
            "singer": singer_name,
        }
    )
    # file_data = fileDB.find_one({"_id": ObjectId(music_data["file_id"])})
    # music = Music(
    #     file=file_data,
    #     **music_data,
    # )

    # response_time = datetime.now()
    # response_metadata = ResponseMetadata(
    #     request_time=time2str(request_time),
    #     response_time=time2str(response_time),
    #     elapsed_time=elapsed(request_time, response_time),
    # )
    # response = music_resp.MusicResponse(
    #     request_metadata=request_metadata,
    #     response_metadata=response_metadata,
    #     music=music,
    # )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(music_data),
    )


@router.get(
    "/musics",
    tags=["Musics"]
)
async def serve_music_chart(
    limit: int
):
    return JSONResponse(
        status_code=status.HTTP_200_OK
    )
