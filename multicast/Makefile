

build:
	docker build -t streamtools/multicast:latest .
	docker run \
		--rm -it \
		-p 8000:80 \
		-p 1935:1935 \
		-v ${PWD}/nginx.conf:/etc/nginx/nginx.conf \
		-v ${PWD}/ingest_servers:/etc/nginx/ingest_servers \
		streamtools/multicast:latest

twitch:
	ffmpeg -f x11grab \
		-s "1920x1080" -r 30 -i :0.0 -ar 44100 \
		-vcodec libx264 -b:v 1M -acodec aac -b:a 256k -f flv \
		rtmp://localhost/live/screen
