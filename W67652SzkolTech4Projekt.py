import cv2
import numpy as np
import threading
if __name__ == '__main__':
    a = input("Wpisz nazwę pliku nagrań do edycji ")
    b = int(input("Wybierz co chcesz zrobić z podanym nagraniem 1 - skalowanie, 2 - zmiana jaskrości, 3- oba "))

    bright = 0
    def scale(frame):
        dim = (width,height)
        return cv2.resize(frame,dim,interpolation=cv2.INTER_AREA)


    def changebrightness(frame):
        if (bright>0 and bright<255):
            return cv2.add(frame,bright)
        elif(bright<0 and bright>-255):
            return cv2.subtract(frame,bright*-1)
    def scaleandchangebrightness(frame):
        if (bright>0 and bright<255):
            newframe = cv2.add(frame,bright)
            dim = (width, height)
            return cv2.resize(newframe, dim, interpolation=cv2.INTER_AREA)
        elif(bright<0 and bright>-255):
            newframe = cv2.subtract(frame,bright*-1)
            dim = (width, height)
            return cv2.resize(newframe, dim, interpolation=cv2.INTER_AREA)

    cap = cv2.VideoCapture(a)
    width = int(cap.get(3))
    height = int(cap.get(4))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if(length%2 ==1):
        length1 = int((length+1)/2)
        length2=int((length-1)/2)
    else:
        length1 = int(length/2)
        length2 = int(length/2)
    frameNr = 0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    framerate = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/16)
    frames = []
    while True:
        read, frame = cap.read()
        if not read:
            break
        frames.append(frame)
    frametable = np.array(frames)
    frametable1 = [0]*length1
    for i in range(0,length1-1):
        frametable1[i] = frametable[i]
    frametable2 = [0]*length2
    j=0
    for i in range(length1,length1+length2):
        frametable2[j] = frametable[i]
        j=j+1
    frametablefinal = [0]*length



    if b == 1:
        width = int(input("Podaj szerokość "))
        height = int(input("Podaj wysokość "))


        def threadfunction1():
            for i in range(0, length1):
                frametablefinal[i] = scale(frametable1[i])


        def threadfunction2():
            for i in range(0, length2-1):
                frametablefinal[i+length1+1] = scale(frametable2[i])


        thread1 = threading.Thread(target=threadfunction1())
        thread2 = threading.Thread(target=threadfunction2())
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), framerate, (width, height))



        for i in frametablefinal:
            out.write(i)
        out.release()
    #     with multiprocessing.Pool(processes=2) as pool:
    #         iterator=0
    #         for i in pool.map(scale,frametable1):
    #             frametablefinal[iterator] = i
    #             iterator = iterator + 1
    #         for i in pool.map(scale,frametable2):
    #             frametablefinal[iterator] = i
    #             iterator = iterator + 1
        print("Skalowanie wykonane")
    elif b == 2:
        bright = int(input("Podaj o jaką ilość podwyższyć lub obniżyć jasność "))

        def threadfunction3():
            for i in range(0,length1):
                frametablefinal[i] = changebrightness(frametable1[i])
        def threadfunction4():
            for i in range(0,length2-1):
                frametablefinal[i+length1+1] = changebrightness(frametable2[i])
        thread3 = threading.Thread(target=threadfunction3())
        thread4 = threading.Thread(target=threadfunction4())

        thread3.start()
        thread4.start()
        thread3.join()
        thread4.join()
        out2 = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), framerate, (width, height))
        for i in frametablefinal:
            out2.write(i)
        out2.release()
        print("Operacja zmiany jasności została wykonana")
    elif b == 3:
        bright = int(input("Podaj o jaką ilość podwyższyć lub obniżyć jasność "))
        width = int(input("Podaj szerokość "))
        height = int(input("Podaj wysokość "))
        def threadfunction5():
            for i in range(0,length1):
                frametablefinal[i] = scaleandchangebrightness(frametable1[i])
        def threadfunction6():
            for i in range(0,length2-1):
                frametablefinal[i+length1+1] = scaleandchangebrightness(frametable1[i])
        thread5 = threading.Thread(target=threadfunction5())
        thread6 = threading.Thread(target=threadfunction6())
        thread5.start()
        thread6.start()
        out3 = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), framerate, (width, height))

        thread5.join()
        thread6.join()
        for i in frametablefinal:
            out3.write(i)
        out3.release()
        print("Skalowanie i zmiana jasności została wykonana")
    else:
        print("Błąd podano zły parametr")

cap.release()