#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv, os, sys, fileinput
import itertools

# From Red Hat and Fedora branding guidelines & colourlovers.com color palettes
COLORMAPS = {"default":('b','w')
        ,"goldfish":('#69d2e7','#a7dbd8','#eoe4cc','#f38630','#fa6900')
        ,"pancake":('#594f4f','#547980','#45ada8','#9de0ad','#e5fcc2')
        ,"thought":('#ecd078','#d95b43','#c02942','#542437','#53777a')
        ,"redhat":('#cc0000','#781f1c','#564979','#60605b')
        ,"fedora":('#3c6eb4','#db3279','#e59728','#79db32','#a07cbc')
}
def colors(name):
    for y in itertools.cycle(COLORMAPS[name]):
        yield y

def barchart(subplot,valcnt,keys,values,label=False,orient_v=True,
        label_offset=0,val_as_int=False,width=0.4,colormap="default"):

    indices = np.arange(len(keys))
    c = colors(colormap)
    for i in xrange(valcnt):
        v = [x[i] for x in values]
        if orient_v:
            if i>0:
                bars = subplot.bar(indices,v,bottom=height,color=c.next())
                height = [(x+y) for x,y in zip(height,v)]
            else:
                bars = subplot.bar(indices,v,color=c.next())
                height = list(v)
            if label:
                for i in xrange(len(bars)):
                    b = bars[i]
                    if val_as_int:
                        subplot.text(b.get_x()+b.get_width()/2.,
                                height[i]+label_offset,
                                '%d'%(int(b.get_height())),
                                ha="center", va="bottom")
                    else:
                        subplot.text(b.get_x()+b.get_width()/2.,
                                height[i]+label_offset,
                                '%.2f'%(b.get_height()),
                                ha="center", va="bottom")
        else:
            if i>0:
                bars = subplot.barh(indices,v,left=height,color=c.next())
                height = [(x+y) for x,y in zip(height,v)]
            else:
                bars = subplot.barh(indices,v,color=c.next())
                height = list(v)
            if label:
                for i in xrange(len(bars)):
                    b = bars[i]
                    if val_as_int:
                        subplot.text(height[i],
                                b.get_y()+width,
                                '%d'%(int(b.get_width())),
                                ha="left", va="center")
                    else:
                        subplot.text(height[i],
                                b.get_y()+width,
                                '%.2f'%(b.get_width()),
                                ha="left", va="center")
    return

CHARTTYPES = {
    "bar":barchart, "stackedbar":barchart
    , "pie":barchart
}

OTHERS_ITEM = "OTHER"

def proc_csv(csvfile,topx=0,as_percent=False):
    values = []
    keys = []
    vals = dict()
    totalval = 0.
    # assume all input is of the form:
    #       label, value, value2, etc...
    for line in csv.reader(fileinput.input(csvfile)):
        if line is None or len(line)<1 or line[0].startswith("#"):
            continue
        # keys.append(line[0])
        t = [float(x) for x in line[1:]]
        totalval += sum(t)
        vals[line[0]] = t
    if as_percent:
        for k,vls in vals.items():
            vals[k] = [float(v)*100/totalval for v in vls]

    count=0
    o_a=False
    for k,v in sorted(vals.items(),key=lambda x:sum(x[1]),reverse=True):
        if topx > 0 and count > topx:
            if not o_a:
                keys.append(OTHERS_ITEM)
                values.append(v)
                o_a = True
            else:
                values[-1] = [x+y for x,y in zip(v,values[-1])]
        else:
            keys.append(k)
            values.append(v)
        count += 1

    return (keys,values)

def csv2chart(keys,values,outfile,charttype="bar",maxy=None,
        xlabel=None,ylabel=None,title=None,orient_v=True,
        width=0.4,val_as_int=False,label=False,colormap="default"):

    is_svg = os.path.splitext(outfile)[1].lower() == ".svg" # otherwise, png
    minvals = 100
    maxval = 0.

    for v in values:
        if len(v) < minvals:
            minvals = len(v)
        if sum(v) > maxval:
            maxval = sum(v)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    CHARTTYPES[charttype](ax,minvals,keys,values,label=label,
            orient_v=orient_v, label_offset=(.01*maxval),
            val_as_int=val_as_int, width=width, colormap=colormap)

    if not maxy is None:
        ax.set_ylim(ymax=maxy) if orient_v else ax.set_xlim(xmax=maxy)
    if ylabel:
        ax.set_ylabel(ylabel) if orient_v else ax.set_xlabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel) if orient_v else ax.set_ylabel(xlabel)
    if title:
        ax.set_title(title)
    if orient_v:
        plt.xticks(np.arange(len(keys))+width,keys)
    else:
        plt.yticks(np.arange(len(keys))+width,keys)

    plt.savefig(outfile,dpi=90,format="svg" if is_svg else "png")


