# Apache Kafka Security with Strimzi Operator

### security options for strimzi operator
```shell
# links
# https://docs.confluent.io/platform/current/security/security_tutorial.html
# https://docs.confluent.io/platform/current/kafka/authentication_ssl.html
# https://docs.confluent.io/platform/current/kafka/encryption.html#kafka-ssl-encryption
# https://github.com/strimzi/strimzi-kafka-operator/tree/main/examples/security
# https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_scram.html

# strimzi security [options]
tls-auth
scram-sha-512-auth
keycloak-authorization

# type = scram-sha-512-auth
# username & password authentication 
# using tls - secure channel
```

```shell
# https://strimzi.io/documentation/
# https://github.com/strimzi/strimzi-kafka-operator/tree/0.25.0/examples/security
# https://strimzi.io/docs/operators/latest/overview.html#security-configuration-authentication_str

# access cluster [k8s]
kubectx aks-owshq-dev

# add & update repos
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# create namespace
k create namespace ingestion

# install strimzi operator
# v.25 
helm install kafka strimzi/strimzi-kafka-operator --namespace ingestion --version 0.25.0

# deploy kafka broker using [tls]
# /Users/luanmorenomaciel/BitBucket/applications/ingestion-data-stores-app/deployment
k apply -f kafka-jbod-scram-sha-512.yaml

# verify operator [log]
k logs strimzi-cluster-operator-687fdd6f77-gv6k6 -f

# retrieve the broker status
kubectl get kafka -o yaml

# deploy topic and user
k apply -f topic.yaml
k apply -f user.yaml

# search for topics and registered users
k get kafkatopics
k get kafkausers

# retrieve secrets ~ users
# user [cert] and user [key] 
k get secrets luan.moreno -o yaml

# retrieve the kafka certificate
# edh-cluster-ca-cert
k get secrets edh-cluster-ca-cert -o yaml

# retrieve password and ca cert
k get secrets/luan.moreno --template={{.data.password}} | base64 -D
k get secret edh-cluster-ca-cert -o jsonpath='{.data.ca\.crt}' | base64 -d > /Users/luanmorenomaciel/BitBucket/applications/ingestion-data-stores-app/deployment/ca.crt

# install openssl on [macos]
# identify certificate information
brew install openssl
openssl version -a

# trigger ingestion
python3.9 cli.py 'strimzi-users-json-ssl'
```