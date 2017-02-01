#!/usr/bin/python
#
# sync Remote ftp directory to local  -  2015 by meigrafd  -  v0.74
# source: remote
# target: local
#
# http://www.forum-raspberrypi.de/Thread-python-python-skript-ftp-sync?pid=154491#pid154491
#

import time, sys, os, re, curses
from datetime import datetime
from ftplib import FTP

#Dictionary docu: http://www.tutorialspoint.com/python/python_dictionary.htm
mirrorDirectories = {}

##----- CONFIG - START ----------------------------------------

ftpHost = '151.236.12.78'
ftpPort = 21
ftpUser = 'ftpuser'
ftpPass = 'ftp!user'
ftpTLS = False

## Verzeichnisse die gesynct werden sollen.
# Format: mirrorDirectories.update({"<local>":"<remote>"})
mirrorDirectories.update({"/home/pi/music":"/music"})
mirrorDirectories.update({"/home/pi/movie":"/movie"})

# Clean out the remote directory?
deleteAfterCopy = False

# Skip this files/dirs/extensions
skipList = ['.', '..', '.backup', '.svn', 'CVS', '.pyc', '.pyo']

##----- CONFIG - END ------------------------------------------


ascii_Files = (".txt", ".htm", ".html")

def write_pidfile_or_die(pidfile):
	if os.access(pidfile, os.F_OK):
		#if the lockfile is already there then check the PID number in the lock file
		with open(pidfile, 'r') as pf:
			pf.seek(0)
			old_pid = pf.readline()
		#Now we check the PID from lock file matches to the current process PID
		if os.path.exists("/proc/%s" % old_pid):
			print 'Error: You already have an instance of the program running.',
			print 'It is running as process %s' % old_pid
			sys.exit(1)
		else:
			print 'Lock File is there but the program is not running.',
			print 'Removing lock file for pid %s' % old_pid
			os.remove(pidfile)
	#Save current pid of script to file
	with open(pidfile, 'w') as pf:
		pf.write('%s' % os.getpid())

def endCurses():
	curses.echo()
	curses.endwin()

def putOut(message):
	try:
		if gV['l'] > (gV['output_max_y']-5): gV['l']=0 ; output.erase()
#		if gV['l'] > gV['output_max_y']:
#			gV['pad_pos']+=1
#			pad.refresh(gV['pad_pos'], 0, 5, 5, 10, gV['output_max_x'])
		output.addstr(gV['l'], 0, str(message) +'\n')
		output.refresh() #update the display immediately
		gV['l']+=1
	except:
		print message

def logError(message):
	#putOut('ERROR: '+str(message))
	print message


# http://www.forum-raspberrypi.de/Thread-python-ftp-upload-wieder-aufnehmen?pid=257332#pid257332
def file_size(path, conn):
    file_list = dict(conn.mlsd(os.path.dirname(path)))
    return int(file_list.get(os.path.basename(path), dict(size="0"))["size"])


def upload(source, dest, conn, callback=None):
    with open(source, "rb") as inf:
        server_side_size = file_size(dest, conn)
        inf.seek(server_side_size)
        conn.storbinary(
            "STOR /tmp/ftp-remote-test-file",
            inf,
            callback=callback,
            rest=str(server_side_size),
        )


#http://code.activestate.com/recipes/499334-remove-ftp-directory-walk-equivalent/
def ftpwalk(ftp, top, topdown=True, onerror=None):
	"""
	Generator that yields tuples of (root, dirs, nondirs).
	"""
	# Make the FTP object's current directory to the top dir.
	ftp.cwd(top)

	# We may not have read permission for top, in which case we can't
	# get a list of the files the directory contains.  os.path.walk
	# always suppressed the exception then, rather than blow up for a
	# minor reason when (say) a thousand readable directories are still
	# left to visit.  That logic is copied here.
	try:
		dirs, nondirs = _ftp_listdir(ftp)
	except os.error, err:
		if onerror is not None:
			onerror(err)
		return
	if topdown:
		yield top, dirs, nondirs
	for entry in dirs:
		dname = entry[0]
		path = os.path.join(top, dname)
		if entry[-1] is None: # not a link
			for x in ftpwalk(ftp, path, topdown, onerror):
				yield x
	if not topdown:
		yield top, dirs, nondirs

