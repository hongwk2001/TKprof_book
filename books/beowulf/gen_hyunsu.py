import asyncio
import edge_tts
import os

async def main():
    text = "프롤로그: 최초의 왕, 실드 셰핑. 들어보라! 고대 데인족 왕들이 누렸던 그 찬란한 영광의 이야기들을!"
    c = edge_tts.Communicate(text, "ko-KR-HyunsuMultilingualNeural")
    out_path = "books/beowulf/samples/test_ko_edge_hyunsu.mp3"
    await c.save(out_path)
    print(f"Generated Hyunsu sample at {out_path}")

if __name__ == "__main__":
    asyncio.run(main())
