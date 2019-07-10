import os
import time
import picamera
import cv2
import numpy as np
import json
def calibrationPhotoSeries():

    from stereovision.calibration import StereoCalibrator
    from stereovision.calibration import StereoCalibration
    # Global variables preset
    countdown = 5  # Interval for count-down timer, seconds
    photo_counter = 0  # Photo counter
    photo_width = 1280
    photo_height = 720
    total_photos = 15

    wn = cv2.namedWindow('preview', cv2.WINDOW_NORMAL)

    # Lets start taking photos!
    print
    "Starting photo sequence"
    with picamera.PiCamera() as camera:
        camera.resolution = (photo_width, photo_height)
        camera.start_preview()
        camera.preview.fullscreen = False
        camera.preview.window = (0, 0, photo_width / 2, photo_height / 2)
        camera.annotate_text_size = 160
        camera.annotate_background = picamera.Color('red')
        camera.hflip = True
        while photo_counter != total_photos:
            photo_counter = photo_counter + 1
            filename = 'scene_' + str(photo_width) + 'x' + str(photo_height) + '_' + \
                       str(photo_counter) + '.png'
            cntr = countdown
            while cntr > 0:
                camera.annotate_text = str(cntr)
                cntr -= 1
                time.sleep(1)
            camera.annotate_text = ''
            camera.capture(filename, use_video_port=True)
            print
            ' [' + str(photo_counter) + ' of ' + str(total_photos) + '] ' + filename

    print
    "Finished photo sequence"
def cutPhoto():

    # Global variables preset
    total_photos = 15
    photo_Width = 1280
    photo_Height = 720
    params_file = './src/pf_' + str(photo_Width) + '_' + str(photo_Height) + '.txt'
    photo_counter = 0

    # Read pair cut parameters
    f = open(params_file, 'r')
    data = json.load(f)
    imageWidth = data['imageWidth']
    jointWidth = data['jointWidth']
    leftIndent = data['leftIndent']
    rightIndent = data['rightIndent']
    f.close()

    # Main pair cut cycle
    if (os.path.isdir("./pairs") == False):
        os.makedirs("./pairs")
    while photo_counter != total_photos:
        photo_counter += 1
        filename = './src/scene_' + str(photo_Width) + 'x' + str(photo_Height) + \
                   '_' + str(photo_counter) + '.png'
        pair_img = cv2.imread(filename, -1)
        #    cv2.imshow("ImagePair", pair_img)
        imgLeft = pair_img[0:photo_Height, leftIndent:imageWidth]  # Y+H and X+W
        imgRight = pair_img[0:photo_Height, rightIndent:rightIndent + imageWidth]
        leftName = './pairs/left_' + str(photo_counter).zfill(2) + '.png'
        rightName = './pairs/right_' + str(photo_counter).zfill(2) + '.png'
        cv2.imwrite(leftName, imgLeft)
        cv2.imwrite(rightName, imgRight)
        print('Pair No ' + str(photo_counter) + ' saved.')

    print('End cycle')
def calibration():

    # Global variables preset
    total_photos = 15
    photo_Width = 1280
    photo_Height = 720
    params_file = './src/pf_' + str(photo_Width) + '_' + str(photo_Height) + '.txt'
    # Chessboard parameters
    rows = 6
    columns = 9
    square_size = 2.5

    # Read pair cut parameters
    f = open(params_file, 'r')
    data = json.load(f)
    imageWidth = data['imageWidth']
    jointWidth = data['jointWidth']
    leftIndent = data['leftIndent']
    rightIndent = data['rightIndent']
    f.close()
    image_size = (imageWidth, photo_Height)

    calibrator = StereoCalibrator(rows, columns, square_size, image_size)
    photo_counter = 0
    print('Start cycle')

    while photo_counter != total_photos:
        photo_counter = photo_counter + 1
        print('Import pair No ' + str(photo_counter))
        leftName = './pairs/left_' + str(photo_counter).zfill(2) + '.png'
        rightName = './pairs/right_' + str(photo_counter).zfill(2) + '.png'
        if os.path.isfile(leftName) and os.path.isfile(rightName):
            imgLeft = cv2.imread(leftName, 1)
            imgRight = cv2.imread(rightName, 1)
            calibrator.add_corners((imgLeft, imgRight), True)
    print('End cycle')

    print('Starting calibration... It can take several minutes!')
    calibration = calibrator.calibrate_cameras()
    calibration.export('ress')
    print('Calibration complete!')

    # Lets rectify and show last pair after  calibration
    calibration = StereoCalibration(input_folder='ress')
    rectified_pair = calibration.rectify((imgLeft, imgRight))

    cv2.imshow('Left CALIBRATED', rectified_pair[0])
    cv2.imshow('Right CALIBRATED', rectified_pair[1])
    cv2.imwrite("rectifyed_left.jpg", rectified_pair[0])
    cv2.imwrite("rectifyed_right.jpg", rectified_pair[1])
    cv2.waitKey(0)

if __name__ == '__main__':
    print(__doc__)
    calibrationPhotoSeries()
    cutPhoto()
    calibration()