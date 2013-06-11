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
