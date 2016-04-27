import os
rootdir = './'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        sum = 0
        log = open(subdir+'/'+file).read().split("commit")
        for commit in log:
            if "fix" in commit:
                sum += 1
        name = subdir.split('/')
        if len(name) > 2:
            print name[2] + "\t" + str(sum) + "\t" + str(len(log))
        else: 
            print subdir + "\t" + str(sum) + "\t" + str(len(log))
