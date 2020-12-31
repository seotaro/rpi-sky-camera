# rpi-sky-camera

ラズパイで空のタイムラプス撮影を行う。

- 日中のみt秒ごとに撮影してローカルディスクに保存する。
- 日中は撮影位置での日の出から日の入まで。
- 12:00、17:00、18:00、19:00にその日の撮影画像でエンコードした動画を Google Cloud Strage にアップロードする。
- 00:10 にローカルディスクに保存した全画像を削除する。
- 生成する動画のファイル名の時刻はUTCとする。

## GCP の設定

PC で下記を実行する。

```bash
make create-google-cloud-resources
```

## サービス開始

ラズパイで下記を実行する。

```bash
make start-sky-camera
```

## サービス停止

ラズパイで下記を実行する。

```bash
make stop-sky-camera
```
