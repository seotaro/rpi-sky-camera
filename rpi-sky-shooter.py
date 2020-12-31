import os
import subprocess
import pathlib
from datetime import datetime, timezone
from astral import Observer
from astral.sun import sun


def main(directory, observer):
    try:
        now = datetime.now(timezone.utc)

        s = sun(observer, now)
        if now < s["sunrise"] or s["sunset"] < now:
            print("not daytime. sunrise:{}, sunset:{}".format(
                s["sunrise"], s["sunset"]))
            return

        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        output = os.path.join(
            directory, now.strftime('%Y%m%d-%H%M%S') + '.jpg')

        result = subprocess.run(['/usr/bin/raspistill',
                                 '--quality', '90',
                                 '--awb', 'sun',
                                 '--timeout', '1000',
                                 '--output', output])

        if result.returncode != 0:
            raise Exception("error raspistill command")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    if os.environ['IMAGE_SEQUENCE_DIRECTORY'] == "":
        print("IMAGE_SEQUENCE_DIRECTORY is empty")

    elif os.environ['LATITUDE'] == "":
        print("LATITUDE is empty")

    elif os.environ['LONGITUDE'] == "":
        print("LONGITUDE is empty")

    else:
        observer = Observer(
            os.environ['LATITUDE'], os.environ['LONGITUDE'])    # 撮影座標

        main(os.environ['IMAGE_SEQUENCE_DIRECTORY'], observer)
