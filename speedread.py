from os.path import expanduser
import sys
import subprocess


speed = ' -w 400'
home = expanduser("~")
speedread_path = '/tools/speedread/speedread'
tool_path = home + speedread_path
conversion_command = 'pdftotext'

if len(sys.argv) != 2:
    print('Please select a pdf file to speedread')
    quit()
filename = sys.argv[1]
if filename[-4:] != '.pdf':
    print('Please select a pdf file to speedread')
    quit()

subprocess.run(conversion_command + ' ' + filename, shell=True, check=True)
txt_file = filename[:-4] + '.txt'
subprocess.run('cat ' + txt_file + ' | ' + tool_path + speed, shell=True, check=True)
