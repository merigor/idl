# idl

Simple Python image downloader

This tool is written to support someone who knows what (s)he is doing and to help preventing most common glitches.
By no means should this tool be exposed to the unfiltered input (e.g. coming from the user).
It has basically no security features, allowing a lot of possibilities for abuse.

## What it does

- it expects a text file with some urls, one per line
- it checks if the file is available and readable
- it tries to check if the url is valid (nothig really sophisticated)
- it checks if the file can be downloaded to disk (size check)
- finally, it just gets the file and writes it to the current folder

## What not

- no authentification
- no encryption
- no dealing with proxies or the like
- no checks for the correctness of the file type
- no manipulation of the images themselves (resizing, merging, whatever ...)
- no prevention for any evil thing can be done inside the url itself
- no real handling of mass downloading and its problems
- no parallelization, no load balancing, no network traffic limits ... just no

## Usage

Just call `python3 idl.py urllist.txt` from a folder where you want the files to be.
