# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Apps\DEV\PROJECTS\KoHighlights\gui_status.ui'
#
# Created: Thu Mar  9 14:39:35 2023
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Status(object):
    def setupUi(self, Status):
        Status.setObjectName("Status")
        Status.resize(277, 55)
        Status.setWindowTitle("")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Status)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(Status)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.anim_lbl = QtWidgets.QLabel(self.frame)
        self.anim_lbl.setText("")
        self.anim_lbl.setObjectName("anim_lbl")
        self.horizontalLayout.addWidget(self.anim_lbl)
        self.show_items_btn = QtWidgets.QToolButton(self.frame)
        self.show_items_btn.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/stuff/show_pages.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_items_btn.setIcon(icon)
        self.show_items_btn.setIconSize(QtCore.QSize(24, 24))
        self.show_items_btn.setChecked(False)
        self.show_items_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.show_items_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.show_items_btn.setObjectName("show_items_btn")
        self.horizontalLayout.addWidget(self.show_items_btn)
        self.horizontalLayout_2.addWidget(self.frame)
        self.act_page = QtGui.QAction(Status)
        self.act_page.setCheckable(True)
        self.act_page.setObjectName("act_page")
        self.act_date = QtGui.QAction(Status)
        self.act_date.setCheckable(True)
        self.act_date.setObjectName("act_date")
        self.act_text = QtGui.QAction(Status)
        self.act_text.setCheckable(True)
        self.act_text.setObjectName("act_text")
        self.act_comment = QtGui.QAction(Status)
        self.act_comment.setCheckable(True)
        self.act_comment.setObjectName("act_comment")
        self.act_chapter = QtGui.QAction(Status)
        self.act_chapter.setCheckable(True)
        self.act_chapter.setObjectName("act_chapter")

        self.retranslateUi(Status)
        QtCore.QMetaObject.connectSlotsByName(Status)

    def retranslateUi(self, Status):
        self.show_items_btn.setToolTip(QtCore.QCoreApplication.translate("Status", "Show/Hide elements of Highlights. Also affects\n"
"what will be saved to the text/html files.", None))
        self.show_items_btn.setStatusTip(QtCore.QCoreApplication.translate("Status", "Show/Hide elements of Highlights. Also affects what will be saved to the text/html files.", None))
        self.show_items_btn.setText(QtCore.QCoreApplication.translate("Status", "Show in Highlights", None))
        self.act_page.setText(QtCore.QCoreApplication.translate("Status", "Page", None))
        self.act_date.setText(QtCore.QCoreApplication.translate("Status", "Date", None))
        self.act_text.setText(QtCore.QCoreApplication.translate("Status", "Highlight", None))
        self.act_comment.setText(QtCore.QCoreApplication.translate("Status", "Comment", None))
        self.act_chapter.setText(QtCore.QCoreApplication.translate("Status", "Chapter", None))
        self.act_chapter.setToolTip(QtCore.QCoreApplication.translate("Status", "Chapter", None))

import images_rc
