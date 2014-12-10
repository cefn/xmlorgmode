import sys
import os
from PyQt4.QtCore import QObject,pyqtSlot,pyqtSignal,QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView
from PyQt4.QtXmlPatterns import QXmlQuery

from watchdog.observers import Observer 
from watchdog.events import FileSystemEvent,FileSystemEventHandler

# provides simple signalling mechanism for watchdog module (could
# be developed to reflect all signatures FileSystemEventHandler)
class QWatchdogAdaptor(QObject):
    
    watchdog_signal = pyqtSignal(FileSystemEvent)
    
    def __init__(self):
        super(QWatchdogAdaptor,self).__init__()
    
    def dispatch(self, event):
        self.watchdog_signal.emit(event)
        import pdb; pdb.set_trace()
    
# Manages an updating view of an XQuery
class QueryDisplay(QObject):

    def __init__(self, datapath, querypath):
        super(QueryDisplay,self).__init__()
        self.datapath = datapath
        self.querypath = querypath
        self.view = QWebView()
        self.queryimpl = QXmlQuery(QXmlQuery.XQuery10)
    
    @pyqtSlot()
    def update(self, watchdog_event=None):
        self.queryimpl.setFocus(QUrl.fromLocalFile(self.datapath))
        self.queryimpl.setQuery(QUrl.fromLocalFile(self.querypath))
        self.view.setHtml(self.queryimpl.evaluateToString())

def main():

    # create application context
    app = QApplication(sys.argv)
    
    # read and sanitise path for source XML, and source XQuery
    datapath = sys.argv[1]
    querypath = sys.argv[2]
    datapath = os.path.realpath(datapath)
    querypath = os.path.realpath(querypath)

    # create a query view which binds to changes in data and query files
    display = QueryDisplay(datapath,querypath)

    # generate Qt signals on watchdog filesystem events
    observer = Observer()
    adaptor = QWatchdogAdaptor()
    observer.schedule(adaptor, os.path.dirname(datapath))
    observer.schedule(adaptor, os.path.dirname(querypath))
    observer.start()
    adaptor.watchdog_signal.connect(display.update)

    # render then reveal
    display.update()
    display.view.show()

    sys.exit(app.exec_())
    
if __name__ == "__main__": main()















