import subprocess
def run_command(command):
    p = subprocess.Popen(command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    return p.communicate()

print 'Pulling updates from website...'
command = 'git pull https://github.com/guanyilun/atmodel.git master'
result = run_command(command)
ret = result[0]
print "pulling DONE"
print "RESULT:"
print ret
