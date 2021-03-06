# プロジェクト ID は好きな名称に変えること。
PROJECT_ID := rpi-sky-camera
SERVICE_ACCOUNT := sky-camera
MOVIE_BUCKET := sky-camera

create-google-cloud-resources:
	gcloud auth login
	gcloud projects create $(PROJECT_ID)
	gcloud config set project $(PROJECT_ID)
	gcloud config set compute/region asia-northeast1
	gcloud config set compute/zone asia-northeast1-b

	# サービスアカウント
	gcloud iam service-accounts create $(SERVICE_ACCOUNT)
	gcloud iam service-accounts keys create credentials.json --iam-account=$(SERVICE_ACCOUNT)@$(PROJECT_ID).iam.gserviceaccount.com

	# ストレージ
	gsutil mb -l ASIA-NORTHEAST1 -c STANDARD -b off  gs://$(MOVIE_BUCKET)
	gsutil iam ch serviceAccount:$(SERVICE_ACCOUNT)@$(PROJECT_ID).iam.gserviceaccount.com:roles/storage.objectViewer gs://$(MOVIE_BUCKET)
	gsutil iam ch serviceAccount:$(SERVICE_ACCOUNT)@$(PROJECT_ID).iam.gserviceaccount.com:roles/storage.objectCreator gs://$(MOVIE_BUCKET)
	gsutil iam ch serviceAccount:$(SERVICE_ACCOUNT)@$(PROJECT_ID).iam.gserviceaccount.com:roles/storage.legacyBucketWriter gs://$(MOVIE_BUCKET)

init-python:
	sudo -H pip3 install -r requirements.txt

start-sky-camera:
	chmod +x rpi-sky-shooter.py
	chmod +x rpi-sky-renderer.py
	chmod +x rpi-sky-deleter.sh

	sudo mkdir -p /etc/rpi-sky-camera
	sudo cp credentials.json /etc/rpi-sky-camera
	sudo cp environment /etc/rpi-sky-camera
	sudo cp rpi-sky-shooter.py /etc/rpi-sky-camera
	sudo cp rpi-sky-renderer.py /etc/rpi-sky-camera
	sudo cp rpi-sky-deleter.sh /etc/rpi-sky-camera
	sudo cp NotoSansJP-Regular.otf /etc/rpi-sky-camera

	sudo cp rpi-sky-shooter.service /etc/systemd/system
	sudo cp rpi-sky-shooter.timer /etc/systemd/system
	sudo cp rpi-sky-renderer.service /etc/systemd/system
	sudo cp rpi-sky-renderer.timer /etc/systemd/system
	sudo cp rpi-sky-deleter.service /etc/systemd/system
	sudo cp rpi-sky-deleter.timer /etc/systemd/system
	sudo systemctl enable rpi-sky-shooter.timer
	sudo systemctl enable rpi-sky-renderer.timer
	sudo systemctl enable rpi-sky-deleter.timer
	sudo systemctl start rpi-sky-shooter.timer
	sudo systemctl start rpi-sky-renderer.timer
	sudo systemctl start rpi-sky-deleter.timer

stop-sky-camera:
	sudo systemctl stop rpi-sky-renderer.timer
	sudo systemctl stop rpi-sky-shooter.timer
	sudo systemctl stop rpi-sky-deleter.timer
	sudo systemctl disable rpi-sky-renderer.timer
	sudo systemctl disable rpi-sky-shooter.timer
	sudo systemctl disable rpi-sky-deleter.timer
	sudo rm /etc/systemd/system/rpi-sky-renderer.timer
	sudo rm /etc/systemd/system/rpi-sky-renderer.service
	sudo rm /etc/systemd/system/rpi-sky-shooter.timer
	sudo rm /etc/systemd/system/rpi-sky-shooter.service
	sudo rm /etc/systemd/system/rpi-sky-deleter.timer
	sudo rm /etc/systemd/system/rpi-sky-deleter.service

	sudo rm -rf /etc/rpi-sky-camera


status-sky-camera:
	systemctl list-timers
	systemctl status rpi-sky-shooter.service
	systemctl status rpi-sky-renderer.service
	systemctl status rpi-sky-deleter.service
