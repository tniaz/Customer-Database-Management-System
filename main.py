#importing required packages
import sys,sqlite3,time
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtCore import QCoreApplication

#defining class to handle database queries
class DBHelper():
    def __init__(self):
        self.conn = sqlite3.connect("cdms.db")
        self.c = self.conn.cursor()
        #initializing database tables if they do not exist already
        self.c.execute("CREATE TABLE IF NOT EXISTS customers(cid INTEGER,name TEXT,gender INTEGER,storeid INTEGER,age INTEGER,address TEXT,mobile INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS transactions(reciept_no INTEGER,cid INTEGER,fee INTEGER,storeid INTEGER,reciept_date TEXT, payment_type INTEGER, eid INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS stores(storeid INTEGER,name TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS employees(eid INTEGER,name TEXT, mobile INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS directory(id INTEGER,name TEXT, mobile INTEGER)")
    #method for adding customer to database
    def addCustomer(self, cid, name, gender, storeid, age, address, mobile):
        try:
            self.c.execute("INSERT INTO customers (cid,name,gender,storeid,age,address,mobile) VALUES (?,?,?,?,?,?,?)", (cid, name, gender, storeid, age, address, mobile))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Successful', 'Customer is added successfully to the database.')
        #exception error
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add customer to the database.')
    #method for adding transaction to database
    def addTransaction(self,cid,fee,storeid,payment_type, eid):
        reciept_no=int(time.time())
        date=time.strftime("%b %d %Y %H:%M:%S")
        try:
            self.c.execute("INSERT INTO transactions (reciept_no,cid,fee,storeid,reciept_date,payment_type,eid) VALUES (?,?,?,?,?,?,?)",(reciept_no, cid, fee, storeid, date, payment_type, eid))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Successful','Transaction is added successfully to the database.\nReference ID=' + str(reciept_no))
        #exception error
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add transaction to the database.')
    #method to search for customer using a cid number and the results are returned to the function showCustomer() which then analyzes the list
    def searchCustomer(self, cid):
        self.c.execute("SELECT * from customers WHERE cid=" + str(cid))
        self.data = self.c.fetchone()
        #if there is no data returned by above cursor function fetchone() then it means there is no record holding the cid number, so a warning box displayed and returned from the function
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any customer with cid no ' + str(cid))
            return None
        self.list = []
        #add query results into list form
        for i in range(0, 7):
            self.list.append(self.data[i])
        self.c.close()
        self.conn.close()
        #calls on function that takes the list and displays the output in tabular form to the user
        showCustomer(self.list)
    #method to search transactions based on cid number
    def searchTransaction(self,cid):
        #initialize text string to hold transaction query results
        text=''
        self.c.execute("SELECT * from transactions WHERE cid="+str(cid)+" ORDER BY reciept_no DESC")
        self.data=self.c.fetchall()
        #error returned if there are no transactions for given cid
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any transactions for customer with cid: '+str(cid))
            return None
        #add query results to text string
        for row in self.data:
            text+=str(row)+"\n"
        self.c.close()
        self.conn.close()
        #passes text string to function to display results to the user
        showTransactionFunction(text)


