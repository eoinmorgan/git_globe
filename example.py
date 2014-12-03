from pprint import pprint
from git_globe import get_location_coords

git_globe_config = {}
git_globe_config["oauth_token"] = "eb9f1c1e55be9fdd7daecdd16540b21edcbafce0"
git_globe_config["mapquest_api_key"] = "Fmjtd%7Cluurn16a2d%2Caw%3Do5-9wts1z"

pprint(get_location_coords("defunkt", "dotjs", git_globe_config))
