import sys
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtGui import QMovie
import csv



# 'StockInfo' page
class StockInfo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data = parent.data

        self.setWindowTitle("Stock Trade Calculator")
        self.resize(900,650)

        # Page title
        #title1
        self.stockInfoTitle1 = QLabel("Stock Information", self)
        self.stockInfoTitle1.setObjectName("stockInfoTitle1")
        self.stockInfoTitle1.setGeometry(325, 10, 400, 55)

        #title2
        self.stockInfoTitle2 = QLabel("Select the Stock you want to view: ", self)
        self.stockInfoTitle2.setObjectName("stockInfoTitle2")
        self.stockInfoTitle2.setGeometry(50, 100, 400, 55)

        # Create stock selection box
        self.stockComboBox = QComboBox(self)
        self.stockComboBox.addItems(sorted(self.data.keys()))
        self.stockComboBox.setGeometry(450, 105, 200, 35)

        # Latest Price layout
        self.latestPriceContainer = QWidget(self)
        self.latestPriceContainer.setGeometry(50, 150, 200, 75)

        self.latestPriceLayout = QVBoxLayout(self.latestPriceContainer)
        self.latestPriceLayout.setContentsMargins(0, 0, 0, 0)
        self.latestPriceLayout.setSpacing(0)

        self.stockInfoTitle3 = QLabel("Latest Price: ", self.latestPriceContainer)
        self.stockInfoTitle3.setObjectName("stockInfoTitle3")
        self.stockInfoTitle3.setFixedSize(200, 40)

        self.latestPriceLayout.addWidget(self.stockInfoTitle3)

        # Highest Price layout (title4)
        self.highestPriceContainer = QWidget(self)
        self.highestPriceContainer.setGeometry(320, 150, 200, 75)

        self.highestPriceLayout = QVBoxLayout(self.highestPriceContainer)
        self.highestPriceLayout.setContentsMargins(0, 0, 0, 0)
        self.highestPriceLayout.setSpacing(0)

        self.stockInfoTitle4 = QLabel("Highest Price: ", self.highestPriceContainer)
        self.stockInfoTitle4.setObjectName("stockInfoTitle4")
        self.stockInfoTitle4.setFixedSize(200, 40)

        self.highestPriceLayout.addWidget(self.stockInfoTitle4)

        self.highestPriceValue = QLabel("--", self.highestPriceContainer)
        self.highestPriceValue.setObjectName("highestPriceValue")
        self.highestPriceValue.setFixedSize(200, 35)

        self.highestPriceLayout.addWidget(self.highestPriceValue)


        #title5
        # Lowest Price layout
        self.lowestPriceContainer = QWidget(self)
        self.lowestPriceContainer.setGeometry(600, 150, 200, 75)

        self.lowestPriceLayout = QVBoxLayout(self.lowestPriceContainer)
        self.lowestPriceLayout.setContentsMargins(0, 0, 0, 0)
        self.lowestPriceLayout.setSpacing(0)

        self.stockInfoTitle5 = QLabel("Lowest Price: ", self.lowestPriceContainer)
        self.stockInfoTitle5.setObjectName("stockInfoTitle5")
        self.stockInfoTitle5.setFixedSize(200, 40)

        self.lowestPriceLayout.addWidget(self.stockInfoTitle5)

        self.lowestPriceValue = QLabel("--", self.lowestPriceContainer)
        self.lowestPriceValue.setObjectName("lowestPriceValue")
        self.lowestPriceValue.setFixedSize(200, 35)

        self.lowestPriceLayout.addWidget(self.lowestPriceValue)



        # Display stock prices
        self.latestPriceValue = QLabel("--", self.latestPriceContainer)
        self.latestPriceValue.setObjectName("latestPriceValue")
        self.latestPriceValue.setFixedSize(200, 35)

        self.latestPriceLayout.addWidget(self.latestPriceValue)

        #title6
        self.stockInfoChart = QLabel("Historical Price Chart: ", self)
        self.stockInfoChart.setObjectName("stockInfoChart")
        self.stockInfoChart.setGeometry(50, 230,400,120)

        # Create a figure for the stock price chart
        self.figure = Figure(figsize=(6, 2))

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(265, 280, 550, 200)

        #title7
        self.stockInfoTitle7 = QLabel("Price Statistics: ", self)
        self.stockInfoTitle7.setObjectName("stockInfoTitle7")
        self.stockInfoTitle7.setGeometry(350, 510, 400, 55)

        # Display price statistics
        self.averagePriceValue = QLabel("--", self)
        self.averagePriceValue.setObjectName("averagePriceValue")
        self.averagePriceValue.setGeometry(630, 520, 200, 30)

        self.totalRecordsValue = QLabel("--", self)
        self.totalRecordsValue.setObjectName("totalRecordsValue")
        self.totalRecordsValue.setGeometry(630, 545, 200, 30)

        self.dateRangeValue = QLabel("--", self)
        self.dateRangeValue.setObjectName("dateRangeValue")
        self.dateRangeValue.setGeometry(630, 570, 240, 30)

        #title8
        self.stockInfoTitle8 = QLabel("Average Price: ", self)
        self.stockInfoTitle8.setObjectName("stockInfoTitle8")
        self.stockInfoTitle8.setGeometry(520, 510, 400, 55)

        #title9
        self.stockInfoTitle9 = QLabel("Total Records: ", self)
        self.stockInfoTitle9.setObjectName("stockInfoTitle9")
        self.stockInfoTitle9.setGeometry(518, 535, 400, 55)

        #title10
        self.stockInfoTitle10 = QLabel("Data Range: ", self)
        self.stockInfoTitle10.setObjectName("stockInfoTitle10")
        self.stockInfoTitle10.setGeometry(518, 560, 400, 55)

        self.stockComboBox.currentTextChanged.connect(self.update_stock_info)
        self.update_stock_info()

    # Add a new method for 'stockInfo' page
    def update_stock_info(self):
        stock = self.stockComboBox.currentText()

        stock_data = self.data[stock]

        self.update_chart(stock)

        prices = []
        valid_dates = []

        for date, price in stock_data.items():
            if price > 0:
                prices.append(price)
                valid_dates.append(date)

        if prices:
            latest_date = sorted(stock_data.keys())[-1]
            latest_price = stock_data[latest_date]

            highest_price = max(prices)
            lowest_price = min(prices)

            average_price = sum(prices) / len(prices)

            total_records = len(prices)

            first_date = min(valid_dates)
            last_date = max(valid_dates)

            date_range = (
                f"{first_date[2]:02d}/{first_date[1]:02d}/{first_date[0]} - "
                f"{last_date[2]:02d}/{last_date[1]:02d}/{last_date[0]}"
            )

            self.latestPriceValue.setText(f"{latest_price:.2f}")
            self.highestPriceValue.setText(f"{highest_price:.2f}")
            self.lowestPriceValue.setText(f"{lowest_price:.2f}")

            self.averagePriceValue.setText(f"{average_price:.2f}")
            self.totalRecordsValue.setText(str(total_records))
            self.dateRangeValue.setText(date_range)

    def update_chart(self, stock):
        stock_data = self.data[stock]

        valid_dates = []
        prices = []

        for date, price in stock_data.items():
            if price > 0:
                valid_dates.append(datetime(date[0], date[1], date[2]))
                prices.append(price)

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        ax.plot(valid_dates, prices, color="black")

        ax.set_title(f"{stock} Historical Price")
        ax.set_xlabel("Year")
        ax.set_ylabel("Price")

        # Add a grid layout to the line chart
        ax.minorticks_on()
        ax.grid(True, which="major", color="#D1D5DB", linestyle="-", linewidth=0.7)
        ax.grid(True, which="minor", color="#E5E7EB", linestyle=":", linewidth=0.5)

        # Remove the top and right borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

        self.figure.tight_layout()
        self.canvas.draw()

