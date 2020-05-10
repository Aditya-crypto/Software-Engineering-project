import os
import json
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from tqdm import tqdm
from matplotlib import cm as CM
from torch.utils.data import Dataset
import cv2
import torch
import torch.nn as nn
import random
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

class trainCrowdDataset(Dataset):
    '''
    crowdDataset
    '''
    def __init__(self,img_root,gt_dmap_root,gt_downsample=1):
        self.img_root=img_root
        self.gt_dmap_root=gt_dmap_root
        self.gt_downsample=gt_downsample

        self.img_names=[filename for filename in os.listdir(img_root) \
                           if os.path.isfile(os.path.join(img_root,filename))]
        self.n_samples=len(self.img_names)

    def __len__(self):
        return self.n_samples

    def __getitem__(self,index):
        assert index <= len(self), 'index range error'
        img_name=self.img_names[index]
        img=plt.imread(os.path.join(self.img_root,img_name))
        if len(img.shape)==2: # expand grayscale image to three channel.
            img=img[:,:,np.newaxis]
            img=np.concatenate((img,img,img),2)

        gt_dmap=np.load(os.path.join(self.gt_dmap_root,img_name.replace('.jpg','.npy')))
       
        if self.gt_downsample>1: # to downsample image and density-map to match deep-model.
            ds_rows=int(img.shape[0]//self.gt_downsample)
            ds_cols=int(img.shape[1]//self.gt_downsample)
            img = cv2.resize(img,(ds_cols*self.gt_downsample,ds_rows*self.gt_downsample))
            
            img=img.transpose((2,0,1)) # convert to order (channel,rows,cols)
            gt_dmap=cv2.resize(gt_dmap,(ds_cols,ds_rows))
            gt_dmap=gt_dmap[np.newaxis,:,:]*self.gt_downsample*self.gt_downsample
        
        img_tensor=torch.tensor(img,dtype=torch.float)
        gt_dmap_tensor=torch.tensor(gt_dmap,dtype=torch.float)

        return img_tensor,gt_dmap_tensor

"""# MCNN"""

class MCNN(nn.Module):
    
    '''
    Implementation of Multi-column CNN for crowd counting
    '''
    
    def __init__(self,load_weights=False):
        super(MCNN,self).__init__()

        self.branch1=nn.Sequential(
            nn.Conv2d(3,16,9,padding=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(16,32,7,padding=3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32,16,7,padding=3),
            nn.ReLU(inplace=True),
            nn.Conv2d(16,8,7,padding=3),
            nn.ReLU(inplace=True)
        )

        self.branch2=nn.Sequential(
            nn.Conv2d(3,20,7,padding=3),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(20,40,5,padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(40,20,5,padding=2),
            nn.ReLU(inplace=True),
            nn.Conv2d(20,10,5,padding=2),
            nn.ReLU(inplace=True)
        )

        self.branch3=nn.Sequential(
            nn.Conv2d(3,24,5,padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(24,48,3,padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(48,24,3,padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(24,12,3,padding=1),
            nn.ReLU(inplace=True)
        )

        self.fuse=nn.Sequential(nn.Conv2d(30,1,1,padding=0))

        if not load_weights:
            self._initialize_weights()

    def forward(self,img_tensor):
        x1=self.branch1(img_tensor)
        x2=self.branch2(img_tensor)
        x3=self.branch3(img_tensor)
        x=torch.cat((x1,x2,x3),1)
        x=self.fuse(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, std=0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

"""# TRAINING"""

if __name__=="__main__":
    
    torch.backends.cudnn.enabled=False
    device=torch.device("cuda")
    mcnn=MCNN().to(device)
    criterion=nn.MSELoss(size_average=False).to(device)
    optimizer = torch.optim.SGD(mcnn.parameters(), lr=1e-6,
                                momentum=0.95)
    
    img_root='/content/sample_data/image'
    gt_dmap_root='/content/sample_data/temp'
    dataset=trainCrowdDataset(img_root,gt_dmap_root,4)
    dataloader=torch.utils.data.DataLoader(dataset,batch_size=1,shuffle=True)

    test_img_root='/content/sample_data/test_image'
    test_gt_dmap_root='/content/sample_data/test_temp'
    test_dataset=trainCrowdDataset(test_img_root,test_gt_dmap_root,4)
    test_dataloader=torch.utils.data.DataLoader(test_dataset,batch_size=1,shuffle=False)

    #training phase
    if not os.path.exists('./checkpoints'):
        os.mkdir('./checkpoints')
    min_mae=10000
    min_epoch=0
    train_loss_list=[]
    epoch_list=[]
    test_error_list=[]
    for epoch in range(0,100):

        mcnn.train()
        epoch_loss=0
        for i,(img,gt_dmap) in enumerate(dataloader):
            img=img.to(device)
            gt_dmap=gt_dmap.to(device)
            # forward propagation
            et_dmap=mcnn(img)
            # calculate loss
            loss=criterion(et_dmap,gt_dmap)
            epoch_loss+=loss.item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print("epoch:",epoch,"loss:",epoch_loss/len(dataloader))
        epoch_list.append(epoch)
        train_loss_list.append(epoch_loss/len(dataloader))
        torch.save(mcnn.state_dict(),'./checkpoints/epoch_'+str(epoch)+".param")
    mcnn.eval()
        mae = 0
        for i,(img,gt_dmap) in enumerate(test_dataloader):
            img=img.to(device)
            gt_dmap=gt_dmap.to(device)
            # forward propagation
            et_dmap=mcnn(img)
            mae+=abs(et_dmap.data.sum()-gt_dmap.data.sum()).item()
            del img,gt_dmap,et_dmap
        if mae/len(test_dataloader)<min_mae:
            min_mae=mae/len(test_dataloader)
            min_epoch=epoch
        test_error_list.append(mae/len(test_dataloader))
        print("epoch:"+str(epoch)+" error:"+str(mae/len(test_dataloader))+" min_mae:"+str(min_mae)+" min_epoch:"+str(min_epoch))
        
        # show an image
        index=random.randint(0,len(test_dataloader)-1)
        img,gt_dmap=test_dataset[index]
        img=img.unsqueeze(0).to(device)
        gt_dmap=gt_dmap.unsqueeze(0)
        et_dmap=mcnn(img)
        et_dmap=et_dmap.squeeze(0).detach().cpu().numpy()

class testCrowdDataset(Dataset):
    '''
    crowdDataset
    '''
    def __init__(self,img_root,gt_downsample=1):
        self.img_root=img_root
        self.gt_downsample=gt_downsample

        self.img_names=[filename for filename in os.listdir(img_root) \
                           if os.path.isfile(os.path.join(img_root,filename))]
        self.n_samples=len(self.img_names)

    def __len__(self):
        return self.n_samples

    def __getitem__(self,index):
        assert index <= len(self), 'index range error'
        img_name=self.img_names[index]
        img=plt.imread(os.path.join(self.img_root,img_name))

        if len(img.shape)==2: # expand grayscale image to three channel.
            img=img[:,:,np.newaxis]
            img=np.concatenate((img,img,img),2)

        if self.gt_downsample>1: # to downsample image and density-map to match deep-model.
            ds_rows=int(img.shape[0]//self.gt_downsample)
            ds_cols=int(img.shape[1]//self.gt_downsample)
            img = cv2.resize(img,(ds_cols*self.gt_downsample,ds_rows*self.gt_downsample))
            img=img.transpose((2,0,1)) # convert to order (channel,rows,cols)
        
        img_tensor=torch.tensor(img,dtype=torch.float)
        return img_tensor

class CrowdCounter:

    def generate_densitymap(self,image,points,sigma=15):
        '''
        The main idea is to count objects indirectly by estimating 
        a density map. The first step is to prepare training samples,
        so that for every image there is a corresponding density map.
        A density map is obtained by applying a convolution with a 
        Gaussian kernel (and normalized so that integrating it gives
        the number of objects).
        generate_densitymap is a function which generates the Density
        map for images, which acts as ground truth values for the MCNN 
        to be trained. These ground truth values are generated using 
        the JSON files, that are being provided as input along with 
        the images. The input is :
        image : Image of a place with people in it.
        image.json : JSON file of the image which consists of the data
        about the location of people in the image.
        The output obtained is the Density map  
        '''
        # the height and width of the image
        image_h = image.shape[0]
        image_w = image.shape[1]
        
        # coordinate of heads in the image
        points_coordinate = points
        
        # quantity of heads in the image
        points_quantity = len(points_coordinate)

        # generate ground truth density map
        densitymap = np.zeros((image_h, image_w))
        for point in points_coordinate:
            c = min(int(round(point[0])),image_w-1)
            r = min(int(round(point[1])),image_h-1)
            densitymap[r,c] = 1
        densitymap = gaussian_filter(densitymap, sigma=sigma, mode='constant')
        densitymap = densitymap / densitymap.sum() * points_quantity
        return densitymap    

    # if __name__ == '__main__':
    def save_density_map(self):
      
        data_path = "/content/sample_data/"
        phase_list = ['train1','test1']
        for phase in phase_list:
            temp_root = data_path + phase
            # print(temp_root)
            for scene in os.listdir(temp_root):
                img_path = os.path.join(temp_root,scene)
                t=img_path.split('.')
                if(t[-1]!='jpg'):
                    continue
                # print(img_path)
                json_path = img_path.replace('jpg','json')
                npy_path = img_path.replace('jpg','npy')
                img = plt.imread(img_path)
                with open(json_path,'r') as load_f:
                    anno = json.load(load_f)
                    keyname = list(anno.keys())[0]
                    anno = anno[keyname]['regions']
                    points = []
                    for head in anno:
                        head = head['shape_attributes']
                        x = head['x']
                        y = head['y']
                        width = head['width']
                        height = head['height']
                        points.append((x,y,width,height))
                    densitymap = self.generate_densitymap(img,points)
                    np.save(npy_path,densitymap)
                    gt_file = np.load(img_path.replace('.jpg','.npy'))
                    # print(gt_file.shape)
                    # plt.imshow(gt_file,cmap=CM.jet)


    people_count = [] #list to store count of people in an image
    def predict_count(self,img_root,model_param_path):
        '''
        Predict the number of people in the input image.
        img_root: the root of test image data.
        model_param_path: the path of specific mcnn parameters.
        '''
        device=torch.device("cuda")
        mcnn=MCNN().to(device)
        mcnn.load_state_dict(torch.load(model_param_path))
        dataset = testCrowdDataset(img_root,4)
        dataloader=torch.utils.data.DataLoader(dataset,batch_size=1,shuffle=False)
        mcnn.eval()
        mae=0
        with torch.no_grad():
            for i,(img) in enumerate(dataloader):
                img=img.to(device)

                # forward propagation
                et_dmap=mcnn(img)
                self.people_count.append(int(et_dmap.data.sum()))
                del img,et_dmap

    def FindCID(self):

        threshold = 20 # Set a threshold for the number of people allowed
        torch.backends.cudnn.enabled=False
        img_root='/content/sample_data/test_image'
        # getting image names from folder
        img_nam = [filename for filename in os.listdir(img_root) \
                              if os.path.isfile(os.path.join(img_root,filename))]
        camera_id = [] #list to store camera Ids
        for img in img_nam:
            cid = img.split('_')
            camera_id.append(cid[0])

        model_param_path='/content/checkpoints/epoch_20.param'
        self.predict_count(img_root,model_param_path)    

        report_camera_id = [] #final list of Camera IDs where rules have been violated
        for i in range(len(self.people_count)):
          if self.people_count[i] > threshold :
            t = self.people_count[i],camera_id[i]
            report_camera_id.append(t)
            
        for x in report_camera_id: # print camera IDs
          print(x)

        return report_camera_id
