# rpi-sky-camera

ラズパイで空のタイムラプス撮影を行う。

- 10秒ごとに撮影してローカルディスクに保存する。ただし撮影位置での日の出の30分前から日の入の30分後までに限定する。
- 正午（12:00）と日没（17:00、18:00、19:00、20:00）のタイミングで、その日の撮影画像で動画を生成する。
- 生成した動画は Google Cloud Strage にアップロードする。オブジェクト名の時刻はUTC。
- 00:00 にローカルディスクに保存した全画像を削除する。

## GCP の設定

```bash
make create-google-cloud-resources
```

## タイムラプス開始

```bash
make start-sky-camera
```

## タイムラプス停止

```bash
make stop-sky-camera
```

## その他

~コンテナは VS Code の Remote-Containers 拡張を使って開発するため。~
VSCode の Remote DevelopmentPreview 拡張を使って、ラズパイ実機でデバッグすると便利。
