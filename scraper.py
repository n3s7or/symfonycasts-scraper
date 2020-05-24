import argparse
from sycs import SimpleSymfonycastScraper as Scs


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
		symfonycasts.authenticate()

	links = []
	# try:
	for direct_link in symfonycasts.get_direct_links():
		print(direct_link)
		links.append(direct_link)
	# except Exception as e:
	# 	print("\nError: %s\n" % e)

	# with open('out.txt', 'w') as f:
	# 	f.write("\n")


if __name__ == '__main__':
	main()
