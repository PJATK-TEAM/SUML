import kagglehub
import os
import shutil
import random

# Download dataset
print("📦 Downloading dataset from KaggleHub...")
path = kagglehub.dataset_download("harshwalia/birds-vs-drone-dataset")

source_data_dir = os.path.join(path, "BirdVsDrone")
#source_data_dir = os.path.join("/Users/mbartuzi/.cache/kagglehub/datasets/harshwalia/birds-vs-drone-dataset/versions/1/BirdVsDrone", "preprocessed")
print("✅ Dataset downloaded to:", source_data_dir)

# Split dataset for training, validation and testing data
def split_dataset(src_dir, dest_dir, split=(0.9, 0.05, 0.05), seed=42):
    random.seed(seed)
    
    # for birds and drones
    classes = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]

    for cls in classes:
        cls_src = os.path.join(src_dir, cls)
        images = [f for f in os.listdir(cls_src) if os.path.isfile(os.path.join(cls_src, f))]
        random.shuffle(images)

        train_split = int(len(images) * split[0])
        val_split = int(len(images) * split[1])

        splits = {
            'train': images[:train_split],
            'val': images[train_split:train_split + val_split],
            'test': images[train_split + val_split:]
        }

        for split_name, files in splits.items():
            split_path = os.path.join(dest_dir, split_name, cls)
            os.makedirs(split_path, exist_ok=True)
            for fname in files:
                shutil.copy(os.path.join(cls_src, fname), os.path.join(split_path, fname))


# store data in local folder
output_dir = "./data_split"
print(f"🗂️ Splitting dataset into train/val/test in: {output_dir}")
split_dataset(source_data_dir, output_dir, split=(0.9, 0.05, 0.05))
print("✅ Data split completed.")

# output folder
DATASET_DIR = output_dir 
print(f"output path for set: {output_dir}")
