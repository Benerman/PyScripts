import os, subprocess, json, sys



def disc_loaded(drive_name):
  if windows:
    pass
  else:
    cmd_out = json.loads(subprocess.check_output('lsblk --json', shell=True).decode('utf8', 'strict'))
    for i,v in enumerate(cmd_out['blockdevices']):
      # print(i,v)
      if drive_name in cmd_out['blockdevices'][i]['name'] and cmd_out['blockdevices'][i]['mountpoint'] != None:
        # print(f"drive: {drive_name}, field: {cmd_out['blockdevices'][i]['name']},"
        # " mount: {cmd_out['blockdevices'][i]['mountpoint']}")
        return True
    return False



try:
  windows = os.environ['OS']
  windows = True
except KeyError:
  windows = False
if len(sys.argv) == 2:
  drive_name = sys.argv[1]
else:
  drive_name = input('Provide disc drive to process on: ')

if disc_loaded(drive_name):
  print('Disc is loaded')
  mkv_out = subprocess.check_output(f'makemkvcon -r --cache=1 info dev:/dev/{drive_name}', shell=True).decode('utf8', 'strict')
  titles = []
  for line in mkv_out:
    if 'TCOUNT:' in line:
      total_titles = line.split(':')[-1]
      print(f'Total Titles = {total_titles}')
    if 'TINFO:0' in line:
      titles.extend(line)
  print(len(titles))
  for line in titles:
    if 'GB' in line:
      print(line)
