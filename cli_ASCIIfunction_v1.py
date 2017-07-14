from collections import deque
import sys
import struct
import numpy as np
import time
from matplotlib import pyplot as plt
import datetime
import re
import cv2
import math
import datetime
import itertools 

def cli_readerascii( fileinput):

    scale = 0.5
    fileinput =  sys.argv[1]
    #bytes_read = open(fileinput, "rb").read()
    poly_line_index = 0

    height = int(1000 * scale)
    width = int(1800 * scale)
    frame = np.ones((height,width,3), np.uint8)
    output_size = (width, height)

    codec = cv2.VideoWriter_fourcc('M','J','P','G')
    fps = 2 
    videof = cv2.VideoWriter()
    success = videof.open('cli.avi',codec,fps,output_size,True) 

    dq1 = deque(['.','.','H','E','A','D','E','R','E','N','D'])
    dq2 = deque(['$','$','H','E','A','D','E','R','E','N','D'])
    first_layer = True
    l = []
    l1 = []
    poly_lines = []
    directions = []


    try:
        with open(fileinput) as fp:
            for data_line in fp:
                data = data_line.split('/')
            #            print data[0] + "command"
                if(data[0] == '$$LAYER'):
                    #                print "new layer"
                    z_height = data[1]
                    #                print data[1] + "height"
                    # zheight = struct.unpack('>f',zheight)[0] * 0.01   # CLI file is in 0.01 mm increments                                                   
                    frame = np.ones((height,width,3), np.uint8)
                    if (first_layer):
                        first_layer = False
                    else:
                        #                    print "poly lines " + str(len(poly_lines))
                        #                    print "directions " + str(len(directions))
                        for l1, d1 in itertools.izip(poly_lines, directions):
                            #                        print d1
                            if d1 == '1':
                                #                            print l1
                                cv2.fillPoly(frame,[l1],(255,255,255))
                            elif d1 == '0': 
                                cv2.fillPoly(frame,[l1],(0,0,0))
                            else:
                                print "direction not 1 or 0"
                                layers.append(poly_lines)
                                layer_directions.append(directions) 
                                directions = []
                                text_string1 = "Youngstown State University"
                                text_string2 = "Z Height=" + str(float(z_height))
                                text_string3 = "CLI Cracker"
                                cv2.putText(frame, text_string1, (230, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                                cv2.putText(frame, text_string3, (400, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                                cv2.putText(frame, text_string2, (635, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                                cv2.imshow("window",frame)
                                cv2.waitKey(1)
                                videof.write(frame)
                                poly_lines = []
        
                                if(data[0] == '$$POLYLINE'):
                                    lines = data[1].split(',') 
                                    #                print "line length " + str(len(data))
                                    #                print lines
                                    id = lines[0]
                                    direction = lines[1]
                                    directions.append(direction)
                                    npts = (int(lines[2]))
                                    index = 3
                                    poly_line = []
                                    while (npts > 0):
                                        #                    print lines[index] 
                                        #                    print lines[index+1] 
                                        #                    print type(lines[index])
                                        x = 2*math.floor(float(lines[index]))
                                        index = index + 1
                                        y = 2*math.floor(float(lines[index]))
                                        index = index + 1 
                                        npts = npts - 1 
                    #                   print "npts" + str(npts)
                                        poly_line.append((x,y))
                                        poly_line = np.array( poly_line, dtype=np.int32)
                                        poly_lines.append(poly_line)
                        
                        
    except StopIteration:
        pass
    return layers, layer_directions

def draw_layer (index, layers, layer_directions):
    polylines = layers[index]
    directions = layer_directions[index]
    text_string1 = "Youngstown State University"
    text_string2 = "Z Height=" + str(float(zheight))
    text_string3 = "CLI Cracker"
    cv2.putText(frame, text_string1, (230, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.putText(frame, text_string2, (635,450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(frame, text_string3, (400, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    frame = draw_layer(5)
    layer_string = 'layer ' + str(index)
    cv2.imshow(layer_string , frame)
    cv2.waitKey(0)
    
    return frame