#function to display results for customer given the query results passed in list form
def showCustomer(list):
    #initialize attributes
    cid = 0
    gender = ""
    storeid = ""
    age = ""
    name = ""
    address = ""
    mobile = -1
    #defining values from list
    cid = list[0]
    name = list[1]

    if list[2] == 0:
        gender = "Male"
    else:
        gender = "Female"

    if list[3] == 0:
        storeid = "Store 0"
    elif list[3] == 1:
        storeid = "Store 1"
    elif list[3] == 2:
        storeid = "Store 2"
    elif list[3] == 3:
        storeid = "Store 3"
    elif list[3] == 4:
        storeid = "Store 4"
    elif list[3] == 5:
        storeid = "Store 5"

    age = list[4]
    address = list[5]
    mobile = list[6]

    #creating a PyQt table and passing in the labels,values in x,y grid form
    table = QTableWidget()
    table.setWindowTitle("Customer Details")
    #setting table dimensions
    table.setRowCount(7)
    table.setColumnCount(2)
    #adding labels, values as widget items in x,y form
    table.setItem(0, 0, QTableWidgetItem("Cid"))
    table.setItem(0, 1, QTableWidgetItem(str(cid)))
    table.setItem(1, 0, QTableWidgetItem("Name"))
    table.setItem(1, 1, QTableWidgetItem(str(name)))
    table.setItem(2, 0, QTableWidgetItem("Gender"))
    table.setItem(2, 1, QTableWidgetItem(str(gender)))
    table.setItem(3, 0, QTableWidgetItem("Store Id"))
    table.setItem(3, 1, QTableWidgetItem(str(storeid)))
    table.setItem(4, 0, QTableWidgetItem("Age"))
    table.setItem(4, 1, QTableWidgetItem(str(age)))
    table.setItem(5, 0, QTableWidgetItem("Address"))
    table.setItem(5, 1, QTableWidgetItem(str(address)))
    table.setItem(6, 0, QTableWidgetItem("Mobile"))
    table.setItem(6, 1, QTableWidgetItem(str(mobile)))
    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    #initilize dialog box and add table widget
    dialog = QDialog()
    dialog.setWindowTitle("Customer Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()

#function to display the transactions for the text string of query results passed in
def showTransactionFunction(text):
    #initializing a QTextEdit widget item to hold the text string
    logOutput = QTextEdit()
    logOutput.setReadOnly(True)
    logOutput.setLineWrapMode(QTextEdit.NoWrap)
    font = logOutput.font()
    font.setFamily("Courier")
    font.setPointSize(10)
    logOutput.moveCursor(QTextCursor.End)
    logOutput.setCurrentFont(font)
    logOutput.setTextColor(QtGui.QColor("black"))
    logOutput.insertPlainText(text)
    sb = logOutput.verticalScrollBar()
    sb.setValue(sb.maximum())
    #initializing dialog box and adding the logOutput widget
    dialog = QDialog()
    dialog.setWindowTitle("Customer Transactions")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(logOutput)
    dialog.exec()


#creating a class which inherits QDialog to create the entry form of adding a new customer to the database
class AddCustomer(QDialog):
    def __init__(self):
        super().__init__()

        #general attributes
        self.gender=-1
        self.storeid=-1
        self.age=-1
        self.cid=-1
        self.name=""
        self.address=""
        self.mobile=-1

        #initilialzing buttons for cancel, reset and add
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)
        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        #creating QComboBox items for dropdown selection of categorical variables
        self.genderCombo = QComboBox(self)
        self.genderCombo.addItem("Male")
        self.genderCombo.addItem("Female")

        self.storeidCombo = QComboBox(self)
        self.storeidCombo.addItem("Store 0")
        self.storeidCombo.addItem("Store 1")
        self.storeidCombo.addItem("Store 2")
        self.storeidCombo.addItem("Store 3")
        self.storeidCombo.addItem("Store 4")
        self.storeidCombo.addItem("Store 5")

        #creating QLabel items for the variables to be entered/selected
        self.cidLabel=QLabel("Cid No")
        self.nameLabel=QLabel("Name")
        self.addressLabel = QLabel("Address")
        self.mobLabel = QLabel("Mobile")
        self.ageLabel = QLabel("Age")
        self.storeidLabel = QLabel("Storeid")
        self.genderLabel=QLabel("Gender")

        #QLineEdit items for variables that must be typed
        self.cidText=QLineEdit(self)
        self.nameText=QLineEdit(self)
        self.addressText = QLineEdit(self)
        self.ageText=QLineEdit(self)
        self.mobText = QLineEdit(self)

        #initializing a QGridLayout and adding labels,items in x,y format
        self.grid=QGridLayout(self)
        self.grid.addWidget(self.cidLabel,1,1)
        self.grid.addWidget(self.nameLabel,2,1)
        self.grid.addWidget(self.genderLabel, 3, 1)
        self.grid.addWidget(self.addressLabel, 4, 1)
        self.grid.addWidget(self.ageLabel, 5, 1)
        self.grid.addWidget(self.storeidLabel, 6, 1)
        self.grid.addWidget(self.mobLabel,7,1)

        self.grid.addWidget(self.cidText,1,2)
        self.grid.addWidget(self.nameText,2,2)
        self.grid.addWidget(self.genderCombo, 3, 2)
        self.grid.addWidget(self.addressText, 4, 2)
        self.grid.addWidget(self.ageText,5,2)
        self.grid.addWidget(self.storeidCombo, 6, 2)
        self.grid.addWidget(self.mobText, 7, 2)

        #adding three buttons into grid
        self.grid.addWidget(self.btnReset,9,1)
        self.grid.addWidget(self.btnAdd,9,2)
        self.grid.addWidget(self.btnCancel,9,3)

        #button connectors where Add calls of addCustomer(), Cancel quits the instance, Reset calls of reset()
        self.btnAdd.clicked.connect(self.addCustomer)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnReset.clicked.connect(self.reset)

        #initializing the window and adding the grid
        self.setLayout(self.grid)
        self.setWindowTitle("Add Customer Details")
        self.resize(500,300)
        self.show()
        sys.exit(self.exec())

    #reset method which resets the text field values
    def reset(self):
        self.cidText.setText("")
        self.nameText.setText("")
        self.addressText.setText("")
        self.ageText.setText("")
        self.mobText.setText("")

    #addCustomer method which takes the values entered/selected and passes them to the DBHelper class to run the database query
    def addCustomer(self):
        self.gender=self.genderCombo.currentIndex()
        self.storeid=self.storeidCombo.currentIndex()
        self.cid=int(self.cidText.text())
        self.name=self.nameText.text()
        self.age=int(self.ageText.text())
        self.address=self.addressText.text()
        self.mobile=int(self.mobText.text())
        #passes fields to DBHelper
        self.dbhelper=DBHelper()
        self.dbhelper.addCustomer(self.cid,self.name,self.gender,self.storeid,self.age,self.address,self.mobile)

