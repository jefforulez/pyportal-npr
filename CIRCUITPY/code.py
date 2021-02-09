
import time
import json

import board
import displayio

from adafruit_pyportal import PyPortal

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

#
# globals settings
#

# edit these values to change station
STATION_DEFAULT_SHOW_NAME = "WBGO | The Jazz Source"
STATION_DEFAULT_HOST_NAME = "WBGO Staff"
STATION_PLAYLIST_UCS      = "5834b54de1c8aada9f4d7a9e"

#
# global convenience
#

# the current working directory (where this file is)
cwd = ( "/" + __file__ ).rsplit( '/', 1 )[0]

text_font = bitmap_font.load_font( cwd + "/fonts/Arial-ItalicMT-17.bdf" )

#
# function
#

class StationPortal():

  def __init__( self ):

    self.pyportal = PyPortal(
        url = f"https://api.composer.nprstations.org/v1/widget/{STATION_PLAYLIST_UCS}/playlist?limit=2",
        status_neopixel = board.NEOPIXEL,
        default_bg = 0x000000 # cwd + "/station_background.bmp",
      )

    self.show_text   = Label( text_font, max_glyphs=40 )
    self.host_text   = Label( text_font, max_glyphs=40 )
    self.track_text  = Label( text_font, max_glyphs=40 )
    self.artist_text = Label( text_font, max_glyphs=40 )

    self.show_text.color   = 0xFFFFFF
    self.host_text.color   = 0xFFFFFF
    self.track_text.color  = 0xFFFFFF
    self.artist_text.color = 0xF05423

    self.show_text.x   = 20
    self.host_text.x   = 20
    self.track_text.x  = 20
    self.artist_text.x = 20

    self.show_text.y   = 35
    self.host_text.y   = 55
    self.track_text.y  = 90
    self.artist_text.y = 110

    self.pyportal.splash.append( self.show_text )
    self.pyportal.splash.append( self.host_text )
    self.pyportal.splash.append( self.track_text )
    self.pyportal.splash.append( self.artist_text )

    # placeholder for album art tilegroup, index 5
    self.pyportal.splash.append( displayio.Group() )
    self.artworkTileGroupIndex = 5

    # append station slug last so that if it fails, it doens't throw off the sprite indices
    station_slug = f"{cwd}/{STATION_PLAYLIST_UCS}_slug.bmp"
    try:
      self.slug_file = open( station_slug, "rb" )
      slug_bitmap = displayio.OnDiskBitmap( self.slug_file )

      self.pyportal.splash.append( displayio.TileGrid(
          slug_bitmap,
          pixel_shader = displayio.ColorConverter(),
          width = 1,
          height = 1,
          x = 190,
          y = 170
        ))
    except OSError as e:
      print( f"Unable to open station slug bitmap, station_slug: {station_slug}" )

    self.cover_file = None
    self.track_id = None


  def fetch( self ):

    values = self.pyportal.fetch()
    data = json.loads( values )
    print( "Fetched new data, type:", type(data) )
    print( "data:", data )

    playlist = data["playlist"][-1]
    curr_track = playlist["playlist"][-1]

    if ( self.track_id != curr_track["id"] ):
      print( "Loading new track, id: ", curr_track["id"] )
      self.track_id = curr_track["id"]
      self._updateTrack( playlist, curr_track )
      print( "Finished loading new track,", curr_track["trackName"] )

  def _setShow( self, val ):
    if ( len( val ) > 35 ):
      self.show_text.text = ( val )[0:32] + "..."
    else:
      self.show_text.text = val

  def _setHost( self, val ):
    if ( len( val ) > 30 ):
      self.host_text.text = "with " + ( val )[0:30] + "..."
    else:
      self.host_text.text = "with " + val

  def _setTrack( self, val ):
    if ( len( val ) > 35 ):
      self.track_text.text = ( val )[0:32] + "..."
    else:
      self.track_text.text = val

  def _setArtist( self, val ):
    if ( len( val ) > 35 ):
      self.artist_text.text = ( "by " + val )[0:30] + "..."
    else:
      self.artist_text.text = "by " + val


  def _updateTrack( self, playlist, curr_track ):

    if "name" in playlist:
      self._setShow( playlist["name"] )
    else:
      self._setShow( STATION_DEFAULT_SHOW_NAME )

    if "hosts" in playlist:
      self._setHost( playlist["hosts"] )
    else:
      self._setHost( STATION_DEFAULT_HOST_NAME )

    if "trackName" in curr_track:
      self._setTrack( curr_track["trackName"] )
    else:
      self._setTrack( "Unknown Title" )

    if "artistName" in curr_track:
      self._setArtist( curr_track["artistName"] )
    else:
      self._setArtist( "Unknown Artist" )

    if "album_art" in curr_track:
      self._updateCoverart( curr_track["album_art"] )


  def _updateCoverart( self, source_url ):

    if ( self.cover_file ):
      self.cover_file.close()

    try:
      image_url = self.pyportal.image_converter_url( source_url, 100, 100 )
      print( f"Converting image, image_url: {image_url}" )

      cover_filename = "/sd/cover-image.bmp"

      self.pyportal.wget( image_url, cover_filename, chunk_size=512 )

      self.cover_file = open( cover_filename, "rb" )
      cover_bitmap = displayio.OnDiskBitmap( self.cover_file )

    except ( OSError, KeyError, Exception ) as e:
      print( f"Error rendering cover art, source_url: {source_url}" )
      cover_bitmap = displayio.Bitmap( 100, 100, 1 )
      cover_bitmap.fill( 0 )

    self.pyportal.splash[ self.artworkTileGroupIndex ] = displayio.TileGrid(
      cover_bitmap,
      pixel_shader = displayio.ColorConverter(),
      width = 1,
      height = 1,
      x = 23,
      y = 130
    )


if __name__ == "__main__":

  stationPortal = StationPortal()

  while True:
    try:
      stationPortal.fetch()

    except ( OSError, RuntimeError ) as e:
      print( "Unexpected error occured while fetching data", e )

    time.sleep(60)

