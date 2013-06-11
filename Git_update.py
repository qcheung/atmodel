import subprocess

def run_command(command):
    p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    return p.communicate()

print "Committing changes..."
result = run_command('git commit -a -m \'update\'')
ret = result[0]
print "Commit DONE"
print "Commit Result:"
print ret

if 'git add' in ret:
    print 'Untracked files found, adding...'
    run_command('git add *.py')
    print 'Untracked files added DONE'
    print "Committing changes..."
    result = run_command('git commit -a -m \'update\'')
    print "Commit DONE"
    ret = result[0]
    
print "RESULT:"
print ret


input_read = raw_input("Do you want to upload your changes to website?(y/n)")
if 'y' in input_read:
    print 'Updating website...'
    command = 'git push origin master'
    p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    result = p.communicate()
    print result[0], 'test'
    p.stdin.write('zoom.aaron@gmail.com')
    p.communicate()
    p.stdin.write('baoding3213')
    result = p.communicate()
    print result[0]
