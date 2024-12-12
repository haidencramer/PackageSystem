# The Package Guys

**Haiden Cramer and Eric Frazer**


Components Used: 

* Adafruit LSM6DS3TR-C 6-DoF Accel + Gyro IMU Sensor
* Adafruit BH1750 Light Sensor
* Miniature Bread Board
* Raspberry Pico 
* Raspberry Pi Zero 2W

Libraries to Install (Follow Step by Step Guide Below on Installation):

* adafruit_bh1750
* adafruit_mpu6050
* CircuitPy
* Apache (To Host Data Site Locally)

**Running this System Step by Step:**

* After obtaining all of the components listed above I will guide you through step-by-step on what you need to do in order to successfully use this system. 

* Install Light Sensor Library: 

    [Follows this git Library Demo because you need to install with Arduino](https://github.com/Starmbi/hp_BH1750)

    Click "Clone or download" -> "Download ZIP" button.

    (For Arduino >= 1.5.x) Use the way above, or Library Manager. Open Arduino IDE, click Sketch -> Include library -> Add .ZIP library  and select the downloaded archive.

    (For Arduino < 1.5.x) Extract the archive to <Your User Directory>/My Documents/Arduino/libraries/ folder and rename it to hp_BH1750. Restart IDE.

* Install Gyro/Accel/Temp Library on Rapberry Zero: pip3 install adafruit-circuitpython-mpu6050

* Install Apache and Start Server Locally with Raspberry Zero: 
    sudo apt install apache2
    sudo service apache2 start

* After ensuring all dependencies are downloaded you can now upload the light sensor reader in SourceOde/finalizedArduino titled "lightData.ino" to your Raspberry Pico. 
* From SourceCode/html Add "index.html" to a folder on your Raspberry Zero var/www/html/index.html
* Once this code has been uploaded you can now run a file in SourceCode/pythonCode/finalizedCode titled "mainProgram.py" on your Raspberry Pi Zero. 

Extra Information: 

Link to [YouTube Video](https://youtu.be/E0emrvPqTsI)