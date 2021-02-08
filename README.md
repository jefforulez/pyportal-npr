
# NPR Station PyPortal

Use a [Adafruit PyPortal](https://www.adafruit.com/product/4116) to show what's currently playing on an [NPR](https://npr.org) station.

The portal defaults to [WBGO 88.3 FM](https://wbgo.org) Newark Public Radio, the world’s premiere jazz public radio station.


## Initial Setup

_Links to PyPortal documentation is available at the bottom of this page._

1\. Update `secrets.py`:

```
cp ./CIRCUITPY/secrets.py.tmpl ./CIRCUITPY/secrets.py
vim ./CIRCUITPY/secrets.py
```

Adafruit IO credentials are used to convert and display album artwork.

2\. Copy code to PyPortal:

```
cp -Rai ./CIRCUITPY/* /Volumes/CIRCUITPY/
```

## Changing Stations

A few updates are needed to change:

1\. Find the `UCS` value for the [NPR Composer API](http://api.composer.nprstations.org/) for the target station:

This can usually be found by going to the station's playlist search and using [Chrome Dev Tools](https://developers.google.com/web/tools/chrome-devtools) to find the background XHR requests to `/v1/widget/.../playlist`

For example, go to [WRTI 90.1 FM](https://wrti.org/) playlist search:

- https://www.wrti.org/classical-playlist-search

and you'll see calls to:

```
https://api.composer.nprstations.org/v1/widget/53c7dbe1e1c8b9c77b4b9b6e/playlist?...
```

In the URL, is **53c7dbe1e1c8b9c77b4b9b6e** is the UCS number of WRTI.

2\. Edit `code.py` and change the following lines:

```
STATION_DEFAULT_SHOW_NAME = "WRTI | Your Classical & Jazz Source"
STATION_DEFAULT_HOST_NAME = "WRTI Staff"
STATION_PLAYLIST_SLUG     = "53c7dbe1e1c8b9c77b4b9b6e"  # <~ the new UC
```

3\. Add a station logo _(optional)_:

Logos should be 120x50-pixel, 24-bit true color bitmaps with a black (0x000000) background.

The logo file must be name `${UCS}_slug.bmp` and be placed the top of the `CIRCUITPY` directory, e.g.

```
$ ls /Volumes/CIRCUITPY/*_slug.bmp
/Volumes/CIRCUITPY/53c7dbe1e1c8b9c77b4b9b6e_slug.bmp
```

On MacOS, you can use `convert` to covert from another image format to bitmap:

```
convert ./120x50-source-image.png -type truecolor /Volumes/CIRCUITPY/53c7dbe1e1c8b9c77b4b9b6e_slug.bmp
```

`convert` can be installed via [Homebrew](https://formulae.brew.sh/formula/imagemagick), if necessary.


## Related Links

#### NPR API URLs

- http://api.composer.nprstations.org/

- https://api.composer.nprstations.org/v1/widget/5834b54de1c8aada9f4d7a9e/playlist?limit=2

- Example NPR Composer API UCS values:
  - WBGO 88.3 FM: `5834b54de1c8aada9f4d7a9e`
  - WRTI 90.1 FM: `53c7dbe1e1c8b9c77b4b9b6e`


#### Adafruit

- Adafruit product page
  - https://www.adafruit.com/product/4116

- Adafruit tutorial
  - https://learn.adafruit.com/adafruit-pyportal

- Adafruit PyPortal Hardware FAQ
  - https://learn.adafruit.com/adafruit-pyportal/pyportal-hardware-faq

- Latest CircuitPython
  - https://circuitpython.org/board/pyportal/

- Latest CircuitPython Libraries
  - https://circuitpython.org/libraries
