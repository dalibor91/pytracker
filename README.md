# pytracker
Program for tracking changes of files in some directory on linux

Usage 
```
./pytracker '/home/' '.php'
```
or 
```
./pytracker '/home/' '.php' -d
```
If you want to track if files are deleted

it will parse all files and enter it in sqllite db 
next time run same command and 
for changed files it will print out which files were changed 


So first time when you run it you will see something like 
```
New   /home/test/test.php
New   /home/test/test1.php
New   /home/test/test2.php
```

Next time when you run it, if nothing is changed inside this 3 files you will get empty output 
else if something is changed you will get 

```
Modified /home/test/test1.php
```

If file is deleted, you will get (if you addded -d as argument)

```
Deleted /home/test/test2.php
```


