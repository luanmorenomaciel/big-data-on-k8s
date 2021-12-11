https://www.docker.com/sites/default/files/d8/2019-09/docker-cheat-sheet.pdf
https://dockerlabs.collabnix.com/docker/cheatsheet/

```shell
# verify docker desktop
https://www.docker.com/products/docker-desktop

# check version
docker --version

# pull image
# by default latest
https://hub.docker.com/_/busybox
docker pull busybox

# verify local images
# busy box = 1.24 mb
docker images

# run the container
# init process
# verify running containers
docker run busybox echo "busybox"
docker ps
docker ps -a

# it = interactive
docker run -it busybox sh
docker ps

# stop docker image
docker stop ff847ce6c34f

# delete containers
docker rm $(docker ps -a -q -f status=exited)
```