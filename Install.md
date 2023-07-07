## Build containers


```
docker-compose build
docker network create shared
docker-compose up
```


## Apply manual configuration:

### sgecore username:
Change minimal UID in SGE master configuration to allow job submission from web apps:

```
docker exec -it sgecore /bin/bash
qconf -as front_end.dockerized_vre

qconf -mconf # change UID from 1000 to 33)
```
