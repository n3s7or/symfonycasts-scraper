import os
import argparse
from getpass import getpass
from sycs import SimpleSymfonycastScraper as Scs


def get_credentials() -> dict:
	"""Provide user's credentials

	Loads credentials from database or environment variables when posible, else it prompts the user
	"""
	# TODO Load from database

	user_email = os.environ.get('SCS_USER', None)
	user_passw = os.environ.get('SCS_PASS', None)

	if not user_email:
		user_email = input('Email: ')
	if not user_passw:
		user_passw = getpass()

	return dict(email=user_email, password=user_passw)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=int, help='download from')
	parser.add_argument('--end', type=int, help='download to')
	parser.add_argument('course', help='course\'s name')
	parser.add_argument('--free', action='store_true', help='free course, no need to authenticate')
	args = parser.parse_args()

	try:
		symfonycasts = Scs(course=args.course, start=args.start, end=args.end)
	except Exception as e:
		print("\nError: %s\n" % e)
		return

	if not args.free:
		symfonycasts.authenticate(**get_credentials())

	print_link = os.environ.get('PRINT_LINK', None)

	try:
		with open('out.txt', 'w') as f:
			for direct_link in symfonycasts.get_direct_links():
				if print_link:
					print(direct_link)
				f.write(direct_link + '\n')
	except Exception as e:
		print("\nError: %s\n" % e)


if __name__ == '__main__':
	main()
