<!-- Linux info -->

<a name="where"></a>
<h4>Download</h4>
<p>
<u><b>Latest release</b></u><br>
<a href="http://prdownloads.sourceforge.net/pytelemeter/pytelemeter_1.5.tar.gz?download">pytelemeter-1.5</a><br>
Older releases can be found <a href="http://sourceforge.net/project/showfiles.php?group_id=99970">here</a>. <!--and a changelog is available <a href="/CHANGELOG">here</a>.-->
<br><br>

<u><b>Packages</b></u><br>
<a href="http://prdownloads.sourceforge.net/pytelemeter/pytelemeter_1.5-0ubuntu1_all.deb?download">Debian package</a> 

<br><br>

<u><b>Repository</b></u><br>
A repository is available as well, this command will add the repository to your /etc/apt/sources.list file and get the signed key. It 
should be added to the official Ubuntu repositories later.<br><br>

<i>sudo su -c ' echo "deb http://ppa.launchpad.net/bamps-kristof-gmail/ppa/ubuntu jaunty main" >> /etc/apt/sources.list' && gpg 
--no-default-keyring --keyring /tmp/piratenaapje.keyring --keyserver keyserver.ubuntu.com --recv   
8A324B856F5C4271D7A9B4137E266B27D4632108 && gpg --no-default-keyring --keyring /tmp/piratenaapje.keyring --export --armor  
8A324B856F5C4271D7A9B4137E266B27D4632108 | sudo apt-key add - && rm /tmp/piratenaapje.keyring</i>
<br><br>
To install it, type <i> sudo aptitude install pytelemeter </i> in a terminal<br><br>

<u><b>Dependencies</b></u><br>
You need some other software to get pytelemeter running:
<ul>
<li><a href="http://www.python.org">Python</a> &gt;= 2.2.x<br>
(If it works with older versions of Python, let me know)
</li>
<li><a href="http://www.pygtk.org">PyGTK</a> &gt;= 2.0.0<br>
(Including python-gnome-extras for the tray icon and Glade for the GUI)
</li>
<li><a href="http://pywebsvcs.sourceforge.net">SOAPpy</a>
 and <a href="http://pyxml.sourceforge.net">PyXML</a> &gt;= 0.8.3<br>
(Needed for the <a href="http://www.google.com/search?q=telemeter4tools">Telemeter4Tools</a> Parser)
</li>
</ul>
</p>

