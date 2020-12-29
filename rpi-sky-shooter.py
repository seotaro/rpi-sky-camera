import os
import subprocess
from datetime import datetime, timedelta, timezone

TZ_LOCAL = timezone(timedelta(hours=+9), 'JST')


def isDaytime(datetime):
    nowLocal = datetime.astimezone(TZ_LOCAL)

    seconds = nowLocal.hour * 3600 + nowLocal.minute * 60 + nowLocal.second

    # 4時半から19時までを簡易的に日中とした。
    if seconds < 4 * 3600 + 30 * 60 or 19 * 3600 < seconds:
        return False

    return True


def main(directory):
    try:
        now = datetime.now(timezone.utc)
        if not isDaytime(now):
            print("not daytime")
            return

        nowLocal = now.astimezone(TZ_LOCAL)
        output = os.path.join(directory, nowLocal.strftime('%Y%m%d'),
                              nowLocal.strftime('%Y%m%d-%H%M%S') + '.jpg')

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

    else:
        main(os.environ['IMAGE_SEQUENCE_DIRECTORY'])
