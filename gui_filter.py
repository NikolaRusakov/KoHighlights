# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Apps\DEV\PROJECTS\KoHighlights\gui_filter.ui'
#
# Created: Thu Apr  6 23:38:59 2023
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui

class Ui_Filter(object):
    def setupUi(self, Filter):
        Filter.setObjectName("Filter")
        Filter.resize(215, 66)
        Filter.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout = QtGui.QVBoxLayout(Filter)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filter_frm1 = QtGui.QFrame(Filter)
        self.filter_frm1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.filter_frm1.setFrameShadow(QtGui.QFrame.Raised)
        self.filter_frm1.setObjectName("filter_frm1")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.filter_frm1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.filter_txt = QtGui.QLineEdit(self.filter_frm1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_txt.sizePolicy().hasHeightForWidth())
        self.filter_txt.setSizePolicy(sizePolicy)
        self.filter_txt.setText("")
        self.filter_txt.setObjectName("filter_txt")
        self.horizontalLayout_4.addWidget(self.filter_txt)
        self.filter_btn = QtGui.QPushButton(self.filter_frm1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_btn.sizePolicy().hasHeightForWidth())
        self.filter_btn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/stuff/filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filter_btn.setIcon(icon)
        self.filter_btn.setObjectName("filter_btn")
        self.horizontalLayout_4.addWidget(self.filter_btn)
        self.verticalLayout.addWidget(self.filter_frm1)
        self.filter_frm2 = QtGui.QFrame(Filter)
        self.filter_frm2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.filter_frm2.setFrameShadow(QtGui.QFrame.Raised)
        self.filter_frm2.setObjectName("filter_frm2")
        self.horizontalLayout = QtGui.QHBoxLayout(self.filter_frm2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filter_box = QtGui.QComboBox(self.filter_frm2)
        self.filter_box.setObjectName("filter_box")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.filter_box.addItem("")
        self.horizontalLayout.addWidget(self.filter_box)
        self.filtered_lbl = QtGui.QLabel(self.filter_frm2)
        self.filtered_lbl.setText("")
        self.filtered_lbl.setObjectName("filtered_lbl")
        self.horizontalLayout.addWidget(self.filtered_lbl)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.clear_filter_btn = QtGui.QPushButton(self.filter_frm2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear_filter_btn.sizePolicy().hasHeightForWidth())
        self.clear_filter_btn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/stuff/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_filter_btn.setIcon(icon1)
        self.clear_filter_btn.setObjectName("clear_filter_btn")
        self.horizontalLayout.addWidget(self.clear_filter_btn)
        self.verticalLayout.addWidget(self.filter_frm2)

        self.retranslateUi(Filter)
        self.filter_box.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Filter)

    def retranslateUi(self, Filter):
        self.filter_txt.setToolTip(QtGui.QApplication.translate("Filter", "Type the keywords to filter the visible items", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_txt.setPlaceholderText(QtGui.QApplication.translate("Filter", "Type here to filter...", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_btn.setToolTip(QtGui.QApplication.translate("Filter", "Set filter", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_btn.setText(QtGui.QApplication.translate("Filter", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_box.setToolTip(QtGui.QApplication.translate("Filter", "Select where to search for the keywords", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_box.setItemText(0, QtGui.QApplication.translate("Filter", "Filter All:", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_box.setItemText(1, QtGui.QApplication.translate("Filter", "Filter Highlights:", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_box.setItemText(2, QtGui.QApplication.translate("Filter", "Filter Comments:", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_box.setItemText(3, QtGui.QApplication.translate("Filter", "Filter Book Titles:", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_filter_btn.setToolTip(QtGui.QApplication.translate("Filter", "Clear the filter field", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_filter_btn.setStatusTip(QtGui.QApplication.translate("Filter", "Clears the filter field", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_filter_btn.setText(QtGui.QApplication.translate("Filter", "Clear", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
