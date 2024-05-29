import os
import cv2
import time
import requests
import numpy as np
from flask import Flask, Response
import torch
import pymysql
import threading
import queue


app = Flask(__name__)
count = 0
task_queue = queue.Queue()

# mysql connect
def get_db_connection():
    return pymysql.connect(
        # ip 주소, localhost 무방(현입력값: localhost)
        host='127.0.0.1',
        # mysql username
        user='root',
        # mysql password
        password='1234',
        # mysql database name
        db='db_kbk',
        # port name
        # port=3306
    )


# Func1 : save img to db(mysql 스트림???같은거 변환 코드 필요함)
def save_image_to_db(image_data):
    # mysql db connection
    connection = get_db_connection()
    # try: 이미지 데이터 저장
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO images (image_data) VALUES (%s)"
            cursor.execute(sql, (image_data,))
        connection.commit()
    # try 실패 시 에러 출력
    except Exception as e:
        print(f'err to connect db: {e}')
    # 연결 종료
    finally:
        connection.close()


# Func2 : save dir path to db
def save_path_to_db(save_path):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'INSERT INTO image_path (imagepathdata) VALUES (%s)'
            cursor.execute(sql, (save_path,))
        connection.commit()
    except Exception as e:
        print(f'err to connect db: {e}')
    finally:
        connection.close()


# stream inference video
def load_video(url):
    global count
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        bytes = b''
        for chunk in r.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                # bgr 형식을 rgb로 변환
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 추론 진행(RGB)
                results = model(frame_rgb)

                # 사람 감지 확인
                print(count)
                person_detected = False
                for obj in results.xyxy[0]:
                    if int(obj[5]) == 0:
                        person_detected = True
                        break

                if person_detected:
                    # dir 없을 시 생성하기
                    save_path = './image_dir/'
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    
                    # 저장 경로 생성
                    save_path = os.path.join(save_path, f'detected_{time.time()}.jpg')

                    # 저장
                    # 작업 큐에 추가 (이미지 저장과 경로 저장 작업)
                    task_queue.put((frame, save_path))
                    # # 이미지 저장
                    # cv2.imwrite(save_path, frame)

                    # # 경로를 DB에 저장
                    # save_path_to_db(save_path)

                    # count += 1

                frame = results.render()[0]
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                # delay 설정
                # time.sleep(0.2)
    else:
        print('Error occured in video stream')
                

def worker():
    while True:
        frame, save_path = task_queue.get()
        if frame is None:
            break
        # 이미지 저장
        cv2.imwrite(save_path, frame)
        # 경로를 DB에 저장
        save_path_to_db(save_path)
        task_queue.task_done()
    

@app.route('/video')
def video():
    # url => 영상을 전달하는 머신 ip
    return Response(load_video(url='http://192.168.0.45:5000/video'), mimetype='multipart/x-mixed-replace; boundary=frame')


global model
if __name__ == '__main__':
    # 커스텀 욜로 사용
    model_path = './best.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    # pretrained 욜로 사용
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    # 워커 스레드 시작
    worker_thread = threading.Thread(target=worker)
    worker_thread.daemon = True
    worker_thread.start()

    try:
        app.run(host='0.0.0.0', port=3333)
    except KeyboardInterrupt:
        print('Shut down well')
    finally:
        # 애플리케이션 종료 시 큐에 None을 넣어 워커 스레드 종료
        task_queue.put((None, None))
        worker_thread.join()

    