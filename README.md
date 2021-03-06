# regionconnect
IIT Human Brain Atlas regionconnect app. 
Before using the regionconnect app, please register your data into the IIT space. See [IIT atlas manual](https://www.nitrc.org/frs/download.php/11488/IIT_Atlas_v.5.0_MANUAL.pdf) for more details.

## Getting the most probabel connections
1. First method: import regionconnect function.   
- To update your `pip` and create a virtual environment: 
```
python -m pip install --upgrade pip
python3 -m venv regionconnectTest
source regionconnectTest/bin/activate
python3 -m pip install regionconnect
```

- Launch python console and run `regionconnect`
```
python
>>from regionconnect import regionconnect
>>regionconnect.regionconnect('path_to_ROI_mask','path_to_output_text_file')
```

2. Second method: run the regionconnect.py script directly.
```
python3 -m pip install numpy nibabel
git clone https://github.com/SheridanQ/regionconnect.git
cd regionconnect
python ./regionconnect/regionconnect.py path_to_ROI_mask path_to_output_text_file

```

## Example
```
python ./regionconnect/regionconnect.py ./test/roi4.nii.gz ./test/results_roi4.txt
```

## Links
To know more details and other resources such as gray matter resources, diffusion tensor template and high angular resolution diffusion imaging template, please go to:
[MRIIT websit](https://www5.iit.edu/~mri/Home.html) and [Neuroimaging Tools & Resources Collaboratory(NITRC)](https://www.nitrc.org/projects/iit/).  

## References
Qi X., Zhang S., Arfanakis K. Enhancement and Evaluation of the White Matter Connectome of the IIT Human Brain Atlas. Proc. Int. Soc. for Magn. Reson. In Med. (ISMRM) 2019.  

## License
For non-commercial usage: IIT license (See LICENSE).  
For commercial usage: Please email to: mri@iit.edu 