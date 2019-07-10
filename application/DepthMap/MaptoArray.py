import numpy as np
import cv2 as cv
def maptoarray():
    print('loading images...')
    imgL = cv.pyrDown(cv.imread(cv.samples.findFile('left.jpg')))  # downscale images for faster processing
    imgR = cv.pyrDown(cv.imread(cv.samples.findFile('right.jpg')))
    # disparity range is tuned for  image pair
    window_size = 3
    min_disp = 16
    num_disp = 112 - min_disp
    stereo = cv.StereoSGBM_create(minDisparity=min_disp,
                                  numDisparities=num_disp,
                                  blockSize=16,
                                  P1=8 * 3 * window_size ** 2,
                                  P2=32 * 3 * window_size ** 2,
                                  disp12MaxDiff=1,
                                  uniquenessRatio=10,
                                  speckleWindowSize=100,
                                  speckleRange=32
                                  )

    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    h, w = imgL.shape[:2]
    f = 0.8 * w  # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
                    [0, 0, 0, -f],  # so that y-axis looks up
                    [0, 0, 1, 0]])
    points = cv.reprojectImageTo3D(disp, Q)
    # конвертируем изображение из RGB в gray
    colors = cv.cvtColor(imgL, cv.COLOR_BGR2RGB)
    print(len(colors), ' length ')
    mask = disp > disp.min()
    out_points = points[mask]
    print(out_points, 'opoints')
    out_colors = colors[mask]
    data = np.(disp - min_disp) / num_disp).reshape((450, 2))
    # Write the array to disk
    with open('test.txt', 'w') as outfile:
        outfile.write('# Array shape: {0}\n'.format(data.shape))
    for data_slice in data:
        np.savetxt(outfile, data_slice, fmt='%-7.2f')
    # Writing out a break to indicate different slices...
    outfile.write('# New slice\n')
    data = np.(disp - min_disp) / num_disp).reshape((450, 2))

    # Write the array to disk
    with open('test.txt', 'w') as outfile:
        outfile.write('# Array shape: {0}\n'.format(data.shape))
    for data_slice in data:
        np.savetxt(outfile, data_slice, fmt='%-7.2f')
    # Writing out a break to indicate different slices...
    outfile.write('# New slice\n')
    # Read the array from disk
    new_data = np.loadtxt('test.txt')
    # Note that this returned a 2D array!
    print
    new_data.shape

