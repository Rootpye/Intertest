import tkinter as tk
import speedtest
import threading
import time

def test_internet_speed(label_download, label_upload, label_ping, label_status):
    """
    인터넷 속도를 측정하고 결과를 업데이트.
    """
    try:
        label_status.config(text="속도 측정 중... 잠시만 기다려 주세요.", fg="blue")
        st = speedtest.Speedtest()

        # 서버 목록 가져오기 및 최적의 서버 선택
        st.get_servers()
        best_server = st.get_best_server()

        label_status.config(text=f"서버: {best_server['host']} ({best_server['d']:.2f} km)", fg="green")

        while True:
            # 다운로드 속도 측정
            download_speed = st.download() / 1_000_000  # Mbps 변환
            label_download.config(text=f"다운로드 속도: {download_speed:.2f} Mbps")
            
            # 업로드 속도 측정
            upload_speed = st.upload() / 1_000_000  # Mbps 변환
            label_upload.config(text=f"업로드 속도: {upload_speed:.2f} Mbps")
            
            # 핑 측정
            ping = best_server['latency']
            label_ping.config(text=f"핑: {ping:.2f} ms")

            time.sleep(2)  # 2초마다 업데이트

    except speedtest.ConfigRetrievalError:
        label_status.config(text="서버 설정을 가져오는 데 실패했습니다.", fg="red")
    except Exception as e:
        label_status.config(text=f"오류 발생: {str(e)}", fg="red")

def start_speed_test(label_download, label_upload, label_ping, label_status):
    """
    별도의 스레드에서 속도 측정을 시작.
    """
    threading.Thread(
        target=test_internet_speed, 
        args=(label_download, label_upload, label_ping, label_status), 
        daemon=True
    ).start()

# GUI 구성
root = tk.Tk()
root.title("인터넷 속도 측정기")

# 레이아웃 설정
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=20, pady=20)

label_status = tk.Label(frame, text="측정을 시작하려면 버튼을 누르세요.", font=("Arial", 14), fg="black")
label_status.grid(row=0, column=0, columnspan=2, pady=10)

label_download = tk.Label(frame, text="다운로드 속도: -- Mbps", font=("Arial", 12))
label_download.grid(row=1, column=0, sticky="w", padx=10)

label_upload = tk.Label(frame, text="업로드 속도: -- Mbps", font=("Arial", 12))
label_upload.grid(row=2, column=0, sticky="w", padx=10)

label_ping = tk.Label(frame, text="핑: -- ms", font=("Arial", 12))
label_ping.grid(row=3, column=0, sticky="w", padx=10)

start_button = tk.Button(
    frame, text="속도 측정 시작", font=("Arial", 12), 
    command=lambda: start_speed_test(label_download, label_upload, label_ping, label_status)
)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

# GUI 실행
root.mainloop()