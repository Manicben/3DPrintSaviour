import cv2
import glob

img_names = glob.glob('img/*.jpg')
img_names.sort()
n = len(img_names)

out = cv2.VideoWriter('output1.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10.0, (1640, 1232))
log = open('img/detected_result.txt')
font = cv2.FONT_HERSHEY_SIMPLEX
RED = (0, 0, 255)
ORANGE = (0, 128, 255)
YELLOW = (0, 255, 255)

for i in range(n):
    curr_file = img_names[i]
    print(curr_file)
    curr_img = cv2.imread(curr_file)
    curr_img = cv2.resize(curr_img, (1640, 1232))
    # cv2.imshow('w', curr_img)
    if i > 6:
        detection = log.readline()
        if detection != None and detection.strip() != '':
            defect = ''
            if 'BUT' in detection:
                defect = 'SPAGHETTI'

            if detection[0] == '*':
                if detection[13:15] == 'Po':
                    defect = 'BREAKAGE'
                elif detection[13:15] == 'Fi':
                    defect = 'AIR PRINT'
                elif detection[13:15] == 'Pr':
                    defect = 'DETACHMENT'
                elif detection[13:15] == 'Sp':
                    defect = 'SPAGHETTI'
            
            if defect == 'SPAGHETTI':
                cv2.rectangle(curr_img, (25, 25), (1615, 1207), RED, 50)
                cv2.putText(curr_img, defect, (100, 1150), font, 8, RED, 20)
            
            if defect == 'DETACHMENT':
                cv2.rectangle(curr_img, (25, 25), (1615, 1207), ORANGE, 50)
                cv2.putText(curr_img, defect, (100, 1150), font, 8, ORANGE, 20)
            
            if defect == 'AIR PRINT':
                cv2.rectangle(curr_img, (25, 25), (1615, 1207), YELLOW, 50)
                cv2.putText(curr_img, defect, (100, 1150), font, 8, YELLOW, 20)

    out.write(curr_img)

out.release()
log.close()

