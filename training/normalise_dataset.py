import cv2
import os

CROP_SIZE = 120  # square size: 120px x 120px
HALF_CROP = CROP_SIZE // 2

def adjust_crop_center(x, y, img_width, img_height):
    #make sure image can be cropped in the middle for X axis
    x = max(HALF_CROP, min(x, img_width - HALF_CROP))
    #make sure image can be cropped in the middle for Y axis
    y = max(HALF_CROP, min(y, img_height - HALF_CROP))
    return x, y


def crop_around_center(img, center_x, center_y):
    x1 = center_x - HALF_CROP
    y1 = center_y - HALF_CROP
    x2 = center_x + HALF_CROP
    y2 = center_y + HALF_CROP

    return img[y1:y2, x1:x2]

def process_images(image_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for image_file in image_files:
        img_path = os.path.join(image_folder, image_file)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Could not load image: {image_file}")
            continue

        h, w = img.shape[:2]

        def on_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                x_adj, y_adj = adjust_crop_center(x, y, w, h)
                cropped = crop_around_center(img, x_adj, y_adj)

                if cropped.shape[:2] == (CROP_SIZE, CROP_SIZE):
                    save_path = os.path.join(output_folder, f"crop_{image_file}")
                    cv2.imwrite(save_path, cropped)
                    print(f"Image saved: {save_path}")
                else:
                    print(f"Error while saving: {image_file}, size: {cropped.shape}")

                cv2.destroyAllWindows()

        cv2.imshow('mouse click - pick center point; ESC - skip', img)
        cv2.setMouseCallback('mouse click - pick center point; ESC - skip', on_click)
        key = cv2.waitKey(0)
        if key == 27:
            cv2.destroyAllWindows()


# input with raw data
#input_dir = '/Users/mbartuzi/.cache/kagglehub/datasets/harshwalia/birds-vs-drone-dataset/versions/1/BirdVsDrone/Drones'  # Folder wejściowy z obrazami
# output for croppped files
#output_dir = '/Users/mbartuzi/.cache/kagglehub/datasets/harshwalia/birds-vs-drone-dataset/versions/1/BirdVsDrone/preprocessed_d'  # Folder, w którym zapiszesz przycięte obrazy

# execute function to crop selected area
#process_images(input_dir, output_dir)


