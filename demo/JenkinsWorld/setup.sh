dir=$(dirname "$0")
xl apply -f $dir/templates/shared_configuration.yaml
xl apply -f $dir/templates/import_jenkins_pipeline.yaml
xl apply -f $dir/templates/track_jenkins_pipeline.yaml
xl apply -f $dir/templates/feature_delivery_process.yaml
xl apply -f $dir/templates/component_delivery_process.yaml
xl apply -f $dir/templates/release_train_process.yaml
