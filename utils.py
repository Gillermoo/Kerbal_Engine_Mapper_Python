import numpy as np


def pareto(X: np.ndarray, directions: list) -> np.ndarray:
    """
    Return only the points in an array that lie on the Pareto frontier of an optimization problem.

    Parameters:
    -----------
    X : numpy.ndarray
        An array of shape (n_samples, n_features) containing the points to evaluate.
    directions : numpy.ndarray
        An array of shape (n_objectives, n_features) representing the direction
        of each objective function.

    Returns:
    --------
    numpy.ndarray
        A 1D array containing the indices of the non-dominated points in X.
    """
    costs = X * directions
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index < len(costs):
        nondominated_point_mask = np.any(costs > costs[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index]) + 1

    return is_efficient


def get_allow_engines():
    return {
        'Spider': True,
        'Twitch': True,
        'Thud': True,
        'Ant': True,
        'Spark': True,
        'Terrier': True,
        'Reliant': True,
        'Swivel': True,
        'Vector': True,
        'Dart': True,
        'Nerv': True,
        'Poodle': True,
        'Skipper': True,
        'Mainsail': True,
        'Twin-Boar': True,
        'Rhino': True,
        'Mammoth': True,
        'R.A.P.I.E.R.': True,
        'Dawn': True,
        'Mastodon': True,
        'Cheetah': True,
        'Bobcat': True,
        'Skiff': True,
        'Wolfhound': True,
        'Kodiak': True,
        'Cub': True,
        'Flea': True,
        'Hammer': True,
        'Thumper': True,
        'Kickback': True,
        'Sepratron I': True,
        'Shrimp': True,
        'Mite': True,
        'Thoroughbred': True,
        'Clydesdale': True,
        'Pullox': True}

def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np


    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(0, nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap
