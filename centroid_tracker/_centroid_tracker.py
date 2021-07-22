import numpy as np
import scipy.spatial

from collections import OrderedDict


class CentroidTracker():
    def __init__(self, max_disappeared=10, max_distance=40):
        self.next_id = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()

        self.max_distance = max_distance
        self.max_disappeared = max_disappeared

        self.object_height = {}

    def register(self, centroid, bounding_box):
        new_id = self._get_new_id()

        self._update_object_height(new_id, bounding_box)
        centroid[1] += self.object_height[new_id]

        self.objects[new_id] = centroid
        self.disappeared[new_id] = 0

    def deregister(self, id):
        del self.objects[id]
        del self.disappeared[id]

    def _get_new_id(self):
        new_id = self.next_id
        self.next_id += 1

        return new_id

    def _update_object_height(self, object_id, bounding_box, weight=2):        
        y1 = bounding_box[1]
        y2 = bounding_box[3]
        new_height = y2 - y1
        if not self.object_height.__contains__(object_id) or \
                new_height > self.object_height[object_id]:
            self.object_height[object_id] = y2 - y1
        else:
            self.object_height[object_id] = (
                self.object_height[object_id] * weight + y2 - y1
            ) / (weight + 1)

    def _get_input_centroids(self, bounding_boxes):
        input_centroids = np.zeros((len(bounding_boxes), 2), dtype="int")

        for i, (x1, y1, x2, y2) in enumerate(bounding_boxes):
            center_x = int((x1 + x2) / 2)
            center_y = int(y1)
            input_centroids[i] = (
                center_x, center_y
            )

        return input_centroids

    def _get_previous_centroids(self):
        previous_ids = list(self.objects.keys())
        previous_centroids = np.array(list(self.objects.values()))
        for i, previous_id in enumerate(previous_ids):
            previous_centroids[i, 1] -= self.object_height[previous_id]

        return previous_centroids, previous_ids

    def _handle_exceptional_cases(self, bounding_boxes, objects):
        exceptional_case = False

        if len(bounding_boxes) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            exceptional_case = True
        elif len(self.objects) == 0:
            input_centroids = self._get_input_centroids(bounding_boxes)
            for i in range(len(input_centroids)):
                self.register(input_centroids[i], bounding_boxes[i])

            exceptional_case = True
        
        return exceptional_case

    def _update_objects(self, distance_matrix, sorted_indices,
            previous_ids, input_centroids, bounding_boxes):
        used_previous_indices = set()
        used_input_indices = set()

        # TODO: Refactor the condition
        for (previous_index, input_index) in sorted_indices:
            if previous_index in used_previous_indices or \
                    input_index in used_input_indices or \
                    distance_matrix[previous_index, input_index] > \
                        self.max_distance:
                continue

            object_id = previous_ids[previous_index]
            new_coordinates = input_centroids[input_index]
            self._update_object(
                object_id,
                new_coordinates,
                bounding_boxes[input_index]
            )

            used_previous_indices.add(previous_index)
            used_input_indices.add(input_index)

        return used_previous_indices, used_input_indices

    def _handle_unused_ids_objects(self, previous_ids, input_centroids,
            used_previous_indices, used_input_indices, bounding_boxes,
            distance_matrix):
        unusedRows = set(
            range(
                0, distance_matrix.shape[0])
            ).difference(used_previous_indices)
        unusedCols = set(
            range(
                0, distance_matrix.shape[1])
            ).difference(used_input_indices)
        for row in unusedRows:
            object_id = previous_ids[row]
            self.disappeared[object_id] += 1

            if self.disappeared[object_id] > self.max_disappeared:
                self.deregister(object_id)
        for col in unusedCols:
            self.register(input_centroids[col], bounding_boxes[col])

    def _assign_ids(self, bounding_boxes):
        exceptional_case = self._handle_exceptional_cases(
            bounding_boxes, self.objects
        )

        if not exceptional_case:
            input_centroids = self._get_input_centroids(bounding_boxes)
            previous_centroids, previous_ids = \
                self._get_previous_centroids()

            distance_matrix = scipy.spatial.distance.cdist(
                previous_centroids, input_centroids
            )

            sorted_indices = np.dstack(
                np.unravel_index(
                    np.argsort(distance_matrix.ravel()),
                    distance_matrix.shape
                )
            )[0]

            used_previous_indices, used_input_indices = \
                self._update_objects(
                    distance_matrix, sorted_indices,
                    previous_ids, input_centroids,
                    bounding_boxes
                )
            
            self._handle_unused_ids_objects(
                previous_ids, input_centroids,
                used_previous_indices, used_input_indices,
                bounding_boxes, distance_matrix
            )

        return self.objects

    def _update_object(self, object_id, new_coordinates, bounding_box):
        self._update_object_height(object_id, bounding_box)

        new_coordinates[1] += self.object_height[object_id]

        self.objects[object_id] = new_coordinates
        self.disappeared[object_id] = 0
        
    def update(self, rects):
        objects = self._assign_ids(rects)
        
        return objects
