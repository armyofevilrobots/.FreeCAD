import FreeCAD, FreeCADGui, inspect
import Part
from PyQt4 import QtCore, QtGui

def menger(size = 100, iterations = 3, base = None, callback = None):
    base = base or Part.makeBox(size,size,size)
    sumshape = None
    for x in range(3):
        for y in range(3):
            for z in range(3):
                if not (x,y,z) in [
                    (1,1,1),
                    (1,1,0), (1,1,2),
                    (1,0,1), (1,2,1),
                    (2,1,1), (0,1,1)]:
                    newshape = base.copy()
                    newshape.translate(
                            FreeCAD.Base.Vector(
                                size*x, size*y, size*z))
                    if sumshape is None:
                        sumshape = newshape
                    else:
                        sumshape = sumshape.fuse(newshape)
                    if callable(callback):
                        callback(((1+x)*(1+y)*(1+z))/iterations)
    txmat = FreeCAD.Base.Matrix()
    txmat.scale(1.0/3, 1.0/3, 1.0/3)
    sumshape.transformShape(txmat)
    if iterations > 1:
        return menger(size, iterations - 1, sumshape).removeSplitter()
    else:
        return sumshape.removeSplitter()


def shape2menger(shape):
    newobj = FreeCAD.ActiveDocument.addObject(
           'Part::Feature',
           "menger")
    newobj.Shape=shape


def gen_menger_dialog():
    dialog = QtGui.QDialog()
    dialog.resize(200,300)
    dialog.setWindowTitle("Menger Generator")
    dlout = QtGui.QVBoxLayout(dialog)
    iter_label = QtGui.QLabel("number of iterations (>3 is SLOW)")
    dlout.addWidget(iter_label)
    menger_iter = QtGui.QSpinBox()
    menger_iter.setRange(1,6)
    dlout.addWidget(menger_iter)
    size_label = QtGui.QLabel("Dimension(size) of Menger")
    dlout.addWidget(size_label)
    menger_size = QtGui.QDoubleSpinBox()
    dlout.addWidget(menger_size)
    menger_size.setRange(0.001,1000.0)
    menger_size.setSingleStep(10.0)
    menger_size.setValue(100.0)
    okbox = QtGui.QDialogButtonBox(dialog)
    okbox.setOrientation(QtCore.Qt.Horizontal)
    okbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    dlout.addWidget(okbox)

    def do_eet():
        """Actually generate the menger"""
        tmpdia = QtGui.QProgressDialog("Building Menger of n=%d" % (menger_iter.value()), "No Abort, sorry!", 0, menger_iter.value()*9.0, dialog.parentWidget())

        def cb(val):
            """Updates the progress"""
            tmpdia.setValue(val)
            tmpdia.repaint()

        dialog.hide()
        tmpdia.show()
        shape2menger(
                menger(
                    iterations = menger_iter.value(),
                    size = menger_size.value(),
                    callback = cb))
        tmpdia.hide()

    QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), do_eet)
    QtCore.QObject.connect(okbox, QtCore.SIGNAL("rejected()"), dialog.hide)
    QtCore.QMetaObject.connectSlotsByName(dialog)
    return dialog


class MengerCommand:
    """Generates a menger cube."""
    def GetResources(self):
        return {
                'Pixmap'  : 'Std_Tool2',
                'MenuText': 'Create menger...',
                'ToolTip': 'Create a menger'
                }

    def IsActive(self):
        if FreeCAD.ActiveDocument == None:
            return False
        else:
            return True


    def Activated(self):
        dialog = gen_menger_dialog()
        dialog.show()




