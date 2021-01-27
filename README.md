# dynamic-dag-assignment

assign IP dynamically to dag configured in panorama


# Running this App


```bash

docker run -e 'REPO=https://gitlab.com/panw-gse/as/dynamic-dag-assignment.git' -p 8082:8080 --rm -t nembery/appetizer:dev

```


The default username and password are `paloalto` and `appetizer`. These may be changed by
setting the following Environment variables before launch:

```bash

export CNC_USERNAME=dag
export CNC_PASSWORD=dag

```