_opts = [('h','help','Displays this information')
        ,('V','vert','Generate vertically-oriented graphs [default]')
        ,('H','horiz','Generate horizontally-oriented graphs')
        ,('c:','colors=','Use color map (see Color Maps section)')
        ,('x:','xlabel=','Set x-axis (variable) label')
        ,('y:','ylabel=','Set y-axis (values) label')
        ,('t:','title=','Set chart title')
        ,('i','int','Use integer values as labels')
        ,('v','values','Label values')
        ,('w:','width=','Set chart value width (for bar charts) [default: 0.4]')
        ,('T:','topx=','Display top X results, 0=all [default: 0]')
        ,('p','use_percent','Use percentages instead of raw values')
]

def print_usage(cmd):
    print("USAGE: %s [opts] <type> <in.csv> <out.[png|svg]>"%(cmd))
    print("Chart types:\n\t%s"%(", ".join(sorted(CHARTTYPES))))
    print("Options:")
    for s,l,d in sorted(_opts,key=lambda x:x[1]):
        print("\t--%s, -%s\n\t\t%s"%(l,s,d))
    print("Color Maps:\n\t%s"%(", ".join(sorted(COLORMAPS))))

def main(argv):
    import getopt

    if len(sys.argv) < 4:
        print_usage(sys.argv[0])
        return 1
    try:
        opts,args = getopt.getopt(sys.argv[1:],
                "".join([x[0] for x in _opts]),[x[1] for x in _opts])
    except getopt.GetoptError, err:
        print(str(err))
        print_usage(sys.argv[0])
        return 1

    if len(args) != 3:
        print_usage(sys.argv[0])
        return 1
    if not args[0].lower() in CHARTTYPES:
        print("ERROR: Unrecognized chart type \"%s\""%(args[0]))
        print_usage(sys.argv[0])
        return 1
    if args[0].lower() == 'pie':
        print("WARN: pie charts are dumb... using bar chart instead")

    chart_args={'orient_v':True
            ,'width':0.4
            ,'title':None
            ,'xlabel':None
            ,'ylabel':None
            ,'colormap':'default'
            ,'val_as_int':False
            ,'label':False
            ,'charttype':args[0].lower()
            ,'maxy':None
    }
    csv_args={'as_percent':False
            ,'topx':0
    }

    for o,a in opts:
        if o in ('-h','--help'):
            print_usage(sys.argv[0])
            return 0
        elif o in ('-i','--int'):
            chart_args['val_as_int'] = True
        elif o in ('-V','--vert'):
            chart_args['orient_v'] = True
        elif o in ('-H','--horiz'):
            chart_args['orient_v'] = False
        elif o in ('-c','--colors'):
            if a.lower() in COLORMAPS:
                chart_args['colormap'] = a.lower()
            else:
                print("ERROR: Unrecognized color map \"%s\", using default"%(a))
                chart_args['colormap'] = "default"
        elif o in ('-t','--title'):
            chart_args['title'] = a
        elif o in ('-x','--xlabel'):
            chart_args['xlabel'] = a
        elif o in ('-y','--ylabel'):
            chart_args['ylabel'] = a
        elif o in ('-v','--values'):
            chart_args['label'] = True
        elif o in ('-T','--topx'):
            csv_args['topx'] = int(a)
        elif o in ('-p','--use_percent'):
            chart_args['maxy'] = 100
            csv_args['as_percent'] = True
        elif o in ('-w','--width'):
            try:
                chart_args['width'] = float(a)
            except:
                print("ERROR: Invalid width value: %s"%(a))
                return 1

    keys,values = proc_csv(args[1],**csv_args)
    csv2chart(keys,values,args[2],**chart_args)

    return 0

if __name__=="__main__":
    sys.exit(main(sys.argv))
