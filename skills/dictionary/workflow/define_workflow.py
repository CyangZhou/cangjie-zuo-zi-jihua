import os

def main():
    guide_path = os.path.join(os.path.dirname(__file__), 'WORKFLOW_GUIDE.md')
    if os.path.exists(guide_path):
        with open(guide_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("Workflow Guide not found.")

if __name__ == "__main__":
    main()
