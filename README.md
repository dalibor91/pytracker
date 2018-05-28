# pytracker
Program for tracking changes of files in some directory on linux, for specific file extension. 

Created for tracking uploads directory on some old joomla websites 
so any suspicious upload will be reported.

Usage 
```
pytracker '/home/' '.php'
```
or 
```
pytracker '/home/' '.php' -d
```
If you want to track if files are deleted

When you run program first time it will parse all files and enter all files in sqlite db.

So first time when you run it you will see something like 
```
New   /home/test/test.php
New   /home/test/test1.php
New   /home/test/test2.php
```

Next time when you run it, if nothing is changed inside of files you will get empty output 
else if something is changed you will get 

```
Modified /home/test/test1.php
```

If file is deleted, you will get (if you added -d as argument)

```
Deleted /home/test/test2.php
```
*INSTALL*

```
sudo mkdir /var/lib/pytracker && \
sudo curl -o /var/lib/pytracker/pytracker https://raw.githubusercontent.com/dalibor91/pytracker/master/pytracker.py && \
sudo chmod +x /var/lib/pytracker/pytracker && \
sudo ln -s /var/lib/pytracker/pytracker /usr/bin/pytracker
```

*HISTORY*

You are also able to search history, 
```
pytracker '/home/' '.php' -history
```
will give you all history records when we had some changes on files 
and 
```
pytracker '/home/' '.php' -history '{some_history_id}'
```
will give you what changed for that specific History ID

*IGNORE*

Ignoring specific files is also posible .
To add new file to ignore list run 
```
pytracker '/home/' '.php' -ignore '/home/path_to_file'
```

To remove file from ignore list run 
```
pytracker '/home/' '.php' -unignore '/home/path_to_file'
```

To see all ignored files run 
```
pytracker '/home/' '.php' -ignore-list
```


# v2

```

```




