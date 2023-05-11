/**
 * This file is part of ORB-SLAM2.
 *
 * Copyright (C) 2014-2016 Raúl Mur-Artal <raulmur at unizar dot es> (University
 * of Zaragoza) For more information see <https://github.com/raulmur/ORB_SLAM2>
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

#ifndef MAP_H
#define MAP_H

#include <mutex>
#include <set>
#include <vector>
#include <map>

#include "KeyFrame.h"
#include "MapPoint.h"
#include "ORBVocabulary.h"

namespace ORB_SLAM2 {

class MapPoint;
class KeyFrame;
class ORBextractor;

class Map {
 public:
  Map();

  void AddKeyFrame(KeyFrame* pKF);
  void AddMapPoint(MapPoint* pMP);
  void EraseMapPoint(MapPoint* pMP);
  void EraseKeyFrame(KeyFrame* pKF);
  void SetReferenceMapPoints(const std::vector<MapPoint*>& vpMPs);
  void clear();
  std::vector<KeyFrame*> GetAllKeyFrames();
  std::vector<MapPoint*> GetAllMapPoints();
  std::vector<MapPoint*> GetReferenceMapPoints();

  long unsigned int MapPointsInMap();
  long unsigned KeyFramesInMap();
  long unsigned int GetMaxKFid();

  bool Save(const std::string& filename);
  bool Load(const std::string& filename, ORBVocabulary& voc);

  vector<KeyFrame*> mvpKeyFrameOrigins;

  std::mutex mMutexMapUpdate;
  // This avoid that two points are created simultaneously in separate threads
  // (id conflict)
  std::mutex mMutexPointCreation;

 protected:
  std::set<MapPoint*> mspMapPoints;
  std::set<KeyFrame*> mspKeyFrames;
  std::vector<MapPoint*> mvpReferenceMapPoints;

  long unsigned int mnMaxKFid;
  std::mutex mMutexMap;

  void _WriteMapPoint(std::ofstream& f, MapPoint* mp);
  void _WriteKeyFrame(std::ofstream& f, KeyFrame* kf,
                      std::map<MapPoint*, unsigned long int>& idx_of_mp);
  MapPoint* _ReadMapPoint(std::ifstream& f);
  KeyFrame* _ReadKeyFrame(std::ifstream& f, ORBVocabulary& voc,
                          std::vector<MapPoint*> amp, ORBextractor* ex);
};

}  // namespace ORB_SLAM2

#endif  // MAP_H
