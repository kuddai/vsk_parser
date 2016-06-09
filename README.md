# Joint animation problems
run the following command to see animation of skeleton joints from Ruslan.vsk file and "Ruslan Cal 03.csv":

    python vicon_anim_parser/src/vicon_anim_convertor.py Ruslan.vsk "Ruslan Cal 03.csv"

It starts from 500 frame in order to skip T pose (can be changed by setting STARTING_FRAME in vicon_anim_convertor.py).
It starts correctly  but then it shows very odd behaviour. It swings along y axis most notably 
starting from 1000 frame.
I have checked original "Ruslan Cal 03.csv" file and it truly confirms that 
global Free joint which is root of skeleton (World_Hips) has big rotation component along y axis 
(variation from -20 to 30 degrees which is a lot!). It can be checked by selecting frames lines 
1000, 1200, 1400 from original csv file and using 

    def glob_rotation(line):
        a = s.split(",")
        print a[-12:-9]

At the same time if we use command to display markers:

    python vicon_anim_parser/src/csv_markers_shower.py "Ruslan Cal 03.csv"
    
Then everything seems to work fine except for some marker disappearance due to occlusion.

Also for example the universal joint "LeftArm_LeftForeArm" (responsible for elbow) can have negative angles
for both of its axis which shouldn't be possible because we can't bend our arm in negative direction:

    def show_LeftArm_LeftForeArm_DOFs(line):
        terms = line.split(",")
        print terms[12:14]
        
Apply it for frame 2833 of "Ruslan Cal 03.csv" to see this. Or just copy this line from here:

    2833,0,,-8.1701,25.6175,18.803,-23.2891,5.81567,4.62622,-4.89712,-8.20922,-5.39868,-40.0206,-114.35,-17.8801,-11.783,-17.6426,,,0,0,-3.98894,5.28708,-13.936,71.2905,8.22028,-123.245,,19.538,23.1561,-379.637,-40.4784,-16.8236,-76.658,,,0,0,11.0729,3.38716,-6.69714,59.9004,39.5392,8.37265,,32.2315,22.0451,17.6023,30.5434,38.1072,10.6972,-14.6668,0.540473,-7.4077,12.7571,-96.3395,37.96,177.518,-17.4998,-103.272,975.3,67.1142,-82.0522,-2.33946,715.903,211.034,1330.16
    
How can arm bend in reverse direction (check axis in the LeftArm_LeftForeArm vsk joint)?


Additionally names of the joints can be viewed via:

    python vicon_anim_parser/src/vsk_parser.py Ruslan.vsk