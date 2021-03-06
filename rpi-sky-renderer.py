import os
import tempfile
import ffmpeg
from datetime import datetime, timezone
from google.cloud import storage
import dateutil.tz


def upload(src, dest):
    """Upload the movie to Cloud Storage."""

    client = storage.Client()
    bucket = client.bucket(dest['bucketName'])

    blob = bucket.blob(dest['objectName'])
    blob.upload_from_filename(src)

    print('upload {} {}'.format(dest['bucketName'], dest['objectName']))


def main(directory, hostname, bucket):
    try:
        tz = dateutil.tz.tzlocal()
        now = datetime.now(tz)

        with tempfile.TemporaryDirectory() as temp:
            src = os.path.join(directory,  '*.jpg')

            filename = now.strftime('%Y%m%d-%H%M%S') + '.mp4'
            dest = os.path.join(temp, filename)

            in_options = {'pattern_type': 'glob', 'framerate': 30}
            out_options = {'vcodec': 'h264_omx', 'vb': '5400k', 'r': 30}
            (
                ffmpeg
                .input(src, **in_options)
                .output(dest, **out_options)
                .run()
            )

            upload(dest, {'bucketName': bucket,
                          'objectName': hostname+'-'+filename})

    except Exception as e:
        print(e)


if __name__ == '__main__':
    if os.environ['IMAGE_SEQUENCE_DIRECTORY'] == "":
        print("IMAGE_SEQUENCE_DIRECTORY is empty")

    elif os.environ['MOVIE_BUCKET'] == "":
        print("MOVIE_BUCKET is empty")

    else:
        main(os.environ['IMAGE_SEQUENCE_DIRECTORY'],
             os.uname()[1],
             os.environ['MOVIE_BUCKET'])
