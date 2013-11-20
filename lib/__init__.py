from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution('homekeeper')
    if not __file__.startswith(os.path.join(_dist.location, 'homekeeper')):
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'please install this project with setup.py'
else:
    __version__ = _dist.version
