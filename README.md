# dynamic-dag-assignment

assign IP dynamically to dag configured in panorama


# Running this App


```bash

docker run -e 'REPO=https://gitlab.com/panw-gse/as/dynamic-dag-assignment.git' -p 8083:8080 --rm -it registry.gitlab.com/panw-gse/as/appetizer:latest
```


The default username and password are `paloalto` and `appetizer`. These may be changed by
setting the following Environment variables before launch:

```bash

export CNC_USERNAME=dag
export CNC_PASSWORD=dag

```

In this example, browse to localhost:8083 in a web browser to launch this app. You may
change the default port mapping to something other than 8083 by modifying the docker 
run command above. 

