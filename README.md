# EMVA Dataset
A code repository to complement the EMVA dataset (www.emva-dataset.org)

### Sample Code
This repository provides sample code that aims to facilitate the use of the Everyday Mobile Visual Attention (EMVA) dataset. 
In this dataset, we have collected videos from the front-facing camera of smartphones as well as associated meta data to better understand visual attention and mobile phone usage, in general.

### Installing Dependencies
The code samples require a Python environment (tested with version 3.7) and the OpenCV python package.
For easier management of different Python environments and dependencies, we recommend Anaconda (https://anaconda.org).

Once the Python environment has been set up, please install the required dependencies using the following command: `pip install -r requirements.txt`. 
This will install the correct OpenCV version, i.e. the one we have tested. Other versions of OpenCV should also work.

### Running the Sample Code

Run the sample code with the following command: `python examples.py`

The sample code helps users to associate meta data from the dataset (e.g. the application running in the foreground or the users' activity) with the image frames from every video recording.

For example, the function `analyseApplication` from the `examples.py` file will associate the application that was running in the foreground (i.e. the application the user was using) with the image frames. 
This association is based on timestamps.
If you have managed to successfully run the sample code, you should see an output like below:

```
...
Time: 171.8s , App: com.netflix.mediaclient
Time: 171.84s , App: com.netflix.mediaclient
Time: 171.87s , App: com.netflix.mediaclient
Time: 171.9s , App: com.netflix.mediaclient
Time: 171.94s , App: com.netflix.mediaclient
Time: 171.97s , App: com.netflix.mediaclient
Time: 172.01s , App: com.netflix.mediaclient
Time: 172.04s , App: com.netflix.mediaclient
Time: 172.07s , App: com.netflix.mediaclient
Time: 172.11s , App: com.netflix.mediaclient
Time: 172.14s , App: com.netflix.mediaclient
Time: 172.18s , App: com.netflix.mediaclient
Time: 172.21s , App: com.netflix.mediaclient
Time: 172.24s , App: com.netflix.mediaclient
Time: 172.28s , App: com.netflix.mediaclient
Time: 172.31s , App: com.netflix.mediaclient
Time: 172.35s , App: com.netflix.mediaclient
Time: 172.38s , App: com.netflix.mediaclient
Time: 172.41s , App: com.netflix.mediaclient
Time: 172.45s , App: com.netflix.mediaclient
...

```

For each image frame, the above sample code will print the time from the beginning of the video recording and the application packaged that the user was using at that time.

### Reference

If you use any of the code from this repository in your work or publications, please cite the following paper:

- Mihai Bâce, Sander Staal, and Andreas Bulling. 2020. Quantification of Users’ Visual Attention During Everyday Mobile Device Interactions. In Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems (CHI ’20). Association for Computing Machinery, New York, NY, USA, 1–14. DOI:https://doi.org/10.1145/3313831.3376449
