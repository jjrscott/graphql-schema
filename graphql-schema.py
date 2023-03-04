#!/usr/bin/env python3

import subprocess
import argparse
import os
import json
import sys
import re
from pathlib import Path
import requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export the GraphQL schema from a URL")

    parser.add_argument("url", help="the URL to download the schema from. E.g. https://example.com/graphql")
    args = parser.parse_args()

    script_dir = Path( __file__ ).absolute()

    with open(script_dir.with_name("introspection.graphqlquery"), 'r') as file:
        introspection_query = file.read()
        introspection_query = re.sub(r'[\s\n]+', ' ', introspection_query)
        introspection_query = re.sub(r'{[\s\n]+', '{', introspection_query)
        introspection_query = re.sub(r'[\s\n]+}', '}', introspection_query)

    query = {
        "operationName": "IntrospectionQuery",
        "query": introspection_query,
        "variables": {}
    }

    request = requests.post(args.url, json=query)
    print(request.text)
