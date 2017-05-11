# Juan Siasoco
# jsia894
# 8104859
import drive
import sys
import os


def Main():
	vdrive = ''
	while True:
		comm = ''
		name = ''
		args = ''
		indexer = 0
		try:
			user_input = input(" > ")
			if user_input == "quit":
				sys.exit()
			else:
				for x in user_input:
					if x == ' ':
						indexer +=1
						break
					else:
						comm += x
						indexer += 1			
				for y in range(indexer, len(user_input)):				
					if user_input[y] != ' ':
						name += user_input[y]
						indexer += 1
					else:
						indexer +=1
						break						
				args = user_input[indexer:]
						
				if comm == "format":
					try:
						vdrive = Volume(name)
						vdrive.format()
					except:
						print("Error: Cannot do format")
				elif comm == "reconnect":
					try:
						vdrive = Volume(name)
						
						vdrive.reconnect(name)

					except:
						print("File does not exist")

				elif comm == "disconnect":
					try:
						vdrive.disconnect()
					except:
						print("Nothing is connected")
				elif comm == "ls":
					vdrive.ls(name)
				elif comm == "mkfile":
					vdrive.mkfile(name)
				elif comm == "mkdir":
					vdrive.mkdir(name)
				elif comm == "append":
					pass
					#print(args)
					#vdrive.append(name,args)
				elif comm == "print":
					pass
				elif comm == "delfile":
					vdrive.delfile(name)
				elif comm == "deldir":
					vdrive.deldir(name)
				else:
					pass
		except:
			break
	pass
