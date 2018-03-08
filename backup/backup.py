#!/usr/bin/python
import time, os, requests,glob,boto,sys;
import simplejson as json;
from datetime import datetime;
from datetime import timedelta;
from subprocess import Popen, PIPE;
import gzip;

from boto.s3.key import Key


print("Starting backup script")

needadVars = ['DISCOVERYURL',
			'S3_BUCKET','S3_ACCESSID','S3_ACCESSKEY',
			'BACKUP_NAME','BACKUP_INTERVAL',
			'MYSQL_HOST','MYSQL_USER','MYSQL_ROOT_PASSWORD','MYSQL_DB'];

for needed in needadVars:
	if not (os.environ[needed] and os.environ[needed].strip() ):
		print(needed +" needed\n");
		exit(-1);

disocveryURL = os.environ['DISCOVERYURL'] + '/backup/' + os.environ['BACKUP_NAME'];
print("using disocveryURL:" + disocveryURL);

TIMEFORMAT = "%Y-%m-%d %H:%M:%S.%f";

dumpCommand = 'mysqldump -v -h ' + os.environ['MYSQL_HOST'] \
	+ ' -u ' + os.environ['MYSQL_USER'] \
	+' -p' + os.environ['MYSQL_ROOT_PASSWORD'] \
	+ ' ' + os.environ['MYSQL_DB']

#args = ['mysqldump', '-h', os.environ['MYSQL_HOST'] ,'-u', os.environ['MYSQL_USER'], '-p'+os.environ['MYSQL_ROOT_PASSWORD'], '--databases', os.environ['MYSQL_DB']]



#print("dump command = " + str(dumpCommand));


while 1:
	print("checking if backup needed");

	mykey = requests.get(url=disocveryURL);

	if mykey :
#		datar = mykey.json();
#		print ("datar :" + str(datar));
		myKeyData = json.loads(mykey.json()["node"]["value"]);
	else :
		print("my key does not exist");
		myKeyData = json.loads('{"lastbackup":"' + datetime.strftime(datetime.now() -timedelta(days=1) ,TIMEFORMAT) + '"}');

	print("using keydata :" + repr(myKeyData));

	print ("last backup time : "+ myKeyData['lastbackup']);

	nextonewouldbe =datetime.strptime(myKeyData['lastbackup'], TIMEFORMAT) + timedelta(hours=int(os.environ['BACKUP_INTERVAL']));
	print ("next backup time : "+ str(nextonewouldbe))

	currentTime = datetime.now();
	print (" currentTime : "+ str(currentTime))

	if currentTime >= nextonewouldbe:
		print("starting back up");
		
		if not os.path.exists('/backup'):
			os.makedirs('/backup')

		for f in glob.glob("/backup/*.gz"):
			os.remove(f)

		for x in range(0, 3):

			fileNameOnly = datetime.strftime(datetime.now() -timedelta(days=1) ,"backup_%Y-%m-%d %H-%M-%S.sql.gz");
			mysqlfile = "/backup/" + fileNameOnly;

			print ('mysqlfile='+mysqlfile)

			p = Popen(dumpCommand, shell=True, stdout=PIPE);
			with gzip.open(mysqlfile, "wb") as f:
				f.writelines(p.stdout)

			exitcode = p.wait();
			print("exitcode = " + str(exitcode));

			currentTime = datetime.now();

			if 0 == exitcode:
				print (" backupcompleted at : "+ str(currentTime) +' starting upload');

				#we have exception if upload fails
				try:
					s3Conn =  boto.connect_s3(os.environ['S3_ACCESSID'], os.environ['S3_ACCESSKEY'])
					bucket = s3Conn.get_bucket(os.environ['S3_BUCKET'])
					s3Key = Key(bucket)
					s3Key.key = 'dbbackup/' + os.environ['BACKUP_NAME'] + '/' + fileNameOnly

					print("uploading to :" + os.environ['S3_BUCKET'] + " : " + s3Key.name)
					s3Key.set_contents_from_filename(mysqlfile)

					os.remove(mysqlfile)

					print ("back up sucess")
					break

				
				except Exception, e:
					print('Failed to upload : '+ str(e))
					#todo: alarm

			else :
				print("backup failed. will try again");

			print("waiting 30 seconds before trying again")
			sys.stdout.flush()
			time.sleep(30);

		myKeyData['lastbackup'] =  datetime.strftime(currentTime ,TIMEFORMAT);
		jsonKey = json.dumps(myKeyData);
		print("new keydata ="+ jsonKey);
		requests.put(disocveryURL,data={'value':jsonKey});

		nextonewouldbe = currentTime + timedelta(hours=int(os.environ['BACKUP_INTERVAL']));
	else :
		print("backup not scheduled")

	print("next backup  scheduled at " + str(nextonewouldbe));
	timeleft = nextonewouldbe - currentTime;

	print("sleep for seconds :"+ str(timeleft.total_seconds()));
	sys.stdout.flush()
	time.sleep(timeleft.total_seconds());
