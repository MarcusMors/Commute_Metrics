# Copyright 2023 marcus
# More details below

# import gmplo  t
import gpxpy
import gpxpy.gpx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize, LinearSegmentedColormap

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


def calculate_velocity(point1, point2):
    distance = point1.distance_2d(point2)
    time_diff = (point2.time - point1.time).total_seconds()
    velocity = distance / time_diff if time_diff != 0 else 0
    return velocity

# def get_total_average_velocity(velocities):
#     average = sum(velocities) / len(velocities)
#     return average


def main():
    subject = "subject_2"
    file_path = './data/'+subject+'--1.gpx'
    gpx_data = read_gpx_file(file_path)

    points = []
    velocities = []
    distance = 0.0
    for track in gpx_data.tracks:
        for segment in track.segments:
            for i in range(len(segment.points) - 1):
                point1 = segment.points[i]
                point2 = segment.points[i + 1]
                distance += point1.distance_2d(point2)
                velocity = calculate_velocity(point1, point2)

                points.append((point1.latitude, point1.longitude))
                velocities.append(velocity)

    average_velocity = sum(velocities) / len(velocities)
    print(f"average_velocity : {average_velocity}")
    print(f"distance : {distance}")

    epsilon = 0.0003 # 0.001 might be also good
    print("points len: ", len(points))
    grouped_points = douglas_peucker(points, epsilon)
    print("grouped points len: ", len(grouped_points))
    print("len(velocities) :",len(velocities))


    g_it = 1
    p_it = 1
    v_it = 1

    velocity_sum = velocities[0]
    velocity_count = 1
    grouped_velocities = []
    min_velocity = 1000000
    max_velocity = -1000000


    while p_it < len(points):
        velocity_sum += velocities[v_it]

        if points[p_it] == grouped_points[g_it]:
            grouped_velocities.append(velocity_sum/velocity_count)
            if grouped_velocities[-1] > max_velocity:
                max_velocity = grouped_velocities[-1]
            elif grouped_velocities[-1] < min_velocity:
                min_velocity = grouped_velocities[-1]
            velocity_sum = velocities[v_it]
            velocity_count = 1
            g_it = g_it+1

        p_it += 1
        v_it += 1
        velocity_count += 1

    print("len(grouped_velocities):",len(grouped_velocities))
    print("grouped_velocities:\t",grouped_velocities)
    print("max_velocity:\t",max_velocity)
    print("min_velocity:\t",min_velocity)

    latitude = [point[0] for point in grouped_points]
    longitude = [point[1] for point in grouped_points]

    if velocities:
        normalized_grouped_velocities = (np.array(grouped_velocities) - min_velocity) / (max_velocity - min_velocity)

    normalized_grouped_velocities = abs(normalized_grouped_velocities)
    # for v in normalized_grouped_velocities:
    #     v = abs(v)


    cmap = plt.get_cmap('coolwarm_r')
    norm = Normalize(vmin=min_velocity, vmax=max_velocity)

    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(grouped_points) - 1):
        x = [longitude[i], longitude[i + 1]]
        y = [latitude[i], latitude[i + 1]]

        t_color = cmap(normalized_grouped_velocities[i])
        ax.plot(x, y, color=t_color, linewidth=2)
        print("%i = %.2f" %(i,normalized_grouped_velocities[i]))

    cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), label='Normalized Velocity')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Grouped Points with Speed Gradient')
    plt.grid(True)

    save_path = "./"+subject+".png"
    plt.savefig(save_path)
    plt.show()




if __name__ == "__main__":
    main()


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
