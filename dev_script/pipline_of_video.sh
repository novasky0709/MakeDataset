#!/bin/bash


dataset_src="data_src/test"
gpu_ids="0"
video_interval="10"
video_offset="20"

cd run


python preprocess_video_input.py \
       --dataset_src $dataset_src \
       --gpu_ids $gpu_ids \
       --video_interval $video_interval \
       --video_offset $video_offset

cd ..
cd $dataset_src/colmap_result

colmap feature_extractor \
  --database_path ./database.db \
  --image_path ../images \
  --ImageReader.camera_model SIMPLE_RADIAL \
  --SiftExtraction.max_image_size 4096

colmap exhaustive_matcher \
 --database_path ./database.db


mkdir sparse
colmap mapper \
    --database_path ./database.db \
    --image_path ../images \
    --output_path ./sparse \
    --Mapper.ba_refine_principal_point true

colmap model_converter \
    --input_path ./sparse/0 \
    --output_path ./sparse/0 \
    --output_type TXT

mkdir dense
colmap image_undistorter \
    --image_path ../images \
    --input_path ./sparse/0 \
    --output_path ./dense \
    --output_type COLMAP \
    --max_image_size 3840

colmap patch_match_stereo \
    --workspace_path ./dense \
    --workspace_format COLMAP \
    --PatchMatchStereo.max_image_size 3840 \
    --PatchMatchStereo.window_radius 9 \
    --PatchMatchStereo.geom_consistency true \
    --PatchMatchStereo.filter_min_ncc 0.07

colmap stereo_fusion \
    --workspace_path ./dense \
    --workspace_format COLMAP \
    --input_type geometric \
    --output_path ./dense/fused.ply

colmap poisson_mesher \
    --input_path ./dense/fused.ply \
    --output_path ./dense/meshed-poisson.ply


cd ../../../run

python preprocess_video_input.py \
       --dataset_src $dataset_src \
       --gpu_ids $gpu_ids \
       --video_interval $video_interval \
       --video_offset $video_offset