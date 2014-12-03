Premise
===
*Given a public github repo URL, return a list of all contributors and their geographic locations*

This is a very basic prototype built as a final project for INFO98. It is meant as more of a thought experiment to display the globalization of data and information through the analysis of Github as a popular center for idea exchange.

My experience in development of this demo gave me insight into freedom of information. Particularly, it showed me that geographic GPS data using free resources is extremely inneficient - there are no (free) robust, modern services to do batch geocode operations. Each geocode request must be sent individually, which is why this library is so slow. It could be easily sped up if one was willing to pay for geocoding services.

Geographic libraries for python are also not easily accesible for beginners, but that can be forgivin based on the fact that they at least exist. I originally planned on creating a demo with ipython notebook and matplotlib, but installing it was a nightmare of broke packages and missing header links. These are serious barriers of entry to new arrivals to python and data modeling.

Notes
===

Need to pass git_globe_config dictionary in the format:

	{
		# Github application token
		"oauth_token": YOUR_TOKEN,
		"mapquest_api_key": YOUR_KEY
	}
	
Check `requirements.txt` and either install those packages, or create a virtualenv and install those packages. As of right now, it's just `python-requests`, but further development might add more dependencies to support plotting or other data analysis.
