import numpy as np
from PIL import Image as img
import math


def img_to_matrix_rgb():
    '''converts the rgb image into rgb matrix  and rgb matrix into 3 different matrices
    of red blue and green'''
    #open image
    mats=np.array(img.open('greyscale.jpg'))
    #find its dimensions and square it
    r,c,u=np.shape(mats)
    if r>c:
        mat=mats[:c,:c]
    else:
        mat=mats[:r,:r]
    print(np.shape(mat))
   #seperate lists to form new matrix 
    red=[]
    green=[]
    blue=[]
    for rows in range(r):
        #this list will contain rows of the above matrix
        t_r=[]
        t_g=[]
        t_b=[]
        for cols in range(c):
            #filling up first row and appending to main list i.e matrix
            t_r.append(mat[rows][cols][0])
            t_g.append(mat[rows][cols][1])
            t_b.append(mat[rows][cols][2])
        red.append(t_r)
        green.append(t_g)
        blue.append(t_b)
    return red,blue,green

def SVD(m):
    '''find eigenvalues and vectors of a given matrix'''
    values,vector=np.linalg.eig(m)
    in_vector=np.linalg.inv(vector)
    return vector,values,in_vector


def img_to_matrix_gray():
    '''useless code since all images nowdays are rgb'''
    mats=np.array(img.open('greyscale.jpg'))
    mat=mats[:5700,:5700]
    print(mat)
    return mat

def Svd(m):
    '''inbuilt svd for cheking weather our output is good or not'''
    mat=np.linalg.svd(m)
    return mat

def scalar_to_diagonal(value,d):
  '''code to convert the list of eigenvalues to diagonal matrix and also drop least values from that matrix'''
  #create proper diagonal matrix of size of the array of eigenvalues  
  n = value.size
  diagonal = np.zeros((n,n),dtype = 'complex' )

  for i in range(n):
      #fill up the diagonal matrix
      diagonal[i,i] = value[i]
  
  for i in range(n):
      #convert all negatuve values in array to positive. insignificant values are close to 0.
      #all complex value to its absolute counterpart, a+ib to root(a**2+b**2)
      a,b=value[i].real,value[i].imag
      value[i]=math.sqrt(a**2+b**2)
    
  for j in range(d):
      #find least eigenvalues and make those diagonal entries 0. array is used to find and then diagonal
      #matrix is updated accordingly
      i=np.argmin(value)
      #print(i,value[i])
      diagonal[i][i]=0
      value[i]=100000 #convert min into something big so we dont keep picking same value
      #print(value[i],i)       
  return diagonal

def drop_values(m,p):
    '''code which takes the matrix as input performs svd , drops values and gives decomposed form(SVD)
    p is percentage of values u want to be dropped 0.1 means 10%.'''
    u,e,v=SVD(m)
    print('---------------------------')
    r=len(e)
    d=int(p*r) 
    E=scalar_to_diagonal(e,d)
    #print(E)
    print('--------------------------')
    mat=u @ E @ v
    mat=mat.astype('uint8') #convert to proper type
    return mat

def compression(m,p):
    '''useless code for grayscale'''
    mat=drop_values(m, p)
    #print(mat)
    mat=mat.astype('uint8')
    temp_img= img.fromarray(mat).save('uncool_rohit.png')

def combine_rgb(r,g,b):
    '''not needed code was just experimenting'''
    rows,cols=np.shape(r)
    rgb_matrix=np.array(rows,'uint8')
    for i in range(rows):
        rgb_list=np.array(cols,'uint8')
        for j in range(cols):
            np.append(rgb_list,[r[i][j],g[i][j],b[i][j]])
            #rgb_array=np.array(rgb_list)
        np.append(rgb_matrix,rgb_list)
        #rgb_matrix_array=np.array(rgb_matrix)
    return rgb_matrix

def compress_rgb_image(p):
    '''drop p fraction of values from svd of the given image, does svd on red green and blue matrices
    seperately and then combine them to give ouput image'''
    r,g,b=img_to_matrix_rgb()
    new_r,new_g,new_b=drop_values(r,p),drop_values(g, p),drop_values(b, p)
    imr=img.fromarray(new_r)
    imgr=img.fromarray(new_g)
    imb=img.fromarray(new_b)
    
    #code to merge the r , g , and b matrices
    temp_img= img.merge('RGB',(imr,imgr,imb)).save('After.png')

#m=img_to_matrix_gray()
#print(m)
#for i in range(0,100,25):
compress_rgb_image(0.3)
