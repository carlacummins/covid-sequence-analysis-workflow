err_file="log.err"
err_log_content=$(jq -Rs '.' ${err_file})
# gcloud pubsub topics publish "projects/prj-int-dev-covid19-nf-gls/topics/covid-pipeline-log-stream" \
# --attribute='name=John Doe,age=30,city=New York' \
# --message="${err_log_content}"
gcloud pubsub subscriptions pull covid-pipeline-log-stream-sub --limit 5 --auto-ack # auto-ack will prevent this message to be pulled by other sub (clear msg queue)