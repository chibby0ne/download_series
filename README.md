# download series
Have you ever watched a series from a streaming video? Ever wanted to download
them to replay them as many times as possible without the overhead of waiting
for the stream to load again the same frames and packets?

Then this is the script for you.

## Installation

Run `./install.sh`

## Usage

Create the folder where you want to download the series and move to that
folder. For example:
```bash
mkdir The_Wire
cd The_Wire
```

Then proceed to use the script:

```bash
download_series.py $SERIES_NAME
```

For example;

```bash
download_series.py the wire
```

Or:

```bash
download_series.py the_wire
```

and even weird capitalization and superfluous spaces

```bash
download_series.py     THE     WiRe
```

But not: 

```bash
download_series.py the_wiree
```

Or:

```bash
download_series.py thewire
```

PS: You should really watch [The
Wire](https://en.wikipedia.org/wiki/The_Wire)

## Requirements
- Linux
- Python >= Python 2.7
- urllib2/urllib3 => Using apt-get: `sudo apt-get install python-urllib3`
- wget

## Features to Add
- Select seasons and episodes
- Select output directory
- Search in more hosting sites than just Gorillavid ex: DaClips, ModoVideo,
  etc..
- Output prettier
- Exit immediately 


## Bugs
- Downloads same episode if the episode is in the directory with a different
  extension
- Doesn't exit immediately when pressing Ctrl-C

## Licence
MIT © 2015 Antonio Gutierrez
