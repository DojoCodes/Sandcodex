# SandCodex

## Dev - start celery worker

```bash
apt install redis # Install redis if you don't have it
pip install .
source env.sh
celery worker -A sandcodex.celery --loglevel=info
```