<?php //include("poll/lp_source.php"); ?>
<!doctype html public "-//w3c//dtd html 4.0 transitional//en">
<html>
<head>
	<meta name="Keywords" content="linux unix GPL climaxius pytelemeter Telenet Telemeter">
	<meta name="Description" content="pytelemeter">
	<meta name="Robots" content="index,follow">
	<meta name="Author" content="Robbie Vanbrabant">
	<meta name="Language" content="English">
	<title>pytelemeter</title>
	<link rel="Shortcut Icon" href="favicon.ico">
	<link rel="icon" href="favicon.ico">
	<link type="text/css" rel="stylesheet" href="style.css">

</head>
<body>

<!-- Menu at the top -->
<p class="right">
	
	<a href="index.php">Start</a>&nbsp;&nbsp;
	<a href="index.php?screen">Screenshot</a>&nbsp;&nbsp;
	<a href="index.php?down">Download</a>&nbsp;&nbsp;
	<a href="index.php?install">Install</a>&nbsp;&nbsp;
	<a href="index.php?support">Support</a>&nbsp;&nbsp;
	<a href="index.php?contrib">Contributors</a>&nbsp;&nbsp;
	<a href="index.php?links">Links</a>
</p>
<hr width="100%" noshade>


<script language="php">
	$page = basename($_SERVER['QUERY_STRING']);
	switch($page)
	{
		case "screen":
			include("screen.inc");
			break;
		case "down":
			include("download.inc");
			break;
		case "install":
			include("install.inc");
			break;
		case "support":
			include("support.inc");
			break;
                case "links":
                        include("links.inc");
                        break;
		case "contrib":
			include("contrib.inc");
			break;
		default:
			include("start.inc");
			break;
	}
</script>

<hr width="100%" noshade>


<!-- Footer -->

<p class="footer">
	The product names used in this web site are for identification purposes only.
	<br>All trademarks and registered trademarks are the property of their respective owners.
<script language="php">
	if ($page == ""){
print '<br><br>
<A href="http://sourceforge.net"> <IMG src="http://sourceforge.net/sflogo.php?group_id=99970&amp;type=5" width="210" height="62" border="0" alt="SourceForge.net Logo" /></A>';}
</script>
</p>
</body>
</html>