# 'About' page
class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.resize(1400, 700)
        layout = QVBoxLayout(self)

        # Create a 'dashboard' title
        self.aboutTitle1 = QLabel("About", self)
        self.aboutTitle1.setObjectName("aboutTitle1")

        self.aboutTitle1.setGeometry(700, 10, 300, 50)

        # Create a title2
        self.aboutTitle2 = QLabel("You can scroll down using the mouse.", self)
        self.aboutTitle2.setObjectName("aboutTitle2")

        self.aboutTitle2.setGeometry(300, 10, 500, 80)

        # Add a multi-line text box for the introduction.
        self.aboutText = QTextEdit(self)
        self.aboutText.setObjectName("aboutText")
        self.aboutText.setGeometry(240, 60, 1100, 600)

        self.aboutText.setPlainText("""(Ⅰ). Application Overview
This software, titled "Stock Trade Profit Calculator," is designed to help users calculate the costs, sale values, and resulting profits or losses from stock trades. It was developed using Python and the PyQt6 framework.

(Ⅱ). Features
The software consists of three main interfaces. The primary interface includes a "Dashboard," a "Trade Calculator," and a "Page Navigation" section. The "Trade Calculator" offers the following functions:
1. Stock selection (Amazon, Apple, Microsoft, Google).
2. Input for the number of shares purchased.
3. Selection of purchase and sale dates.
4. Automatic calculation of the total purchase cost.
5. Automatic calculation of the total sale value.
6. Display of the final profit or loss.
The "Page Navigation" section allows users to switch to other screens, specifically the "Stock Info" and "About" pages.
The "Stock Info" interface provides the following features:
1. Viewing historical prices for various stocks.
2. A historical price line chart.
3. The latest available price.
4. High and low price points.
5. Average price, the number of data records, and the date range.

(Ⅲ). Dataset and Purpose
1.Data Source:
The application utilizes a CSV dataset of historical stock prices provided by a Griffith College course.
2.Data Usage:
The data is processed to retrieve stock prices for specific dates, supporting both the calculation of trade profits/losses and the generation of historical price charts.
3.Design Objective:
The goal was to create an application that is user-friendly and features a diverse visual design. The background imagery was created by the developer—hand-drawn on an iPad and subsequently integrated into the software via Python. Additionally, certain icons and GIFs were sourced from free, publicly available online resources. The application aims to help users track stock price fluctuations and quickly determine the outcomes of their trades.
""")

        self.aboutText.setReadOnly(True)

        # Gif1
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(10, 50, 256, 256)

        self.movie = QMovie("Assets/confused.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()



# Main Page
class StockTradeProfitCalculator(QDialog):


    def __init__(self):
        super().__init__()

    # Add logic for GIFs
        # Gif1
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(10, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif2
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(110, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif3
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(210, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif4
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(320, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif5
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(430, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif6
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(540, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif7
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(640, 300, 128, 128)

        self.movie = QMovie("Assets/kuzu420-dancing-27562_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif8
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(750, 300, 128, 128)

        self.movie = QMovie("Assets/pikura-star-20750_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif9
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(860, 300, 128, 128)

        self.movie = QMovie("Assets/pikura-star-20750_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif10
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(970, 300, 128, 128)

        self.movie = QMovie("Assets/pikura-star-20750_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif11
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(1080, 300, 128, 128)

        self.movie = QMovie("Assets/pikura-star-20750_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif11
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(1080, 300, 128, 128)

        self.movie = QMovie("Assets/pikura-star-20750_128.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif12
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(50, 60, 256, 256)

        self.movie = QMovie("Assets/statistic1.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif13
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(350, 60, 256, 256)

        self.movie = QMovie("Assets/statistic2.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif14
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(650, 60, 256, 191)

        self.movie = QMovie("Assets/statistic3.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif15
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(650, 140, 256, 191)

        self.movie = QMovie("Assets/statistic4.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()

        # Gif16
        self.gifLabel = QLabel(self)
        self.gifLabel.setGeometry(900, 70, 256, 191)

        self.movie = QMovie("Assets/statistic5.gif")
        self.gifLabel.setMovie(self.movie)
        self.movie.start()



        with open("style.css", "r", encoding="utf-8") as file:
          self.setStyleSheet(file.read())

        # Format of the design window
        self.resize(1200,750)
        self.move(170,20)
        self.setWindowTitle("Stock Trade Profit Calculator")

        # Load font
        font_id = QFontDatabase.addApplicationFont(
            "Assets/Fonts/Caveat-VariableFont_wght.ttf"
)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # Create a 'dashboard' title
        self.titleLabel1 = QLabel("Dashboard", self)
        self.titleLabel1.setObjectName("titleLabel1")

        # Create a 'Trade Calculator' title
        self.titleLabel2 = QLabel("Trade Calculator", self)
        self.titleLabel2.setObjectName("titleLabel2")

        # Create a 'Page Transfer' title
        self.titleLabel3 = QLabel("Page Transfer", self)
        self.titleLabel3.setObjectName("titleLabel3")

    

        # Dashboard - top centre
        self.titleLabel1.setGeometry(538, 5, 300, 50)
        

        # Trade Calculator - lower left section
        self.titleLabel2.setGeometry(190, 408, 400, 45)
        self.titleLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Page Transfer - lower right section
        self.titleLabel3.setGeometry(820, 408, 300, 45)
        self.titleLabel3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the first window borderline
        self.borderLine1 = QFrame(self)
        self.borderLine1.setObjectName('borderLine1')
        self.borderLine1.setGeometry(0,0,1200,4)

        self.borderLine1.setFrameShape(QFrame.Shape.HLine)

        # Create the second window borderline
        self.borderLine2 = QFrame(self)
        self.borderLine2.setObjectName('borderLine2')
        self.borderLine2.setGeometry(0,742,1200,4)

        self.borderLine2.setFrameShape(QFrame.Shape.HLine)

        # Create the third window border line
        self.borderLine3 = QFrame(self)
        self.borderLine3.setObjectName('borderLine3')
        self.borderLine3.setGeometry(0, 0, 4, 750)

        self.borderLine3.setFrameShape(QFrame.Shape.VLine)

        # Create the fourth window border line
        self.borderLine4 = QFrame(self)
        self.borderLine4.setObjectName('borderLine4')
        self.borderLine4.setGeometry(1192,0,4,750)

        self.borderLine4.setFrameShape(QFrame.Shape.VLine)



        # Add a divider line (horizontal)
        self.horizontalLine = QFrame(self)
        self.horizontalLine.setObjectName("horizontalLine")
        self.horizontalLine.setGeometry(0,410,1200,2)

        self.horizontalLine.setFrameShape(QFrame.Shape.HLine)

        # Add a divider line (horizontal)_under_the_'Trade Calculator'
        self.horizontalLine = QFrame(self)
        self.horizontalLine.setObjectName("horizontalLine2")
        self.horizontalLine.setGeometry(100,455,540,1)
        
        self.horizontalLine.setFrameShape(QFrame.Shape.HLine)

        # Add a divider line (horizontal)_under_the_'Page Transfer'
        self.horizontalLine = QFrame(self)
        self.horizontalLine.setObjectName("horizontalLine3")
        self.horizontalLine.setGeometry(800,455,340,1)

        # Add a divider line (horizontal)_under_the_'Dashboard'
        self.horizontalLine = QFrame(self)
        self.horizontalLine.setObjectName("horizontalLine4")
        self.horizontalLine.setGeometry(180,53,850,1)

        # Add a divider line (vertical)
        self.verticalLine = QFrame(self)
        self.verticalLine.setObjectName("verticalLine")
        self.verticalLine.setGeometry(720,410,2,400)

        self.verticalLine.setFrameShape(QFrame.Shape.VLine)

        

        # Create a rectangular container (used to represent 'stock info')
        self.calculatorFrame = QFrame(self)
        self.calculatorFrame.setObjectName("calculatorFrame1")
        self.calculatorFrame.setGeometry(1024,480,150,125)

        # Create a rectangular container (used to represent 'About info')
        self.calculatorFrame = QFrame(self)
        self.calculatorFrame.setObjectName("calculatorFrame2")
        self.calculatorFrame.setGeometry(1024,615,150,125)

        # Add an 'About' image
        self.imageLabel = QLabel(self)

        self.imageLabel.setGeometry(1058, 615, 80, 80)

        pixmap = QPixmap("Assets/about-svgrepo-com.svg")

        self.imageLabel.setPixmap(pixmap)

        self.imageLabel.setScaledContents(True)
        # Add a navigation button for the "About" page
        self.aboutButton =QPushButton("About", self)
        self.aboutButton.setObjectName("aboutButton")
        #When the user clicks the About button, the open_about_page method is called.
        self.aboutButton.clicked.connect(self.open_about_page)

        self.aboutButton.setGeometry(1070, 712, 60, 22)

        # Add an 'Stock_Info' image
        self.imageLabel = QLabel(self)
        
        self.imageLabel.setGeometry(1058, 480, 80, 80)
        
        pixmap = QPixmap("Assets/book-svgrepo-com.svg")
        
        self.imageLabel.setPixmap(pixmap)
        
        self.imageLabel.setScaledContents(True)
        # Add a navigation button for the "stockInfo" page
        self.stockInfoButton = QPushButton("stockInfo", self)
        self.stockInfoButton.setObjectName("stockInfoButton")
        self.stockInfoButton.setGeometry(1070, 575, 60, 22)
        # Add click logic for stockInfo
        self.stockInfoButton.clicked.connect(self.open_stock_info)

        # Contents of the 'Trade Calculator'
        self.TC_Content1 = QLabel("Stock Selection:", self)
        self.TC_Content1.setObjectName("TC_Content1")
         
        # Create a 'Trade Calculator' title
        self.TC_Content2 = QLabel("Quantity:", self)
        self.TC_Content2.setObjectName("TC_Content2")
         
        # Create a 'Page Transfer' title
        self.TC_Content3 = QLabel("Purchase Date:", self)
        self.TC_Content3.setObjectName("TC_Content3")

        # Create a 'Sell Date' title
        self.TC_Content4 = QLabel("Sell Date:", self)
        self.TC_Content4.setObjectName("TC_Content4")

        # Create the instruction1 for 'Stock Info'
        self.instruction1 = QLabel("Clicking this will take you to the 'stock ", self)
        self.instruction1.setObjectName("instruction1")

        # Create the instruction2 for 'Stock Info'
        self.instruction2 = QLabel("info' page, which displays basic details,", self)
        self.instruction2.setObjectName("instruction2")

        # Create the instruction3 for 'Stock Info'
        self.instruction3 = QLabel("'historical prices, and relevant market", self)
        self.instruction3.setObjectName("instruction3")

        # Create the instruction4 for 'Stock Info'
        self.instruction4 = QLabel("'data for each stock in the dataset.", self)
        self.instruction4.setObjectName("instruction4")


        # Create the instruction5 for 'About'
        self.instruction5 = QLabel("Clicking this will take you to the 'About'", self)
        self.instruction5.setObjectName("instruction5")
        
        # Create the instruction6 for 'About'
        self.instruction6 = QLabel("page, which displays the features, purpose,", self)
        self.instruction6.setObjectName("instruction6")
        
        # Create the instruction7 for 'About'
        self.instruction7 = QLabel("and developer information for the Stock", self)
        self.instruction7.setObjectName("instruction7")
        
        # Create the instruction8 for 'About'
        self.instruction8 = QLabel("Trade Profit Calculator.", self)
        self.instruction8.setObjectName("instruction8")

        # Create the display1
        self.display1 = QLabel("Purchase Total:", self)
        self.display1.setObjectName("display1")

        # Create the display2
        self.display2 = QLabel("Sell Total:", self)
        self.display2.setObjectName("display2")

        # Create the display3
        self.display3 = QLabel("Profit/Loss:", self)
        self.display3.setObjectName("display3")
        # Create labels for calculation results
        self.purchaseTotalValue = QLabel("0.00", self)
        self.sellTotalValue = QLabel("0.00", self)
        self.profitLossValue = QLabel("0.00", self)

        self.purchaseTotalValue.setObjectName("purchaseTotalValue")
        self.sellTotalValue.setObjectName("sellTotalValue")
        self.profitLossValue.setObjectName("profitLossValue")

        # 'About' Title
        self.about = QLabel("About", self)
        self.about.setObjectName("about")

        # 'Stock Info' Title
        self.stockinfo = QLabel("Stock Info", self)
        self.stockinfo.setObjectName("stockinfo")

             
         
        # position of 'Stock Selection'
        self.TC_Content1.setGeometry(40, 460, 300, 50)
                 
         
        # position of 'Quantity'
        self.TC_Content2.setGeometry(40, 520, 400, 45)
         
        # position of 'Purchase Date'
        self.TC_Content3.setGeometry(360, 460, 300, 45)

        # position of 'Sell Date'
        self.TC_Content4.setGeometry(360, 520, 300, 45)

        # position of 'instruction1'
        self.instruction1.setGeometry(730, 470, 300, 45)

        # position of 'instruction2'
        self.instruction2.setGeometry(730, 495, 300, 45)

        # position of 'instruction3'
        self.instruction3.setGeometry(730, 520, 300, 45)

        # position of 'instruction4'
        self.instruction4.setGeometry(730, 545, 300, 45)

        # position of 'instruction5'
        self.instruction5.setGeometry(730, 595, 300, 45)

        # position of 'instruction6'
        self.instruction6.setGeometry(730, 620, 300, 45)

        # position of 'instruction7'
        self.instruction7.setGeometry(730, 645, 300, 45)

        # position of 'instruction7'
        self.instruction8.setGeometry(730, 670, 300, 45)

        # position of 'about'
        self.about.setGeometry(1070, 680, 300, 45)

        # position of 'stockinfo'
        self.stockinfo.setGeometry(1050, 540, 300, 45)

        # position of 'display1'
        self.display1.setGeometry(40, 590, 300, 45)

        # position of 'display2'
        self.display2.setGeometry(40, 630, 300, 45)

        # position of 'display3'
        self.display3.setGeometry(40, 670, 300, 45)
        # Position of calculation result labels
        self.purchaseTotalValue.setGeometry(260, 590, 180, 45)
        self.sellTotalValue.setGeometry(260, 630, 180, 45)
        self.profitLossValue.setGeometry(260, 670, 180, 45)


        # Create a QComboBox after 'Stock Selection' (It allows users to select a stock name)
        self.stockComboBox = QComboBox(self)

        self.stockComboBox.addItems([
            "Amazon",
            "Apple",
            "Microsoft",
            "Google"
])

        self.stockComboBox.setGeometry(196, 466, 150, 38)

        # Create a QLineEdit after 'Quantity'
        self.priceInput = QLineEdit(self)

        self.priceInput.setPlaceholderText("Enter quantity")

        self.priceInput.setGeometry(135, 526, 180, 38)

        # Create a Purchase Date calendar
        self.purchaseDateEdit = QDateEdit(self)
        self.purchaseDateEdit.setCalendarPopup(True)
        self.purchaseDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.purchaseDateEdit.setGeometry(510, 466, 180, 38)

        # Create a Sell Date calendar
        self.sellDateEdit = QDateEdit(self)
        self.sellDateEdit.setCalendarPopup(True)
        self.sellDateEdit.setDisplayFormat("dd/MM/yyyy")
        self.sellDateEdit.setGeometry(510, 526, 180, 38)

        self.purchaseDateEdit.setDate(QDate.currentDate())
        self.sellDateEdit.setDate(QDate.currentDate())































        # setting up dictionary of Stocks
        self.data = self.make_data()

      # Set the default dates
        # And Correct the date
        if 'Amazon' in self.data and self.data['Amazon']:
            self.sellCalendarDefaultDate = sorted(self.data['Amazon'].keys())[-1]

            self.sellDateEdit.setDate(QDate(*self.sellCalendarDefaultDate))

            self.purchaseDateEdit.setDate(
                self.sellDateEdit.date().addDays(-14)
            )
        else:
            print("Amazon not found in the dataset.")
            self.sellDateEdit.setDate(QDate.currentDate())
            self.purchaseDateEdit.setDate(
            self.sellDateEdit.date().addDays(-14)

            )
        print("Latest Amazon date:", self.sellCalendarDefaultDate)
        print("Purchase date:", self.purchaseDateEdit.date().toString("dd/MM/yyyy"))
        print("Sell date:", self.sellDateEdit.date().toString("dd/MM/yyyy"))


        # Connect controls to updateUi
        self.stockComboBox.currentTextChanged.connect(self.updateUi)
        self.priceInput.textChanged.connect(self.updateUi)
        self.purchaseDateEdit.dateChanged.connect(self.updateUi)
        self.sellDateEdit.dateChanged.connect(self.updateUi)

        self.updateUi()

    # open_about_page
    def open_about_page(self):
        self.about_window = About(self)
        self.about_window.setStyleSheet(self.styleSheet())
        self.about_window.show()

    # open_stock_info
    def open_stock_info(self):
        self.stock_info_window = StockInfo(self)
        self.stock_info_window.setStyleSheet(self.styleSheet())
        self.stock_info_window.show()

    def updateUi(self):

        try:
            # Get selected stock and dates
            stock = self.stockComboBox.currentText()

            purchase_date = self.purchaseDateEdit.date()
            sell_date = self.sellDateEdit.date()

            #Check whether the purchase date is later than the sale date.
            if purchase_date > sell_date:
                self.purchaseTotalValue.setText("N/A")
                self.sellTotalValue.setText("N/A")
                self.profitLossValue.setText("N/A")
                print("Purchase date cannot be later than sell date.")
                return


            purchase_key = (
                purchase_date.year(),
                purchase_date.month(),
                purchase_date.day()
            )

            sell_key = (
                sell_date.year(),
                sell_date.month(),
                sell_date.day()
            )

            # Get stock prices
            purchase_price = self.data[stock].get(purchase_key)
            sell_price = self.data[stock].get(sell_key)

            # Check if prices are available
            if purchase_price is None or sell_price is None or purchase_price <= 0 or sell_price <= 0:
                self.purchaseTotalValue.setText("N/A")
                self.sellTotalValue.setText("N/A")
                self.profitLossValue.setText("N/A")

                print("No stock price available for the selected date.")
                return

            # Get quantity
            quantity_text = self.priceInput.text()

            if not quantity_text.isdigit() or int(quantity_text) <= 0:
                self.purchaseTotalValue.setText("N/A")
                self.sellTotalValue.setText("N/A")
                self.profitLossValue.setText("N/A")

                print("Please enter a valid quantity.")
                return

            quantity = int(quantity_text)

            # Calculate totals
            purchase_total = purchase_price * quantity
            sell_total = sell_price * quantity
            profit_loss = sell_total - purchase_total

            # Update calculation results on the dashboard
            self.purchaseTotalValue.setText(f"{purchase_total:.2f}")
            self.sellTotalValue.setText(f"{sell_total:.2f}")
            self.profitLossValue.setText(f"{profit_loss:.2f}")

            print("Selected stock:", stock)
            print("Purchase price:", purchase_price)
            print("Sell price:", sell_price)


        except Exception as error:
            print(f"Error in updateUi: {error}")

    def make_data(self):
        '''
        This code reads the stock market CSV file and generates a dictionary structure.
        :return: a dictionary of dictionaries
        '''
        data = {}

        try:
            with open('Stock_Market_Dataset.csv', mode='r') as file:
                reader = csv.DictReader(file)
                stock_names = reader.fieldnames[1:]  # All columns except 'Date' are stock names

                for row in reader:
                    date_string = row['Date']
                    date_tuple = self.string_date_into_tuple(date_string)

                    for stock in stock_names:
                        price = row[stock].replace(',', '')
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0

                        if stock not in data:
                            data[stock] = {}

                        data[stock][date_tuple] = price

            print("Data loaded successfully.")
            print(f"Stocks available: {stock_names}")  # Debugging: Print all available stock names

        except Exception as error:
            print(f"Error reading data: {error}")
        return data

    def string_date_into_tuple(self, date_string):
        '''
        Converts a date in string format (e.g., "02-02-2024") into a tuple (year, month, day).
        :return: tuple representing the date
        '''
        try:
            if '-' in date_string:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            else:
                date_obj = datetime.strptime(date_string, "%d/%m/%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print(f"Error parsing date: {date_string}")
            return None


# This is complete
if __name__ == '__main__':

    app = QApplication(sys.argv)
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    
    sys.exit(app.exec())



