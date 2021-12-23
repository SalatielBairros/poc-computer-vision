This folder contains both the dataset and model used in our paper "Deep Learning for Logo Recognition".


If you use any of this material, please cite:
@article{bianco2017deep,
  title={Deep learning for logo recognition},
  author={Simone Bianco and Marco Buzzelli and Davide Mazzini and Raimondo Schettini},
  journal={Neurocomputing},
  volume={245},
  pages={23--30},
  year={2017},
  issn={0925-2312},
  doi={http://dx.doi.org/10.1016/j.neucom.2017.03.051},
  url={http://www.sciencedirect.com/science/article/pii/S0925231217305660}
}
@inproceedings{bianco2015logo,
  title={Logo recognition using cnn features},
  author={Bianco, Simone and Buzzelli, Marco and Mazzini, Davide and Schettini, Raimondo},
  booktitle={International Conference on Image Analysis and Processing},
  pages={438--448},
  year={2015},
  organization={Springer}
}


Logos-32plus.zip (DATASET) (1.95GB)
- images
	Contains one subfolder per class ("adidas", "aldi", ...).
	Each subfolder contains a list of JPG images.
- groundtruth.mat
	Contains a MATLAB struct-array "groundtruth", each element having the following fields:
	- file
		Relative path to the image (e.g. 'adidas\000001.jpg').
	- bboxes
		Nx4 double array of bounding boxes.
		The bounding box format is X,Y,W,H.
		X and Y indices start from 1.
	- name
		Name of the logo class (only one class per image).

Model.mat (MODEL) (1.06 MB)
Contains the architecture and parameters for a Convolutional Neural Network in MatConvNet version 1.0-beta16


---------------------------------------------------------------------------


EDIT HISTORY:

2017-04-11 (v1.0.1):
Groundtruth annotations are corrected in order to stay inside the image limits

2017-04-06:
Dataset and model are first uploaded
