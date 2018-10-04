git describe --tags > ./src/repo-info
LAYER_PATH=./layers INTERFACE_PATH=./interfaces charm build ./src --force
