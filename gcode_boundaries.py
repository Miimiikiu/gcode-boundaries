"""
Copyright (c) 2023 Kieran Aponte
This software is licensed under the MIT License.
"""


# This script finds the WCS boundaries along X and Y, which may be needed to know where to put workpiece clamps
# to prevent collisions. The result factors in the radius of the tool & collet nut.

# Units are arbitrary as long as you're consistent between these values and your G Code

path = 'G:\\My Drive\\NC Files\\Lathe Adapter V2\\6.34mm Stock Test\\Speed Tiger 6.35mm - 6.34mm Steel Test Cut.nc'
max_tool_diameter = 6.35
max_collet_nut_diameter = 34



max_tool_diameter = max(max_tool_diameter, max_collet_nut_diameter) #Assume collet nut will otherwise collide with clamp at some Z

print('WARNING: This script does not fully account for G2/G3 movements. Use with caution.\n')
print('If G Code includes a synchronization line (such as G28 G91 X0 Y0 as generated from Fusions 360), you may want to temporarily remove it for an accurate reading.\n')

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
                        else: # positive value, or separated by space, such as X 1.618
                            value = float(line[i+1]) # get the numerical value of the full next split item
                            
                            if x_min == None or value < x_min:
                                x_min = value
                            if x_max == None or value > x_max: # not using elif in case of single x value in g code
                                x_max = value
                            
                            skip = True # skip the next item since we already found the value
                            
                            
                    if item[0].upper() == 'Y':
                        if len(item) > 1: # negative value, or clustered together, such as Y1.618
                            try:
                                value = float(item[1:])
                            except:
                                break
                            if y_min == None or value < y_min:
                                y_min = value
                            if y_max == None or value > y_max: # not using elif in case of single y value in g code
                                y_max = value
                        else: # positive value, or separated by space, such as Y 1.618
                            value = float(line[i+1]) # get the numerical value of the full next split item
                            
                            if y_min == None or value < y_min:
                                y_min = value
                            if y_max == None or value > y_max: # not using elif in case of single y value in g code
                                y_max = value
                            
                            skip = True # skip the next item since we already found the value
                            
                            
            elif skip == True:
                skip == False
                            
                
            
                    
        
tool_radius = max_tool_diameter / 2 


print('Tool Center X min:     {}'.format(x_min))
print('Tool Center X max:     {}'.format(x_max))
print('Tool Center Y min:     {}'.format(y_min))
print('Tool Center Y max:     {}\n'.format(y_max))


    
print('Tool/Collet Nut X min: {}'.format(x_min - tool_radius))
print('Tool/Collet Nut X max: {}'.format(x_max + tool_radius))
print('Tool/Collet Nut Y min: {}'.format(y_min - tool_radius))
print('Tool/Collet Nut Y max: {}'.format(y_max + tool_radius))
