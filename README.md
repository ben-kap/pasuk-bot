# The Pasuk Bot

A simple Mastodon bot that posts a random pasuk (verse) from the Tanach (Hebrew Bible) in both the original Hebrew and English translation on command.

The text for the pesukim was taken from [Mechon Mamre](https://mechon-mamre.org/p/pt/pt0.htm).

The code as it appears here works on my Linux home server, but you may need to make adjustements for it to run in your environment. Though the text could theoretically be scraped directly from the web, for the sake of stability, I opted to have it pull from a local copy of the Mechon Mamre's html, which you can download from their site [here](https://mechon-mamre.org/dlpt.htm). The `create_csv.py` script will pull from the local files to make a list of every pasuk along with its corresponding html file. In order for this script to run properly, you will have to manually delete the html files that do not contain single Tanach chapters (the files to keep are generally formatted as `ptXXXX.htm` with the first two digits representing the book and the latter two the chapter). You will also need to add the access token from the Mastodon bot account you will be using in a text file named `access_token.txt`.

The `select_verse.py` script can be set to run using cron or another automated solution to post at the desired interval.
 
