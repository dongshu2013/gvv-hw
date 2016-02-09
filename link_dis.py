def test_1():
    probes, links = read_data()
    print "Data loaded"
    info = nearest_link_and_height(links, [2, 4, 5, 9], probes[0])
    print "Probe: %s, Link: %s, Height: %f" % (probes[0], links[info[0]][0], info[1])


def nearest_link_and_height(links, link_candidates, probe):
    dists = {}
    for idx in link_candidates:
        # compute distance from probe to each link point
        min_height = probe_to_link_dist(links[idx], probe)
        dists[idx] = min_height

    # select link from link candidates
    return min(dists.items(), key=lambda x: x[1])


def probe_to_link_dist2(link_points, probe):
    dists = {}
    for link_point in link_points:
        dists[link_point] = compute_dist(link_point, probe)

    heights = []
    for i in range(len(link_points) - 1):
        l1_to_l2 = compute_dist(link_points[i], link_points[i+1])
        p_to_l1 = dists[link_points[i]]
        p_to_l2 = dists[link_points[i+1]]
        heights.append(compute_height(p_to_l1, p_to_l2, l1_to_l2))
    return min(heights)


def probe_to_link_dist(link_points, probe):
    size = len(link_points)
    l1_to_l2 = compute_dist(link_points[0], link_points[size - 1])
    p_to_l1 = compute_dist(probe, link_points[0])
    p_to_l2 = compute_dist(probe, link_points[size - 1])
    return compute_height(p_to_l1, p_to_l2, l1_to_l2)


def compute_height(p_to_l1, p_to_l2, l1_to_l2):
    p = (p_to_l1 + p_to_l2 + l1_to_l2) / 2
    s = math.sqrt(p * (p - p_to_l1) * (p - p_to_l2) * (p - l1_to_l2))
    height = 2 * s / l1_to_l2
    return height

