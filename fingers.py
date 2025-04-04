import autopy
import mediapipe as mp
import datetime
import pyautogui
import time
import cv2
capture = cv2.VideoCapture(0) # получаем видео с ip камеры
hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=1,
                                 min_tracking_confidence=0.9,
                                 min_detection_confidence=0.6,
                                )
draw = mp.solutions.drawing_utils
tipIds = [4, 8, 12, 16, 20]
width, height = autopy.screen.size() # в перемен. хранится высота и ширина экрана
while True:
    _, img = capture.read()
    img = cv2.flip(img,1)
    result = hands.process(img)
    lmList = []
    if result.multi_hand_landmarks:
        for id, lm in enumerate(result.multi_hand_landmarks[0].landmark): # id - номера пальцев по рисунку, lm - координатц
            h, w, _ = img.shape # высота и ширина окна с камеры
            cx, cy = int(lm.x * w), int(lm.y * h) #абсолютная координата пальца
            lmList.append([id, cx, cy, h, w])
        draw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands_connections.HAND_CONNECTIONS)
        if len(lmList) != 0:
            fingers = []
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]):
                    fingers.append(0)
            totalFingers = fingers.count(1)
            print('totfin', totalFingers)
            # 1палец вверх - активация мыши
            if totalFingers == 1:
                if lmList[8][2] < lmList[5][2] and lmList[8][2] < lmList[12][2] and lmList[8][2] < lmList[16][2]:
                    try:
                        autopy.mouse.move(lmList[8][1] * width / lmList[8][4], lmList[8][2] * height / lmList[8][3])
                    except:
                        autopy.mouse.move(0,0)
                    if lmList[4][2] < lmList[5][2]:
                        print('click')
                        pyautogui.click()
            # 2 пальца вверх - прокрутка вверх
            if totalFingers == 2:
                if (lmList[8][2] < lmList[5][2] and lmList[8][2] < lmList[16][2]) and (lmList[12][2] < lmList[9][2] and lmList[12][2] < lmList[16][2]):
                    #autopy.key.toggle(autopy.key.Code.PAGE_UP, down=True)
                    pyautogui.scroll(100)
            # 3 пальца вверх - прокрутка вниз
            if totalFingers == 3:
                if (lmList[8][2] < lmList[5][2] and lmList[12][2] < lmList[9][2]) and (lmList[16][2] < lmList[13][2] and lmList[20][2] > lmList[16][2]):
                    pyautogui.scroll(-100)
            # 4 пальца вверх - скриншот
            if totalFingers == 4:
                if (lmList[8][2] < lmList[5][2] and lmList[12][2] < lmList[9][2]) and (lmList[16][2] < lmList[13][2] and lmList[20][2] < lmList[17][2]) and lmList[4][1] > lmList[6][1]:
                    print("-")
                    im1 = pyautogui.screenshot()
                    cur_time=datetime.datetime.now().strftime('%m-%d_%H-%M-%S')
                    im1.save(f'C:/testp/test{cur_time}.png')
                    #time.sleep(2)
            # 5 пальцев вверх - мастшаб больше
            if totalFingers == 4:
                if lmList[8][2] < lmList[5][2] and lmList[12][2] < lmList[9][2] and lmList[16][2] < lmList[13][2] and lmList[20][2] < lmList[17][2] and lmList[4][1] < lmList[6][1]:
                    print("+")
                    pyautogui.hotkey('ctrl', '+')
                    time.sleep(1)
            #если сжат кулак - масштаб меньше
            if totalFingers == 0:
                pyautogui.hotkey('ctrl', '-')
                time.sleep(1)


    cv2.imshow('From camera', img)
    if cv2.waitKey(1) == ord('q'):
        break