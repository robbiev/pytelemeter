<!-- Development -->

<a name="install"></a>
<h4>Install</h4>
<p>
<b>NOTE:</b> If you are using a distribution specific package, follow your distribution's instructions.<br><br>
<u><b>Installation</b></u><br>
You need to be root to install pytelemeter. If you don't have root, just copy all .py
files in the distribution into a dir and run it from that dir.<br>
Just run as root (using sudo is even better, but this should always work):<br><br>

<code>python setup.py install</code><br>
<br>
<u><b>Setting up for use</b></u><br>
Log on with your normal user account to set up a config file:<br><br>
<code>
cp pytelemeterrc ~/.pytelemeterrc<br><br>
</code>
Edit ~/.pytelemeterrc to match your Telenet login and password.<br>
Last but not least, chmod your config file to safe permissions:<br>
<br>
<code>chmod 600 ~/.pytelemeterrc<br><br>
</code>
Now run pytelemeter-gtk, pytelemeter-tray or pytelemeter-cli (add -h to view cli options).<br><br>
Don't forget to read the <a href="index.php?support">FAQ section</a> if you encounter any problems.
</p>

