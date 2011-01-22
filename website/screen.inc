<!-- Contact info -->

<a name="screen"></a>
<h4>Screenshot</h4>

<p>
<b><u>GTK and System Tray:</u></b><br><br>
<img src="pytelemeter-1.1.jpg">
<br>
(also check out the <a href="https://sourceforge.net/project/screenshots.php?group_id=99970">v1.4 screenshot</a>)
<br><br>
<b><u>CLI:</u></b><br>
<pre>
$ pytelemeter -h

pytelemeter v1.4
Fetch bandwidth usage statistics from the Belgian ISP Telenet
Homepage: <http://pytelemeter.sourceforge.net>

Usage:  pytelemeter [options...]
        pytelemeter-gtk [options...]
        pytelemeter-tray [options...]

Interface options:
  -c, --cli             command line interface
                            default when invoked as pytelemeter
  -g, --gui, --gtk      open the GTK graphical user interface
                            default when invoked as pytelemeter-gtk
  -t, --tray            open the system tray icon
                            default when invoked as pytelemeter-tray

Output options:
  -m, -r, --remaining   also output remaining bandwidth
  -d, --daily           also output daily statistics

  -s, --silent          silent mode
  -v. --verbose         verbose output (always on for cli)
  -D, --debug           show (http) debug info

Help options:
  -h, --help            print this message and exit
  -V, --version         print the version string and exit

$ pytelemeter
Fetching information... done!

Telemeter statistics @ 12 Feb 2006
----------------------------------
Download Volume:  [=================   ]  8817 MiB (86%)
 Upload  Volume:  [=========           ]   938 MiB (45%)
</pre>
<p><b><i> -m adds:</i></b></p>
<pre>
Before 15/02/06, you can download 1423 MiB without exceeding your prepaid download volume.
Before 15/02/06, you can upload 1110 MiB without exceeding your prepaid upload volume.
</pre>
<p><b><i>-d adds:</i></b></p>
<pre>
Daily statistics:
-----------------
   Day   | Download |  Upload
15/01/06 |       13 |        1
16/01/06 |      137 |        9
17/01/06 |      267 |       19
18/01/06 |      242 |       12
19/01/06 |        6 |        1
20/01/06 |      521 |       35
21/01/06 |     1029 |       60
22/01/06 |        8 |        1
23/01/06 |      172 |       11
24/01/06 |      192 |       24
25/01/06 |      767 |       66
26/01/06 |        1 |        0
27/01/06 |        4 |        1
28/01/06 |       79 |        5
29/01/06 |      444 |       38
30/01/06 |      494 |       49
31/01/06 |      531 |       71
01/02/06 |        5 |        1
02/02/06 |      258 |       25
03/02/06 |      393 |       86
04/02/06 |      125 |       42
05/02/06 |       86 |       18
06/02/06 |      136 |       10
07/02/06 |      610 |       79
08/02/06 |      521 |       88
09/02/06 |      132 |        6
10/02/06 |      960 |       94
11/02/06 |      670 |       85
12/02/06 |       14 |        1
</pre>
</p>    

