# remove old container and image
docker stop -t 0 yecl-bib
docker image rm -f yecl-bib:0.1
docker rm -f yecl-bib &>/dev/null

# build
docker build -t yecl-bib:0.1 .

docker run -td --privileged --net=host --ipc=host \
    --name="yecl-bib" \
    yecl-bib:0.1