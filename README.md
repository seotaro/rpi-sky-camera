# rpi-sky-camera

ラズパイで空のタイムラプス撮影を行う。

- 12秒ごとに撮影してローカルディスクに保存する。ただし撮影位置での日の出の30分前から日の入の30分後までに限定する。
- 日中の毎正時にその日の撮影画像で動画を生成する。
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

VSCode の Remote DevelopmentPreview 拡張を使って、ラズパイ実機でデバッグすると便利。
