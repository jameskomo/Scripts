#! /bin/bash

## create the directory, -p means it will create parent dirs
## and not complain if the file already exists

DIR=$(pwd)
images="$DIR/images"
mkdir -p "$images"
videos="$DIR/videos"
mkdir -p "$videos"
music="$DIR/music"
mkdir -p "$music"

for file in $DIR/*
do
	## basename removes file path and remove the extension if
	## a second arg is provided
	name="$(basename "$file")"
	if [ "${name##*.}" == "jpg" ] || [ "${name##*.}" == "png" ] ; then
		mv "$file" "images"
	elif [ "${name##*.}" == "mp3" ] || [ "${name##*.}" == "flac" ] ; then
		mv "$file" "$music"
    elif [ "${name##*.}" == "avi" ] || [ "${name##*.}" == "mov" ] ; then
		mv "$file" "$videos"
	elif [ "${name##*.}" == "log" ] ; then
		rm "$file" 
	else
		true
	fi
done