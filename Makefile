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

start-sky-camera:
	sudo -H pip3 install -r requirements.txt

	chmod +x rpi-sky-shooter.sh
	chmod +x rpi-sky-renderer.py
	chmod +x rpi-sky-deleter.sh

	sudo mkdir -p /etc/rpi-sky-camera
	sudo cp credentials.json /etc/rpi-sky-camera
	sudo cp environment /etc/rpi-sky-camera
	sudo cp rpi-sky-shooter.sh /etc/rpi-sky-camera
	sudo cp rpi-sky-renderer.py /etc/rpi-sky-camera
	sudo cp rpi-sky-deleter.sh /etc/rpi-sky-camera

	sudo cp rpi-sky-shooter.service /etc/systemd/system
	sudo cp rpi-sky-shooter.timer /etc/systemd/system
	sudo cp rpi-sky-renderer.service /etc/systemd/system
	sudo cp rpi-sky-renderer.timer /etc/systemd/system
	sudo cp rpi-sky-deleter.service /etc/systemd/system
	sudo cp rpi-sky-deleter.timer /etc/systemd/system
	sudo systemctl enable rpi-sky-shooter.service
	sudo systemctl enable rpi-sky-shooter.timer
	sudo systemctl enable rpi-sky-renderer.service
	sudo systemctl enable rpi-sky-renderer.timer
	sudo systemctl enable rpi-sky-deleter.service
	sudo systemctl enable rpi-sky-deleter.timer
	sudo systemctl start rpi-sky-shooter.timer
	sudo systemctl start rpi-sky-renderer.timer
	sudo systemctl start rpi-sky-deleter.timer

stop-sky-camera:
	sudo systemctl stop rpi-sky-renderer.timer
	sudo systemctl stop rpi-sky-shooter.timer
	sudo systemctl stop rpi-sky-deleter.timer
	sudo systemctl disable rpi-sky-renderer.timer
	sudo systemctl disable rpi-sky-renderer.service
	sudo systemctl disable rpi-sky-shooter.timer
	sudo systemctl disable rpi-sky-shooter.service
	sudo systemctl disable rpi-sky-deleter.timer
	sudo systemctl disable rpi-sky-deleter.service
	sudo rm /etc/systemd/system/rpi-sky-renderer.timer
	sudo rm /etc/systemd/system/rpi-sky-renderer.service
	sudo rm /etc/systemd/system/rpi-sky-shooter.timer
	sudo rm /etc/systemd/system/rpi-sky-shooter.service
	sudo rm /etc/systemd/system/rpi-sky-deleter.timer
	sudo rm /etc/systemd/system/rpi-sky-deleter.service

	sudo rm -rf /etc/rpi-sky-camera
