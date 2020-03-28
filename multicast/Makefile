

build:
	docker build -t streamtools/multicast:latest .
	docker run \
		--rm -it \
		-p 8000:80 \
		-v ${PWD}/nginx.conf:/etc/nginx/nginx.conf \
		streamtools/multicast:latest