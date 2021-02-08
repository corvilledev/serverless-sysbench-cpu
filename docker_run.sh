#!/bin/bash
cat > /etc/cb_client.json << EOF
$cb_client
EOF
./run.sh
