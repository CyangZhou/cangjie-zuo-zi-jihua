#!/usr/bin/env python3
"""
剪 (jian) - 视频剪辑
"""

import sys
import json

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    print(json.dumps({"status": "error", "message": "Missing: pip install moviepy"}))
    sys.exit(1)


def execute(params):
    input_path = params.get("input", "").strip()
    output_path = params.get("output", "").strip()

    if not input_path or not output_path:
        return {"status": "error", "message": "Input and output paths required"}

    try:
        clip = VideoFileClip(input_path)
        start = params.get("start", 0)
        end = params.get("end", clip.duration)

        subclip = clip.subclip(start, end)
        subclip.write_videofile(output_path, codec="libx264")

        return {
            "status": "success",
            "data": {"output_path": output_path, "duration": end - start},
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        params = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
