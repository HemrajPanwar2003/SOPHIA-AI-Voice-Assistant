import multiprocessing
import time
import traceback


# ================= PROCESS FUNCTIONS =================
def startKrishna():
    while True:
        try:
            print("🚀 Krishna process started")
            from main import start

            start()

        except Exception as e:
            print("❌ Krishna crashed:", e)
            traceback.print_exc()
            time.sleep(3)  # 🔁 safer delay


def listenHotword():
    while True:
        try:
            print("🎤 Hotword process started")
            from engine.features import hotword

            hotword()

        except Exception as e:
            print("❌ Hotword crashed:", e)
            traceback.print_exc()
            time.sleep(3)


# ================= MAIN SUPERVISOR =================
def run_system():

    process_map = {"Krishna": startKrishna, "Hotword": listenHotword}

    processes = {}

    try:
        # 🔹 Start all processes
        for name, target in process_map.items():
            p = multiprocessing.Process(target=target, name=name)
            p.start()
            processes[name] = p

        # 🔹 Monitor loop
        while True:
            for name, p in list(processes.items()):
                if not p.is_alive():
                    print(f"⚠️ {name} died. Restarting...")

                    # 🔹 Restart safely
                    new_p = multiprocessing.Process(target=process_map[name], name=name)
                    new_p.start()
                    processes[name] = new_p

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")

        for p in processes.values():
            p.terminate()
            p.join()

        print("✅ System stopped cleanly")


# ================= ENTRY =================
if __name__ == "__main__":
    multiprocessing.freeze_support()  # ✅ Windows safe
    run_system()
