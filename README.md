# Native-Study-Music

멜론에서 스크랩핑한 음원 정보를 MongoDB에 저장해주는 Service 입니다.

<br>

### DB 스키마

- Collection : `MusicFile`
    
    
    | Attribute | Data Type | Description |
    | --- | --- | --- |
    | fileId | Integer | 음원 파일 ID |
    | fileName | String | 곡명 |
    | sample_width | Integer |  |
    | fileRate | Integer |  |
    | fileChannels | Integer |  |
    | fileSize | Integer | 해당 음원 파일의 사이즈 |
    | fileURL | String | S3에 저장된 해당 음원 파일 URL |
- Collection : `Music`
    
    
    | Attribute | Data Type | Description |
    | --- | --- | --- |
    | musicId | Integer | 음원 ID |
    | musicName | String | 곡명 |
    | singer | String | 가수명 |
    | PlayTotal | Integer | 음원 플레이 횟수 |
    | musicFile | MusicFile | S3에 저장된 해당 음원 파일 정보 |
- Document 예시 :
    
    ```json
    music_file_example = {
        "fileId": "12952",
        "fileName": "12842lalsdfa.wav",
        "sample_width": 2,
        "fileRate": 44100,
        "fileChannels": 2,
        "fileSize": 5023999,
    		"fileURL": "https://ginee-awslearner-bucket.s3.ap-northeast-2.amazonaws.com/image/12842lalsdfa.wav"
    }
    
    music_example = {
        "musicId": 112452,
        "musicName": "다시만난세계",
        "singer": "소녀시대",
        "PlayTotal": 128,
        "musicFile": music_file_example,
    }
    ```
    


<!-- Security scan triggered at 2025-09-02 16:17:14 -->