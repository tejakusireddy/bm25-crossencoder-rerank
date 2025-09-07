def stop(cls, name):
        
        cls.timer_end[name] = time.time()
        if cls.debug:
            print("Timer", name, "stopped ...")