_calmonths = dict( (x, i+1) for i, x in
	enumerate(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')) )

def _ftp_listdir(ftp):
	"""
	List the contents of the FTP opbject's cwd and return two tuples of

	(filename, size, mtime, mode, link)

	one for subdirectories, and one for non-directories (normal files and other
	stuff).  If the path is a symbolic link, 'link' is set to the target of the
	link (note that both files and directories can be symbolic links).

	Note: we only parse Linux/UNIX style listings; this could easily be
	extended.
	"""
	dirs, nondirs = [], []
	listing = []
	ftp.retrlines('LIST', listing.append)
	for line in listing:
		# Parse, assuming a UNIX listing
		words = line.split(None, 8)
		if len(words) < 6:
			print >> sys.stderr, 'Warning: Error reading short line', line
			continue
		# Get the filename.
		filename = words[-1].lstrip()
		if filename in ('.', '..'):
			continue
		# Get the link target, if the file is a symlink.
		extra = None
		i = filename.find(" -> ")
		if i >= 0:
			# words[0] had better start with 'l'...
			extra = filename[i+4:]
			filename = filename[:i]
		# Get the file size.
		size = int(words[4])
		# Get the date.
		year = datetime.today().year
		month = _calmonths[words[5]]
		day = int(words[6])
		mo = re.match('(\d+):(\d+)', words[7])
		if mo:
			hour, min = map(int, mo.groups())
		else:
			mo = re.match('(\d\d\d\d)', words[7])
			if mo:
				year = int(mo.group(1))
				hour, min = 0, 0
			else:
				raise ValueError("Could not parse time/year in line: '%s'" % line)
		dt = datetime(year, month, day, hour, min)
		mtime = time.mktime(dt.timetuple())
		# Get the type and mode.
		mode = words[0]
		entry = (filename, size, mtime, mode, extra)
		if mode[0] == 'd':
			dirs.append(entry)
		else:
			nondirs.append(entry)
	return dirs, nondirs

def connectFtp():
	connected = True
	if ftpTLS:
		ftp = FTP_TLS()
	else:
		ftp = FTP()
	ftp.set_debuglevel(0)
	try:
		connect = ftp.connect(ftpHost, ftpPort, 10)
		login = ftp.login(ftpUser, ftpPass)
	except OSError, e:
		putOut('Got error: "%s"' % e)
		connected = False
	return ftp, connected


def transfer(ftp, remote_file, local_file, extension):
	putOut("Transfering: '"+remote_file+"'")
	gV['received_size'] = 0
	try:
		with open(local_file, 'wb') as lf:
			def callback(chunk):
				lf.write(chunk)
				gV['received_size'] += len(chunk)
				recsize=float(gV['received_size'])/1024
				status.move(0, 0) #move cursor to (new_y, new_x)
				status.clrtoeol() ; status.move(1, 0) ; status.clrtoeol()
				status.addstr(0, 0, '{} uploading Progress:'.format(remote_file))
				status.addstr(1, 0, '{0:10} kB / {1} kB'.format(round(recsize, 2), round(gV['remote_file_sizeKB'], 2)))
				status.refresh() #update the display immediately

			gV['start_time'] = time.time()
			if extension in ascii_Files:
				ftp.retrlines("RETR " + remote_file, callback)
				#ftp.retrlines("RETR " + remote_file, lambda s, w=outfile.write: w(s+"\n"), callback)
			else:
				ftp.retrbinary("RETR " + remote_file, callback)
	except Exception, e:
		putOut('transfer Error: %s' % (e))
		if os.path.isfile(local_file):
			os.remove(local_file)
		pass
		return
	gV['end_time'] = time.time()
	#check size of remote and local file to verfy complete transfer
	local_file_size = os.path.getsize(local_file)
	if local_file_size == gV['remote_file_size']:
		transfered.update({remote_dir : remote_file})
		transferTime = round(gV['end_time'] - gV['start_time'], 3)
		transferSpeed = round((float(gV['remote_file_sizeKB'])/1024) / transferTime, 3)
		putOut('File {} ({} bytes) seems to be finished.'.format(local_file, local_file_size),)
		putOut('Transfer took {} sec. ({} MB/s)'.format(transferTime, transferSpeed),)
		if deleteAfterCopy:
			try:
				ftp.delete(remote_file)
				putOut('Remote File Deleted.')
			except Exception, e:
				logError(e)
		putOut('-----')
	else:
		putOut('!! WARNING !! "{}" seems incomplete!'.format(local_file))
		putOut('local: {} remote: {}'.format(local_file_size, gV['remote_file_size']))


if __name__ == '__main__':
	pidfile = '/var/run/ftp_sync'
	write_pidfile_or_die(pidfile)
	gV = {} #globalVar's dictionary
	gV['l']=0 #output line count
	stdscr = curses.initscr() #init curses and create window object stdscr
	stdscr.clear()
	stdscr.refresh() #update the display immediately
	status = stdscr.subwin(0, 0) #(begin_y, begin_x)
	output = stdscr.subwin(4, 0)
	# http://stackoverflow.com/questions/2515244/how-to-scroll-text-in-python-curses-subwindow
	# http://ubuntuforums.org/showthread.php?t=1384598&p=8688465#post8688465
	#output.nodelay(1)
	gV['output_max_y'], gV['output_max_x'] = output.getmaxyx()
	pad = curses.newpad(gV['output_max_y'], gV['output_max_x'])
	gV['pad_pos'] = 0
	#pad.refresh(gV['pad_pos'], 0, 5, 5, 10, gV['output_max_x'])
	ftp = None
	try:
		ftp, connected = connectFtp()
		if not connected:
			putOut('Cant connect to remote! Exiting Script')
			sys.exit(1)
		for key in mirrorDirectories:
			localDir = key
			remoteDir = mirrorDirectories.get(key)
			if not os.path.exists(localDir):
				putOut('Local Directory {} doesnt Exists! Skipping!'.format(localDir))
			else:
				# cut maybe ending '/' away..
				localPath = localDir.rstrip('/')
				remotePath = remoteDir.rstrip('/')
				# remove all whitespace characters (space, tab, newline, and so on)
				pattern = re.compile(r'\s+')
				localPath = re.sub(pattern, '', localPath)
				remotePath = re.sub(pattern, '', remotePath)
				# change to remote dir
				try:
					ftp.cwd(remotePath)
				except OSError, e:
					putOut('Remote Directory {} doesnt Exists! Skipping!'.format(remotePath))
					continue
				# go through remote dir and check if it exists local..
				recursive = ftpwalk(ftp, remotePath, onerror=logError)
				for TopPath,subDirs,Files in recursive:
					#putOut(TopPath)
					#putOut(subDirs)
					#putOut(Files)
					remote_dir = TopPath
					gV['local_dir'] = remote_dir.replace(remotePath, localPath, 1)
					# check if remote dir exists local
					if not os.path.isdir(gV['local_dir']):
						putOut('Creating new directory: {}'.format(gV['local_dir']))
						os.makedirs(gV['local_dir'])
					if Files:
						transfered = {}
						for File in Files:
							#putOut(File)
							fileName = File[0]
							Basename, Extension = os.path.splitext(fileName)
							if Extension in skipList or Extension.endswith('~') or Extension.endswith('#') or Basename.startswith('.'):
								putOut("Skipping unwanted '%s'\n" % fileName)
								continue
							remote_file = remote_dir+'/'+fileName
							local_file = gV['local_dir']+'/'+fileName
							gV['remote_file_size'] = File[1] #bytes
							gV['remote_file_sizeKB'] = float(gV['remote_file_size'])/1024 #kBytes
							# check if remote file exists local and if its newer/bigger
							if os.path.isfile(local_file):
								valid=False
								if os.path.getsize(local_file) == gV['remote_file_size']:
									putOut("Skip: {} same size: l {} Vs. r {}".format(remote_file, os.path.getsize(local_file), gV['remote_file_size']))
									continue
								else:
									putOut("Bigger: {} size: l {} Vs. r {}".format(remote_file, os.path.getsize(local_file), gV['remote_file_size']))
									valid=True
								local_mtime = int(os.path.getmtime(local_file))
								remote_mtime = int(File[2])
								if not valid and local_mtime != remote_mtime:
									if local_mtime < remote_mtime:
										Type='remote newer'
										valid=True
									elif local_mtime > remote_mtime:
										Type='local newer'
									elif local_mtime == remote_mtime:
										Type='same'
									if valid == False:
										putOut("Skip: {} with {} timestamp: l {} Vs. r {}".format(remote_file, Type, local_mtime, remote_mtime))
										continue
							# transfere..
							transfer(ftp, remote_file, local_file, Extension)
						# clean up
						if deleteAfterCopy and transfered:
							for remotedir in sorted(transfered, reverse=True):
								try:
									ftp.rmd(remotedir)
									putOut('Remote Directory deleted: %s\n' % remotedir)
								except Exception, e:
									logError(e)
								putOut('-----')

#	except Exception, e:
#		print 'Error: %s' % (e)
	except (KeyboardInterrupt, SystemExit):
		putOut('\nQuit\n')
	try: ftp.close()
	except: pass
	endCurses()
	try: os.remove(pidfile)
	except: pass