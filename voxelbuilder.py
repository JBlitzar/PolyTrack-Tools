import numpy as np
import trimesh
from trackbuilder import TrackBuilder
from tqdm import tqdm

class VoxelBuilder(TrackBuilder):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)

    def load_mesh(self, file_path):
        mesh = trimesh.load(file_path)
        return mesh


    def scale_mesh(self, mesh, scale_factor):

        scale_matrix = np.eye(4)
        scale_matrix[:3, :3] *= scale_factor

        mesh.apply_transform(scale_matrix)
        return mesh

    def scale_y_values(self, mesh, y_scale_factor):

        y_scale_matrix = np.eye(4)
        y_scale_matrix[1, 1] *= y_scale_factor

        mesh.apply_transform(y_scale_matrix)
        return mesh

    def adjust_y_values(self, array):

        y_values = array[:, 1]

        min_y = np.min(y_values)

        array[:, 1] += np.abs(min_y)


        y_values = array[:, 1]

        min_y = np.min(y_values)

        array[:, 1] -= np.abs(min_y)


        return array


    def voxelize_mesh(self, mesh, voxel_size):

        voxelized = mesh.voxelized(pitch=voxel_size)

        filled_voxels = voxelized.fill()
        return filled_voxels
    
    def add_file(self, file_path, scale_factor=2):
        mesh = self.load_mesh(file_path)

        mesh = self.scale_mesh(mesh, scale_factor)

        mesh = self.scale_y_values(mesh, 4)

        filled_voxels = self.voxelize_mesh(mesh, 1)

        voxel_coords = filled_voxels.points

        voxel_coords = self.adjust_y_values(voxel_coords)

        for coord in tqdm(voxel_coords):
            self.add_piece(self.get_id_alias("block"), int(coord[0]), int(coord[1]), int(coord[2]), 0, None)

