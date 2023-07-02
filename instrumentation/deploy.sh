oc create configmap prom-config --from-file=prometheus.yml
oc new-app grafana/grafana
oc apply -f deploy-prometheus.yml
oc apply -f deploy-prometheus-service.yml
#oc new-app prom/prometheus
oc expose svc/prometheus
oc expose svc/grafana

