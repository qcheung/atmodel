import subprocess

def run_command(command):
    p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    return p.communicate()

result = run_command('git commit -a -m \'update\'')
ret = result[0]

if 'git add' in result[0]:
    print 'in'
    result = run_command('git add *.py')

print result[0]
