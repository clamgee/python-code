from PyQt5.uic import loadUi #使用.ui介面模組
from PyQt5.QtCore import pyqtSlot,QDate,QTime,QDateTime,QTimer,Qt,QThread,pyqtSignal,QAbstractTableModel #插入資訊模組
from PyQt5.QtWidgets import QApplication,QDialog,QFileDialog,QMainWindow,QGraphicsScene,QHeaderView,QTableWidgetItem,QMessageBox #PyQt5介面與繪圖模組
from PyQt5 import QtCore, QtGui, QtWidgets


has_pandas = False
try:
  import pandas as pd
  has_pandas = True
except:
  pass

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super(TableModel, self).__init__()
        self.datatable = None
        self.headerdata = None

    def update(self, dataIn):
        print ('Updating Model')
        self.datatable = dataIn
        print('Datatable : {0}'.format(self.datatable))
        if has_pandas:
          headers = dataIn.columns.values
        else:
          headers = dataIn.columns
        header_items = [
                    str(field)
                    for field in headers
        ]
        self.headerdata = header_items
        print ('Headers')
        print (self.headerdata)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if has_pandas:
          return len(self.datatable.columns.values)
        else:
          return len(self.datatable.columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return QtCore.QVariant('{0}'.format(self.datatable.iget_value(i, j)))
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if index.column() == 4:
            self.datatable.iset_value(index.row(), 4, value)
            return value
        return value

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return '{0}'.format(self.headerdata[col])

    def flags(self, index):
        if index.column() == 4:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled


class TableView(QtWidgets.QTableView):
    """
    A simple table to demonstrate the QComboBox delegate.
    """
    def __init__(self, *args, **kwargs):
        QtWidgets.QTableView.__init__(self, *args, **kwargs)
        self.setItemDelegateForColumn(4, CheckBoxDelegate(self))


class CheckBoxDelegate(QtWidgets.QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        '''
        Important, otherwise an editor is created if the user clicks in this cell.
        ** Need to hook up a signal to the model
        '''
        return None

    def paint(self, painter, option, index):
        '''
        Paint a checkbox without the label.
        '''

        checked = index.data().toBool()
        check_box_style_option = QtGui.QStyleOptionButton()

        if (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QtGui.QStyle.State_Enabled
        else:
            check_box_style_option.state |= QtGui.QStyle.State_ReadOnly

        if checked:
            check_box_style_option.state |= QtGui.QStyle.State_On
        else:
            check_box_style_option.state |= QtGui.QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)

        # this will not run - hasFlag does not exist
        #if not index.model().hasFlag(index, QtCore.Qt.ItemIsEditable):
            #check_box_style_option.state |= QtGui.QStyle.State_ReadOnly

        check_box_style_option.state |= QtGui.QStyle.State_Enabled

        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_CheckBox, check_box_style_option, painter)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        '''
        print ('Check Box editor Event detected : ')
        print (event.type())
        if not (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False

        print ('Check Box editor Event detected : passed first check')
        # Do not change the checkbox-state
        if event.type() == QtCore.QEvent.MouseButtonPress:
          return False
        if event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() != QtCore.Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Select:
                return False
        else:
            return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        print ('SetModelData')
        newValue = not index.data().toBool()
        print ('New Value : {0}'.format(newValue))
        model.setData(index, newValue, QtCore.Qt.EditRole)

    def getCheckBoxRect(self, option):
        check_box_style_option = QtGui.QStyleOptionButton()
        check_box_rect = QtGui.QApplication.style().subElementRect(QtGui.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QtCore.QPoint (option.rect.x() +
                            option.rect.width() / 2 -
                            check_box_rect.width() / 2,
                            option.rect.y() +
                            option.rect.height() / 2 -
                            check_box_rect.height() / 2)
        return QtCore.QRect(check_box_point, check_box_rect.size())


###############################################################################################################################
class Dataframe(dict):
    def __init__(self, columns, values):
        if len(values) != len(columns):
            raise Exception("Bad values")
        self.columns = columns
        self.values = values
        self.index = values[0]
        super(Dataframe, self).__init__(dict(zip(columns, values)))
        pass

    def iget_value(self, i, j):
        return(self.values[j][i])

    def iset_value(self, i, j, value):
        self.values[j][i] = value


if __name__=="__main__":
    from sys import argv, exit

    class Widget(QtWidgets.QWidget):
        """
        A simple test widget to contain and own the model and table.
        """
        def __init__(self, parent=None):
            QtWidgets.QWidget.__init__(self, parent)

            l=QtWidgets.QVBoxLayout(self)
            cdf = self.get_data_frame()
            self._tm=TableModel(self)
            self._tm.update(cdf)
            self._tv=TableView(self)
            self._tv.setModel(self._tm)
            for row in range(0, self._tm.rowCount()):
                self._tv.openPersistentEditor(self._tm.index(row, 4))
            self.setGeometry(300, 300, 550, 200)
            l.addWidget(self._tv)

        def get_data_frame(self):
            if has_pandas:
              df = pd.DataFrame({'Name':['a','b','c','d'],
              'First':[2.3,5.4,3.1,7.7], 'Last':[23.4,11.2,65.3,88.8], 'Class':[1,1,2,1], 'Valid':[True, False, True, False]})
            else:
              columns = ['Name', 'First', 'Last', 'Class', 'Valid']
              values = [['a','b','c','d'], [2.3,5.4,3.1,7.7], [23.4,11.2,65.3,88.8], [1,1,2,1], [True, False, True, False]]
              df = Dataframe(columns, values)
            return df

    a=QApplication(argv)
    w=Widget()
    w.show()
    w.raise_()
    exit(a.exec_())