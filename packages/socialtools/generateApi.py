from instagram.client import InstagramAPI
import facebook


def get_instagram_api(instagram_access_token,instagram_client_secret):
	return InstagramAPI(access_token=instagram_access_token,client_secret=instagram_client_secret)

def get_facebook_api(fb_access_token,fb_version):
	return facebook.GraphAPI(access_token=fb_access_token,version=fb_version)
