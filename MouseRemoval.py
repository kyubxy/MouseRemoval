from time import sleep
import keyboard
import mouse
import platform
import os.path

CONFIG = "config";
DEFAULT_BINDS = {
    "left_click" : "e",
    "right_click" : "r",
    "middle_click" : "t",
    "enable_scroll" : "w",
    "disable_scroll" : "q",
    "left" : "h",
    "right" : "l",
    "up" : "k",
    "down" : "j",
    "slower" : "a",
    "slow" : "s",
    "normal" : "d",
    "fast" : "f",
    "reset" : "esc",
    "speed_slower" : 1,
    "speed_slow" : 5,
    "speed_normal" : 10,
    "speed_fast" : 20,
    "enable" : "home",
    "disable" : "end",
}

class App:
    def __init__(self):
        print ("MouseRemoval")
        print (f"running on ({platform.system()})")
        print ("peipacut 2021")

        self.readConfig()
        self.setState(True)

        # movement
        self.xdir = 0
        self.ydir = 0
        self.speed = 10
        self.scrolling = False

        self.enabled = True

    def readConfig(self):
        if (os.path.exists (CONFIG)):
            print ("detected config")
            lines = []
            # read file
            with open(CONFIG) as f:
                lines = f.readlines()
            
            self.binds = {}

            for line in lines:
                tokens = line.split (":")
                if (len(tokens) < 2):
                    continue

                key = tokens[0].strip()
                value = tokens[1].split("#")[0].strip()

                # invalid key
                if not key in DEFAULT_BINDS.keys():
                    print (f"no such {key} recognised, ommiting this from load")
                    continue

                self.binds[key] = value

            print (self.binds)
        else:
            print ("no config found, just using the defaults")
            self.binds = DEFAULT_BINDS

    def setBinds(self):
        keyboard.on_press_key(self.getBind("left_click"), lambda _: mouse.press(mouse.LEFT), True)
        keyboard.on_release_key(self.getBind("left_click"), lambda _: mouse.release(mouse.LEFT), True)

        keyboard.on_press_key(self.getBind("right_click"), lambda _: mouse.press(mouse.RIGHT), True)
        keyboard.on_release_key(self.getBind("right_click"), lambda _: mouse.release(mouse.RIGHT), True)

        keyboard.on_press_key(self.getBind("middle_click"), lambda _: mouse.press(mouse.MIDDLE), True)
        keyboard.on_release_key(self.getBind("middle_click"), lambda _: mouse.release(mouse.MIDDLE), True)

        keyboard.on_press_key(self.getBind("slower"), lambda _: self.setSpeed(self.getBind("speed_slower")), True)
        keyboard.on_press_key(self.getBind("slow"), lambda _: self.setSpeed(self.getBind("speed_slow")), True)
        keyboard.on_press_key(self.getBind("normal"), lambda _: self.setSpeed(self.getBind("speed_normal")), True)
        keyboard.on_press_key(self.getBind("fast"), lambda _: self.setSpeed(self.getBind("speed_fast")), True)

        keyboard.add_hotkey(self.getBind("reset"), lambda: self.reset(), suppress=True)

        keyboard.on_press_key(self.getBind("left"), lambda _: self.setXDir(-1), True)
        keyboard.on_release_key(self.getBind("left"), lambda _: self.setXDir(0), True)

        keyboard.on_press_key(self.getBind("right"), lambda _: self.setXDir(1), True)
        keyboard.on_release_key(self.getBind("right"), lambda _: self.setXDir(0), True)

        keyboard.on_press_key(self.getBind("down"), lambda _: self.setYDir(1), True)
        keyboard.on_release_key(self.getBind("down"), lambda _: self.setYDir(0), True)

        keyboard.on_press_key(self.getBind("up"), lambda _: self.setYDir(-1), True)
        keyboard.on_release_key(self.getBind("up"), lambda _: self.setYDir(0), True)

        keyboard.on_press_key(self.getBind("enable_scroll"), lambda _: self.setScroll(True), True)
        keyboard.on_press_key(self.getBind("disable_scroll"), lambda _: self.setScroll(False), True)

    def setState(self, value):
        self.enabled = value

        if self.enabled:
            keyboard.unhook_all()
            self.setBinds()
            keyboard.add_hotkey(self.getBind("disable"), lambda: self.setState(False), suppress=True)
        else:
            keyboard.unhook_all();
            keyboard.add_hotkey(self.getBind("enable"), lambda: self.setState(True), suppress=True)

        print ("--ENABLED--" if self.enabled else "--DISABLED--")

    def getBind (self, key):
        return self.binds[key] if key in self.binds else DEFAULT_BINDS[key]

    def setScroll (self, value):
        self.scrolling = value

    def setSpeed(self, value):
        self.speed = int(value);

    def setXDir(self, value):
        if self.enabled:
            self.xdir = value

    def setYDir(self, value):
        if self.enabled:
            self.ydir = value

    def reset(self):
        self.speed = 10
        self.scrolling = False
        self.setState(False)

    def run(self):
        while True:
            if self.scrolling:
                mouse.wheel (-self.ydir)
            else:
                mouse.move (self.speed*self.xdir, self.speed*self.ydir, False)

            sleep(0.01)

app = App()
app.run()