#creating a class which inherits QDialog to create the entry form of adding a new transaction to the database
class AddTransaction(QDialog):
    def __init__(self):
        super().__init__()

        #general attributes
        self.reciept_no=-1
        self.cid=-1
        self.fee=-1
        self.storeid=-1
        self.reciept_date=-1
        self.payment_type=-1
        self.eid=-1

        #initializing cancel,add,reset buttons
        self.btnCancel=QPushButton("Cancel",self)
        self.btnReset=QPushButton("Reset",self)
        self.btnAdd=QPushButton("Add",self)
        self.btnCancel.setFixedHeight(30)
        self.btnReset.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        #creating QComboBox items for dropdown selection of categorical variables
        self.storeidCombo = QComboBox(self)
        self.storeidCombo.addItem("Store 0")
        self.storeidCombo.addItem("Store 1")
        self.storeidCombo.addItem("Store 2")
        self.storeidCombo.addItem("Store 3")
        self.storeidCombo.addItem("Store 4")
        self.storeidCombo.addItem("Store 5")

        self.paymenttypeCombo = QComboBox(self)
        self.paymenttypeCombo.addItem("Cash")
        self.paymenttypeCombo.addItem("Debit")
        self.paymenttypeCombo.addItem("Credit")

        #creating QLabel items for variables
        self.cidLabel=QLabel("Cid No")
        self.feeLabel=QLabel("Total Fee")
        self.storeidLabel = QLabel("Store id")
        self.paymenttypeLabel = QLabel("Payment type")
        self.eidLabel = QLabel("Employee id")

        #creating QLineEdit items for values that need to be typed by the user
        self.cidText=QLineEdit(self)
        self.feeText=QLineEdit(self)
        self.eidText=QLineEdit(self)

        #creating a grid and adding the labels,widgets in x,y format
        self.grid=QGridLayout(self)
        self.grid.addWidget(self.cidLabel,1,1)
        self.grid.addWidget(self.feeLabel,2,1)
        self.grid.addWidget(self.storeidLabel, 3, 1)
        self.grid.addWidget(self.paymenttypeLabel, 4, 1)
        self.grid.addWidget(self.eidLabel, 5, 1)

        self.grid.addWidget(self.cidText,1,2)
        self.grid.addWidget(self.feeText,2,2)
        self.grid.addWidget(self.storeidCombo, 3, 2)
        self.grid.addWidget(self.paymenttypeCombo, 4, 2)
        self.grid.addWidget(self.eidText, 5, 2)

        #adding three buttons in grid form
        self.grid.addWidget(self.btnReset,6,1)
        self.grid.addWidget(self.btnAdd,6,2)
        self.grid.addWidget(self.btnCancel,6,3)

        #button connections for Add which calls on addTransaction(), Cancel which quits the instance, Reset which calls on reset()
        self.btnAdd.clicked.connect(self.addTransaction)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnReset.clicked.connect(self.reset)

        #setting the window layout and adding the grid
        self.setLayout(self.grid)
        self.setWindowTitle("Add Transaction Details")
        self.resize(400,200)
        self.show()
        sys.exit(self.exec())

    #reset method that resets the text fields
    def reset(self):
        self.cidText.setText("")
        self.feeText.setText("")
        self.eidText.setText("")

    #addTransaction method which takes the field values and passes them to the DBHelper class to run the database query
    def addTransaction(self):
        self.storeid=self.storeidCombo.currentIndex()
        self.paymenttype=self.paymenttypeCombo.currentIndex()
        self.cid=int(self.cidText.text())
        self.fee=int(self.feeText.text())
        self.eid=int(self.eidText.text())

        #passes fields to DBHelper class
        self.dbhelper=DBHelper()
        self.dbhelper.addTransaction(self.cid,self.fee,self.storeid,self.paymenttype,self.eid)


