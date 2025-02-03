import os
import numpy as np
import scipy.io as sio
import nibabel as nib

# Define the target size
target_size = (64, 64, 64)

# Define the directories
input_directory  = '/Users/abharian/Downloads/train_intensity/2'
output_directory = '/Users/abharian/Downloads/train_intensity/2_nii'

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)
'''
'''
def pad_to_target_size(data, target_size):
    """Pad the data to the target size with zeros."""
    padded_data = np.zeros(target_size, dtype=data.dtype)
    slices = tuple(slice(0, min(sz, tsz)) for sz, tsz in zip(data.shape, target_size))
    padded_data[slices] = data[slices]
    return padded_data

def convert_mat_to_nii(mat_file_path, nii_file_path, target_size):
    """Convert a .mat file to a .nii file with zero padding."""
    # Load .mat file
    mat_data = sio.loadmat(mat_file_path)
    data = mat_data['intensity']  # Adjust if needed

    # Pad data to target size
    #padded_data = pad_to_target_size(data, target_size)
    padded_data = data
    # Create a NIfTI image
    nifti_img = nib.Nifti1Image(padded_data, np.eye(4))

    # Save NIfTI image
    nib.save(nifti_img, nii_file_path)

# Iterate through .mat files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.mat'):
        mat_file_path = os.path.join(input_directory, filename)
        nii_file_name = os.path.splitext(filename)[0] + '.nii'
        nii_file_path = os.path.join(output_directory, nii_file_name)
        
        convert_mat_to_nii(mat_file_path, nii_file_path, target_size)
        print(f'Converted {filename} to {nii_file_name}')
