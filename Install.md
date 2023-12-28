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
### KeyCloak:
Check match user and secret with keycloak config.
Keycloak to front-end should be allowes via iptables in some systems
```
sudo iptables -I INPUT -s {keycloak internal IP} -p tcp --dport 8080 -j ACCEPT
```