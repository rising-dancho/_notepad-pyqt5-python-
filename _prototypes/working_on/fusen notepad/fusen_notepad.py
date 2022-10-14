import os
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.Qsci import * 
# test

from pathlib import Path

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        # add before init
        self.side_bar_clr = "#282c34"

        self.init_ui()

        self.current_file = None
        self.current_side_bar = None

    def init_ui(self):
        self.setWindowTitle("PYQT EDITOR")
        self.resize(1300, 900)

        self.setStyleSheet(open("./css/style.qss", "r").read())

        # alternative Consolas font
        self.window_font = qtg.QFont("Consolas") # font needs to be installed in your computer if its not use something else
        self.window_font.setPointSize(11)
        self.setFont(self.window_font) 


        self.set_up_menu()
        self.set_up_body()
        self.statusBar().showMessage("Ready")

        self.show()


    def set_up_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        
        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        # new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        # open_file.triggered.connect(self.open_file)

        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        # open_folder.triggered.connect(self.open_folder)

        file_menu.addSeparator()
        
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        # save_file.triggered.connect(self.save_file)

        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        # save_as.triggered.connect(self.save_as)
        

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        # you can add more


    def get_editor(self, path: Path = None, is_python_file=True) -> QsciScintilla:
        
        #editor
        editor = QsciScintilla()

        # Font
        editor.setFont(self.window_font)

        # brace matching
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # indentation
        editor.setIndentationGuides(True)
        editor.setTabWidth(4)
        editor.setIndentationsUseTabs(False)
        editor.setAutoIndent(True)

        # autocomplete
        editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        editor.setAutoCompletionThreshold(1) 
        editor.setAutoCompletionCaseSensitivity(False)
        editor.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # caret
        # editor.setCaretForegroundColor(QColor("#dedcdc"))
        # editor.setCaretLineVisible(True)
        # editor.setCaretWidth(2)
        # editor.setCaretLineBackgroundColor(QColor("#2c313c"))
        
        # EOL
        editor.setEolMode(QsciScintilla.EolWindows)
        editor.setEolVisibility(False)

        # lexer
        editor.setLexer(None)

        # line numbers
        editor.setMarginType(0, QsciScintilla.NumberMargin)
        editor.setMarginWidth(0, "000")
        editor.setMarginsForegroundColor(qtg.QColor("#ff888888"))
        editor.setMarginsBackgroundColor(qtg.QColor("#282c34"))
        editor.setMarginsFont(self.window_font)
        
        return editor


    def is_binary(self, path):
        '''
        Check if file is binary
        '''
        with open(path, 'rb') as f:
            return b'\0' in f.read(1024)


    def set_new_tab(self, path: Path, is_new_file=False):
        if not path.is_file():
            return
        if not is_new_file and self.is_binary(path):
            self.statusBar().showMessage("Cannot Open Binary File", 2000)
            return
        
        # check if file already open
        if not is_new_file:
            for i in range(self.tab_view.count()):
                if self.tab_view.tabText(i) == path.name:
                    self.tab_view.setCurrentIndex(i)
                    self.current_file = path
                    return

        # create new tab
        editor = self.get_editor()

        self.tab_view.addTab(editor, path.name)

        if not is_new_file:
            editor.setText(path.read_text())
        self.setWindowTitle(path.name)
        self.current_file = path
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.statusBar().showMessage(f"Opened {path.name}", 2000)
            

    # def get_frame(self) -> qtw.QFrame:
    #     frame = qtw.QFrame()
    #     frame.setFrameShape(qtw.QFrame.NoFrame)
    #     frame.setFrameShadow(qtw.QFrame.Plain)
    #     frame.setContentsMargins(0, 0, 0, 0)
    #     frame.setStyleSheet('''
    #         QFrame {
    #             background-color: #21252b;
    #             border-radius: 5px;
    #             border: none;
    #             padding: 5px;
    #             color: #D3D3D3;
    #         }
    #         QFrame:hover {
    #             color: white;
    #         }
    #     ''')
    #     return frame

    def set_up_body(self):

        # Body        
        body_frame = qtw.QFrame()
        body_frame.setFrameShape(qtw.QFrame.NoFrame)
        body_frame.setFrameShadow(qtw.QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0) 
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        body = qtw.QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        ##############################
        ###### SIDE BAR ##########
        self.side_bar = qtw.QFrame()
        self.side_bar.setFrameShape(qtw.QFrame.StyledPanel)
        self.side_bar.setFrameShadow(qtw.QFrame.Plain)
        self.side_bar.setStyleSheet(
        f'''
            background-color: {self.side_bar_clr};
        ''')   
         
        side_bar_layout = qtw.QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(qtc.Qt.AlignTop | qtc.Qt.AlignCenter)
        
        # setup labels
        folder_label = qtw.QLabel()
        folder_label.setPixmap(qtg.QPixmap("./icons/folder.png").scaled(qtc.QSize(30, 30)))
        folder_label.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)
        folder_label.setFont(self.window_font)
        folder_label.mousePressEvent = self.show_hide_tab()
        side_bar_layout.addWidget(folder_label)
        self.side_bar.setLayout(side_bar_layout)

        body.addWidget(self.side_bar)

        # split view
        self.hsplit = qtw.QSplitter(qtc.Qt.Horizontal)

         # frame layout to hold tree view (file manager)
        self.tree_frame = qtw.QFrame()
        self.tree_frame.setLineWidth(1)
        self.tree_frame.setMaximumWidth(400)
        self.tree_frame.setMinimumWidth(200)
        self.tree_frame.setBaseSize(100,0)
        self.tree_frame.setContentsMargins(0,0,0,0)
        tree_frame_layout = qtw.QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)
        self.tree_frame.setStyleSheet(
            """
                QFrame{
                    background-color: #21252b;
                    border-radius: 5px;
                    border: none;
                    padding: 5px;
                    color: #d3d3d3;
                }
                QFrame:hover{
                    color: white;
                }
            """
        )
        # Create file system model to show in tree view
        self.model = qtw.QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        # File system filters
        self.model.setFilter(qtc.QDir.NoDotAndDotDot | qtc.QDir.AllDirs | qtc.QDir.Files)


        ##############################
        ###### FILE VIEWER ##########
        self.tree_view = qtw.QTreeView()
        self.tree_view.setFont(qtg.QFont("Consolas", 11))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(qtw.QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(qtw.QTreeView.SelectRows)
        self.tree_view.setEditTriggers(qtw.QTreeView.NoEditTriggers)
        # add custom context menu
        self.tree_view.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        # handling click
        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10) 
        self.tree_view.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        # Hide header and hide other columns except for name
        self.tree_view.setHeaderHidden(True) # hiding header
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        # # setup layout
        tree_frame_layout.addWidget(self.tree_view)
        self.tree_frame.setLayout(tree_frame_layout)

        ##############################
        ###### TAB VIEW ##########

        # Tab Widget to add editor to
        self.tab_view = qtw.QTabWidget()
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)


        # # add tree view and tab view
        self.hsplit.addWidget(self.tree_frame)
        self.hsplit.addWidget(self.tab_view)

               
        body.addWidget(self.hsplit)
        body_frame.setLayout(body)
        self.setCentralWidget(body_frame)
     
        

    def tree_view_context_menu(self, pos):
        ...


    def tree_view_clicked(self, index: qtc.QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)


    def close_tab(self, index):
        self.tab_view.removeTab(index)

    def show_hide_tab(self):
        ...
        # if type_ == "folder-icon":
        #     if not (self.file_manager_frame in self.hsplit.children()):
        #         self.hsplit.replaceWidget(0, self.file_manager_frame)
        # elif type_ == "search-icon":
        #     if not (self.search_frame in self.hsplit.children()):
        #         self.hsplit.replaceWidget(0, self.search_frame)

        # if self.current_side_bar == type_:
        #     frame = self.hsplit.children()[0]
        #     if frame.isHidden():
        #         frame.show()
        #     else:
        #         frame.hide()
        
        # self.current_side_bar = type_
        
   
    def new_file(self):
        self.set_new_tab(None, is_new_file=True)

    def save_file(self):
        if self.current_file is None and self.tab_view.count() > 0:
            self.save_as()
        
        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)

    
    def save_as(self):
        # save as 
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        
        file_path = qtw.QFileDialog.getSaveFileName(self, "Save As", os.getcwd())[0]
        if file_path == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return 
        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(), path.name)
        self.statusBar().showMessage(f"Saved {path.name}", 2000)
        self.current_file = path


    def open_file(self):
        # open file
        ops = qtw.QFileDialog.Options() # this is optional
        ops |= qtw.QFileDialog.DontUseNativeDialog
        # i will add support for opening multiple files later for now it can only open one at a time
        new_file, _ = qtw.QFileDialog.getOpenFileName(self,
                    "Pick A File", "", "All Files (*);;Python Files (*.py)",
                    options=ops)
        if new_file == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)


    def open_folder(self):
        # open folder
        ops = qtw.QFileDialog.Options() # this is optional
        ops |= qtw.QFileDialog.DontUseNativeDialog

        new_folder = qtw.QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options=ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)

    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()



if __name__ == '__main__':
    app = qtw.QApplication([])
    window = MainWindow()
    sys.exit(app.exec())