class Volume:
	BLK_SIZE = 512
	VOLUME_SIZE = 127
	EMPTY_BLK = ' ' * BLK_SIZE
	SEPARATOR = '\n**     **\n'
	count=128 #count where the blocks currently are. We will increment by 64 everytime to get to the next place
	block_content=[] #list of tuples. The tuples will include the file name, and a list containing a few bits of information including file type and the 
	bitmap='+'+('-'*127)
	bitmap=list(bitmap)

	def __init__(self, vdrive):
		self.vdrive = drive.Drive(vdrive)

	def format(self):
		
		self.vdrive.format()
		block_0 = "+"
		empty = '-'
		block1_to_127 = empty * 127
		vol_size = block_0 + block1_to_127		
		format_write = "f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 "
		file6 = format_write * 6
		vol_size += file6
		self.vdrive.write_block(0, vol_size)
		count=128
		block_content=[]

	def reconnect(self, name):
		self.vdrive.name = name
		self.vdrive.reconnect()


	def disconnect(self):
		self.file.close()



	def mkfile(self,name):
		#start bitmap count
		bitmap_count=0
		block_size = self.vdrive.read_block(0)
		#check if block size from 128 to 128+64 is the empty if it is, check that the name is less than 9
		if block_size[Volume.count:Volume.count+64]=="f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 ":
			if len(name) <= 9:				
				#split it at the / 
				name = name.split("/")
				#turn the block into a list so we can change it then proceed to update the values from 128 to 128+11 (max number for the name and type)
				root = list(block_size)	
				root[Volume.count:Volume.count+11] = "f:" + name[-1] + (" " * (9 - len(name[-1])))
				#then iterate through the blocks 0 to 127 and turn the first - symbol into a + then break. then you increment the count
				for i in block_size[0:127]:
					if i =='-':
						root[Volume.count+16:Volume.count+19]=('0'*(3-len(str(bitmap_count))))+str(bitmap_count)
						root[bitmap_count] = '+'
						break
					bitmap_count+=1
				#take the root. and join them into a string.
				new = "".join(root)
				#write to the block then increment the count
				self.vdrive.write_block(0,new)
				Volume.count+=64
			else:
				print("Name too long")
			
		else:
			print("not same")


	def mkdir(self,name):
		#start bitmap count
		bitmap_count=0
		block_size = self.vdrive.read_block(0)
		#check if block size from 128 to 128+64 is the empty if it is, check that the name is less than 9
		if block_size[Volume.count:Volume.count+64]=="f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 ":
			if len(name) <= 9:				
				#split it at the / 
				name = name.split("/")
				#turn the block into a list so we can change it then proceed to update the values from 128 to 128+11 (max number for the name and type)
				root = list(block_size)	
				root[Volume.count:Volume.count+11] = "d:" + name[-1] + (" " * (9 - len(name[-1])))
				#then iterate through the blocks 0 to 127 and turn the first - symbol into a + then break. then you increment the count
				for i in block_size[0:127]:
					if i =='-':
						root[Volume.count+16:Volume.count+19]=('0'*(3-len(str(bitmap_count))))+str(bitmap_count)
						root[bitmap_count] = '+'
						break
					bitmap_count+=1
				#take the root. and join them into a string.
				new = "".join(root)
				#write to the block then increment the count
				self.vdrive.write_block(0,new)
				Volume.count+=64
			else:
				print("Name too long")
			
		else:
			print("block taken")

	def ls(self,directory):
		block_size = self.vdrive.read_block(0)
		root=list(block_size)
		block_number=128
		name=''
		#If the directory called is the root print the header and iterate through the 6 blocks. Onnce the counter block_number hits 512, it means we've reached the end of the file
		if directory=="/":
			print("Directory: "+directory)
			print("Name      Type   Size   Allocated Blocks")
			print("----      ----   ----   ----------------------------------------------------")
			while block_number!=512:
				#Check if the name is empty, if it is, append to the block content. Then, print out the name, the type, the size and the values in the allocated blocks
				if block_size[block_number+2:block_number+11]!="         ":
					Volume.block_content.append((block_size[block_number+2:block_number+11],block_size[block_number]))
					name=block_size[block_number+2:block_number+11]
					print(name +'   '+block_size[block_number]+'    '+block_size[block_number+11:block_number+15]+'   '+block_size[block_number+16:block_number+64])
				block_number+=64
				#reset the block content, just so this doesn't grow in size everytime we call ls /
				Volume.block_content=[]

		#This is useful for the delfile and deldir. It basically collects the relevant information, to know that the file it is deleting actually exists
		#Note this doesn't set the block number back, thats because it does that at the delfile and deldir, after it calls these.
		elif directory == "delfile":
			while block_number!=512:
				if block_size[block_number+2:block_number+11]!="         ":
					#This adds the relevant information abot each file name into a list of tuples called block_content.
					#The tuple consists of the following (file name, [the filetype, where it is written to on the 6 pssible places, its bitmap location, the length of the file])
					Volume.block_content.append((block_size[block_number+2:block_number+11].replace(" ",""),[block_size[block_number],block_number,block_size[block_number+16:block_number+19],block_size[block_number+11:block_number+15]]))
				block_number+=64


	def delfile(self,filename):
		bitmap_count=0
		block_size = self.vdrive.read_block(0)
		root=list(block_size)
		#We call the delfile ls here because this one stores some stuff into our list of tuples that has all of the information we need. See ls for details
		self.ls('delfile')
		name = filename.split("/")
		name=''.join(name)
		#Iterate through every tuple in the list check the first value of the tuple which is the name. See if the name is equivalent to the filename
		for i in Volume.block_content:
			if i[0]==name:
				#ensure that this name is of the type file. if it is, update it to the original value which is f:     0000:.....etc
				if i[1][0]=="f":
					root[i[1][1]:i[1][1]+64]="f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 "
					#delete item from bitmap
					root[int(i[1][2])]='-'
					new="".join(root)
					self.vdrive.write_block(0,new)
					Volume.count=i[1][1]
		#turn the block content into empty again
		Volume.block_content=[]	

	def deldir(self,filename):
		block_size = self.vdrive.read_block(0)
		root=list(block_size)
		#We call the delfile ls here because this one stores some stuff into our list of tuples that has all of the information we need. See ls for details
		self.ls('delfile')
		name = filename.split("/") 	
		name=''.join(name)
		#Iterate through every tuple in the list check the first value of the tuple which is the name. See if the name is equivalent to the filename
		for i in Volume.block_content:
			if i[0]==name:
				#ensure that this name is of the type file. if it is, update it to the original value which is f:     0000:.....etc
				if i[1][0]=="d":
					root[i[1][1]:i[1][1]+64]="f:         0000:000 000 000 000 000 000 000 000 000 000 000 000 "
					#delete item from bitmap
					root[int(i[1][2])]='-'					
					new="".join(root)
					self.vdrive.write_block(0,new)
					Volume.count=i[1][1]
		#turn the block content into empty again					
		Volume.block_content=[]	

#	def append(self,filename,data):
#		length_of_file=0
#		data=data[1:-1]
#		block_size = self.vdrive.read_block(0)
#		root=list(block_size)
#		self.ls('delfile')
#		name = filename.split("/") 	
#		name=''.join(name)
#		for i in Volume.block_content:
#			#Check if file exists
#			if i[0]==filename:
				#Check length of the file
#				length_of_file=int(i[1][3])+len(data)
#				if length_of_file%512==0:
#					number_of_blocks=math.ceil(length_of_file/512)
#
#				elif length_of_file%512!=0:





class DirectoryEntry():
	pass

Main()
