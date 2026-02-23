import os

def main():
    guide_path = os.path.join(os.path.dirname(__file__), 'IDIOM_GUIDE.md')
    
    print("=== 成语工作流指南 ===")
    if os.path.exists(guide_path):
        with open(guide_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("Idiom Guide not found.")

if __name__ == "__main__":
    main()
