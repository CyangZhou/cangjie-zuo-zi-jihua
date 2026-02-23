import os
import argparse

def get_skill_path(char_name):
    # Construct path relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'characters', char_name, 'SKILL.md')

def list_chars(base_dir):
    chars_dir = os.path.join(base_dir, 'characters')
    if not os.path.exists(chars_dir):
        return []
    return [d for d in os.listdir(chars_dir) if os.path.isdir(os.path.join(chars_dir, d))]

def get_char_summary(char_name):
    path = get_skill_path(char_name)
    if not os.path.exists(path):
        return f"Character '{char_name}' not found."
    
    summary = ""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('description:'):
                summary = line.strip()
                break
    return summary if summary else "No description available."

def get_char_detail(char_name):
    path = get_skill_path(char_name)
    if not os.path.exists(path):
        return f"Character '{char_name}' not found."
    
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="Progressive Disclosure Retrieval for Character Skills")
    parser.add_argument('--name', type=str, help='Name of the character skill to retrieve')
    parser.add_argument('--detail', action='store_true', help='Show full details (Layer 3)')
    
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if not args.name:
        # Layer 1: List all
        chars = list_chars(base_dir)
        print("Available Character Skills (Layer 1):")
        for char in chars:
            print(f"- {char}")
    else:
        if args.detail:
            # Layer 3: Detail
            print(f"Detail for '{args.name}' (Layer 3):")
            print(get_char_detail(args.name))
        else:
            # Layer 2: Summary
            print(f"Summary for '{args.name}' (Layer 2):")
            print(get_char_summary(args.name))

if __name__ == "__main__":
    main()
