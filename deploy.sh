oc create configmap generator-config --from-file=config.json
oc apply -f Consumer/consumer.yml
oc apply -f producer.yml
