import time

def read_input(file):
    max_width = 0
    total_area = 0

    with open(file, 'r') as f:
        data = f.readlines()
        rectangles = []
        for line in data:
            parts = line.split()
            identifier, width, height = parts[0], int(parts[1]), int(parts[2])
            rectangles.append([identifier, width, height])
            max_width = max(max_width, width)
            total_area += width * height

    return rectangles, max_width, total_area



def sort_rectangles(rectangles):
    return sorted(rectangles, key=lambda x: (x[1], x[2]), reverse=True)



def update_skyline(current_skyline, point, rect_height, rect_width):
    if point[0] == 0:
        for i in range(point[1], point[1] + rect_width):
            current_skyline[i] = point[2] + rect_height
    else:
        for i in range(point[1] - rect_width, point[1]):
            current_skyline[i] = point[2] + rect_height

    return current_skyline



def optimize_skyline(current_skyline, rect_width, valid_points_list):
    for i in range(1, len(valid_points_list) - 2):
        if valid_points_list[i][0] == 0 and valid_points_list[i + 1][0] == 1:
            local_min_length = valid_points_list[i + 1][1] - valid_points_list[i][1]
            next_max_height = min(current_skyline[valid_points_list[i][1] - 1],
                                  current_skyline[valid_points_list[i + 1][1]])
            if local_min_length < rect_width:
                for j in range(valid_points_list[i][1], valid_points_list[i + 1][1]):
                    current_skyline[j] = next_max_height

    return current_skyline



def find_valid_points(skyline, box_width):
    points = [[0, 0, skyline[0]]]

    for i in range(box_width - 1):
        if skyline[i] > skyline[i + 1]:
            points.append([0, i + 1, skyline[i + 1]])
        elif skyline[i] < skyline[i + 1]:
            points.append([1, i + 1, skyline[i]])

    points.append([1, box_width, skyline[box_width - 1]])

    return points



def is_valid_placement(rect_height, rect_width, point, skyline):
    if point[0] == 0:
        try:
            for i in range(point[1], point[1] + rect_width):
                if skyline[i] <= point[2]:
                    continue
                else:
                    return False
            return True
        except:
            return False
    else:
        try:
            for i in range(point[1] - rect_width, point[1]):
                if skyline[i] <= point[2]:
                    continue
                else:
                    return False
            return True
        except:
            return False



def pack_rectangles(rectangle_sequence, box_width, total_area):
    output = []
    skyline = [0] * box_width

    for rectangle in rectangle_sequence:
        valid_points_list = find_valid_points(skyline, box_width)
        should_optimize = True

        for i in range(len(valid_points_list) - 1):
            gap = valid_points_list[i][1] - valid_points_list[i + 1][1]
            if gap >= rectangle[1]:
                should_optimize = False
                break

        if should_optimize:
            skyline = optimize_skyline(skyline, rectangle[1], valid_points_list)

        valid_points_list = find_valid_points(skyline, box_width)
        sorted_valid_points = sorted(valid_points_list, key=lambda x: (x[2], x[1]))

        for point in sorted_valid_points:
            if is_valid_placement(rectangle[2], rectangle[1], point, skyline):
                if point[0] == 0:
                    output.append([rectangle[0], point[1], point[2]])
                    update_skyline(skyline, point, rectangle[2], rectangle[1])
                else:
                    output.append([rectangle[0], point[1] - rectangle[1], point[2]])
                    update_skyline(skyline, point, rectangle[2], rectangle[1])
                break

    height = max(skyline)
    efficiency = total_area / (height * box_width)

    return output, efficiency, height



best_efficiency = 0
best_index = 0
start_time = time.perf_counter()

input_rectangles, max_box_width, total_area = read_input("input.txt")

for width in range(max_box_width, max_box_width*5):
    # print("-",end='')
    placement_list, efficiency, final_height = pack_rectangles(sort_rectangles(input_rectangles), width, total_area)
    if best_efficiency < efficiency:
        best_index = width
        best_efficiency = efficiency
print()
print("time(s) - ",time.perf_counter() - start_time)
print("best_efficiency - ",best_efficiency)


placement_list, efficiency, final_height = pack_rectangles(sort_rectangles(read_input("input.txt")[0]), best_index,total_area)
placement_list = sorted(placement_list, key=lambda x: int(x[0][1:]))

with open("output.txt", "w") as file:

    file.write(f"bounding_box {best_index} {final_height}\n")


    for rect in placement_list:
        file.write(f"{rect[0]} {rect[1]} {rect[2]}\n")
