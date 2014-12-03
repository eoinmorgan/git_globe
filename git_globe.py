import requests
from urllib import unquote
from pprint import pprint

github_api_root = "https://api.github.com"
mapquest_api_root = "http://www.mapquestapi.com/geocoding/v1/address"

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

# return dictionary of usernames and their location names
def get_location_names(repo_owner, repo_name, git_globe_config):
    return [(login, get_location_name(login, git_globe_config))
    	for login in get_repo_contributors(repo_owner, repo_name, git_globe_config)]

# return dictionary of usernames and their lat/lon coordinates
def get_location_coords(repo_owner, repo_name, git_globe_config):
	return [(login, get_coords(get_location_name(login, git_globe_config), git_globe_config))
    	for login in get_repo_contributors(repo_owner, repo_name, git_globe_config)]

git_globe_config = {}
git_globe_config["oauth_token"] = "eb9f1c1e55be9fdd7daecdd16540b21edcbafce0"
git_globe_config["mapquest_api_key"] = "Fmjtd%7Cluurn16a2d%2Caw%3Do5-9wts1z"

pprint(get_location_coords("defunkt", "dotjs", git_globe_config))
