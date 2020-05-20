import argparse
from sycs import SimpleSymfonycastScraper as Scs


def main():
	# Prompt user disabled, user and pass must be wired in the constructor
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=int, help='download from', default=1)
	parser.add_argument('--end', type=int, help='download to', default=-1)
	parser.add_argument('--course', required=True, help='Course\'s name')
	args = parser.parse_args()

	symfonycasts = Scs(course=args.course, start=args.start, end=args.end)

	with open('out.txt', 'w') as f:
		for direct_link in symfonycasts.get_direct_links():
			f.write(direct_link + '\n')


if __name__ == '__main__':
	main()
