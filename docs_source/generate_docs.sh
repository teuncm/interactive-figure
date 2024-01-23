#!/usr/bin/env bash

src_dir=$(dirname "$0")
sphinx-build -b html "$src_dir" "$src_dir/../docs"