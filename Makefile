build-tjump:
	docker build . -t tjump

xhost:
	xhost +	

run-test:	xhost
	docker run --privileged -it --rm \
	--cap-add=SYS_PTRACE \
	-u 1000:1000 \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY \
	-v /run/dbus:/run/dbus \
	-v /dev/shm:/dev/shm \
	--device /dev/snd \
	--device /dev/dri \
	-e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
	-v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native \
	-v /run/user/1000/pulse:/run/user/1000/pulse \
	-v /var/run/dbus:/var/run/dbus \
	-v ~/Desktop/T-Jump-:/home/docker \
	tjump

