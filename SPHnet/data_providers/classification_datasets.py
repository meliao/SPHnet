import os

# preprocess = ['normalize', 'scale', 'rotate', 'jitter', 'kd_tree_idx']


classes = ['airplane', 'bathtub', 'bed', 'bench', 'bookshelf', 'bottle',
           'bowl', 'car', 'chair', 'cone', 'cup', 'curtain', 'desk',
           'door', 'dresser', 'flower_pot', 'glass_box', 'guitar', 'keyboard',
           'lamp', 'laptop', 'mantel', 'monitor', 'night_stand', 'person',
           'piano', 'plant', 'radio', 'range_hood', 'sink', 'sofa', 'stairs',
           'stool', 'table', 'tent', 'toilet', 'tv_stand', 'vase', 'wardrobe', 'xbox']

datset_dir = '/local/meliao/projects/SPHnet/data/modelnet40_ply_hdf5_2048'

train_files_list = os.path.join(datset_dir, 'train_files.txt')
val_files_list = os.path.join(datset_dir, 'test_files.txt')
test_files_list = os.path.join(datset_dir, 'test_files.txt')

"""
train_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original_rotated/data_hdf5')
val_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original_rotated/data_hdf5')
test_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original_rotated/data_hdf5')
"""

# train_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original/data_hdf5')
# val_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original/data_hdf5')
# test_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original/data_hdf5')
train_data_folder = datset_dir
val_data_folder = datset_dir
test_data_folder = datset_dir


modelnet40rotated_augmented = {'name': 'modelnet40rotated_augmented',
                               'num_classes': 40,
                               'classes': classes,
                               'train_data_folder': train_data_folder,
                               'val_data_folder': val_data_folder,
                               'test_data_folder': test_data_folder,
                               'train_files_list': train_files_list,
                               'val_files_list': val_files_list,
                               'test_files_list': test_files_list,
                               # 'train_preprocessing': ['scale', 'rotate', 'kd_tree_idx'],
                               'train_preprocessing': ['rotate', 'scale', 'kd_tree_idx'],
                               'val_preprocessing': ['kd_tree_idx'],
                               'test_preprocessing': ['kd_tree_idx']}

modelnet40rotated = {'name': 'modelnet40aligned',
                     'num_classes': 40,
                     'classes': classes,
                     'train_data_folder': train_data_folder,
                     'val_data_folder': val_data_folder,
                     'test_data_folder': test_data_folder,
                     'train_files_list': train_files_list,
                     'val_files_list': val_files_list,
                     'test_files_list': test_files_list,
                     'train_preprocessing': ['scale', 'kd_tree_idx'],
                     'val_preprocessing': ['kd_tree_idx'],
                     'test_preprocessing': ['kd_tree_idx']}

train_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original/data_hdf5')
val_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original/data_hdf5')
test_data_folder = os.path.join(datset_dir, 'modelnet40_hdf5_2048_original/data_hdf5')

modelnet40aligned = {'name': 'modelnet40aligned',
                     'num_classes': 40,
                     'classes': classes,
                     'train_data_folder': train_data_folder,
                     'val_data_folder': val_data_folder,
                     'test_data_folder': test_data_folder,
                     'train_files_list': train_files_list,
                     'val_files_list': val_files_list,
                     'test_files_list': test_files_list,
                     'train_preprocessing': ['scale', 'kd_tree_idx'],
                     'val_preprocessing': ['kd_tree_idx'],
                     'test_preprocessing': ['kd_tree_idx']}

modelnet40aligned_test_rot = {'name': 'modelnet40aligned_test_rot',
                     'num_classes': 40,
                     'classes': classes,
                     'train_data_folder': train_data_folder,
                     'val_data_folder': val_data_folder,
                     'test_data_folder': test_data_folder,
                     'train_files_list': train_files_list,
                     'val_files_list': val_files_list,
                     'test_files_list': test_files_list,
                     'train_preprocessing': ['scale', 'kd_tree_idx'],
                     'val_preprocessing': ['kd_tree_idx'],
                     'test_preprocessing': ['rotate', 'kd_tree_idx']}


modelnet40rot_y = {'name': 'modelnet40rot_y',
                     'num_classes': 40,
                     'classes': classes,
                     'train_data_folder': train_data_folder,
                     'val_data_folder': val_data_folder,
                     'test_data_folder': test_data_folder,
                     'train_files_list': train_files_list,
                     'val_files_list': val_files_list,
                     'test_files_list': test_files_list,
                     'train_preprocessing': ['scale', 'rotate_y', 'kd_tree_idx'],
                     'val_preprocessing': ['kd_tree_idx'],
                     'test_preprocessing': ['kd_tree_idx']}


datasets_list = [modelnet40rotated_augmented]

