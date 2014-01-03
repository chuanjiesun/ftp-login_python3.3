#All I need is YOU
from ftplib import FTP
import ftplib, sys, re, socket, os

#shuru_ip = input('input a ftp server ip : ')
#ip = '192.168.163.129'
patt = 'pwd|cwd|dir|retr|stor|rename|delete|mkd|rmd|help'#允许的命令

length = len(sys.argv)
if length != 2:#判断是否有参数
	print('Parameter error! We need one parameters.')
	print('For example : '
			+'python  '+sys.argv[0] +'  ip/hostname')
else:
	ip = socket.gethostbyname(sys.argv[1])
	#ip = sys.argv[1]
	print('{} <=> {}'.format(sys.argv[1], ip))
	print('Usage: \n'
			+'      python '+sys.argv[0]+'  '
			+ ip +'\n')

	
	try:#判断是否可连接
		ftp = FTP(ip)
		print('Connected to {}.'.format(ip))
#		ftp.set_debuglevel(0)
		resp = ''


		ftp_version = ftp.connect()
		print(ftp_version)#打印连接后ftp服务端信息
		
		name = input('Name ({}:root): '.format(ip))
		print('331 Please specify the password.')
		password = input('Password: ')
		try :
			resp = ftp.login(name, password)
			print('try to login: {}'.format(resp))
		except ftplib.error_perm as e:
			#print('error is : {}'.format(e))
			print(e)

			
		resp1 = re.match('230 ', resp)	
		#if resp == '230 Login successful.': #含有230这个登录成功的代码
		if resp1 is not None: #登录成功
			flag = True
			print('\nAvaiable Command :\n'+
			' pwd  dir  q   quit   exit   h      help   '+
			' cwd(\'/xxx\')    delete(\'/xxx\') \n mkd(\'/xxx\')  '+
			' rmd(\'/xxx\')   retr(\'file\')   stor(\'file\')  '+
			' rename(\'old\', \'new\')\n')
		else :
			flag = False
		print(flag)#登录成功标志位
		

		
		while flag:
			mingling = input('ftp> ')
			mingling_space = mingling.strip()
			mingling_match = re.match(patt, mingling)
			patt_path = '(?<=\(\')/?[\w+/]{0,}[\w+]{0,}[\.\w+]{0,}' #dir('/xxx/xxx') cwd('/xxx/xxx.txt') 字符串不需要把引号带入到函数
			patt_rename_old = '(?<=rename\(\')\w+[\.\w+]{0,}'
			patt_rename_new = '(?<=\')\w+[\.\w+]{0,}(?=\'\))'#前向与后向界定匹配
								#rename('old',  'new')
			mingling_rename_old = re.search(patt_rename_old, mingling)
			mingling_rename_new = re.search(patt_rename_new, mingling)
			mingling_dir = re.search(patt_path, mingling)
			mingling_delete = re.search(patt_path, mingling)
			mingling_mkd = re.search(patt_path, mingling)
			mingling_rmd = re.search(patt_path, mingling)
			mingling_cwd = re.search(patt_path, mingling)
#			patt_retr_stor = '(?<=\(\')\w+[\.\w+]{0,}'
			mingling_retr = re.search(patt_path, mingling)
			mingling_stor = re.search(patt_path, mingling)
#			mingling_retrbinary = re.search(patt_path, mingling)
#			mingling_storbinary = re.search(patt_path, mingling)
			if (mingling_space == 'exit') or (mingling_space == 'quit') or (mingling_space == 'q'):
				flag = False
				print('it\'s going to exit...')
			elif  (mingling_space == 'help') or (mingling_space == 'h'):
				print('\nAvaiable Command :\n'+
					' pwd  dir  q   quit   exit   h      help   '+
					' cwd(\'/xxx\')    delete(\'/xxx\') \n mkd(\'/xxx\')  '+
					' rmd(\'/xxx\')   retr(\'file\')   stor(\'file\')  '+
					' rename(\'old\', \'new\')\n')
			else:
				if mingling_match is not None:
					print(mingling)
#					print(mingling_retr.group()) 
#					print(mingling_rename_new.group()) 
					if mingling == 'pwd':
						print(ftp.pwd())
					elif mingling == 'dir':
						ftp.dir()
					elif (mingling_match.group() == 'dir') and (mingling_dir is not None):
#						print(mingling)
#						print(mingling_dir.group())
#						print(mingling_dir.group())
						ftp.dir(mingling_dir.group())
					elif (mingling_match.group() == 'cwd') and (mingling_cwd is not None):
#						print(mingling)
#						print(mingling_cwd.group())
						ftp.cwd(mingling_cwd.group())
					elif (mingling_match.group() == 'rename') and (mingling_rename_old is not None) and (mingling_rename_new is not None):
						ftp.rename(mingling_rename_old.group(), mingling_rename_new.group())
					elif (mingling_match.group() == 'delete') and (mingling_delete is not None):
						ftp.delete(mingling_delete.group())
					elif (mingling_match.group() == 'mkd') and (mingling_mkd is not None):
						ftp.mkd(mingling_mkd.group())
					elif (mingling_match.group() == 'rmd') and (mingling_rmd is not None):
						ftp.rmd(mingling_rmd.group())
					elif (mingling_match.group() == 'retr') and (mingling_retr is not None):
						f_w = open(mingling_retr.group(), 'wb')
						ftp.retrbinary("retr {}".format(os.path.basename(mingling_retr.group())),f_w.write)
						f_w.close()
					#	retrlines效果不太好 #download a file
					#	print(retr)
					elif (mingling_match.group() == 'stor') and (mingling_stor is not None):
						f_r = open(mingling_stor.group(), 'rb')
						ftp.storbinary("stor {}".format(os.path.basename(mingling_stor.group())),f_r)
						f_r.close()
#					# upload a file 
#
					else:
						print('command syntax error! please try "help" for more details.')
				else:
					print('command not exists.\n'+
							'please try "help" for more details.')
		quit = ftp.quit()
		print('exiting ...'.format(quit))
	except Exception as e:
		print('error occured : {}'.format(e))
