# SandCodex

## Launch Cluster @ Home

- First, [Get Docker](https://docs.docker.com/get-docker/)
- Then install [Docker-compose](https://docs.docker.com/compose/install/)
- Clone the repository and go to the repo folder
```bash
git clone https://github.com/DojoCodes/Sandcodex.git
cd Sandcodex
```
- Build the worker image (only python for now):
```bash
docker build -t sandcodex_worker_python worker_images/python
```
- Build the stack running the following command
```bash
docker-compose up -d
```

If you want to restart the stask use
```bash
docker-compose up -d --force-recreate
```

If you want to see the logs
```bash
docker-compose logs
```
