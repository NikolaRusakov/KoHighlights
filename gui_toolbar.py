# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Apps\DEV\PROJECTS\KoHighlights\gui_toolbar.ui'
#
# Created: Thu Nov 24 15:53:16 2022
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ToolBar(object):
    def setupUi(self, ToolBar):
        ToolBar.setObjectName("ToolBar")
        ToolBar.resize(967, 73)
        ToolBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        ToolBar.setWindowTitle("")
        ToolBar.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.verticalLayout_2 = QtGui.QVBoxLayout(ToolBar)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 2, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tool_frame = QtGui.QFrame(ToolBar)
        self.tool_frame.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tool_frame.setObjectName("tool_frame")
        self.horizontalLayout = QtGui.QHBoxLayout(self.tool_frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.check_btn = QtGui.QToolButton(self.tool_frame)
        self.check_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.check_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../KataLib/:/stuff/exec.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.check_btn.setIcon(icon)
        self.check_btn.setIconSize(QtCore.QSize(48, 48))
        self.check_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.check_btn.setAutoRaise(True)
        self.check_btn.setObjectName("check_btn")
        self.horizontalLayout.addWidget(self.check_btn)
        self.scan_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scan_btn.sizePolicy().hasHeightForWidth())
        self.scan_btn.setSizePolicy(sizePolicy)
        self.scan_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/stuff/folder_reader.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scan_btn.setIcon(icon1)
        self.scan_btn.setIconSize(QtCore.QSize(48, 48))
        self.scan_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.scan_btn.setAutoRaise(True)
        self.scan_btn.setObjectName("scan_btn")
        self.horizontalLayout.addWidget(self.scan_btn)
        self.export_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_btn.sizePolicy().hasHeightForWidth())
        self.export_btn.setSizePolicy(sizePolicy)
        self.export_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/stuff/file_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.export_btn.setIcon(icon2)
        self.export_btn.setIconSize(QtCore.QSize(48, 48))
        self.export_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.export_btn.setAutoRaise(True)
        self.export_btn.setObjectName("export_btn")
        self.horizontalLayout.addWidget(self.export_btn)
        self.open_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_btn.sizePolicy().hasHeightForWidth())
        self.open_btn.setSizePolicy(sizePolicy)
        self.open_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/stuff/files_view.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_btn.setIcon(icon3)
        self.open_btn.setIconSize(QtCore.QSize(48, 48))
        self.open_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.open_btn.setAutoRaise(True)
        self.open_btn.setObjectName("open_btn")
        self.horizontalLayout.addWidget(self.open_btn)
        self.filter_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_btn.sizePolicy().hasHeightForWidth())
        self.filter_btn.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/stuff/filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filter_btn.setIcon(icon4)
        self.filter_btn.setIconSize(QtCore.QSize(48, 48))
        self.filter_btn.setCheckable(True)
        self.filter_btn.setChecked(False)
        self.filter_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.filter_btn.setAutoRaise(True)
        self.filter_btn.setObjectName("filter_btn")
        self.horizontalLayout.addWidget(self.filter_btn)
        self.merge_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.merge_btn.sizePolicy().hasHeightForWidth())
        self.merge_btn.setSizePolicy(sizePolicy)
        self.merge_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/stuff/files_merge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.merge_btn.setIcon(icon5)
        self.merge_btn.setIconSize(QtCore.QSize(48, 48))
        self.merge_btn.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.merge_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.merge_btn.setAutoRaise(True)
        self.merge_btn.setObjectName("merge_btn")
        self.horizontalLayout.addWidget(self.merge_btn)
        self.delete_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_btn.sizePolicy().hasHeightForWidth())
        self.delete_btn.setSizePolicy(sizePolicy)
        self.delete_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/stuff/files_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(icon6)
        self.delete_btn.setIconSize(QtCore.QSize(48, 48))
        self.delete_btn.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.delete_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.delete_btn.setAutoRaise(True)
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout.addWidget(self.delete_btn)
        self.clear_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear_btn.sizePolicy().hasHeightForWidth())
        self.clear_btn.setSizePolicy(sizePolicy)
        self.clear_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/stuff/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clear_btn.setIcon(icon7)
        self.clear_btn.setIconSize(QtCore.QSize(48, 48))
        self.clear_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.clear_btn.setAutoRaise(True)
        self.clear_btn.setObjectName("clear_btn")
        self.horizontalLayout.addWidget(self.clear_btn)
        spacerItem = QtGui.QSpacerItem(86, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.view_grp = QtGui.QGroupBox(self.tool_frame)
        self.view_grp.setObjectName("view_grp")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.view_grp)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.books_view_btn = QtGui.QToolButton(self.view_grp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.books_view_btn.sizePolicy().hasHeightForWidth())
        self.books_view_btn.setSizePolicy(sizePolicy)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/stuff/view_books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.books_view_btn.setIcon(icon8)
        self.books_view_btn.setIconSize(QtCore.QSize(48, 48))
        self.books_view_btn.setCheckable(True)
        self.books_view_btn.setChecked(True)
        self.books_view_btn.setAutoExclusive(True)
        self.books_view_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.books_view_btn.setAutoRaise(True)
        self.books_view_btn.setObjectName("books_view_btn")
        self.horizontalLayout_3.addWidget(self.books_view_btn)
        self.high_view_btn = QtGui.QToolButton(self.view_grp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.high_view_btn.sizePolicy().hasHeightForWidth())
        self.high_view_btn.setSizePolicy(sizePolicy)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/stuff/view-highlights.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.high_view_btn.setIcon(icon9)
        self.high_view_btn.setIconSize(QtCore.QSize(48, 48))
        self.high_view_btn.setCheckable(True)
        self.high_view_btn.setAutoExclusive(True)
        self.high_view_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.high_view_btn.setAutoRaise(True)
        self.high_view_btn.setObjectName("high_view_btn")
        self.horizontalLayout_3.addWidget(self.high_view_btn)
        self.horizontalLayout.addWidget(self.view_grp)
        self.mode_grp = QtGui.QGroupBox(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mode_grp.sizePolicy().hasHeightForWidth())
        self.mode_grp.setSizePolicy(sizePolicy)
        self.mode_grp.setObjectName("mode_grp")
        self.verticalLayout = QtGui.QVBoxLayout(self.mode_grp)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.loaded_btn = QtGui.QToolButton(self.mode_grp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loaded_btn.sizePolicy().hasHeightForWidth())
        self.loaded_btn.setSizePolicy(sizePolicy)
        self.loaded_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/stuff/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loaded_btn.setIcon(icon10)
        self.loaded_btn.setIconSize(QtCore.QSize(24, 24))
        self.loaded_btn.setCheckable(True)
        self.loaded_btn.setChecked(True)
        self.loaded_btn.setAutoExclusive(True)
        self.loaded_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.loaded_btn.setAutoRaise(True)
        self.loaded_btn.setObjectName("loaded_btn")
        self.verticalLayout.addWidget(self.loaded_btn)
        self.db_btn = XToolButton(self.mode_grp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.db_btn.sizePolicy().hasHeightForWidth())
        self.db_btn.setSizePolicy(sizePolicy)
        self.db_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/stuff/db.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.db_btn.setIcon(icon11)
        self.db_btn.setIconSize(QtCore.QSize(24, 24))
        self.db_btn.setCheckable(True)
        self.db_btn.setAutoExclusive(True)
        self.db_btn.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.db_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.db_btn.setAutoRaise(True)
        self.db_btn.setObjectName("db_btn")
        self.verticalLayout.addWidget(self.db_btn)
        self.horizontalLayout.addWidget(self.mode_grp)
        self.about_btn = QtGui.QToolButton(self.tool_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_btn.sizePolicy().hasHeightForWidth())
        self.about_btn.setSizePolicy(sizePolicy)
        self.about_btn.setMinimumSize(QtCore.QSize(80, 0))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/stuff/logo64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.about_btn.setIcon(icon12)
        self.about_btn.setIconSize(QtCore.QSize(48, 48))
        self.about_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.about_btn.setAutoRaise(True)
        self.about_btn.setObjectName("about_btn")
        self.horizontalLayout.addWidget(self.about_btn)
        self.verticalLayout_2.addWidget(self.tool_frame)

        self.retranslateUi(ToolBar)
        QtCore.QMetaObject.connectSlotsByName(ToolBar)

    def retranslateUi(self, ToolBar):
        self.scan_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Scans a directory for Koreader metadata files\n"
