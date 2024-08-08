import argparse


def sort_versions_by_latest(versions):
    def version_key(version):
        # Strip the 'v' and split the version into a tuple of integers
        return tuple(map(int, version.lstrip('v').split('.')))

    # Sort the versions using the version_key, in reverse order for latest first
    return sorted(versions, key=version_key, reverse=True)


# Create the parser
parser = argparse.ArgumentParser(description='Process some tags.')
parser.add_argument('--current_tag', default="", action='store', help='Current tag')
# Add the tags argument
parser.add_argument('--tags', default=[], action='store', nargs='*', help='List of tags to process')

# Parse the arguments
args = parser.parse_args()

# Output the list of tags
print("Tags received:", args.tags)

# filter out empty tags
args.tags = [tag for tag in args.tags if tag]
options = [fr'<option value="../{i}/index.html" {"selected" if i == args.current_tag else ""}>{i}</option>'
           for i in sort_versions_by_latest(args.tags)]
if not args.current_tag:
    options.append(r'<option value="../dev/index.html" selected>dev</option>')
options = '\n'.join(options)

html = rf"""<!-- HTML header for doxygen 1.11.0-->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="$langISO">
<head>
<meta http-equiv="Content-Type" content="text/xhtml;charset=UTF-8"/>
<meta http-equiv="X-UA-Compatible" content="IE=11"/>
<meta name="generator" content="Doxygen $doxygenversion"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<!--BEGIN PROJECT_NAME--><title>$projectname: $title</title><!--END PROJECT_NAME-->
<!--BEGIN !PROJECT_NAME--><title>$title</title><!--END !PROJECT_NAME-->
<!--BEGIN PROJECT_ICON-->
<link rel="icon" href="$relpath^$projecticon" type="image/x-icon" />
<!--END PROJECT_ICON-->
<link href="$relpath^tabs.css" rel="stylesheet" type="text/css"/>
<!--BEGIN DISABLE_INDEX-->
  <!--BEGIN FULL_SIDEBAR-->
<script type="text/javascript">var page_layout=1;</script>
  <!--END FULL_SIDEBAR-->
<!--END DISABLE_INDEX-->
<script type="text/javascript" src="$relpath^jquery.js"></script>
<script type="text/javascript" src="$relpath^dynsections.js"></script>
<!--BEGIN COPY_CLIPBOARD-->
<script type="text/javascript" src="$relpath^clipboard.js"></script>
<!--END COPY_CLIPBOARD-->
$treeview
$search
$mathjax
$darkmode
<link href="$relpath^$stylesheet" rel="stylesheet" type="text/css" />
$extrastylesheet
</head>
<body>
<!--BEGIN DISABLE_INDEX-->
  <!--BEGIN FULL_SIDEBAR-->
<div id="side-nav" class="ui-resizable side-nav-resizable"><!-- do not remove this div, it is closed by doxygen! -->
  <!--END FULL_SIDEBAR-->
<!--END DISABLE_INDEX-->

<div id="top"><!-- do not remove this div, it is closed by doxygen! -->

<!--BEGIN TITLEAREA-->
<div id="titlearea">
<table cellspacing="0" cellpadding="0">
 <tbody>
 <tr id="projectrow">
  <!--BEGIN PROJECT_LOGO-->
  <td id="projectlogo"><img alt="Logo" src="$relpath^$projectlogo"$logosize/></td>
  <!--END PROJECT_LOGO-->
  <!--BEGIN PROJECT_NAME-->
  <td id="projectalign">
   <div id="projectname">$projectname<span id="projectnumber">&#160;$projectnumber</span>
     <!-- Version Selector -->
     <select id="versionSelector" onchange="location = this.value;">
       {options}
     </select>
   </div>
   <!--BEGIN PROJECT_BRIEF--><div id="projectbrief">$projectbrief</div><!--END PROJECT_BRIEF-->
  </td>
  <!--END PROJECT_NAME-->
  <!--BEGIN !PROJECT_NAME-->
   <!--BEGIN PROJECT_BRIEF-->
    <td>
    <div id="projectbrief">$projectbrief</div>
    </td>
   <!--END PROJECT_BRIEF-->
  <!--END !PROJECT_NAME-->
  <!--BEGIN DISABLE_INDEX-->
   <!--BEGIN SEARCHENGINE-->
     <!--BEGIN !FULL_SIDEBAR-->
    <td>$searchbox</td>
     <!--END !FULL_SIDEBAR-->
   <!--END SEARCHENGINE-->
  <!--END DISABLE_INDEX-->
 </tr>
  <!--BEGIN SEARCHENGINE-->
   <!--BEGIN FULL_SIDEBAR-->
   <tr><td colspan="2">$searchbox</td></tr>
   <!--END FULL_SIDEBAR-->
  <!--END SEARCHENGINE-->
 </tbody>
</table>
</div>
<!--END TITLEAREA-->
<!-- end header part -->"""
with open("docs/header.html", "w", encoding='UTF-8') as f:
    f.write(html)
