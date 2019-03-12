ICPSR Variables

Taking all 4-something million ICPSR variables and trying to find relationships between them across datasets.


## Docker

#### Build

`docker build -t icpsr-vars .`

#### Run interactive

get `<image_id>`:

`docker image ls`

& 

`docker run -it -p "8888:8888" <image_id> /bin/bash`

## Run Jupyter from inside container

`jupyter notebook --ip=0.0.0.0 --no-browser --allow-root`
