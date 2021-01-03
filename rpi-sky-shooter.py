import os
import pathlib
import picamera
from time import sleep
from datetime import datetime, timedelta, timezone
from astral import Observer
from astral.sun import sun
from PIL import Image, ImageFont, ImageDraw
import dateutil.tz


def drawText(path, text):
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/etc/rpi-sky-camera/NotoSansJP-Regular.otf', 24)
    draw.text((5, 0), text, font=font, fill=(218, 218, 218))
    img.save(path)


def main(directory, observer, daytimeMargin, exposure):
    try:
        tz = dateutil.tz.tzlocal()
        now = datetime.now(tz)
        delte = timedelta(seconds=daytimeMargin)

        s = sun(observer=observer, date=now, tzinfo=tz)
        if now < s["sunrise"] - delte or delte + s["sunset"] < now:
            print("not daytime. sunrise:{}, sunset:{}, margin:{}[sed]".format(
                s["sunrise"], s["sunset"], daytimeMargin))
            return

        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        output = os.path.join(
            directory, now.strftime('%Y%m%d-%H%M%S') + '.jpg')

        # picamera のテキスト出力はフォントと位置が選べないので使わない。
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.awb_mode = 'sunlight'
            camera.iso = exposure['iso']

            sleep(1)

            camera.exposure_mode = 'off'
            camera.shutter_speed = exposure['speed']
            
            camera.capture(output, quality=90)

        # タイムスタンプを描画する。
        drawText(output, now.strftime('%Y-%m-%d %H:%M'))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    if os.environ['IMAGE_SEQUENCE_DIRECTORY'] == "":
        print("IMAGE_SEQUENCE_DIRECTORY is empty")

    elif os.environ['LATITUDE'] == "":
        print("LATITUDE is empty")

    elif os.environ['LONGITUDE'] == "":
        print("LONGITUDE is empty")

    elif os.environ['ISO'] == "":
        print("ISO is empty")

    elif os.environ['SPEED'] == "":
        print("SPEED is empty")

    elif os.environ['DAYTIME_MARGIN'] == "":
        print("DAYTIME_MARGIN is empty")

    else:
        observer = Observer(
            os.environ['LATITUDE'], os.environ['LONGITUDE'])    # 撮影座標

        exposure = {'iso':int(os.environ['ISO']), 'speed':int(os.environ['SPEED'])}

        main(os.environ['IMAGE_SEQUENCE_DIRECTORY'],
             observer, int(os.environ['DAYTIME_MARGIN']), exposure)
