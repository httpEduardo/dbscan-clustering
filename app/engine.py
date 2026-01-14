import math


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def region_query(points, idx, eps):
    return [i for i, point in enumerate(points) if distance(points[idx], point) <= eps]


def dbscan(points, eps=1.2, min_pts=3):
    labels = [-1] * len(points)
    cluster_id = 0
    visited = set()

    for idx in range(len(points)):
        if idx in visited:
            continue
        visited.add(idx)
        neighbors = region_query(points, idx, eps)
        if len(neighbors) < min_pts:
            labels[idx] = -1
            continue
        labels[idx] = cluster_id
        seeds = [n for n in neighbors if n != idx]
        while seeds:
            current = seeds.pop()
            if current not in visited:
                visited.add(current)
                current_neighbors = region_query(points, current, eps)
                if len(current_neighbors) >= min_pts:
                    for neighbor in current_neighbors:
                        if neighbor not in seeds:
                            seeds.append(neighbor)
            if labels[current] == -1:
                labels[current] = cluster_id
        cluster_id += 1

    return labels
