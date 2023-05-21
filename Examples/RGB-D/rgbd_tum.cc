/**
* This file is part of ORB-SLAM2.
*
* Copyright (C) 2014-2016 Raúl Mur-Artal <raulmur at unizar dot es> (University of Zaragoza)
* For more information see <https://github.com/raulmur/ORB_SLAM2>
*
* ORB-SLAM2 is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* ORB-SLAM2 is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with ORB-SLAM2. If not, see <http://www.gnu.org/licenses/>.
*/


#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#include <opencv2/core/core.hpp>

#include <Frame.h>
#include <System.h>

using namespace std;
struct ORB_SLAM2::DynaParams;

void LoadImages(const string& strAssociationFilename, vector<string>& vstrImageFilenamesRGB,
                vector<string>& vstrImageFilenamesD,  vector<string>& vstrImageFilenamesSeg,
                vector<double>& vTimestamps);

// Usage: ./rgbd_tum /root/catkin_ws/src/MySLAM/Vocabulary/ORBvoc.txt /root/catkin_ws/src/MySLAM/Examples/RGB-D/TUM1.yaml /root/Dataset/fr3_w_xyz /root/Dataset/fr3_w_xyz/associate.txt

int main(int argc, char **argv) {
    if (argc < 5) {
        cerr << endl << "Usage: ./rgbd_tum path_to_vocabulary path_to_settings path_to_sequence path_to_association people_init_score dynamic_thresh alpha beta" << endl;
        return 1;
    }

    // Retrieve paths to images
    vector<string> vstrImageFilenamesRGB;
    vector<string> vstrImageFilenamesD;
    vector<string> vstrImageFilenamesSeg;
    vector<double> vTimestamps;
    string strAssociationFilename = string(argv[4]);
    string strPascalPNG = string(argv[3]) + "/pascal.png";  // yzhao: Used to generate colorful seg results.
    LoadImages(strAssociationFilename, vstrImageFilenamesRGB, vstrImageFilenamesD, vstrImageFilenamesSeg, vTimestamps);

    // Check consistency in the number of images and depthmaps
    int nImages = vstrImageFilenamesRGB.size();
    if (vstrImageFilenamesRGB.empty()) {
        cerr << endl << "No images found in provided path." << endl;
        return 1;
    } else if (vstrImageFilenamesD.size() != vstrImageFilenamesRGB.size()) {
        cerr << endl << "Different number of images for rgb and depth." << endl;
        return 1;
    } else if (vstrImageFilenamesSeg.size() != vstrImageFilenamesRGB.size()) {
        cerr << endl << "Different number of images for rgb and raw_seg." << endl;
        return 1;
    }

    // ORB_SLAM2::Viewer *viewer;
    // viewer = new ORB_SLAM2::Viewer();
    // Create SLAM system. It initializes all system threads and gets ready to process frames.
    // ORB_SLAM2::System SLAM(argv[1], argv[2], strPascalPNG, ORB_SLAM2::System::RGBD, viewer);
    ORB_SLAM2::DynaParams dyna_params;
    if (argc > 5) {
        dyna_params.people_init_score = stod(string(argv[5]));
    }
    if (argc > 6) {
        dyna_params.dynamic_thresh = stod(string(argv[6]));
    }
    if (argc > 7) {
        dyna_params.alpha = stod(string(argv[7]));
    }
    if (argc > 8) {
        dyna_params.beta = stod(string(argv[8]));
    }

    ORB_SLAM2::System SLAM(argv[1], argv[2], strPascalPNG, dyna_params, ORB_SLAM2::System::RGBD);

    // Vector for tracking time statistics
    vector<float> vTimesTrack;
    vTimesTrack.resize(nImages);

    cout << endl << "-------" << endl;
    cout << "Start processing sequence ..." << endl;
    cout << "Images in the sequence: " << nImages << endl << endl;

    // Main loop
    cv::Mat imRGB, imD, imSeg;
    for (int ni = 0; ni < nImages; ni++) {
        // Read image and depthmap from file
        imRGB = cv::imread(string(argv[3]) + "/" + vstrImageFilenamesRGB[ni], CV_LOAD_IMAGE_UNCHANGED);
        imD = cv::imread(string(argv[3]) + "/" + vstrImageFilenamesD[ni], CV_LOAD_IMAGE_UNCHANGED);
        imSeg = cv::imread(string(argv[3]) + "/" + vstrImageFilenamesSeg[ni], CV_LOAD_IMAGE_UNCHANGED);
        double tframe = vTimestamps[ni];

        if (imRGB.empty()) {
            cerr << endl << "Failed to load image at: "
                 << string(argv[3]) << "/" << vstrImageFilenamesRGB[ni] << endl;
            return 1;
        }

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t1 = std::chrono::monotonic_clock::now();
#endif

        // Pass the image to the SLAM system
        SLAM.TrackRGBD(imRGB, imD, imSeg, tframe);

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t2 = std::chrono::monotonic_clock::now();
#endif

        double ttrack = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1).count();

        vTimesTrack[ni] = ttrack;

        // Wait to load the next frame
        double T = 0;
        if (ni < nImages - 1) {
            T = vTimestamps[ni + 1] - tframe;
        } else if (ni > 0) {
            T = tframe - vTimestamps[ni - 1];
        }
        
        if (ttrack < T) {
            usleep((T - ttrack) * 1e6);
        }
    }

    // Stop all threads
    SLAM.Shutdown();

    // Tracking time statistics
    sort(vTimesTrack.begin(), vTimesTrack.end());
    float totaltime = 0;
    for(int ni = 0; ni < nImages; ni++) {
        totaltime += vTimesTrack[ni];
    }
    cout << "-------" << endl << endl;
    cout << "median tracking time: " << vTimesTrack[nImages / 2] << endl;
    cout << "mean tracking time: " << totaltime / nImages << endl;

    // Save camera trajectory
    SLAM.SaveTrajectoryTUM("CameraTrajectory.txt");
    SLAM.SaveKeyFrameTrajectoryTUM("KeyFrameTrajectory.txt");   

    return 0;
}

void LoadImages(const string& strAssociationFilename, vector<string>& vstrImageFilenamesRGB,
                vector<string>& vstrImageFilenamesD, vector<string>& vstrImageFilenamesSeg,
                vector<double>& vTimestamps) {
    cout << "Loading images from " << strAssociationFilename << " ..." << endl;
    std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();
    ifstream fAssociation;
    fAssociation.open(strAssociationFilename.c_str());
    while (!fAssociation.eof()) {
        string s;
        getline(fAssociation,s);
        // cout << s << endl;
        if (!s.empty()) {
            stringstream ss;
            ss << s;
            double t;
            string sRGB, sD, sSeg;
            ss >> t;
            vTimestamps.push_back(t);
            ss >> sRGB;
            vstrImageFilenamesRGB.push_back(sRGB);
            sSeg = "raw_seg/" + to_string(t) + ".png";
            vstrImageFilenamesSeg.push_back(sSeg);
            ss >> t;
            ss >> sD;
            vstrImageFilenamesD.push_back(sD);
            // cout << sSeg << " read." << endl;
        }
    }
    std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
    double image_loading_time = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1).count();
    cout << "Loading completed in " << image_loading_time << " ms." << endl;
}
