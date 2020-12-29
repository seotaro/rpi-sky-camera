# rpi-sky-camera

ラズパイで空のタイムラプス撮影を行う。

- t秒ごとに撮影してローカルディスクに保存する。
- n時間毎にエンコードした動画を Google Cloud Strage にアップロードする。
- ~日没後の hh:mm:ss に、~前日のローカルディスクに保存した画像を削除する。

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
