import argparse
import os
# Create the parser
parser = argparse.ArgumentParser()
# Add the version argument
parser.add_argument('--version', action='store', type=str, help='The version to redirect to')
# Parse the arguments
args = parser.parse_args()
# Output the redirecting html
version = args.version
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url={version}/index.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>If you are not redirected, <a href="{version}/index.html">click here</a>.</p>
</body>
</html>"""
# create the index folder if it does not exist
if not os.path.exists('docs/index'):
    os.makedirs('docs/index')
with open('docs/index/index.html', 'w', encoding="UTF-8") as f:
    f.write(html)
