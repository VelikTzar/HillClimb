import math
import random


def mapv(v, ol, oh, nl, nh):
    """maps the value `v` from old range [ol, oh] to new range [nl, nh]
    """
    return nl + (v * ((nh - nl) / (oh - ol)))


def terrain_naive(count, height=100):
    """returns the list of integers representing height at each point.
    """
    return [
        mapv(random.random(), 0, 1, 0, height)
        for i in range(count)
    ]


def linp(a, b, mu):
    """returns the intermediate point between `a` and `b`
    which is `mu` factor away from `a`.
    """
    return a * (1 - mu) + b * mu


def terrain_linp(naive_terrain, sample=4):
    """Using naive terrain `naive_terrain` the function generates
    Linearly Interpolated terrain on sample data.
    """
    terrain = []

    # get every `sample point from the naive terrain.
    sample_points = naive_terrain[::sample]

    # for every point in sample point denoting
    for i in range(len(sample_points)):

        # add current peak (sample point) to terrain.
        terrain.append(sample_points[i])

        # fill in `sample - 1` number of intermediary points using
        # linear interpolation.
        for j in range(sample - 1):
            # compute relative distance from the left point
            mu = (j + 1)/sample

            # compute interpolated point at relative distance of mu
            a = sample_points[i]
            b = sample_points[(i + 1) % len(sample_points)]
            v = linp(a, b, mu)

            # add an interpolated point to the terrain
            terrain.append(v)

    # return the terrain
    return terrain


def cosp(a, b, mu):
    """returns the intermediate point between `a` and `b`
    which is `mu` factor away from `a`.
    """
    mu2 = (1 - math.cos(mu * math.pi)) / 2
    return a * (1 - mu2) + b * mu2


def terrain_cosp(naive_terrain, sample=4):
    """Using naive terrain `naive_terrain` the function generates
    Cosine Interpolated terrain on sample data.
    """
    terrain = []

    # get every `sample point from the naive terrain.
    sample_points = naive_terrain[::sample]

    # for every point in sample point denoting
    for i in range(len(sample_points)):

        # add current peak (sample point) to terrain.
        terrain.append(sample_points[i])

        # fill in `sample - 1` number of intermediary points using
        # linear interpolation.
        for j in range(sample - 1):
            # compute relative distance from the left point
            mu = (j + 1)/sample

            # compute interpolated point at relative distance of mu
            a = sample_points[i]
            b = sample_points[(i + 1) % len(sample_points)]
            v = cosp(a, b, mu)

            # add an interpolated point to the terrain
            terrain.append(v)

    # return the terrain
    return terrain


def terrain_superpos_linp(naive_terrain, iterations=8):
    """Using naive terrain `naive_terrain` the function generates
    Linearly Interpolated Superpositioned terrain that looks real world like.
    """
    terrains = []

    # holds the sum of weights for normalization
    weight_sum = 0

    # for every iteration
    for z in range(iterations, 0, -1):
        terrain = []

        # compute the scaling factor (weight)
        weight = 1 / (2 ** (z - 1))

        # compute sampling frequency suggesting every `sample`th
        # point to be picked from the naive terrain.
        sample = 1 << (iterations - z)

        # get the sample points
        sample_points = naive_terrain[::sample]

        weight_sum += weight

        for i in range(len(sample_points)):

            # append the current sample point (scaled) to the terrain
            terrain.append(weight * sample_points[i])

            # perform interpolation and add all interpolated values to
            # to the terrain.
            for j in range(sample - 1):
                # compute relative distance from the left point
                mu = (j + 1) / sample

                # compute interpolated point at relative distance of mu
                a = sample_points[i]
                b = sample_points[(i + 1) % len(sample_points)]
                v = linp(a, b, mu)

                # add interpolated point (scaled) to the terrain
                terrain.append(weight * v)

        # append this terrain to list of terrains preparing
        # it to be superpositioned.
        terrains.append(terrain)

    # perform super position and normalization of terrains to
    # get the final terrain
    return [sum(x)/weight_sum for x in zip(*terrains)]


def terrain_superpos_cosp(naive_terrain, iterations=8):
    """Using naive terrain `naive_terrain` the function generates
    Cosine Interpolated Superpositioned terrain that looks real world like.
    """
    terrains = []

    # holds the sum of weights for normalization
    weight_sum = 0

    # for every iteration
    for z in range(iterations, 0, -1):
        terrain = []

        # compute the scaling factor (weight)
        weight = 1 / (2 ** (z - 1))

        # compute sampling frequency suggesting every `sample`to
        # point to be picked from the naive terrain.
        sample = 1 << (iterations - z)

        # get the sample points
        sample_points = naive_terrain[::sample]

        weight_sum += weight

        for i in range(len(sample_points)):

            # append the current sample point (scaled) to the terrain
            terrain.append(weight * sample_points[i])

            # perform interpolation and add all interpolated values to
            # to the terrain.
            for j in range(sample - 1):
                # compute relative distance from the left point
                mu = (j + 1) / sample

                # compute interpolated point at relative distance of mu
                a = sample_points[i]
                b = sample_points[(i + 1) % len(sample_points)]
                v = cosp(a, b, mu)

                # add interpolated point (scaled) to the terrain
                terrain.append(weight * v)

        # append this terrain to list of terrains preparing
        # it to be superpositioned.
        terrains.append(terrain)

    # perform super position and normalization of terrains to
    # get the final terrain
    return [sum(x)/weight_sum for x in zip(*terrains)]


def return_terrain_height_cos(count, height = 100, smoothness=8):
    return terrain_superpos_cosp(terrain_naive(count, height), smoothness)