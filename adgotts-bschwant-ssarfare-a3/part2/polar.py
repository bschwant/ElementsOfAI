#!/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

'''
    Commands For Testinig Different Images with coordinates 

*** Image 09.png ***
    python3 polar.py test_images/09.png 95 23 132 44

### Image 16.png ***
    python3 polar.py test_images/16.png 34 20 137 48

*** Image 23.png ***
    python3 polar.py test_images/23.png 99 39 46 113

*** Image 30.png ***
    python3 polar.py test_images/30.png 72 20 144 59

*** Image 31.png 
    python3 polar.py test_images/31.png 118 25 52 52

'''

# calculate "Edge strength map" of an image      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

''' 
    Helper function to normaize edge stregths
'''
def normalize(edge_strength):
    norm = uint8(255 * edge_strength / amax(edge_strength))
    return norm

'''
    Helper function to compute emission probability for edge in column
'''
def compute_emission_prob(curr_col):
    e = [i / sum(curr_col) for i in curr_col]
    return asarray(e).reshape(len(e), 1)

'''
    Helper function to compute transition probabilites based on distance from row of previous edge

    Increases probability that next edge will be within 5 pixels of current row.
    Originally used 9 pixel range based on assumption that boundaries are 10 pixels apart,
        but found 5 pixels wored better
'''
def comp_trans_prob(prev_edge_row, curr_col):
    temp_col = curr_col/sum(curr_col)
    temp_col[prev_edge_row - 5:prev_edge_row+6] = 0.1*curr_col[prev_edge_row-5:prev_edge_row+6]
    temp_dist = [abs(prev_edge_row-row) for row in range (len(curr_col))]
    max_dist = max(temp_dist)
    temp_dist = abs(asarray(temp_dist)-max_dist)
    temp_col *= temp_dist
    temp_col = [t/sum(temp_col)for t in temp_col]
    temp_col = asarray(reshape(temp_col, (-1,1)), dtype='float32')

    return temp_col


'''
    Function that computes the a simple Bates Net to estimate the two boundaries 
'''
def simple_bayes(edge_strength):

    # airice_edge = zeros(edge_strength.shape[1])
    icerock_edge = zeros(edge_strength.shape[1])

    # First find airice edge 
    airice_edge = [argmax(edge_strength[:,i]) for i in range (edge_strength.shape[1])]
    
    # Find icerock edge
    for i in range (edge_strength.shape[1]):
        min_row = airice_edge[i] + 10

        max_edge = 0
        max_index = 0
        for j in range (min_row, edge_strength.shape[0]):

            if j == min_row:
                max_edge = edge_strength[j][i]
                max_index = j

            elif max_edge < edge_strength[j][i]:
                max_edge = edge_strength[j][i]
                max_index = j

        icerock_edge[i] = max_index
        
    # print(airice_edge)
    # print(icerock_edge)       
    
    return (airice_edge, icerock_edge)

