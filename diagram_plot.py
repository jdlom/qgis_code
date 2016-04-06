import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
#from basic_units import cm

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)



#fig1 = plt.figure(figsize=cm2inch(9, 12))
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
#ax1.set_axis_off()
#ax1.axes.get_yaxis().set_visible(False)
#ax1.axes.get_xaxis().set_visible(False)

max_value = 1600
max_r = 5
nb_categories = 4
list_r = range(5,1,-1)
list_label = [max_value]
for i in range(1,nb_categories):
    list_label.append(list_label[-1]/2)
    
#list_r = list_r * cm
#for p in [
#    patches.Circle(
#        (max_r, r),   # (x,y)
#        r,
#        fill=False,
#        linewidth=1.5,
#        ) for r in list_r ] :
#    ax1.add_patch(p)
for index ,r in enumerate(list_r):
    
#create circle 
    ax1.add_patch(patches.Circle(
        (max_r, r),   # (x,y)
        r,
        #fill=False,
        linewidth=1.5,
        facecolor="#00ffff"
        )
    )
 #create lines
    line = [(max_r,2*r), (2.2*max_r,2*r)]
    (line_xs, line_ys) = zip(*line)
#    line_xs = line_xs * cm
#    line_ys = line_ys * cm
    ax1.add_line(lines.Line2D(line_xs, line_ys, linewidth=1.5, color='black'))
#create label
    plt.text(2.3*max_r, 2*r, list_label[index])
#create title
fig1.suptitle('bold figure suptitle', fontsize=14)
#create axe subtitle
ax1.set_title('axes title')
print(list_label)
plt.xlim(-1,3*max_r)
plt.ylim(-1,2*max_r+1)
fig1.show()