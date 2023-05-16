import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone2.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.catList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.bname.textChanged.connect(self.getBusinessNames)
        self.ui.businesses.itemSelectionChanged.connect(self.displayBusinessCity)

    def cleanStr4SQL(self, s):
        return s.replace("'","''").replace("\n"," ")

    def execQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='admin'")
        except:
            print('Failed Connection')

        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = ('SELECT distinct state_name FROM business ORDER BY state_name;')
        try:
            results = self.execQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print('StateList failed')

        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        self.ui.zipList.clear()
        self.ui.catList.clear()
        self.ui.succTable.clear()
        self.ui.popTable.clear() 
        self.ui.avgIncome.clear()
        self.ui.population.clear()
        self.ui.busiNo.clear()

        state = self.ui.stateList.currentText()

        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT distinct city_name FROM business WHERE state_name= '" + state + "' ORDER BY city_name;"
            print(sql_str)

            try:
                results = self.execQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print('City query failed')

            for i in reversed(range(self.ui.busiTable.rowCount())):
                self.ui.busiTable.removeRow(i)

            sql_str = "SELECT business_name, business_address, CAST(stars AS FLOAT), CAST(avgRating AS FLOAT), numReviews, checkins FROM business WHERE state_name = '" + state + "' ORDER BY business_name;"
            print(sql_str)

            try:
                results = self.execQuery(sql_str)
                self.ui.busiTable.setColumnCount(len(results[0]))
                self.ui.busiTable.setRowCount(len(results))

                self.ui.busiTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'Stars', 'Average Score', 'Review Count', 'Checkins'])
                self.ui.busiTable.resizeColumnsToContents()
                self.ui.busiTable.setColumnWidth(0, 200)
                self.ui.busiTable.setColumnWidth(1, 200)
                self.ui.busiTable.setColumnWidth(2, 100)
                self.ui.busiTable.setColumnWidth(3, 100)
                self.ui.busiTable.setColumnWidth(4, 100)
                self.ui.busiTable.setColumnWidth(5, 100)
                
                currentRowCount = 0

                for row in results:
                    for colCount in range (0,len(results[0])):
                        self.ui.busiTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except:
                print('Business query failed')

    def cityChanged(self):

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            self.ui.succTable.clear()
            self.ui.popTable.clear() 
            self.ui.avgIncome.clear()
            self.ui.population.clear()
            self.ui.busiNo.clear()


            sql_str = "SELECT zip, business_name, business_address, CAST(stars AS FLOAT), CAST(avgRating AS FLOAT), numReviews, checkins FROM business WHERE state_name = '" + state + "' AND city_name = '" + city + "' ORDER BY business_name;"

            try:
                results = self.execQuery(sql_str)
                self.ui.zipList.clear()
                self.ui.catList.clear()
                zipcodes = []

                for x in results:
                    if x[0] not in zipcodes:
                        zipcodes.append(x[0])
                        self.ui.zipList.addItem(x[0])

                self.ui.busiTable.setColumnCount(len(results[0]) - 1)
                self.ui.busiTable.setRowCount(len(results))

                self.ui.busiTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'Stars', 'Average Score', 'Review Count', 'Checkins'])
                self.ui.busiTable.resizeColumnsToContents()
                self.ui.busiTable.setColumnWidth(0, 200)
                self.ui.busiTable.setColumnWidth(1, 200)
                self.ui.busiTable.setColumnWidth(2, 100)
                self.ui.busiTable.setColumnWidth(3, 100)
                self.ui.busiTable.setColumnWidth(4, 100)
                self.ui.busiTable.setColumnWidth(5, 100)
                
                currentRowCount = 0           

                for row in results:
                    for colCount in range (1,len(results[0])):
                        self.ui.busiTable.setItem(currentRowCount, colCount - 1, QTableWidgetItem(str(row[colCount])))

                    currentRowCount += 1

            except:
                print('Business query failed')

    def zipChanged(self):

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0):
            self.ui.succTable.clear()
            self.ui.popTable.clear() 
            self.ui.avgIncome.clear()
            self.ui.population.clear()
            self.ui.busiNo.clear()

            zip = self.ui.zipList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT business_name, business_address, CAST(stars AS FLOAT), CAST(avgRating AS FLOAT), numReviews, checkins FROM business WHERE state_name = '" + state + "' AND city_name = '" + city + "' AND zip = '" + zip + "' ORDER BY business_name;"

            #update busiTable
            try:
                results = self.execQuery(sql_str)
                sql_str = "SELECT business_name, checkins FROM business WHERE issuccessful = TRUE AND state_name = '" + state + "' AND city_name = '" + city + "' AND zip = '" + zip + "' ORDER BY business_name;"
                succResults = self.execQuery(sql_str)

                sql_str = "SELECT business_name, stars, avgRating, checkins FROM business WHERE ispopular = TRUE AND state_name = '" + state + "' AND city_name = '" + city + "' AND zip = '" + zip + "' ORDER BY business_name;"
                popResults = self.execQuery(sql_str)

                sql_str = "SELECT medianIncome, avgIncome, population FROM zipdata WHERE zipcode = '" + zip + "';"
                zipResults = self.execQuery(sql_str)

                # set zipcode statistics
                self.ui.avgIncome.setText(str(zipResults[0][1]))
                self.ui.population.setText(str(zipResults[0][2]))
                self.ui.busiNo.setText(str(zipResults[0][0]))

                self.ui.busiTable.setColumnCount(len(results[0]))
                self.ui.busiTable.setRowCount(len(results))

                self.ui.busiTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'Stars', 'Average Score', 'Review Count', 'Checkins'])
                self.ui.busiTable.resizeColumnsToContents()
                self.ui.busiTable.setColumnWidth(0, 200)
                self.ui.busiTable.setColumnWidth(1, 200)
                self.ui.busiTable.setColumnWidth(2, 100)
                self.ui.busiTable.setColumnWidth(3, 100)
                self.ui.busiTable.setColumnWidth(4, 100)
                self.ui.busiTable.setColumnWidth(5, 100)
                
                 # format successful businesses table
                self.ui.succTable.setColumnCount(2)
                self.ui.succTable.setRowCount(len(succResults))
                self.ui.succTable.setHorizontalHeaderLabels(['Business Name', 'Checkins'])
                self.ui.succTable.resizeColumnsToContents()
                self.ui.succTable.setColumnWidth(0, 200)
                self.ui.succTable.setColumnWidth(1, 50)

                # format popular businesses table
                self.ui.popTable.setColumnCount(4)
                self.ui.popTable.setRowCount(len(popResults))
                self.ui.popTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Average Score', 'Checkins'])
                self.ui.popTable.resizeColumnsToContents()
                self.ui.popTable.setColumnWidth(0, 200)
                self.ui.popTable.setColumnWidth(1, 50)
                self.ui.popTable.setColumnWidth(2, 100)
                self.ui.popTable.setColumnWidth(3, 50)
                
                # add elements to businesses table
                currentRowCount = 0
                for row in results:
                    for colCount in range (0,len(results[0])):
                        self.ui.busiTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))

                    currentRowCount += 1

                # add elements to success table
                currentRowCount = 0
                for row in succResults:
                    self.ui.succTable.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                    self.ui.succTable.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))
                    currentRowCount += 1

                # add elements to popular table
                currentRowCount = 0
                for row in popResults:
                    self.ui.popTable.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                    self.ui.popTable.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))
                    self.ui.popTable.setItem(currentRowCount, 2, QTableWidgetItem(str(row[2])))
                    self.ui.popTable.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    currentRowCount += 1

                self.ui.catList.clear()

            except:
                print('Business query failed')

            # update categories List
            sql_str = "SELECT distinct categories.category FROM business INNER JOIN categories ON business.bid = categories.business_id WHERE business.zip = " + "'" + zip + "'" + "ORDER BY categories.category"
            self.ui.catList.clear()

            try:
                results = self.execQuery(sql_str)
                
                for x in results:
                    self.ui.catList.addItem(x[0])

            except:
                print('Error getting categories for zipcode')

    def categoryChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0) and len(self.ui.catList.selectedItems()) > 0:

            zip = self.ui.zipList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            category = self.ui.catList.selectedItems()[0].text()

            try:
                sql_str = "SELECT distinct categories.category, business_name, business_address, CAST(stars AS FLOAT), CAST(avgRating AS FLOAT), numReviews, checkins FROM business INNER JOIN categories on business.bid = categories.business_id WHERE state_name = '" + state + "' AND city_name = '" + city + "' AND zip = '" + zip + "' AND categories.category ='" + category + "' ORDER BY business_name;"
                results = self.execQuery(sql_str)

                sql_str = "SELECT business_name, checkins FROM business INNER JOIN categories on business.bid = categories.business_id WHERE issuccessful = TRUE AND state_name = '" + state + "' AND city_name = '" + city + "' AND zip = '" + zip + "' AND categories.category = '" + self.cleanStr4SQL(category) + "' ORDER BY business_name;"
                succResults = self.execQuery(sql_str)

                sql_str = "SELECT business_name, stars, avgRating, checkins FROM business INNER JOIN categories on business.bid = categories.business_id WHERE ispopular = TRUE AND state_name = '" + state + "' AND city_name = '" + city + "' AND zip = '" + zip + "' AND categories.category = '" + self.cleanStr4SQL(category) + "'ORDER BY business_name;"
                popResults = self.execQuery(sql_str)

            except:
                print('One or more queries failed on category change.')

            if len(results) > 0:
                self.ui.busiTable.setColumnCount(len(results[0]) - 1)
                self.ui.busiTable.setRowCount(len(results))

                self.ui.busiTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'Stars', 'Average Score', 'Review Count', 'Checkins'])
                self.ui.busiTable.resizeColumnsToContents()
                self.ui.busiTable.setColumnWidth(0, 200)
                self.ui.busiTable.setColumnWidth(1, 200)
                self.ui.busiTable.setColumnWidth(2, 100)
                self.ui.busiTable.setColumnWidth(3, 100)
                self.ui.busiTable.setColumnWidth(4, 100)
                self.ui.busiTable.setColumnWidth(5, 100)

                # format successful businesses table
                self.ui.succTable.setColumnCount(2)
                self.ui.succTable.setRowCount(len(succResults))
                self.ui.succTable.setHorizontalHeaderLabels(['Business Name', 'Checkins'])
                self.ui.succTable.resizeColumnsToContents()
                self.ui.succTable.setColumnWidth(0, 200)
                self.ui.succTable.setColumnWidth(1, 50)

                # format popular businesses table
                self.ui.popTable.setColumnCount(4)
                self.ui.popTable.setRowCount(len(popResults))
                self.ui.popTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Average Score', 'Checkins'])
                self.ui.popTable.resizeColumnsToContents()
                self.ui.popTable.setColumnWidth(0, 200)
                self.ui.popTable.setColumnWidth(1, 50)
                self.ui.popTable.setColumnWidth(2, 100)
                self.ui.popTable.setColumnWidth(3, 50)
                
                # add elements to businesses table
                currentRowCount = 0
                for row in results:
                    for colCount in range (1,len(results[0])):
                        self.ui.busiTable.setItem(currentRowCount, colCount - 1, QTableWidgetItem(str(row[colCount])))

                    currentRowCount += 1

                # add elements to success table
                currentRowCount = 0
                for row in succResults:
                    self.ui.succTable.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                    self.ui.succTable.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))
                    currentRowCount += 1

                # add elements to popular table
                currentRowCount = 0
                for row in popResults:
                    self.ui.popTable.setItem(currentRowCount, 0, QTableWidgetItem(str(row[0])))
                    self.ui.popTable.setItem(currentRowCount, 1, QTableWidgetItem(str(row[1])))
                    self.ui.popTable.setItem(currentRowCount, 2, QTableWidgetItem(str(row[2])))
                    self.ui.popTable.setItem(currentRowCount, 3, QTableWidgetItem(str(row[3])))
                    currentRowCount += 1


    def getBusinessNames(self):
        self.ui.businesses.clear()
        businessname = self.ui.bname.text()

        if "'" in businessname: # deals with businessnames that have apostrophes
                temp = businessname.split("'")
                for i in range(0, len(temp)-1):
                    temp[i] = temp[i] + "''"

                businessname = ''.join(temp)  

        sql_str = "SELECT business_name FROM business WHERE business_name LIKE '%" + businessname + "%' ORDER BY business_name;"

        try:
            results = self.execQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("Search query failed")

    def displayBusinessCity(self):
        if len(self.ui.businesses.selectedItems()) > 0:
            businessname = self.ui.businesses.selectedItems()[0].text()
            
            if "'" in businessname:
                temp = businessname.split("'")
                for i in range(0, len(temp)-1):
                    temp[i] = temp[i] + "''"

                businessname = ''.join(temp)                  

            sql_str = "SELECT city_name FROM business WHERE business_name = '" + businessname + "';"
            
            try:
                results = self.execQuery(sql_str)
                print(results)
                self.ui.bcity.setText(results[0][0])
            except:
                print("City Display query failed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())