
import os
import argparse
import keras
import keras_nlp
import tensorflow as tf # For input pipeline if needed, or stick to native Keras
# Note: Keras 3 works with JAX, Torch, TF. We'll use JAX or Torch backend ideally for Gemma, 
# but KerasNLP defaults are usually optimized.
# For Vertex AI L4, JAX is often fastest for PaliGemma.

# Set backend to JAX or Torch. JAX is great for TPUs/GPUs with KerasNLP.
os.environ["KERAS_BACKEND"] = "jax"

def train(args):
    print(f"Starting training on {args.bucket_dir}...")
    
    # 1. Load Model
    # PaliGemma 3B Mix 224
    # We use the preset.
    print("Loading PaliGemma preset...")
    model = keras_nlp.models.PaliGemmaCausalLM.from_preset("pali_gemma_3b_mix_224")

    # 2. Enable LoRA
    # Fine-tine top K layers or specific modules. 
    # KerasNLP makes this easy with `enable_lora`.
    # rank=4 is a consistent default for efficiency.
    print("Enabling LoRA...")
    model.backbone.enable_lora(rank=4)
    
    # Verify trainable weights (should be small % of total)
    model.summary()

    # 3. Load Data
    # For this script, we assume data is prepared in a format amenable to tf.data or similar.
    # PROMPT: "detect signs of diabetic retinopathy and glaucoma, and describe the optic disc and macula"
    # This is a dummy data loader for the skeleton. 
    # In a real run, we'd load generated JSON pairs from Phase 1.
    
    # Example dummy data for checking compile status
    # images = np.random.rand(2, 224, 224, 3)
    # prompts = ["describe condition", "describe condition"]
    # labels = ["healthy", "glaucoma"]
    
    # 4. Compile
    # Use typically AdamW for LLMs
    learning_rate = 1e-5
    optimizer = keras.optimizers.AdamW(
        learning_rate=learning_rate,
        weight_decay=0.01,
    )
    
    # Loss: SparseCategoricalCrossentropy is standard for Causal LM, 
    # but PaliGemmaCausalLM usually handles loss internally or we specify it.
    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        optimizer=optimizer,
        metrics=[keras.metrics.SparseCategoricalAccuracy()],
    )

    print("Model compiled. Ready for training loop.")
    # model.fit(...) 
    
    # 5. Save Model
    # Save the LoRA weights specifically or the whole model.
    # On Vertex, we check the AIP_MODEL_DIR or default export path.
    export_path = os.environ.get("AIP_MODEL_DIR", "model_output")
    print(f"Saving model to {export_path}...")
    model.save(export_path) # Saves the fine-tuned adapter + base configuration

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_dir", type=str, default="gs://visionlink-data", help="GCS Bucket for data")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()
    
    train(args)
