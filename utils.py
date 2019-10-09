def validate_new_artist(artist):
  if (artist['name'] == "" or artist['city'] == "" or
      artist['state'] == "" or artist['phone'] == "" or 
      len(artist['genres']) == 0 or artist['facebook_link'] == "" or 
      artist['image_link'] == ""
    ):
    return False
  else:
    return True
