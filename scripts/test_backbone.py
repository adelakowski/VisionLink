import os
import keras_nlp
import keras

print("Testing Backbone Loading...")
try:
    # Attempt to load only the backbone from the local preset
    # We point to the same directory; the backbone config is usually embedded or separate.
    # from_preset on Backbone usually looks for config.json of the backbone.
    # The extracted directory has 'config.json' which is likely the task config.
    # But let's try.
    backbone = keras_nlp.models.PaliGemmaBackbone.from_preset(
        r"d:\Users\axeld\MCIT\VisionLink\VisionLink\pali_gemma_local_model",
        load_weights=True
    )
    print("Backbone loaded successfully!")
except Exception as e:
    print(f"Backbone load failed: {e}")