#creating a main Window class with inheritance QMainWindow that holds the buttons for Enter Customer Details, Enter Payment Details, Show Customer Details, Show Transaction Details
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #intializing QDialog prompt for case where search for Show Customer Details is selected
        self.cidToBeSearched=0
        #initializing box layout and creating label, entry field and Seach button
        self.vbox = QVBoxLayout()
        self.text = QLabel("Enter the cid no of the customer")
        self.editField = QLineEdit()
        self.btnSearch = QPushButton("Search", self)
        #calls on showCustomer method when clicked
        self.btnSearch.clicked.connect(self.showCustomer)
        #adding widgets to box layout
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.editField)
        self.vbox.addWidget(self.btnSearch)
        #creating dialog and adding box layout
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Enter cid No")
        self.dialog.setLayout(self.vbox)

        #intializing QDialog prompt for case where search for Show Transaction Details is selected
        self.cidForTransaction = 0
        #initializing box layout and creating label, entry field and Seach button
        self.vboxTransaction = QVBoxLayout()
        self.textTransaction = QLabel("Enter the cid no of the customer")
        self.editFieldTransaction = QLineEdit()
        self.btnSearchTransaction = QPushButton("Search", self)
        #calls on showCustomerTransaction method when clicked
        self.btnSearchTransaction.clicked.connect(self.showCustomerTransaction)
        #adding widgets to box layout
        self.vboxTransaction.addWidget(self.textTransaction)
        self.vboxTransaction.addWidget(self.editFieldTransaction)
        self.vboxTransaction.addWidget(self.btnSearchTransaction)
        #creating dialog and adding box layout
        self.dialogTransaction = QDialog()
        self.dialogTransaction.setWindowTitle("Enter Cid No")
        self.dialogTransaction.setLayout(self.vboxTransaction)

        #creating the 4 buttons on the main window
        self.btnEnterCustomer=QPushButton("Enter Customer Details", self)
        self.btnEnterTransaction=QPushButton("Enter Transaction Details",self)
        self.btnShowCustomerDetails=QPushButton("Show Customer Details",self)
        self.btnShowTransactionDetails=QPushButton("Show Transaction Details",self)

        #adding image
        self.image=QLabel(self)
        self.image.resize(150,150)
        self.image.move(120,20)
        self.image.setScaledContents(True)
        self.image.setPixmap(QtGui.QPixmap("icon.png"))

        #placing buttons and mapping to their respective methods
        self.btnEnterCustomer.move(15,170)
        self.btnEnterCustomer.resize(180,40)
        self.btnEnterCustomerFont=self.btnEnterCustomer.font()
        self.btnEnterCustomerFont.setPointSize(13)
        self.btnEnterCustomer.setFont(self.btnEnterCustomerFont)
        self.btnEnterCustomer.clicked.connect(self.entercustomer)

        self.btnEnterTransaction.move(205,170)
        self.btnEnterTransaction.resize(180, 40)
        self.btnEnterTransaction.setFont(self.btnEnterCustomerFont)
        self.btnEnterTransaction.clicked.connect(self.entertransaction)

        self.btnShowCustomerDetails.move(15, 220)
        self.btnShowCustomerDetails.resize(180, 40)
        self.btnShowCustomerDetails.setFont(self.btnEnterCustomerFont)
        self.btnShowCustomerDetails.clicked.connect(self.showCustomerDialog)

        self.btnShowTransactionDetails.move(205, 220)
        self.btnShowTransactionDetails.resize(180, 40)
        self.btnShowTransactionDetails.setFont(self.btnEnterCustomerFont)
        self.btnShowTransactionDetails.clicked.connect(self.showCustomerTransactionDialog)

        #resizing and setting window title
        self.resize(400,280)
        self.setWindowTitle("Customer Database Management System")

    #entercustomer method which call on the AddCustomer function
    def entercustomer(self):
        enterCustomer=AddCustomer()

    #entertransaction method which calls on the AddTransaction function
    def entertransaction(self):
        enterTransaction=AddTransaction()

    #showCustomerDialog method which executes QDialog prompt for case where Show Customer Details is selected
    def showCustomerDialog(self):
        self.dialog.exec()

    #showCustomerTransactionDialog method which executes QDialog prompt for case where Show Transaction Details is selected
    def showCustomerTransactionDialog(self):
        self.dialogTransaction.exec()

    #showCustomer method that takes editField entry and passes to DBHelper class to run query
    def showCustomer(self):
        if self.editField.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the cid number to show the results for.')
            return None
        showcustomer = DBHelper()
        #runs DBhelper class for searchCustomer
        showcustomer.searchCustomer(int(self.editField.text()))

    #showCustomerTransaction method that takes editField entry and passes to DBHelper class to run query
    def showCustomerTransaction(self):
        if self.editFieldTransaction.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the cid number to show the results for.')
            return None
        showcustomer = DBHelper()
        #runs DBhelper class for searchTransaction
        showcustomer.searchTransaction(int(self.editFieldTransaction.text()))

#creating a Login window class with inheritance QDialog
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        #label and QLineEdit fields for username and password
        self.userNameLabel=QLabel("Username")
        self.userPassLabel=QLabel("Password")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        #Login button which calls upon handleLogin when clicked
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        #adding widget items to QGridLayout layout dialog in x,y format
        layout = QGridLayout(self)
        layout.addWidget(self.userNameLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)
        layout.addWidget(self.textName,1,2)
        layout.addWidget(self.textPass,2,2)
        layout.addWidget(self.buttonLogin,3,1,1,2)
        self.setWindowTitle("Login")

    #handleLogin method that verifies entered login details
    def handleLogin(self):
        if (self.textName.text() == 'admin' and
            self.textPass.text() == 'admin'):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

#main function which executes the login dialog first
#main window is opened upon a succesful login
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()

    sys.exit(app.exec_())
