# BBD's Krita Script Starter Feb 2018
 
from krita import Extension
import os

EXTENSION_ID_L = 'pykrita_rotatebrushtip_left'
EXTENSION_ID_R = 'pykrita_rotatebrushtip_right' 
EXTENSION_ID_L10 = 'pykrita_rotatebrushtip_left_10'
EXTENSION_ID_R10 = 'pykrita_rotatebrushtip_right_10'

MENU_ENTRY_L = 'Rotate Brush Tip Left'
MENU_ENTRY_R = 'Rotate Brush Tip Right' 
MENU_ENTRY_L10 = 'Rotate Brush Tip Left by 10°'
MENU_ENTRY_R10 = 'Rotate Brush Tip Right by 10°'

ANGLE = 1 

from PyQt5.QtCore import (
        QItemSelectionModel,Qt,pyqtSignal)

from PyQt5.QtWidgets import (
        QApplication, QListView,
        QFrame,QWidget, QDoubleSpinBox, QLabel, QMessageBox, QSlider,
)

class Rotatebrushtip(Extension):

    def __init__(self, parent):
        # Always initialise the superclass.
        # This is necessary to create the underlying C++ object 
        super().__init__(parent)

    def setup(self): 
        pass

    def createActions(self, window):
        # parameter 1 = the name that Krita uses to identify the action
        # parameter 2 = the text to be added to the menu entry for this script
        # parameter 3 = location of menu entry
        action = window.createAction(EXTENSION_ID_L, MENU_ENTRY_L, "tools/scripts") 
        action.triggered.connect(self.rotate_tip_left)

        action = window.createAction(EXTENSION_ID_R, MENU_ENTRY_R, "tools/scripts") 
        action.triggered.connect(self.rotate_tip_right)
        
        action = window.createAction(EXTENSION_ID_L10, MENU_ENTRY_L10, "tools/scripts") 
        action.triggered.connect(self.rotate_tip_left_10)

        action = window.createAction(EXTENSION_ID_R10, MENU_ENTRY_R10, "tools/scripts") 
        action.triggered.connect(self.rotate_tip_right_10)
  
        pass  

    def rotate_tip_left(self): 
        self.set_brushRotValue(ANGLE)  
        
        self.reload() 
        pass    

    def rotate_tip_right(self): 
        self.set_brushRotValue(-1 * ANGLE)  

        self.reload() 
        pass    

    def rotate_tip_left_10(self): 
        self.set_brushRotValue(10)  
        
        self.reload() 
        pass    

    def rotate_tip_right_10(self): 
        self.set_brushRotValue(-10)  

        self.reload() 
        pass    


    def reload(self):  
        Krita.instance().action('toggle_brush_outline').trigger()
        Krita.instance().action('toggle_brush_outline').trigger() 
    #----------------------------------------------------#
    # For Traversing nodes to get to Brush Editor Docker #
    #                                                    #
    #----------------------------------------------------#
    
    def walk_widgets(self,start):
        stack = [(start, 0)]
        while stack:
            cursor, depth = stack.pop(-1)
            yield cursor, depth
            stack.extend((c, depth + 1) for c in reversed(cursor.children()))


    def get_brush_editor(self):
        for window in QApplication.topLevelWidgets():
            if isinstance(window, QFrame) and window.objectName() == 'popup frame' or window.objectName() == 'KisPopupButtonFrame':
                for widget, _ in self.walk_widgets(window):
                    real_cls_name = widget.metaObject().className()
                    obj_name = widget.objectName()
                    if real_cls_name == 'KisPaintOpPresetsEditor' and obj_name == 'KisPaintOpPresetsEditor':
                        return widget   


    def selectBrushContainer(self,br_property):
        editor = self.get_brush_editor()
        option_widget_container = editor.findChild(QWidget, 'frmOptionWidgetContainer')
        current_view = None
        selectedRow  = None 
        for view in option_widget_container.findChildren(QListView):
            if view.metaObject().className() == 'KisCategorizedListView':
                if view.isVisibleTo(option_widget_container):
                    current_view = view
                    break
                
        if current_view:
            current_settings_widget = current_view.parent()
            s_model = current_view.selectionModel()
            model = current_view.model()
            target_index = None
            for row in range(model.rowCount()):
                index = model.index(row,0)   
                if index.data() == br_property: 
                    target_index = index
                    selectedRow = row
                    break
                    
            if target_index is not None: 
                s_model.clear()
                s_model.select(target_index, QItemSelectionModel.SelectCurrent)
                s_model.setCurrentIndex(target_index, QItemSelectionModel.SelectCurrent)
                current_view.setCurrentIndex(target_index)
                current_view.activated.emit(target_index)
                
        
        container_info = dict()
        container_info["model_index"]  = target_index
        container_info["current_view"] = current_view
        container_info["row_count"]    = selectedRow
        container_info["option_widget_container"] = option_widget_container
        container_info["current_settings_widget"] = current_settings_widget

        return container_info  
 
                    
    def set_brushRotValue(self, rotationValue):  
        container_info = self.selectBrushContainer("Brush Tip")
        current_view = container_info["current_view"] 
        option_widget_container = container_info["option_widget_container"] 
        current_settings_widget = container_info["current_settings_widget"]  

        brushSize = Krita.instance().activeWindow().activeView().brushSize()
        if current_view:
            for spin_box in current_settings_widget.findChildren(QDoubleSpinBox): 
                if spin_box.isVisibleTo(option_widget_container) and (spin_box.objectName() == "inputRadius" or spin_box.objectName() == "brushSizeSpinBox"):  
                    spin_box.setValue(brushSize) 

                if spin_box.isVisibleTo(option_widget_container) and spin_box.metaObject().className() == 'KisAngleSelectorSpinBox' :   
                    curValue = spin_box.value() + rotationValue
                    if curValue >= 0 and curValue <= 360:
                        spin_box.setValue(curValue)
                    elif curValue < 0 : 
                        spin_box.setValue(360 + curValue)
                    else: 
                        spin_box.setValue(0 + (curValue - 360))
                    break 
 

 
