# SandCodex

## Launch Cluster @ Home

- First, [Get Docker](https://docs.docker.com/get-docker/)
- Then install [Docker-compose](https://docs.docker.com/compose/install/)
- Clone the repository and go to the repo folder
```bash
git clone https://github.com/DojoCodes/Sandcodex.git
cd Sandcodex
```
- Build the stack running the following command
```bash
docker-compose up -d
```

> If you want to restart the stask use
> ```bash
> docker-compose up -d --force-recreate
> ```

> If you want to see the logs use
> ```bash
> docker-compose logs
> ```

> If you want to scale the number of workers
> ```bash
> docker-compose up -d --scale worker=3
> ```