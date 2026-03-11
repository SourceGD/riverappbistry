class CameraCalibration:
    def __init__(self, camera_matrix=None):
        self.camera_matrix = camera_matrix if camera_matrix is not None else self.get_default_camera_matrix()

    @classmethod
    def from_dict(cls, data):
        return cls(camera_matrix=data.get('camera_matrix'))

    @classmethod
    def from_json(cls, json_str):
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)

    def get_default_camera_matrix(self):
        import numpy as np
        return np.eye(3)  # Identity matrix as default

    def generate_camera_matrix(self, focal_length, sensor_width, sensor_height):
        # Example of camera matrix generation
        cx = sensor_width / 2
        cy = sensor_height / 2
        return [[focal_length, 0, cx], 
                [0, focal_length, cy], 
                [0, 0, 1]]

class CameraPose:
    def __init__(self, rotation_matrix=None, translation_vector=None):
        self.rotation_matrix = rotation_matrix if rotation_matrix is not None else self.get_default_rotation_matrix()
        self.translation_vector = translation_vector if translation_vector is not None else self.get_default_translation_vector()

    @classmethod
    def from_dict(cls, data):
        return cls(rotation_matrix=data.get('rotation_matrix'), 
                   translation_vector=data.get('translation_vector'))

    @classmethod
    def from_json(cls, json_str):
        import json
        data = json.loads(json_str)
        return cls.from_dict(data)

    def get_default_rotation_matrix(self):
        import numpy as np
        return np.eye(3)  # Identity matrix as default

    def get_default_translation_vector(self):
        import numpy as np
        return np.zeros(3)  # Zero vector as default

    def generate_pose_transformation_matrix(self):
        import numpy as np
        T = np.eye(4)
        T[:3, :3] = self.rotation_matrix
        T[:3, 3] = self.translation_vector
        return T