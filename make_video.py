import cv2
import os
import shutil
import PIL.Image
from pathlib import Path



def lengthen(dream_length, path_dream_name):
	multiply = int(input('How many times longer should it be?: (int) '))
	frames = []
	for i in range(dream_length+1):
		img_path = path_dream_name / f'img_{i}.jpg'
		frame = cv2.imread(str(img_path))
		frames.extend([frame for _ in range(multiply)])
	for i in range(len(frames)):
		cv2.imwrite(str(path_dream_name/f'img_{i}.jpg'), frames[i])
	return dream_length * multiply



def construct_video(dream_name, will_lengthen):
	path_root = Path('.')
	path_dreams = path_root / 'dreams'
	path_dream_name = path_dreams / dream_name

	# Windows:
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	# Linux:
	#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

	frame = cv2.imread(str(path_dream_name/'img_0.jpg'))
	height, width = frame.shape[:-1]

	out = cv2.VideoWriter(str(path_dream_name/f'{dream_name}.avi'), fourcc, 30.0, (width,height))

	dream_length = 0
	while True:
		if os.path.isfile(path_dream_name/f'img_{dream_length+1}.jpg'):
			pass
		else:
			break
		dream_length += 1

	if will_lengthen:
		dream_length = lengthen(dream_length, path_dream_name)


	for i in range(dream_length + 1):
		img_path = path_dream_name / f'img_{i}.jpg'
		print(img_path)
		frame = cv2.imread(str(img_path))
		out.write(frame)

	out.release()


if __name__ == '__main__':
	dream_name = input('What is the name of the dream?: ')
	will_lengthen = True if input('Do you want to lengthen the video?: (y/n) ').lower() == 'y' else False
	construct_video(dream_name, will_lengthen)
