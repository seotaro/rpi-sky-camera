# rpi-sky-camera

ラズパイで空のタイムラプス撮影を行う。

- 日中のみt秒ごとに撮影してローカルディスクに保存する。
- 4時半から19時までを簡易的に日中とした。

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
