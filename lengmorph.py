# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 18:39:17 2020

@author: mi19356
"""

import numpy as np
import pandas as pd 
import os



class load_info:
   
    def __init__(self,cname):
        loc=os.path.join(os.path.dirname(__file__),'data')
        
            
        nodes=np.array(file_read(os.path.join(loc,cname + '_nodes.inp'),',')).astype(np.float64)
        elemes=np.array(file_read(os.path.join(loc,cname + '_elems.inp'),',')).astype(np.float64)
        gbels=np.array(file_read(os.path.join(loc,cname + '_gbels.txt'),' '))
        gbels=pd.DataFrame(gbels,columns=["location","feature"],dtype='float')
        
  
        featureinfo=pd.read_csv(os.path.join(loc, cname + '.csv'),skiprows=1)
        centroid=np.asarray([featureinfo['Centroids_0'],featureinfo['Centroids_1'],featureinfo['Centroids_2']]).T
        self.nodes=nodes
        self.elemes=elemes
        self.gbels=gbels
        self.centroid=centroid
        
        
        """This function will increase the number of nodes defining the voxel
        This may particularly important if you are using FFT solvers where you
        dealing with voxels rather than nodes
        """
        
    def increase_nodes(self):
        nodes=self.nodes
        elemes=self.elemes
        
       
        #increase the number of nodes by added a node between each defined node
        nodesnew=nodes[:,1:]
        
        #add nodes at every 0.5
        updatenew=[[]]*4
        
        #find maximum number of nodes
        
        findtotalmax=int(np.max(nodesnew))*2 +1
        
        column1=np.transpose(np.tile([np.arange(0,int(np.max(nodesnew[:,0]))+0.5,0.5)],int(((np.max(nodesnew[:,0])*2)+1)*((np.max(nodesnew[:,1])*2)+1))))
       
        column1=column1.reshape(np.size(column1),)
        
        column2= np.tile([i for i in np.arange(0,int(np.max(nodesnew[:,1]))+0.5,0.5) for _ in range(findtotalmax)],findtotalmax)

        column3=np.asarray([i for i in np.arange(0,int(np.max(nodesnew[:,2]))+0.5,0.5) for _ in range(int(((np.max(nodesnew[:,0])*2)+1)*((np.max(nodesnew[:,1])*2)+1))) ])

        column0=np.arange(1,np.size(column3)+1,1)
        updatenew[0]=column0
        updatenew[1]=column1
        updatenew[2]=column2
        updatenew[3]=column3
        updatenew=np.asarray(updatenew).T
        
        #update the element array to include extra nodes
        
        #start column values
        startnodes1=[1,2,3]
        maxlength=(int(np.max(nodesnew[:,0]))*2)+1
        startnodes2=[(startnodes1[0]+maxlength),(startnodes1[1]+maxlength),(startnodes1[2]+maxlength)]
        startnodes3=[(startnodes2[0]+maxlength),(startnodes2[1]+maxlength),(startnodes2[2]+maxlength)]
        
        maxlengthupdate=(maxlength*((int(np.max(nodesnew[:,1]))*2)+1))
        startnodes4=[(startnodes1[0]+maxlengthupdate),(startnodes1[1]+maxlengthupdate),(startnodes1[2]+maxlengthupdate)]
        startnodes5=[(startnodes4[0]+maxlength),(startnodes4[1]+maxlength),(startnodes4[2]+maxlength)]
        startnodes6=[(startnodes5[0]+maxlength),(startnodes5[1]+maxlength),(startnodes5[2]+maxlength)]
       
        maxlengthupdate2=(maxlengthupdate)*2
        startnodes7=[(startnodes1[0]+maxlengthupdate2),(startnodes1[1]+maxlengthupdate2),(startnodes1[2]+maxlengthupdate2)]
        startnodes8=[(startnodes7[0]+maxlength),(startnodes7[1]+maxlength),(startnodes7[2]+maxlength)]
        startnodes9=[(startnodes8[0]+maxlength),(startnodes8[1]+maxlength),(startnodes8[2]+maxlength)]
        
        totalnodearray=np.asarray(startnodes1+startnodes2+startnodes3+startnodes4+startnodes5+startnodes6+startnodes7+startnodes8+startnodes9)
        
        nodestotal=[[]]*len(elemes)
        extraval=0
        inc=0
        for i in range(0,len(elemes)):
            if i != 0 :
                if i % int(np.max(nodesnew[:,0]))==0 and i !=0 :
                    if inc == int(np.max(nodesnew[:,1]))-1:
                       
      
                        extra=(maxlength*((int(np.max(nodesnew[:,1]))*2)+1)) + 2*maxlength +3
                        inc=0
                        totalnodearray=nodestotal[i-1] 
                        nodestotal[i]=np.append(nodestotal[i],nodestotal[i-1]+extra)
                    else:
                        extraval=maxlength + 3
                        nodestotal[i]=np.append(nodestotal[i],nodestotal[i-1]+extraval)
                        inc += 1
                else:
                   
                    nodestotal[i]=np.append(nodestotal[i],nodestotal[i-1]+2)
            else:
                nodestotal[i]=totalnodearray
                    
                    
        nodestotal=np.asarray(nodestotal)
        elid=np.arange(1,len(elemes)+1,1).reshape(len(elemes),1)
        elemes=np.hstack((elid,nodestotal))
        
        self.elemes=elemes
        self.nodes=updatenew
        
    """find grain boundary nodes corresponding to each grain"""    
        
    def grain_boundary(self,**kwargs):
        
        nodes=self.nodes
        elemes=self.elemes
        gbels=self.gbels
        
        #check to see if the node increase function was used to determine
        #how many nodes per voxel
        if kwargs['nodeinc']==False :
           nodenum=8
        else:
           nodenum=27

        #find all elements at a boundary and order according to feature id
        
        bfeature=gbels.loc[gbels['location']==0,'feature']
        indexfeature=gbels.loc[gbels['location']==0,'feature'].index.tolist()
        
        #creating an array from this info which has the element number and grain feature this belongs to 
        #respectively
        
        el_feature=np.array([list(np.asarray(indexfeature)+1),bfeature]).T
        
        #Now create an array of grains to search through the 'el_feature' array to find
        #the elements that belongs to it.  Add these elements to the row which  feature
        #the element belongs to.
        
        searchfeat=np.arange(1,np.amax(el_feature[:,1],axis=0)+1)
        
        #Search through the el_feature array for each individual value in searchfeat
        #and find when this feature appears in the array and assign the element from the
        #first column of the array.
        
        #Now elloc has the features which are the grains but are 1 value out since
        #the starting index is zero.  The rows correspond to the elements which are on the boundary
        #for that feature.
        
        elloc=[[None]*len(searchfeat)]*len(searchfeat)
        featelnode=[[None]*len(searchfeat)]*len(searchfeat)
        intersect=[[]*len(searchfeat)]*len(searchfeat)
        featurenodes=[[]*len(searchfeat)]*len(searchfeat)
        xnodes=[[]*len(searchfeat)]*len(searchfeat)
        ynodes=[[]*len(searchfeat)]*len(searchfeat)
        znodes=[[]*len(searchfeat)]*len(searchfeat)
        boundfeat=[[]*len(searchfeat)]*len(searchfeat)
    
     
        
        #converting dataframe to array to see if it is easier for me to use
        
        newelemes=elemes
        newnodes=nodes
        
        # finding the centroid nodal coordinates for each element
        nodecoord=[[]*len(newelemes[:,0])]*len(newelemes[:,0])
        avcoord=[[]*3]*len(newelemes[:,0])
        
        for i in range(0,len(newelemes[:,0])):
            nodecoord[i]=newnodes[(newelemes[i,1:]-1).astype(np.int64)]
            
            avcoord[i]=sum(nodecoord[i][:,1:])/nodenum
            
           # *******need to add a tool in here to decipher whether increasing nodes***
            
            
        for i in range(0,len(searchfeat)):
            
            elloc[i]=el_feature[np.where(el_feature[:,1]==searchfeat[i]),0]
            
           # Now we need to find the nodes which correspond to those elements for each feature/grain"""
            #featelnode[i]=newelemes[list((np.asarray(elloc[i])-1).astype(np.int64)),:][0,:,1:9]
            featelnode[i]=newelemes[list((np.asarray(elloc[i])-1).astype(np.int64)),:][0,:,1:]
        
        
        #Now we need to see which features have overlapping nodes with other features as these 
        #nodes will then belong to the very outer surface."""
    
        for i in range(0,len(searchfeat)):
            for j in range(0,len(searchfeat)):
                intersectarray=np.intersect1d(featelnode[i],featelnode[j])
                if np.size(intersectarray) > 0 :
                    if i != j :
                        intersect[i]=np.append(intersect[i],intersectarray,axis=0)
                        boundfeat[i]=np.append(boundfeat[i],np.size(intersectarray)*[j+1])
                        
                        #Intersect array now has the nodes corresponding to each grain on the surface 
                        #of the grain.  The row location corresponds to the feature-1
                       
                        #now we need to find the x,y,z coordinates which correspond to these nodes
                        
                        featurenodes[i]=newnodes[np.asarray(intersect[i]-1).astype(int)]
                        xnodes[i]=featurenodes[i][:,1]
                        ynodes[i]=featurenodes[i][:,2]
                        znodes[i]=featurenodes[i][:,3]
                        
        #saving to self to use in other functions
        self.featurenodes=featurenodes
        self.boundfeat=boundfeat
        
                       
        #Writing the node coordinates to separate txt files
        #firstly enumerate list to provide a dictionary depedent on the index of the list
        
        xnodelist = dict(enumerate(xnodes))
        ynodelist = dict(enumerate(ynodes))
        znodelist = dict(enumerate(znodes))
        boundfeat = dict(enumerate(boundfeat))
        
       
        #Then create a dataframe for export
        #'9999999's are added to rows missing values to ensure each row is the same dimension
        #for reading into crystal plasicity UMAT
        
        xnodedataframe= pd.DataFrame.from_dict(xnodelist, orient='index').fillna(9999999)
        ynodedataframe= pd.DataFrame.from_dict(ynodelist, orient='index').fillna(9999999)
        znodedataframe= pd.DataFrame.from_dict(znodelist, orient='index').fillna(9999999)
        boundfeatframe= pd.DataFrame.from_dict(boundfeat, orient='index').fillna(9999999)
        
        
        #saving as binary file
        #xvalues
        numRowarrx=np.array([np.size(xnodedataframe.values,0)],dtype=np.float64)
        numColarrx=np.array([np.size(xnodedataframe.values,1)],dtype=np.float64)
        xvalues=open('xvalues.bin','wb')
        numRowarrx.tofile(xvalues)
        numColarrx.tofile(xvalues)
        xnodedataframe.values.astype(np.float64).tofile(xvalues)
        xvalues.close()
        #np.savetxt('xvalues.txt', xnodedataframe.values, fmt='%f')
        
        #yvalues
        numRowarry=np.array([np.size(ynodedataframe.values,0)],dtype=np.float64)
        numColarry=np.array([np.size(ynodedataframe.values,1)],dtype=np.float64)
        yvalues=open('yvalues.bin','wb')
        numRowarry.tofile(yvalues)
        numColarry.tofile(yvalues)
        ynodedataframe.values.astype(np.float64).tofile(yvalues)
        yvalues.close()
        #np.savetxt('yvalues.txt', ynodedataframe.values, fmt='%f')
        
        #zvalues
        numRowarrz=np.array([np.size(znodedataframe.values,0)],dtype=np.float64)
        numColarrz=np.array([np.size(znodedataframe.values,1)],dtype=np.float64)
        zvalues=open('zvalues.bin','wb')
        numRowarrz.tofile(zvalues)
        numColarrz.tofile(zvalues)
        znodedataframe.values.astype(np.float64).tofile(zvalues)
        zvalues.close()
       #np.savetxt('zvalues.txt', znodedataframe.values, fmt='%f')
        
        #boundfeat
        numRowarrbf=np.array([np.size(boundfeatframe.values,0)],dtype=np.float64)
        numColarrbf=np.array([np.size(boundfeatframe.values,1)],dtype=np.float64)
        bfvalues=open('boundfeat.bin','wb')
        numRowarrbf.tofile(bfvalues)
        numColarrbf.tofile(bfvalues)
        boundfeatframe.values.astype(np.float64).tofile(bfvalues)
        bfvalues.close()
        #np.savetxt('boundfeat.txt',boundfeatframe.values,fmt='%f')
    
  
        elcentroid=np.array(avcoord)
        
        self.elcentroid=elcentroid
        self.elloc=elloc
        
        #saving the centroid coordinates for each voxel to text file
        #saving a binary file
        numRowarr=np.array([np.size(elcentroid,0)],dtype=np.float64)
        numColarr=np.array([np.size(elcentroid,1)],dtype=np.float64)
        centfile=open('el_centroid.bin','wb')
        numRowarr.tofile(centfile)
        numColarr.tofile(centfile)
        elcentroid.astype(np.float64).tofile(centfile)

        centfile.close()
        
  
        
def file_read(fname,delim):
        with open(fname) as textFile:
            content_array = [line.split(delim) for line in textFile if not (line.startswith("*") or "GBManhattanDistances" in line)]
               
        return (content_array)
    


    
load=load_info('testcase')

#load.increase_nodes()

load.grain_boundary(nodeinc=False)




