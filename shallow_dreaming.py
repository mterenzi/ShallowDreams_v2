'''
Some info on various layers, so you know what to expect
depending on which layer you choose:

layer 1: wavy
layer 2: lines
layer 3: boxes
layer 4: circles?
layer 5: Hell
layer 6: dogs, bears, cute animals.
layer 7: faces, buildings
layer 8: fish begin to appear, frogs/reptilian eyes.
layer 10: Monkeys, lizards, snakes, duck

Choosing various parameters like num_iterations, rescale,
and num_repeats really varies on which layer you're doing.


Layer 3: 20 iterations, 0.5 rescale, and 8 repeats is decent start
Layer 10: 40 iterations and 25 repeats is good.
'''

from deepdreamer import model, load_image, recursive_optimize
from make_video import construct_video
from pathlib import Path
import numpy as np
import PIL.Image
import random
import cv2
import shutil
import os



def define_parameters():
	dream_name = input('Name your dream: ')
	base_file = input('Provide a base file: ')
	max_frames = int(input('How many frames should we dream for?: '))
	if input('Do you want to let the colors flow?: (y/n) ').lower() == 'y':
		random_color = True
	else:
		random_color = False

	return dream_name, base_file, max_frames, random_color


def perform_setup(dream_name, base_file):
	path_root = Path('.')
	path_dreams = path_root / 'dreams'
	path_dream_name = path_dreams / dream_name
	if os.path.exists(path_dream_name):
		shutil.rmtree(path_dream_name)
	os.makedirs(path_dream_name)

	base_file = path_root / 'inputs' / base_file
	img_result = load_image(filename=base_file)
	shutil.copy(base_file, path_dream_name/'img_0.jpg')

	y_size, x_size = img_result.shape[:-1]
	layer_index = random.randint(1, 10)
	return path_dream_name, y_size, x_size, layer_index


def dream_loop(path_dream_name, max_frames, y_size, x_size, layer_index, random_color):
	r
	g
	b
	for i in range(max_frames):

		if os.path.isfile(path_dream_name/f'img_{i+1}.jpg'):
			print(f'{i+1} already exists, continuing along...')			
		else:
			img_result = load_image(filename=path_dream_name/f'img_{i}.jpg')

		# this impacts how quick the "zoom" is
		x_trim = 2
		y_trim = 1

		img_result = img_result[0+x_trim:y_size-y_trim, 0+y_trim:x_size-x_trim]
		img_result = cv2.resize(img_result, (x_size, y_size))

		# Use these to modify the general colors and brightness of results.
		# results tend to get dimmer or brighter over time, so you want to
		# manually adjust this over time.

		# +2 is slowly dimmer
		# +3 is slowly brighter
		for j in range(3):
			if not random_color:
				img_result[:, :, j] += 5 if i % 3 == 0 else 2
			else:
				img_result[:, :, j] += random.randint(-2, 7)

		img_result = np.clip(img_result, 0.0, 255.0)
		img_result = img_result.astype(np.uint8)

		if i % 20 == 0:
			layer_index = random.randint(1, 10)
			while layer_index == 5:
				layer_index = random.randint(1, 10)
			fraction = layer_index / 10
			repeats = max(1, int(6 * fraction))
			iterations = max(1, int(12 * fraction))

			print()
			print('Layer Index: ' + str(layer_index))
			print('Repeats: ' + str(repeats))
			print('Iterations: ' + str(iterations))
			print()
		
		img_result = recursive_optimize(layer_tensor=model.layer_tensors[layer_index],
										image=img_result,
										num_iterations=iterations,
										step_size=1.0,
										rescale_factor=0.7,
										num_repeats=repeats,
										blend=0.2)

		img_result = np.clip(img_result, 0.0, 255.0)
		img_result = img_result.astype(np.uint8)
		result = PIL.Image.fromarray(img_result, mode='RGB')
		result.save(path_dream_name/f'img_{i+1}.jpg')
		print(f'Finished {i+1}/{max_frames}')


if __name__ == '__main__':
	print() # Buffer Tensorflow Startup

	dream_name, base_file, max_frames, random_color = define_parameters()

	path_dream_name, y_size, x_size, layer_index = perform_setup(dream_name, base_file)

	dream_loop(path_dream_name, max_frames, y_size, x_size, layer_index, random_color)

	if input('\nConstruct video?: (y/n) ').lower() == 'y':
		will_lengthen = True if input('Do you want to lengthen the video?: ').lower() == 'y' else False
		construct_video(dream_name, will_lengthen)
