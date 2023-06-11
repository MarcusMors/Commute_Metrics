# Copyright 2023 marcus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gpxpy
import gpxpy.gpx
import numpy as np

import matplotlib.pyplot as plt

def read_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        return gpx

def perpendicular_distance(point, line_start, line_end):
    numerator = abs((line_end[1] - line_start[1]) * point[0] - (line_end[0] - line_start[0]) * point[1] + line_end[0] * line_start[1] - line_end[1] * line_start[0])
    denominator = np.sqrt((line_end[1] - line_start[1]) ** 2 + (line_end[0] - line_start[0]) ** 2)
    distance = numerator / denominator
    return distance



def douglas_peucker(points, epsilon):
    # Find the point with the maximum distance
    dmax = 0
    index = 0
    end = len(points) - 1
    for i in range(1, end):
        d = perpendicular_distance(points[i], points[0], points[end])
        if d > dmax:
            index = i
            dmax = d

    # If max distance is greater than epsilon, recursively simplify both parts
    if dmax > epsilon:
        results1 = douglas_peucker(points[:index + 1], epsilon)
        results2 = douglas_peucker(points[index:], epsilon)
        results = results1[:-1] + results2
    else:
        results = [points[0], points[end]]

    return results


def main():
    file_path = './data/Route from 2023-04-19 09 09_20230419090901.gpx'
    gpx_data = read_gpx_file(file_path)

    points = []
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))

    epsilon = 0.001  # Set your desired epsilon value for grouping points
    grouped_points = douglas_peucker(points, epsilon)
    # Extract latitude and longitude from grouped points
    latitude = [point[0] for point in grouped_points]
    longitude = [point[1] for point in grouped_points]

    # Plot the grouped points
    plt.figure(figsize=(10, 6))
    plt.plot(longitude, latitude, 'b-')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Grouped Points')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
