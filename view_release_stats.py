
"""
this script was built to track downloads of dnppy assets.
since dnppy doesn't really have assets yet, it isn't as usefull as imagined.
"""

import requests
import datetime

# init log and total download counter
now = datetime.datetime.now()
log = ["Report generated on {0}\n\n".format(now)]
total_downloads = 0

# send the request to the github API and read the json
r = requests.get("https://api.github.com/repos/nasa/dnppy/releases")
rjson = r.json()

# check for overuse warnings
if r.status_code is not 200:
    if r.status_code is 403:
        print("You have made too many requests to the GitHub API this hour. Try again later")


# generate download statistics report
for release in rjson:

    log.append("{0}\n".format(release["name"]))

    if not release["assets"]:
        log.append("\t[this release has no assets]\n")

    for asset in release["assets"]:

        log.append("\t{0}: \n\t\t{1} = {2}\n\t\t{3} = {4}\n\t\t{5} = {6}\n".format(
            asset["name"],
            "updated".ljust(10), asset["updated_at"].replace("T"," at "),
            "downloads".ljust(10), asset["download_count"],
            "asset url".ljust(10), asset["url"]))

        total_downloads += int(asset["download_count"])

    log.append("")

# add total download summary to the log
log.append("\nTotal downloads of all assets = {0}\n".format(total_downloads))


# write the log to a text file.
with open("dnppy_stat_report.txt",'w+') as f:
    for entry in log:
        print(entry)
        f.write(entry)
