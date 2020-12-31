import os
import subprocess
import pathlib
from datetime import datetime, timedelta, timezone
from astral import Observer
from astral.sun import sun


def main(directory, observer, daytimeMargin):
    try:
        now = datetime.now(timezone.utc)
        delte = timedelta(seconds=daytimeMargin)

        s = sun(observer, now)
        if now < s["sunrise"] - delte or delte + s["sunset"] < now:
            print("not daytime. sunrise:{}, sunset:{}, margin:{}[sed]".format(
                s["sunrise"], s["sunset"], daytimeMargin))
            return

        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        output = os.path.join(
            directory, now.strftime('%Y%m%d-%H%M%S') + '.jpg')

        result = subprocess.run(['/usr/bin/raspistill',
                                 '--quality', '90',
                                 '--width', '1920',
                                 '--height', '1080',
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

    elif os.environ['DAYTIME_MARGIN'] == "":
        print("DAYTIME_MARGIN is empty")

    else:
        observer = Observer(
            os.environ['LATITUDE'], os.environ['LONGITUDE'])    # 撮影座標

        main(os.environ['IMAGE_SEQUENCE_DIRECTORY'],
             observer, int(os.environ['DAYTIME_MARGIN']))
