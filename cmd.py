# import the necessary packages
import argparse
from gptldr_podcast import run

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,
	help="url to tldr")
args = vars(ap.parse_args())

run(args["url"])