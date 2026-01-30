import pandas as pd
import os
import json

# Define paths
base_path = r'd:\Users\axeld\MCIT\VisionLink\VisionLink'
csv_path = os.path.join(base_path, 'archive', 'full_df.csv')
image_dir = os.path.join(base_path, 'archive', 'preprocessed_images')

def prepare_few_shot():
    if not os.path.exists(csv_path):
        print(f"CSV not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    
    # We want a few examples for different labels: N (Normal), D (Diabetic Retinopathy), G (Glaucoma), C (Cataract), A (Age-related Macular Degeneration), H (Hypertension), M (Myopia), O (Others)
    labels = ['N', 'D', 'G', 'C', 'A', 'H', 'M', 'O']
    few_shot_examples = {}

    for label in labels:
        # Filter for rows that have this label in the 'labels' column
        # The 'labels' column looks like "['N']" or "['D', 'H']"
        mask = df['labels'].apply(lambda x: label in eval(x))
        sample = df[mask].head(3) # Take top 3 for each
        
        examples = []
        for _, row in sample.iterrows():
            # Determine if it's left or right eye from the 'filename' or 'filepath'
            # Looking at the CSV sample, 'filename' is like '0_right.jpg'
            is_right = '_right' in row['filename']
            keywords = row['Right-Diagnostic Keywords'] if is_right else row['Left-Diagnostic Keywords']
            
            # Check if image exists
            img_path = os.path.join(image_dir, row['filename'])
            if os.path.exists(img_path):
                examples.append({
                    "image_path": img_path,
                    "label": label,
                    "keywords": keywords
                })
        
        few_shot_examples[label] = examples

    # Output to a json file
    output_path = os.path.join(base_path, 'few_shot_examples.json')
    with open(output_path, 'w') as f:
        json.dump(few_shot_examples, f, indent=4)
    
    print(f"Few-shot examples saved to {output_path}")

if __name__ == "__main__":
    prepare_few_shot()
