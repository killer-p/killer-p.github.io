import os
import re
import shutil

def process_markdown(md_path):
    print(f"Processing markdown file: {md_path}")
    base = os.path.splitext(md_path)[0]
    img_dir = base

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 ![alt](path) 形式的图片
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    matches = pattern.findall(content)
    print(f"Found {len(matches)} images in {md_path}")

    if matches:
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
            print(f"Created image directory: {img_dir}")

    for alt, img_path in matches:
        img_path = img_path.strip()
        img_name = os.path.basename(img_path)
        md_dir = os.path.dirname(md_path)
        real_img_path = os.path.join(md_dir, img_path)
        new_img_path = os.path.join(img_dir, img_name)
        print(f"  Image: {real_img_path} -> {new_img_path}")
        # 复制图片到新文件夹
        if os.path.exists(real_img_path):
            shutil.copy(real_img_path, new_img_path)
            print(f"    Copied {real_img_path} to {new_img_path}")
        else:
            print(f"    WARNING: Image file {real_img_path} does not exist!")
        # 替换 markdown 中的图片路径为仅文件名
        content = content.replace(f']({img_path})', f']({img_name})')

    if matches:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Finished processing {md_path}\n")

def main():
    for root, dirs, files in os.walk('.'):
        for fname in files:
            if fname.endswith('.md'):
                process_markdown(os.path.join(root, fname))
    # 删除所有名为pictures的文件夹
    for root, dirs, files in os.walk('.', topdown=False):
        for d in dirs:
            if d == 'pictures':
                dir_path = os.path.join(root, d)
                print(f"Deleting folder: {dir_path}")
                shutil.rmtree(dir_path)

if __name__ == '__main__':
    main()