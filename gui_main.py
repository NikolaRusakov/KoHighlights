# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Apps\DEV\PROJECTS\KoHighlights\gui_main.ui'
#
# Created: Thu Mar  9 14:39:40 2023
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Base(object):
    def setupUi(self, Base):
        Base.setObjectName("Base")
        Base.resize(640, 512)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/stuff/logo64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Base.setWindowIcon(icon)
        Base.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        Base.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(Base)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.views = QtGui.QStackedWidget(self.centralwidget)
        self.views.setObjectName("views")
        self.books_pg = QtGui.QWidget()
        self.books_pg.setObjectName("books_pg")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.books_pg)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtGui.QSplitter(self.books_pg)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.file_table = DropTableWidget(self.splitter)
        self.file_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.file_table.setFrameShape(QtGui.QFrame.WinPanel)
        self.file_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.file_table.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.file_table.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.file_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.file_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.file_table.setWordWrap(False)
        self.file_table.setCornerButtonEnabled(False)
        self.file_table.setColumnCount(8)
        self.file_table.setObjectName("file_table")
        self.file_table.setColumnCount(8)
        self.file_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.file_table.setHorizontalHeaderItem(7, item)
        self.file_table.horizontalHeader().setDefaultSectionSize(22)
        self.file_table.horizontalHeader().setHighlightSections(False)
        self.file_table.horizontalHeader().setMinimumSectionSize(22)
        self.file_table.horizontalHeader().setSortIndicatorShown(True)
        self.file_table.verticalHeader().setDefaultSectionSize(22)
        self.file_table.verticalHeader().setHighlightSections(True)
        self.file_table.verticalHeader().setMinimumSectionSize(22)
        self.frame = QtGui.QFrame(self.splitter)
        self.frame.setFrameShape(QtGui.QFrame.WinPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtGui.QWidget(self.frame)
        self.header.setObjectName("header")
        self.horizontalLayout = QtGui.QHBoxLayout(self.header)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fold_btn = QtGui.QToolButton(self.header)
        self.fold_btn.setStyleSheet("QToolButton{border:none;}")
        self.fold_btn.setCheckable(True)
        self.fold_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.fold_btn.setArrowType(QtCore.Qt.DownArrow)
        self.fold_btn.setObjectName("fold_btn")
        self.horizontalLayout.addWidget(self.fold_btn)
        self.frame_2 = QtGui.QFrame(self.header)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtGui.QFrame.HLine)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.header)
        self.book_info = QtGui.QFrame(self.frame)
        self.book_info.setFrameShape(QtGui.QFrame.StyledPanel)
        self.book_info.setFrameShadow(QtGui.QFrame.Raised)
        self.book_info.setObjectName("book_info")
        self.gridLayout = QtGui.QGridLayout(self.book_info)
        self.gridLayout.setContentsMargins(6, 0, 6, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.title_lbl = QtGui.QLabel(self.book_info)
        self.title_lbl.setObjectName("title_lbl")
        self.gridLayout.addWidget(self.title_lbl, 0, 0, 1, 1)
        self.series_lbl = QtGui.QLabel(self.book_info)
        self.series_lbl.setObjectName("series_lbl")
        self.gridLayout.addWidget(self.series_lbl, 2, 0, 1, 1)
        self.author_lbl = QtGui.QLabel(self.book_info)
        self.author_lbl.setObjectName("author_lbl")
        self.gridLayout.addWidget(self.author_lbl, 1, 0, 1, 1)
        self.lang_lbl = QtGui.QLabel(self.book_info)
        self.lang_lbl.setObjectName("lang_lbl")
        self.gridLayout.addWidget(self.lang_lbl, 4, 0, 1, 1)
        self.pages_lbl = QtGui.QLabel(self.book_info)
        self.pages_lbl.setObjectName("pages_lbl")
        self.gridLayout.addWidget(self.pages_lbl, 4, 2, 1, 1)
        self.lang_txt = QtGui.QLineEdit(self.book_info)
        self.lang_txt.setReadOnly(True)
        self.lang_txt.setObjectName("lang_txt")
        self.gridLayout.addWidget(self.lang_txt, 4, 1, 1, 1)
        self.pages_txt = QtGui.QLineEdit(self.book_info)
        self.pages_txt.setReadOnly(True)
        self.pages_txt.setObjectName("pages_txt")
        self.gridLayout.addWidget(self.pages_txt, 4, 3, 1, 1)
        self.tags_lbl = QtGui.QLabel(self.book_info)
        self.tags_lbl.setObjectName("tags_lbl")
        self.gridLayout.addWidget(self.tags_lbl, 3, 0, 1, 1)
        self.description_btn = QtGui.QToolButton(self.book_info)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/stuff/description.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.description_btn.setIcon(icon1)
        self.description_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.description_btn.setObjectName("description_btn")
        self.gridLayout.addWidget(self.description_btn, 4, 4, 1, 1)
        self.tags_txt = QtGui.QLineEdit(self.book_info)
        self.tags_txt.setReadOnly(True)
        self.tags_txt.setObjectName("tags_txt")
        self.gridLayout.addWidget(self.tags_txt, 3, 1, 1, 4)
        self.series_txt = QtGui.QLineEdit(self.book_info)
        self.series_txt.setReadOnly(True)
        self.series_txt.setObjectName("series_txt")
        self.gridLayout.addWidget(self.series_txt, 2, 1, 1, 4)
        self.author_txt = QtGui.QLineEdit(self.book_info)
        self.author_txt.setReadOnly(True)
        self.author_txt.setObjectName("author_txt")
        self.gridLayout.addWidget(self.author_txt, 1, 1, 1, 4)
        self.title_txt = QtGui.QLineEdit(self.book_info)
        self.title_txt.setReadOnly(True)
        self.title_txt.setObjectName("title_txt")
        self.gridLayout.addWidget(self.title_txt, 0, 1, 1, 4)
        self.review_lbl = QtGui.QLabel(self.book_info)
        self.review_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.review_lbl.setObjectName("review_lbl")
        self.gridLayout.addWidget(self.review_lbl, 5, 0, 1, 1)
        self.review_txt = QtGui.QLabel(self.book_info)
        self.review_txt.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.review_txt.setFrameShape(QtGui.QFrame.NoFrame)
        self.review_txt.setText("")
        self.review_txt.setWordWrap(True)
        self.review_txt.setObjectName("review_txt")
        self.gridLayout.addWidget(self.review_txt, 5, 1, 1, 4)
        self.verticalLayout.addWidget(self.book_info)
        self.high_list = QtGui.QListWidget(self.frame)
        self.high_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.high_list.setFrameShape(QtGui.QFrame.WinPanel)
        self.high_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.high_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.high_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.high_list.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.high_list.setWordWrap(True)
        self.high_list.setObjectName("high_list")
        self.verticalLayout.addWidget(self.high_list)
        self.verticalLayout_3.addWidget(self.splitter)
        self.views.addWidget(self.books_pg)
        self.highlights_pg = QtGui.QWidget()
        self.highlights_pg.setObjectName("highlights_pg")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.highlights_pg)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.high_table = QtGui.QTableWidget(self.highlights_pg)
        self.high_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.high_table.setFrameShape(QtGui.QFrame.WinPanel)
        self.high_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.high_table.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.high_table.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.high_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.high_table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.high_table.setWordWrap(False)
        self.high_table.setCornerButtonEnabled(False)
        self.high_table.setColumnCount(8)
        self.high_table.setObjectName("high_table")
        self.high_table.setColumnCount(8)
        self.high_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.high_table.setHorizontalHeaderItem(7, item)
        self.high_table.horizontalHeader().setHighlightSections(False)
        self.high_table.horizontalHeader().setMinimumSectionSize(22)
        self.high_table.horizontalHeader().setSortIndicatorShown(True)
        self.high_table.horizontalHeader().setStretchLastSection(True)
        self.high_table.verticalHeader().setDefaultSectionSize(22)
        self.high_table.verticalHeader().setHighlightSections(True)
        self.high_table.verticalHeader().setMinimumSectionSize(22)
        self.verticalLayout_4.addWidget(self.high_table)
        self.views.addWidget(self.highlights_pg)
        self.verticalLayout_2.addWidget(self.views)
        Base.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Base)
        self.statusbar.setStyleSheet("QStatusBar{padding-left:8px;font-weight:bold;}")
        self.statusbar.setObjectName("statusbar")
        Base.setStatusBar(self.statusbar)
        self.tool_bar = QtGui.QToolBar(Base)
        self.tool_bar.setWindowTitle("toolBar")
        self.tool_bar.setMovable(True)
        self.tool_bar.setAllowedAreas(QtCore.Qt.BottomToolBarArea|QtCore.Qt.TopToolBarArea)
        self.tool_bar.setIconSize(QtCore.QSize(32, 32))
        self.tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.tool_bar.setObjectName("tool_bar")
        Base.addToolBar(QtCore.Qt.TopToolBarArea, self.tool_bar)
        self.act_english = QtGui.QAction(Base)
        self.act_english.setCheckable(True)
        self.act_english.setChecked(False)
        self.act_english.setObjectName("act_english")
        self.act_greek = QtGui.QAction(Base)
        self.act_greek.setCheckable(True)
        self.act_greek.setChecked(False)
        self.act_greek.setObjectName("act_greek")
        self.act_view_book = QtGui.QAction(Base)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/stuff/files_view.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.act_view_book.setIcon(icon2)
        self.act_view_book.setObjectName("act_view_book")

        self.retranslateUi(Base)
        self.views.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Base)

    def retranslateUi(self, Base):
        self.file_table.setSortingEnabled(True)
        self.file_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Base", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Base", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Base", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Base", "Percent", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Base", "Rating", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("Base", "Highlights", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("Base", "Modified", None, QtGui.QApplication.UnicodeUTF8))
        self.file_table.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("Base", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.fold_btn.setText(QtGui.QApplication.translate("Base", "Hide Book Info", None, QtGui.QApplication.UnicodeUTF8))
        self.title_lbl.setText(QtGui.QApplication.translate("Base", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.series_lbl.setText(QtGui.QApplication.translate("Base", "Series", None, QtGui.QApplication.UnicodeUTF8))
        self.author_lbl.setText(QtGui.QApplication.translate("Base", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.lang_lbl.setText(QtGui.QApplication.translate("Base", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.pages_lbl.setText(QtGui.QApplication.translate("Base", "Pages", None, QtGui.QApplication.UnicodeUTF8))
        self.tags_lbl.setText(QtGui.QApplication.translate("Base", "Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.description_btn.setText(QtGui.QApplication.translate("Base", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.review_lbl.setText(QtGui.QApplication.translate("Base", "Review", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.setSortingEnabled(True)
        self.high_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Base", "Highlight", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Base", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Base", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Base", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Base", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("Base", "Page", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("Base", "Chapter", None, QtGui.QApplication.UnicodeUTF8))
        self.high_table.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("Base", "Book path", None, QtGui.QApplication.UnicodeUTF8))
        self.act_english.setText(QtGui.QApplication.translate("Base", "English", None, QtGui.QApplication.UnicodeUTF8))
        self.act_greek.setText(QtGui.QApplication.translate("Base", "Greek", None, QtGui.QApplication.UnicodeUTF8))
        self.act_view_book.setText(QtGui.QApplication.translate("Base", "View Book", None, QtGui.QApplication.UnicodeUTF8))
        self.act_view_book.setShortcut(QtGui.QApplication.translate("Base", "Ctrl+B", None, QtGui.QApplication.UnicodeUTF8))

from secondary import DropTableWidget
import images_rc
