import argparse
from sycs import SimpleSymfonycastScraper as Scs


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=int, help='download from')
	parser.add_argument('--end', type=int, help='download to')
	parser.add_argument('--course', required=True, help='Course\'s name')
	args = parser.parse_args()

	try:
		symfonycasts = Scs(course=args.course, start=args.start, end=args.end)
	except Exception as e:
		print("\nError: %s\n" % e)
		return

	try:
		with open('out.txt', 'w') as f:
			for direct_link in symfonycasts.get_direct_links():
				f.write(direct_link + '\n')
	except Exception as e:
		print("\nError: %s\n" % e)


if __name__ == '__main__':
	main()
