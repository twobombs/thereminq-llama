#!/bin/bash

docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest

docker run -d opensearchproject/opensearch-dashboards:latest

