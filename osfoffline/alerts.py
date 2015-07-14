__author__ = 'himanshu'
from PyQt5.QtWidgets import QSystemTrayIcon
import functools
import asyncio

class Alert(object):
    DOWNLOAD = 0
    UPLOAD = 1
    MODIFYING = 2
    DELETING = 3

    ALERT_TIME = 10000 # in ms

    def __init__(self, system_tray_icon, loop):
        self.alert_icon = system_tray_icon
        self.alert_queue = asyncio.LifoQueue()
        self.loop = loop or asyncio.get_event_loop()
        self.running = False

    def start(self):
        self.running = True
        self.run_alert_queue_in_background()

    def stop(self):
        self.running = False


    # @asyncio.coroutine
    # def backgrounded(func, *args, **kwargs):
    #     """Runs the given function with the given arguments in
    #     a background thread
    #     """
    #     loop = asyncio.get_event_loop()
    #     if asyncio.iscoroutinefunction(func):
    #         func = __coroutine_unwrapper(func)
    #
    #     return (yield from loop.run_in_executor(
    #         None,  # None uses the default executer, ThreadPoolExecuter
    #         functools.partial(func, *args, **kwargs)
    #     ))


    def info(self, file_name, action):
        title = {
            self.DOWNLOAD: "Downloading",
            self.UPLOAD: "Uploading",
            self.MODIFYING: "Modifying",
            self.DELETING: "Deleting",
        }
        text = "{} {}".format(title[action], file_name)
        self.alert_queue.put(text)

    @asyncio.coroutine
    def make_alert(self,text):
        print('HIMANSHU. INSIDE make_alert(text)')
        if self.alert_icon:
            self.alert_icon.showMessage(
                text,
                "      - OSF Offline",  # todo: there is some way to format strings in pyqt. how again?
                QSystemTrayIcon.NoIcon,
                self.ALERT_TIME  # fixme: currently, I have NO control over duration of alert.
            )

    def run_alert_queue_in_background(self):
        self.loop.call_soon_threadsafe(
                asyncio.async,
                self.start_alert_queue()
            )

    @asyncio.coroutine
    def start_alert_queue(self):
        while self._running:
            print('HIMANSHU INSIDE start_alert_queue!!!!!!!!!')
            text = None
            if len(self.alert_queue) > 1:
                text = "{} files being synced".format(len(self.alert_queue))
                self.alert_queue.clear()
                # with self.alert_queue.mutex:
                #     self.alert_queue.queue.clear()
            elif len(self.alert_queue) == 1:
                text = yield from self.alert_queue.get()

            if text:
                self.make_alert(text)
            yield from asyncio.sleep(self.ALERT_TIME/1000)



# if __name__=="__main__":
# app = QApplication(sys.argv)
#
#     if not QSystemTrayIcon.isSystemTrayAvailable():
#         QMessageBox.critical(None, "Systray",
#                 "Could not detect a system tray on this system")
#         sys.exit(1)
#
#     QApplication.setQuitOnLastWindowClosed(False)
#     dialog = QDialog()
#     setup_alerts(dialog)
#     info('hi',DOWNLOAD)
#
#     app.exec_()

