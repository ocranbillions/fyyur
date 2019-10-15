def validate_new_artist(artist):
  if (artist['name'] == "" or artist['city'] == "" or
      artist['state'] == "" or artist['phone'] == "" or 
      len(artist['genres']) == 0 or artist['facebook_link'] == "" or 
      artist['image_link'] == ""
    ):
    return False
  else:
    return True

def validate_new_venue(venue):
  if (venue['name'] == "" or venue['city'] == "" or
      venue['state'] == "" or venue['phone'] == "" or 
      len(venue['genres']) == 0 or venue['facebook_link'] == "" or 
      venue['image_link'] == "" or venue['address'] == "" 
    ):
    return False
  else:
    return True

def validate_edit_venue(venue):
  if (venue['name'] == "" or venue['phone'] == "" or 
      len(venue['genres']) == 0 or venue['facebook_link'] == "" or 
      venue['image_link'] == "" or venue['address'] == "" 
    ):
    return False
  else:
    return True