"Can also be the eReader\'s root directory (Ctrl+L)", None, QtGui.QApplication.UnicodeUTF8))
        self.scan_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Scans a directory for Koreader metadata files. Can also be the eReader\'s root directory (Ctrl+L)", None, QtGui.QApplication.UnicodeUTF8))
        self.scan_btn.setText(QtGui.QApplication.translate("ToolBar", "Scan Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.export_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Export selected highlights (Ctrl+S)", None, QtGui.QApplication.UnicodeUTF8))
        self.export_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Export selected highlights (Ctrl+S)", None, QtGui.QApplication.UnicodeUTF8))
        self.export_btn.setText(QtGui.QApplication.translate("ToolBar", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.open_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "View the selected book (Ctrl+B)", None, QtGui.QApplication.UnicodeUTF8))
        self.open_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "View the selected book (Ctrl+B)", None, QtGui.QApplication.UnicodeUTF8))
        self.open_btn.setText(QtGui.QApplication.translate("ToolBar", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Open the filtering popup (Alt+F)", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Open the filtering popup (Alt+F)", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_btn.setText(QtGui.QApplication.translate("ToolBar", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.filter_btn.setShortcut(QtGui.QApplication.translate("ToolBar", "Alt+F", None, QtGui.QApplication.UnicodeUTF8))
        self.merge_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Merge the highlights from the same book in two different\n"
"devices, and/or sync their reading position.\n"
"Activated only if two entries of the same book are selected.", None, QtGui.QApplication.UnicodeUTF8))
        self.merge_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Merge the highlights from the same book in two different devices, and/or sync their reading position. Activated only if two entries of the same book are selected.", None, QtGui.QApplication.UnicodeUTF8))
        self.merge_btn.setText(QtGui.QApplication.translate("ToolBar", "Merge/Sync", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Delete selected Highlights (Del)", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Delete selected Highlights (Del)", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_btn.setText(QtGui.QApplication.translate("ToolBar", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Clears the books list (Ctrl+Backspace)", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Clears the books list (Ctrl+Backspace)", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_btn.setText(QtGui.QApplication.translate("ToolBar", "Clear List", None, QtGui.QApplication.UnicodeUTF8))
        self.books_view_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Books View", None, QtGui.QApplication.UnicodeUTF8))
        self.books_view_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Books View", None, QtGui.QApplication.UnicodeUTF8))
        self.books_view_btn.setText(QtGui.QApplication.translate("ToolBar", "Books", None, QtGui.QApplication.UnicodeUTF8))
        self.high_view_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Highlights View", None, QtGui.QApplication.UnicodeUTF8))
        self.high_view_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Highlights View", None, QtGui.QApplication.UnicodeUTF8))
        self.high_view_btn.setText(QtGui.QApplication.translate("ToolBar", "Highlights", None, QtGui.QApplication.UnicodeUTF8))
        self.loaded_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Show the loaded files", None, QtGui.QApplication.UnicodeUTF8))
        self.loaded_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Show the loaded files", None, QtGui.QApplication.UnicodeUTF8))
        self.loaded_btn.setText(QtGui.QApplication.translate("ToolBar", "Loaded", None, QtGui.QApplication.UnicodeUTF8))
        self.db_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Show the archived files in the database\n"
"(Right click to change the database file)", None, QtGui.QApplication.UnicodeUTF8))
        self.db_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Show the archived files in the database (Right click to change the database file)", None, QtGui.QApplication.UnicodeUTF8))
        self.db_btn.setText(QtGui.QApplication.translate("ToolBar", "Archived", None, QtGui.QApplication.UnicodeUTF8))
        self.about_btn.setToolTip(QtGui.QApplication.translate("ToolBar", "Info about the KoHighlights", None, QtGui.QApplication.UnicodeUTF8))
        self.about_btn.setStatusTip(QtGui.QApplication.translate("ToolBar", "Info about the KoHighlights", None, QtGui.QApplication.UnicodeUTF8))
        self.about_btn.setText(QtGui.QApplication.translate("ToolBar", "About", None, QtGui.QApplication.UnicodeUTF8))

from secondary import XToolButton
import images_rc
