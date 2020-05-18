import numpy as np
import sys
from matplotlib import pyplot as plt
import matplotlib
import drawSvg as draw

def hilbert_plot(name, fname,score=""):
    if __name__ != '__main__' and score == "":
        raise Exception("Come on, you gotaa give me name and score!")

    for i in range(17):
            if len(score) < 4**(i):
                    break
    # Coordinates generated using hilbert_points.py -> create_hilbert(i)
    img_scale = [2**i,2**i]
    try:
        coordinates = list(np.load('./coordinates/coord_int_' + str(i) + '.npy'))
    except:
        import hilbert_points
        make_folder('coordinates')
        coordinates = hilbert_points.create_hilbert(i)
        np.save('./coordinates/coord_int_' + str(i) + '.npy', coordinates)
    range_of_coord = [int(float(i) / len(score) * (len(coordinates))) for i in range(len(score))]
    
    print(name, score[0])
    if "smina" in name:
        score = [-i for i in score]
    bar_score = [min(score), max(score)]
    score = (np.array(score) - min(score)) / max(score)
    make_hilbert(img_scale,coordinates,range_of_coord,score,fname,name)
    make_bar(fname,name, bar_score)


def make_hilbert(img_scale,coordinates,range_of_coord,score,fname,name):
    Cm = plt.get_cmap('rainbow')
    d = draw.Drawing(*img_scale)
    range_of_coord.append(len(coordinates)-1)
    coord_to_index = {}
    for i in range(len(range_of_coord)-1):
        col =matplotlib.colors.rgb2hex(Cm(score[i]))
        p = draw.Path(stroke_width=0.5,fill ="none",stroke=col)
        x = coordinates[range_of_coord[i]][0]
        y = coordinates[range_of_coord[i]][1]
        coord_to_index[str(x)+","+str(y)] = i
        p.M(x,y)
        start=range_of_coord[i]-1
        end=range_of_coord[i+1]
        for j in range(start,end):
                if j == len(coordinates):
                        break
                x = coordinates[j][0]
                y = coordinates[j][1]
                coord_to_index[str(x)+","+str(y)] = i
                p.L(x,y)
        d.append(p)
    d.setRenderSize(4096,4096)
    make_folder('./hilbert_bar')
    make_folder('./hilbert_bar/hilbert')
    make_folder('./hilbert_bar/hilbert/'+fname)
    d.savePng('./hilbert_bar/hilbert/'+fname+'/'+name+'.png')
    coord_to_index['scale'] = img_scale
    make_folder('coord_to_index')
    np.save("coord_to_index/"+fname+".npy",coord_to_index,allow_pickle=True)

def make_bar(fname,name, score):
    fig = plt.figure(figsize=(1,3))
    ax1 = fig.add_axes([0.05, 0.05, 0.3, 0.90])
    cmap = matplotlib.cm.rainbow
    ticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    if "smina" in name:
        score = [-i for i in score]
    tick_labels = ['{:.2f}'.format(i/5*score[1] + score[0]) for i in range(6)]
    
    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    cb1 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='vertical',ticks=ticks)
    cb1.set_ticklabels(ticklabels=tick_labels,update_ticks=True)
    make_folder('./hilbert_bar')
    make_folder('./hilbert_bar/bar')
    make_folder('./hilbert_bar/bar/'+fname)
    plt.savefig('./hilbert_bar/bar/'+fname+'/'+name+'.svg')
    plt.close("all")

def process_files(file):
    fname = file.split('/')[-1][:-4]
    data = np.load(file,allow_pickle=True).item()
    for i in data:
        if i in ["ids", "links", "smiles"] or "mad" in i:
            continue
        hilbert_plot(i,fname,data[i])

def make_folder(folder_path_name):
    import os
    if not os.path.isdir(folder_path_name):
        os.mkdir(folder_path_name)

if __name__ == '__main__':
    import os
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            files=[sys.argv[1]+'/'+i for i in os.listdir(sys.argv[1])]
            for file in files:
                process_files(file)
        else:
            files=[i for i in sys.argv if os.path.isfile(i) and i != __file__]
            for file in files:
                process_files(file)
    else:
        print("Don't know what to do!")
