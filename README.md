# OPENCV4.0  
# PYTHON 3.7  
# KERAS 2.2.5  
# TENSORFLOW 1.14.0  

# WE USE AN SPECIFIC VERSION OF DARKNET TO RPI THIS SHOULD NOT WORK ON OTHER SYSTEMS  
# THERE ARE SOM PROBLEMS USING TENSORFLOW > 2.0.0, we use 1.x instead.  
# none-linux_armv7l.whl Raspberry PI 2/3  
https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.14.0-buster/tensorflow-1.14.0-cp37-none-linux_armv7l.whl  
### HERE ARE SOME RELEASES OF TENSORFLOW IN WHL  
https://github.com/lhelontra/tensorflow-on-arm/releases  


# INSTALL PeachPy and confu  
pip install --upgrade git+https://github.com/Maratyszcza/PeachPy  
pip install --upgrade git+https://github.com/Maratyszcza/confu  
# INSTALL NINJA  
git clone https://github.com/ninja-build/ninja.git  
cd ninja  
git checkout release  
./configure.py --bootstrap  
export NINJA_PATH=$PWD  
# INSTALL CLANG  
sudo apt-get install clang  
# INSTALL NNPACK  
git clone https://github.com/shizukachan/NNPACK  
cd NNPACK  
confu setup  
# REPLACE file in NNPACK/src/init.c with replace/init.c  
# ADD -fPIC to cflags and cxxflags in NNPACK/build.ninja  
# AFTER DOING THAT EXCECUTE  
$NINJA_PATH/ninja  
bin/convolution-inference-smoketest  
sudo cp -a lib/* /usr/lib/  
sudo cp include/nnpack.h /usr/include/  
sudo cp deps/pthreadpool/include/pthreadpool.h /usr/include/  
cd ../  
# CLONE darknet-nnpack  
git clone https://github.com/shizukachan/darknet-nnpack  
cd darknet-nnpack  
# REPLACE Makefile with replace/Makefile  
make  
# IF libdarknet.so is generated go ahead!  


### MAIN REFERENCE  
https://github.com/shizukachan/darknet-nnpack  
### SIMILAR PROJECT THAT REACH THE GOAL USING DARKNET ON RPI  
https://github.com/NTUEE-ESLab/2017Fall-IntelligentSecurityGuard  

### ISSUES  
# THE FILE ARE ALREADY ACTUALIZED BUT HERE WE EXPLAIN SOME ISSUES  

# NNPACK error (50)  
# YOU MUST TO INITILIZE NNPACK BEFORE EACH DETECTION  
# ON darknet.py  
'''  
srand = lib.srand  
srand.argtypes = [c_int]  
nnp_initialize = lib.nnp_initialize  

#and before you call detect use this  
srand(2222222) <<--- maybe this is not necessary  
nnp_initialize()  
'''  
#REF: https://github.com/pjreddie/darknet/issues/1288  



#URLS
http://121.181.221.75/mjpg/video.mjpg
http://211.212.169.88:8000/webcapture.jpg?command=snap&channel=1?1581212360
http://114.35.51.48/webcapture.jpg?command=snap&channel=1?1581212459
http://218.50.253.35:8000/webcapture.jpg?command=snap&channel=1?0
http://114.33.79.14/webcapture.jpg?command=snap&channel=1?0
http://114.35.191.202:85/webcapture.jpg?command=snap&channel=1?1581213496
http://2.236.20.159:86/jpgmulreq/1/image.jpg?key=1516975535684&lq=1&1581269665
