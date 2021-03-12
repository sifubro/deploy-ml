#!/bin/bash

# Building packages and uploading them to a Gemfury repository

GEMFURY_URL=$GEMFURY_PUSH_URL

set -e

DIRS="$@"
BASE_DIR=$(pwd)
SETUP="setup.py"  # We specify where the setup.py file is
# we are doing this in 

warn() {
    echo "$@" 1>&2
}

die() {
    warn "$@"
    exit 1
}

build() {
    DIR="${1/%\//}"
    echo "Checking directory $DIR"
    cd "$BASE_DIR/$DIR"
    [ ! -e $SETUP ] && warn "No $SETUP file, skipping" && return
    PACKAGE_NAME=$(python $SETUP --fullname)
    echo "Package $PACKAGE_NAME"

    # Here we generate the distibution
    python "$SETUP" sdist bdist_wheel || die "Building package $PACKAGE_NAME failed" 

    # We loop over the dist directory /regression_model/dist/  and upload the files found in there to gemfury
    # e.g. regression_model-0.1.3.tar.gz and regression_model-0.1.3-py3-non-ar
    for X in $(ls dist)
    do
        curl -F package=@"dist/$X" "$GEMFURY_URL" || die "Uploading package $PACKAGE_NAME failed on file dist/$X"
    done
}

if [ -n "$DIRS" ]; then
    for dir in $DIRS; do
        build $dir
    done
else
    ls -d */ | while read dir; do
        build $dir
    done
fi