import subprocess

def run_command(command):
    p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    return p.communicate()

result = run_command('git commit -a -m \'update\'')
ret = result[0]

if 'git add' in ret:
    print 'in'
    run_command('git add *.py')
    result = run_command('git commit -a -m \'update\'')
    ret = result[0]
    
print ret
