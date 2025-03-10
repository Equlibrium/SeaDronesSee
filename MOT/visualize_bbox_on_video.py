import argparse
import json

import cv2
import time
import os

'''
one color for each category (excluding category nr 7)
    1: swimmer
    2: floater
    3: boat
    4: swimmer on boat
    5: floater on boat
    6: life jacket
    7: ignored
'''
colors = {1: (0,255,0), 2: (0,0,255), 3: (255,255,51), 4: (0,255,255), 5: (255, 102, 255), 6: (51, 153, 255)}

if __name__ == '__main__':
    scriptTime = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--annotation', type=str, default=None, help='path to the annotations json file')
    parser.add_argument('--pictures', type=str, default=None, help='path to the pictures')
    parser.add_argument('--output', type=str, default=None, help='Path to output')
    options = parser.parse_args()
    if (options.annotation == None):
        print("Please enter a valid path to the annotation json file ")
        exit()
    if (options.pictures == None):
        print("Please enter a valid path to folder where the pictures are located")
        exit()
    if (options.output == None):
        print("Please enter a valid path for the output directory, where the pictures will be saved")
        exit()

    with open(options.annotation) as f:
        data = json.load(f)

        # needed to show the current progression
        numberOfImages = len(data['images'])
        currentImage = 0

        # currently the video has fixed 30 frames per second
        width = data['images'][0]['width']
        height = data['images'][0]['height']
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fps = 30
        count = 0
        videoName = options.output + "\\video_" + str(fps) + "fps_" + str(count) + ".avi"
        # avoid overriding existing videos
        # is not really needed because a new output folder will be generated each time the script runs
        while os.path.isfile(videoName):
            count += 1
            videoName = options.output + "\\video_" + str(fps) + "fps_" + str(count) + ".avi"
        out = cv2.VideoWriter(videoName, fourcc, fps, (width, height))
        for image in data['images']:
            currentImage += 1
            img = cv2.imread(options.pictures + "\\" + image['file_name'])
            start = time.time()
            # draw all boundingBoxes, which belong to one image, on it with the corresponding colors of the categories
            for annotation in data['annotations']:
                if annotation['image_id'] == image['id']:
                    topLeftX = annotation['bbox'][0]
                    topLeftY = annotation['bbox'][1]
                    width = annotation['bbox'][2]
                    height = annotation['bbox'][3]
                    for category in data['categories']:
                        if category['id'] == annotation['category_id']:
                            label = category['name']
                    cv2.rectangle(img, (topLeftX, topLeftY), (topLeftX + width, topLeftY + height), colors[annotation['category_id']], 3)
            out.write(img)
            print('Finished: {0}%'.format(round((currentImage / numberOfImages) * 100, 2)))
        # save video
        out.release()
        scriptRunTime = time.time() - scriptTime
        print('\nScript run time in seconds: {0}'.format(scriptRunTime))
        print("mean time per image: {0}".format(scriptRunTime / numberOfImages))