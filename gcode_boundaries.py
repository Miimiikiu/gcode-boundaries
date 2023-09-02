# This script finds the WCS boundaries along X and Y, which may be needed to know where to put workpiece clamps
# to prevent collisions. The result factors in the radius of the tool & collet nut.

# Units are arbitrary as long as you're consistent between these values and your G Code

path = 'G:\\My Drive\\NC Files\\Lathe Adapter V2\\6.5mm Stock\\Speed Tiger 6.35mm - Lathe Router Adapter 6.5mm Stock.nc'
max_tool_diameter = 6.35
max_collet_nut_diameter = 34

# My stock is rectangular with the longest edge along the y axis with the clamps at the top & bottom edges
allow_edge_x = True  # True if you're okay with the tool center hitting the left/right edges, such as if the clamps are along the top & bottom edges
allow_edge_y = False # True if you're okay with the tool center hitting the top/bottom edges, such as if the clamps are along the left & right edges
 
max_tool_diameter = max(max_tool_diameter, max_collet_nut_diameter) #Assume collet nut will otherwise collide with clamp at some Z

print('WARNING: This script does not fully account for G2/G3 movements. Use this script with caution.')
print('If g code was generated in Fusions 360, you may want to temporarily remove the G28 G91 X0 Y0 line at the bottom of your file for an accurate reading.')

with open(path, 'r') as infile:
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    
    #TODO: calculate boundaries for G2, G3
    #TODO: Ignore comments in G Code
    for line in infile:
        line = line.split(' ')
        skip = False
        for i, item in enumerate(line):
            if skip == False:
                if len(item) > 0:
                    if item[0].upper() == 'X':
                        if len(item) > 1: # negative value, or clustered together, such as X-1.618
                            try:
                                value = float(item[1:])
                            except:
                                break
                            if x_min == None or value < x_min:
                                x_min = value
                            if x_max == None or value > x_max: # not using elif in case of single x value in g code
                                x_max = value
                        else: # positive value, or separated, such as X 1.618
                            value = float(line[i+1]) # get the numerical value of the full next split item
                            
                            if x_min == None or value < x_min:
                                x_min = value
                            if x_max == None or value > x_max: # not using elif in case of single x value in g code
                                x_max = value
                            
                            skip = True # skip the next item since we already found the value
                            
                            
                    if item[0].upper() == 'Y':
                        if len(item) > 1: # negative value, or clustered together, such as Y-1.618
                            try:
                                value = float(item[1:])
                            except:
                                break
                            if y_min == None or value < y_min:
                                y_min = value
                            if y_max == None or value > y_max: # not using elif in case of single y value in g code
                                y_max = value
                        else: # positive value, or separated, such as Y 1.618
                            value = float(line[i+1]) # get the numerical value of the full next split item
                            
                            if y_min == None or value < y_min:
                                y_min = value
                            if y_max == None or value > y_max: # not using elif in case of single y value in g code
                                y_max = value
                            
                            skip = True # skip the next item since we already found the value
                            
                            
            elif skip == True:
                skip == False
                            
                
            
                    
        
tool_radius = max_tool_diameter / 2 
tool_radius_x = max_tool_diameter/2 if allow_edge_x == False else 0
tool_radius_y = max_tool_diameter/2 if allow_edge_y == False else 0


print('Clearance X min: {}'.format(x_min - tool_radius_x))
print('Clearance X max: {}'.format(x_max + tool_radius_x))
print('Clearance Y min: {}'.format(y_min - tool_radius_y))
print('Clearance Y max: {}'.format(y_max + tool_radius_y))
