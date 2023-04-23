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
