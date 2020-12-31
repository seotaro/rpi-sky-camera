import os
import subprocess
import tempfile
from datetime import datetime, timezone
from google.cloud import storage


def upload(src, dest):
    """Upload the movie to Cloud Storage."""

    client = storage.Client()
    bucket = client.bucket(dest['bucketName'])

    blob = bucket.blob(dest['objectName'])
    blob.upload_from_filename(src)

    print('upload {} {}'.format(dest['bucketName'], dest['objectName']))


def main(directory, camera, bucket):
    try:
        now = datetime.now(timezone.utc)

        with tempfile.TemporaryDirectory() as temp:
            src = os.path.join(directory,  '*.jpg')

            filename = now.strftime('%Y%m%d-%H%M%S') + '.mp4'
            dest = os.path.join(temp, filename)

            result = subprocess.run(['ffmpeg', '-framerate', '30',
                                     '-pattern_type', 'glob', '-i', src,
                                     '-s', '1920x1080',
                                     '-vcodec', 'h264_omx',
                                     '-vb', '5400k',
                                     '-r', '30',
                                     dest])

            if result.returncode != 0:
                raise Exception("error ffmpeg command")

            upload(dest, {'bucketName': bucket,
                          'objectName': camera+'-'+filename})

    except Exception as e:
        print(e)


if __name__ == '__main__':
    if os.environ['IMAGE_SEQUENCE_DIRECTORY'] == "":
        print("IMAGE_SEQUENCE_DIRECTORY is empty")

    elif os.environ['MOVIE_BUCKET'] == "":
        print("MOVIE_BUCKET is empty")

    elif os.environ['CAMERA_ID'] == "":
        print("CAMERA_ID is empty")

    else:
        main(os.environ['IMAGE_SEQUENCE_DIRECTORY'],
             os.environ['CAMERA_ID'],
             os.environ['MOVIE_BUCKET'])
