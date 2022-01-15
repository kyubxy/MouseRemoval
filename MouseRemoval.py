from time import sleep
from pynput import keyboard
from pynput.mouse import Controller, Button
import platform

mouse = Controller()

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
    "fastest" : "g",
    "reset" : keyboard.Key.esc,
    "speed_slower" : 1,
    "speed_slow" : 5,
    "speed_normal" : 10,
    "speed_fast" : 20,
    "speed_fastest" : 40, # not for the faint of heart
    "enable" : keyboard.Key.caps_lock,
    "disable" : keyboard.Key.caps_lock,
    "kill" : "b"
}

class App:
    def __init__(self):
        print ("MouseRemoval, pynput branch")
        print (f"running on ({platform.system()})")
        print ("peipacut 2021")
        print()
        e = self.getBind("enable")
        print(f"press {e} to get started")

        # movement
        self.xdir = 0
        self.ydir = 0
        self.speed = 10
        self.scrolling = False

        self.keypress = []
        self.keyrelease = []

        self.setBinds()
        self.setEnabled(True)
        self.setEnabled(False)

        self.toggle_listener = keyboard.Listener(on_press=self.toggle_press,suppress=False)
        self.toggle_listener.start()

    def toggle_press (self, key):
        if key == self.getBind("enable") and not self.enabled:
            self.setEnabled(True)
        elif key == self.getBind ("disable") and self.enabled:
            self.setEnabled(False)

    def on_press(self, key):
        if not self.enabled:
            if key == self.getBind("enable"):
                self.setEnabled(True)
            return

        self.handleKey(key, self.keypress)

    def on_release(self, key):
        if not self.enabled:
            return

        self.handleKey(key, self.keyrelease)

    def handleKey (self, key, collection):
        for (bind, action) in collection:
            try:
                if key.char == bind:
                    action()
            except (AttributeError):
                if key == bind:
                    action()

    def setEnabled(self, value):
        self.enabled = value

        if self.enabled:
            self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release,suppress=True)
            self.listener.start()
        else:
            self.listener.stop()

    def getBind (self, key):
        return DEFAULT_BINDS[key]

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
        self.speed = self.getBind("speed_normal")
        self.scrolling = False

    def run(self):
        self.running = True

        while self.running:
            dx, dy = self.speed * self.xdir, self.speed * self.ydir

            if self.scrolling:
                mouse.scroll(self.xdir, -self.ydir)
            else:
                mouse.move (dx, dy)

            sleep(0.01)

    def kill(self):
        self.running = False
        exit(0)

    def setBinds(self):
        self.keypress.append ((self.getBind("left_click"), lambda : mouse.press(Button.left)))
        self.keyrelease.append ((self.getBind("left_click"), lambda : mouse.release(Button.left)))

        self.keypress.append ((self.getBind("right_click"), lambda : mouse.press(Button.right)))
        self.keyrelease.append ((self.getBind("right_click"), lambda : mouse.press(Button.right)))

        self.keypress.append ((self.getBind("middle_click"), lambda : mouse.press(Button.middle)))
        self.keyrelease.append ((self.getBind("middle_click"), lambda : mouse.press(Button.middle)))

        self.keypress.append ((self.getBind("enable_scroll"), lambda : self.setScroll(True)))
        self.keyrelease.append ((self.getBind("disable_scroll"), lambda : self.setScroll(False)))

        self.keypress.append ((self.getBind("left"), lambda : self.setXDir(-1)))
        self.keyrelease.append ((self.getBind("left"), lambda : self.setXDir(0)))

        self.keypress.append ((self.getBind("right"), lambda : self.setXDir(1)))
        self.keyrelease.append ((self.getBind("right"), lambda : self.setXDir(0)))

        self.keypress.append ((self.getBind("down"), lambda : self.setYDir(1)))
        self.keyrelease.append ((self.getBind("down"), lambda : self.setYDir(0)))

        self.keypress.append ((self.getBind("up"), lambda : self.setYDir(-1)))
        self.keyrelease.append ((self.getBind("up"), lambda : self.setYDir(0)))

        self.keypress.append ((self.getBind("slower"), lambda : self.setSpeed(self.getBind("speed_slower"))))
        self.keypress.append ((self.getBind("slow"), lambda : self.setSpeed(self.getBind("speed_slow"))))
        self.keypress.append ((self.getBind("normal"), lambda : self.setSpeed(self.getBind("speed_normal"))))
        self.keypress.append ((self.getBind("fast"), lambda : self.setSpeed(self.getBind("speed_fast"))))
        self.keypress.append ((self.getBind("fastest"), lambda : self.setSpeed(self.getBind("speed_fastest"))))

        self.keypress.append ((self.getBind("reset"), lambda : self.reset()))

        self.keypress.append ((self.getBind("kill"), self.kill))

app = App()
app.run()
