import requests
from urllib import unquote

github_api_root = "https://api.github.com"
mapquest_api_root = "http://www.mapquestapi.com/geocoding/v1/address"
chunk_size = 100

def get_repo_contributors(repo_owner, repo_name, git_globe_config):
	request_url = '/'.join([github_api_root, "repos",
		repo_owner, repo_name, "contributors"])

	headers = {'Authorization': 'token ' + git_globe_config["oauth_token"]}

	r = requests.get(request_url, headers=headers)
	if r.status_code < 200 or r.status_code >= 300:
		print 'failed to fetch contributor list'
	return map_contributor_usernames(r.json())

def map_contributor_usernames(contributors):
	return [contributor["login"] for contributor in contributors]

def get_location_name(login, git_globe_config):
	request_url = '/'.join([github_api_root, "users", login])

	headers = {'Authorization': 'token ' + git_globe_config["oauth_token"]}

	r = requests.get(request_url, headers = headers)
	if r.status_code < 200 or r.status_code >= 300:
		print 'failed to fetch user location for login: {}'.format(login)
	return r.json()["location"]	

def get_coords(location_name, git_globe_config):
	request_url = mapquest_api_root
	
	params = {
		'key': unquote(git_globe_config["mapquest_api_key"]),
		'location': location_name
	}

	r = requests.get(request_url, params=params)

	if r.status_code < 200 or r.status_code >= 300:
		print 'failed to fetch coordinates for location: {}'.format(location_name)

	try:
		return r.json()["results"][0]["locations"][0]["latLng"]
	except IndexError:
		return None

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# return dictionary of usernames and their location names
def get_location_names(repo_owner, repo_name, git_globe_config):
    return [(login, get_location_name(login, git_globe_config))
    	for login in get_repo_contributors(repo_owner, repo_name, git_globe_config)]

# return dictionary of usernames and their lat/lon coordinates. Splits contributor list
# to get around mapquest rate limiting
def get_location_coords(repo_owner, repo_name, git_globe_config):
	contributors = get_repo_contributors(repo_owner, repo_name, git_globe_config)
	if len(contributors) > chunk_size:
		data = []
		for chunk in chunks(contributors, chunk_size):
			data.extend([(login, get_coords(get_location_name(login, git_globe_config), git_globe_config))
				for login in chunk])
		return data
	else:
		return [(login, get_coords(get_location_name(login, git_globe_config), git_globe_config))
			for login in contributors]

