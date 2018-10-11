dir=$(dirname "$0")
./xlw version
./xlw apply -f $dir/templates/shared_configuration.yaml
./xlw apply -f $dir/templates/import_jenkins_pipeline.yaml
./xlw apply -f $dir/templates/track_jenkins_pipeline.yaml
./xlw apply -f $dir/templates/feature_delivery_process.yaml
./xlw apply -f $dir/templates/component_delivery_process.yaml
./xlw apply -f $dir/templates/release_train_process.yaml
./xlw apply -f $dir/templates/manual_setup.yaml
