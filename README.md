# BeeGenn

## How to run

First, make sure to [install GeNN](https://genn-team.github.io/genn/documentation/4/html/d8/d99/Installation.html) and in particular pygenn.

Then, install this package.

```bash
https://github.com/giacThePhantom/genn-network-model/
cd genn-network-model
pip install -e .
```

Then, set up a simulation:

```bash
python -m beegenn.simulation data <simname>
```


## Set up docker

If you wish to run docker locally, after checking out the project, install Docker and then proceed to build an image:

```bash
docker build . -t beegenn/beegenn:latest
```

Our entrypoint will automatically start a simulation in a hardened scenario. To get outputs you should bind-mount an output directory to `/home/genn`, and a data directory to `/data`. For example:

```bash
docker run -it \
  --mount type=bind,source=$(pwd)/data,target=/data \
  --mount type=bind,source=/some/output/folder,target=/home/genn \
  beegenn/beegenn:latest
```

### Run inside the cluster 

Please refer to our [internal guide](https://github.com/giacThePhantom/genn-network-model/blob/master/cluster/README.md).

### Authors

- Giacomo Fantoni (Giacomo.Fantoni@studenti.unitn.it)
- Enrico Trombetta (Enrico.Trombetta@studenti.unitn.it)

### Preprint describing wake-sleep transitions simulating with this code

Sebastian Moguilner, Ettore Tiraboschi, Giacomo Fantoni, Heather Strelevitz, Hamid Soleimani, Luca Del Torre, Uri Hasson, Albrecht Haase bioRxiv 2024.10.11.617548; doi: https://doi.org/10.1101/2024.10.11.617548
