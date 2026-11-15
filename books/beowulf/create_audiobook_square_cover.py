import os
from PIL import Image, ImageOps

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_COVER = os.path.join(SCRIPT_DIR, "cover_ko.jpg")
DST_COVER = os.path.join(SCRIPT_DIR, "cover_audio_ko.jpg")

def main():
    if not os.path.exists(SRC_COVER):
        print(f"[ERROR] Source cover not found: {SRC_COVER}")
        return

    print("Generating 3000x3000px Square Audiobook Cover Art...")
    img = Image.open(SRC_COVER).convert("RGB")
    
    # Target size 3000x3000px
    target_size = (3000, 3000)

    # Use ImageOps.fit or pad with background color matching top/bottom
    # Extract background color from top-left pixel
    bg_color = img.getpixel((10, 10))

    # Center crop / pad to square
    w, h = img.size
    min_dim = min(w, h)
    
    # Crop to 1:1 square centered around top portion (artwork + text)
    crop_box = (0, 0, w, w) if h >= w else (0, 0, h, h)
    img_square = img.crop(crop_box)
    
    img_resized = img_square.resize(target_size, Image.Resampling.LANCZOS)
    img_resized.save(DST_COVER, format="JPEG", quality=95)

    size_mb = os.path.getsize(DST_COVER) / (1024 * 1024)
    print(f"[SUCCESS] Created Audiobook Cover: {DST_COVER}")
    print(f"  Dimensions: {img_resized.width}x{img_resized.height} | Mode: {img_resized.mode} | Size: {size_mb:.2f} MB")

if __name__ == "__main__":
    main()
