#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比 (bi) - 对比分析技能
对比数据，提供分析建议
"""

import sys
import json
import re


def compare_texts(text1, text2):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    common = words1 & words2
    return {
        "length_diff": abs(len(text1) - len(text2)),
        "common_words": list(common)[:10],
    }


def analyze_text(text):
    words = text.split()
    sentences = re.split(r"[.!?。！？]", text)
    return {
        "length": len(text),
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
    }


def extract_numbers(text):
    return [float(n) for n in re.findall(r"-?\d+\.?\d*", text)]


def compare_data(data1, data2):
    nums1 = extract_numbers(str(data1))
    nums2 = extract_numbers(str(data2))
    if not nums1 or not nums2:
        return {"message": "No numbers to compare"}
    return {
        "data1_avg": sum(nums1) / len(nums1) if nums1 else 0,
        "data2_avg": sum(nums2) / len(nums2) if nums2 else 0,
        "difference": (sum(nums2) / len(nums2) if nums2 else 0)
        - (sum(nums1) / len(nums1) if nums1 else 0),
    }


def execute(params):
    action = params.get("action", "compare")

    if action == "compare":
        text1 = params.get("text1", "")
        text2 = params.get("text2", "")
        if text1 and text2:
            return {"status": "success", "data": compare_texts(text1, text2)}
        return {
            "status": "success",
            "data": compare_data(params.get("data1", {}), params.get("data2", {})),
        }

    elif action == "analyze":
        return {"status": "success", "data": analyze_text(params.get("text", ""))}

    return {"status": "error", "message": "Unknown action"}


if __name__ == "__main__":
    try:
        input_str = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
        params = json.loads(input_str) if input_str.strip() else {}
        print(json.dumps(execute(params), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