'''
    Function to find the two boundaries using bayes net that uses viterbi
'''
def viterbi(norm_edge_strength, gt_airice = None, gt_icerock = None):

    # norm_edge_stregth = normalize(edge_strength)

    if(not gt_airice or not gt_icerock):
        init_row_airice = int(argmax(norm_edge_strength[:, 0]))
        init_col_airice = 0

        init_row_icerock = 0
        init_col_icerock = 0

    else:
        # init_row_airice = gt_airice[0]
        # init_col_airice = gt_airice[1]

        # init_row_icerock = gt_icerock[0]
        # init_col_icerock = gt_icerock[1]
        init_row_airice = gt_airice[1]
        init_col_airice = gt_airice[0]

        init_row_icerock = gt_icerock[1]
        init_col_icerock = gt_icerock[0]

    # # init_row = int(argmax(norm_edge_strength[:, 0]))
    # init_col = input_col

    # Find airice_edge first
    airice_edge = zeros(norm_edge_strength.shape[1])

    # Handles points after user column input when not 0
    for col in range (init_col_airice, norm_edge_strength.shape[1]):

        if col == init_col_airice:
            airice_edge[col] = init_row_airice
            # print("\n\nHere", init_row_airice )

        else:
            prev_row = int(airice_edge[col-1])
            trans_prob = comp_trans_prob(prev_row, norm_edge_strength[:, col])
            vt = norm_edge_strength[prev_row, col-1]/sum(norm_edge_strength[:, col-1])
            e_prob = compute_emission_prob(norm_edge_strength[:, col]) * trans_prob * vt
            airice_edge[col] = argmax(e_prob)

    # Handles points after user column input when not 0
    for col in range (init_col_airice - 1, - 1, -1):
        prev_row = int(airice_edge[col+1])
        trans_prob = comp_trans_prob(prev_row, norm_edge_strength[:, col])
        vt = norm_edge_strength[prev_row, col+1]/sum(norm_edge_strength[:, col+1])
        e_prob = compute_emission_prob(norm_edge_strength[:, col]) * trans_prob * vt
        airice_edge[col] = argmax(e_prob)


    # print("airice edge", airice_edge)

    # Find icerock_edge based of air_ice edge
    icerock_edge = zeros(norm_edge_strength.shape[1])

    # Compute initial row
    # init_row = input_row
    # init_col = 0
    min_row = int(airice_edge[init_row_icerock] + 10)
    max_edge = 0
    max_index = 0

    if (not init_row_icerock):
        for j in range (min_row, edge_strength.shape[0]):
            if j == min_row:
                max_edge = edge_strength[j][init_col_icerock]
                max_index = j

            elif max_edge < edge_strength[j][init_col_icerock]:
                max_edge = edge_strength[j][init_col_icerock]
                max_index = j
        init_row = max_index

    else:
        init_row = init_row_icerock

    # Handles points after user column input when not 0
    for col in range (init_col_icerock, norm_edge_strength.shape[1]):

        if col == init_col_icerock:
            icerock_edge[col] = init_row

        else:
            prev_row = int(icerock_edge[col-1])
            trans_prob = comp_trans_prob(prev_row, norm_edge_strength[:, col])
            vt = norm_edge_strength[prev_row, col-1]/sum(norm_edge_strength[:, col-1])
            e_prob = compute_emission_prob(norm_edge_strength[:, col]) * trans_prob * vt
            icerock_edge[col] = argmax(e_prob)


    # Handles points after user column input when not 0
    for col in range (init_col_icerock - 1, - 1, -1):
        prev_row = int(icerock_edge[col+1])
        trans_prob = comp_trans_prob(prev_row, norm_edge_strength[:, col])
        vt = norm_edge_strength[prev_row, col+1]/sum(norm_edge_strength[:, col+1])
        e_prob = compute_emission_prob(norm_edge_strength[:, col]) * trans_prob * vt
        icerock_edge[col] = argmax(e_prob)


    # print("IceRock Edge",icerock_edge)

    return (airice_edge,icerock_edge)



# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.
    '''
    airice_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    airice_hmm = [ image_array.shape[0]*0.5 ] * image_array.shape[1]
    airice_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]

    icerock_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    icerock_hmm = [ image_array.shape[0]*0.5 ] * image_array.shape[1]
    icerock_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]
    '''
    # norm_edge_strength = normalize(edge_strength)

    '''
        Part 1: Compute air-ice and ice-rock edges using simple bayes
    '''
    airice_simple, icerock_simple = simple_bayes(edge_strength)
    #print(airice_simple)

    '''
        Part 2: Compute boundaries with Bayes using viterbi no user input 
    '''
    #in_row = int(argmax(edge_strength[:, 0]))
    #in_col = 0
    airice_hmm, icerock_hmm = viterbi(edge_strength)

    '''
        Part 3: Compute boundaries with Bayes using viterbi with user input
    '''
    airice_feedback, icerock_feedback = viterbi(edge_strength, gt_airice , gt_icerock)


    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
