# Simple centroid tracker

A simple centroid tracker intended for people tracking.

Based on: [Centroid-Based_Object_Tracking](https://github.com/lev1khachatryan/Centroid-Based_Object_Tracking)

# Notice
This is a personal project under development. All bug reports and feature requests are welcome.

# Prerequisites
1. numpy (tested with 1.19.4)
2. scipy (tested with 1.5.4)

# Installation
```bash
python3 -m pip install https://github.com/sandstorm12/simple_centroid_tracker
```

# Usage
```python
from centroid_tracker import CentroidTracker

tracker = CentroidTrackre(max_disappeared=10, max_distance=40)

# Get bounding boxes from your detector
# bounding_boxes = [[x1, y1, x2, y2], ...]

objects = tracker.update(bounding_boxes)

# Objects is a list of objects being tracked
# Each element is a tuple with id and centroid coordinates
# objects = [(id, (x, y))]
```

# Urgent issues and future work
1. [nothing yet]

# Issues and future work
1. Possible performance optimization

# Contributors
1. Hamid Mohammadi: <sandstormeatwo@gmail.com>
