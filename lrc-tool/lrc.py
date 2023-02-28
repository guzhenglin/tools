# 将.lrc歌词全部提前或推迟, 并以原文件名覆盖保存
import os
import re

# 文件名
filename = ''

# 歌词
lrc = ''

def change(second):
	""" 修改并写回改变后的内容 """
	global lrc
	# 找到时间标签, 匹配 [01:23.456]
	timestamp = re.findall('\[([0-9]{0,3}\:[0-9]{0,2}\.[0-9]{0,3})\]', lrc)
	timestamp_n = []
	for i in range(len(timestamp)):
		min = timestamp[i].split(':')
		second_n = int(min[0]) * 60 + float(min[1]) - second
		if second_n < 0:	# 避免出现负值
			second_n = 0
		min_n = second_n // 60
		second_n = second_n % 60
		timestamp_n.append(('%02d' % min_n) + ':' + ('%05.2f' % second_n))
		lrc = lrc.replace(timestamp[i], timestamp_n[i])
	return lrc

def save():
	""" 覆盖保存文件 """
	with open(filename, 'w', encoding='utf-8') as fp:
		fp.write(lrc)

def main():
	""" 打开(.lrc)文件并返回文件内容 """
	global lrc
	global filename
	global total
	total=0
	# 询问提前时间
	while True:
		try:
			second = float(input('输入歌词要提前的时间(s): '))
			break
		# 防止输入非数字导致的程序终止
		except ValueError:
			print('请输入数字!\n\a')
	path=os.getcwd()
	for curDir, dirs, files in os.walk(path):
		for file in files:
			if file.endswith(".lrc"):
				print(os.path.join(curDir, file))
				filename = file.replace('"', '', 2)  # 将两个"删去
				if os.path.isfile(filename):
					if os.path.exists(filename):
						with open(filename, 'r', encoding='utf-8') as fp:
							lrc = fp.read()

							# 修改lrc
							lrc = change(second)
							total+=1
							save()
	print("共处理了"+str(total)+"个文件")
	os.system("pause")

if __name__ == "__main__":
	main()