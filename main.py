import tkinter as tk
import speedtest
import threading

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intertest")

        # GUI Setup
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack(padx=20, pady=20)

        self.label_status = tk.Label(self.frame, text="Press the button to start the test.", font=("Arial", 14), fg="black")
        self.label_status.grid(row=0, column=0, columnspan=2, pady=10)

        self.label_server = tk.Label(self.frame, text="Server: --", font=("Arial", 12))
        self.label_server.grid(row=1, column=0, sticky="w", padx=10)

        self.label_download = tk.Label(self.frame, text="Download Speed: -- Mbps", font=("Arial", 12))
        self.label_download.grid(row=2, column=0, sticky="w", padx=10)

        self.label_upload = tk.Label(self.frame, text="Upload Speed: -- Mbps", font=("Arial", 12))
        self.label_upload.grid(row=3, column=0, sticky="w", padx=10)

        self.label_ping = tk.Label(self.frame, text="Ping: -- ms", font=("Arial", 12))
        self.label_ping.grid(row=4, column=0, sticky="w", padx=10)

        self.start_button = tk.Button(self.frame, text="Start Speed Test", font=("Arial", 12), command=self.start_speed_test)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Speed test object and state
        self.st = speedtest.Speedtest()
        self.best_server = None
        self.running = False

    def perform_speed_test(self):
        """
        Measures internet speed and updates the labels with results.
        """
        try:
            # Measure download speed
            download_speed = self.st.download() / 1_000_000  # Convert to Mbps
            self.label_download.config(text=f"Download Speed: {download_speed:.2f} Mbps")

            # Measure upload speed
            upload_speed = self.st.upload() / 1_000_000  # Convert to Mbps
            self.label_upload.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")

            # Update ping (retrieved from the selected server)
            ping = self.best_server['latency']
            self.label_ping.config(text=f"Ping: {ping:.2f} ms")

            # Completion message
            self.label_status.config(text="Test Completed", fg="green")
        except speedtest.ConfigRetrievalError:
            self.label_status.config(text="Failed to retrieve server configuration.", fg="red")
        except speedtest.SpeedtestHTTPError:
            self.label_status.config(text="HTTP error occurred during the test.", fg="red")
        except Exception as e:
            self.label_status.config(text=f"Error: {e}", fg="red")
        finally:
            self.running = False  # End test state

    def start_speed_test(self):
        """
        Starts the speed test.
        """
        if self.running:
            return  # Ignore if already running

        self.running = True
        self.label_status.config(text="Finding the closest server...", fg="blue")

        # Initialize server in a separate thread
        threading.Thread(target=self.initialize_speedtest, daemon=True).start()

    def initialize_speedtest(self):
        """
        Selects the closest server and performs the speed test.
        """
        try:
            self.st.get_servers()  # Retrieve all servers
            self.best_server = self.st.get_best_server()  # Select the closest server

            server_info = f"{self.best_server['host']} ({self.best_server['name']}, {self.best_server['country']})"
            self.label_server.config(text=f"Server: {server_info}")

            # Update status to indicate server connection
            self.label_status.config(text="Running the speed test...", fg="blue")

            # Perform the speed test
            self.perform_speed_test()
        except speedtest.ConfigRetrievalError:
            self.label_status.config(text="Failed to retrieve servers.", fg="red")
        except Exception as e:
            self.label_status.config(text=f"Server initialization failed: {e}", fg="red")
        finally:
            self.running = False  # End test state

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()
