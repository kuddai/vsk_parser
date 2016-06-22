import sys
import matplotlib.pyplot as plt

def main():
    mouse_data_file_name = sys.argv[1]
    mouse_data = parse_mouse_data(mouse_data_file_name)
    plot_horizontal_data(mouse_data)

def plot_horizontal_data(mouse_data):
    xx = [r[0] for r in mouse_data]
    vx = [r[2] for r in mouse_data]
    plt.figure()
    plt.plot(xx, vx, "-*")
    plt.xlabel("Position X")
    plt.ylabel("Velocity X")
    plt.show()

def parse_mouse_data(mouseDataFileName):
    mouseData = []
    with open(mouseDataFileName) as f:
        #skip header
        f.readline()
        for line in f:
            try:
                mouseData.append(map(float, line.split(",")))
            except:
                print line
                raise ValueError("problem on " + line)
    return mouseData

if __name__ == "__main__":
    main()