#!/usr/bin/env python
import os
import re

# マーカータグ - READMEにこれらのタグ間のコンテンツが自動更新されます
START_MARKER = "<!-- BEGIN DOCS LIST -->"
END_MARKER = "<!-- END DOCS LIST -->"

def get_docs_tree(path="docs", prefix="", is_last=False, is_root=True):
    """ディレクトリの内容を再帰的に探索してMarkdownのツリーを生成します"""
    if not os.path.exists(path):
        return "docs ディレクトリが見つかりません。"
    
    lines = []
    items = sorted(os.listdir(path))
    dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(path, item))]
    
    # 最初にディレクトリを処理
    for i, item in enumerate(dirs):
        if item.startswith('.'):  # 隠しディレクトリをスキップ
            continue
        
        is_last_dir = (i == len(dirs) - 1 and not files)
        
        if is_root:
            # ルートディレクトリの場合は特別な処理
            lines.append(f"- [{item}/](./{path}/{item}/)")
            lines.extend(get_docs_tree(f"{path}/{item}", "  ", is_last_dir, False))
        else:
            # 非ルートディレクトリの場合の処理
            this_prefix = prefix + ("└── " if is_last else "├── ")
            next_prefix = prefix + ("    " if is_last else "│   ")
            lines.append(f"{this_prefix}[{item}/](./{path}/{item}/)")
            lines.extend(get_docs_tree(f"{path}/{item}", next_prefix, is_last_dir, False))
    
    # 次にファイルを処理
    for i, item in enumerate(files):
        if item.startswith('.'):  # 隠しファイルをスキップ
            continue
            
        is_last_file = (i == len(files) - 1)
        
        if is_root:
            # ルートディレクトリの場合
            lines.append(f"- [{item}](./{path}/{item})")
        else:
            # 非ルートディレクトリの場合
            this_prefix = prefix + ("└── " if is_last_file else "├── ")
            lines.append(f"{this_prefix}[{item}](./{path}/{item})")
    
    return lines

def update_readme():
    """README.mdを更新します"""
    # README.mdが存在しなければ作成する
    if not os.path.exists("README.md"):
        with open("README.md", "w") as f:
            f.write("# public-docs\n\n")
            f.write(f"{START_MARKER}\n{END_MARKER}\n")
    
    # 既存のREADME.mdを読み込む
    with open("README.md", "r") as f:
        content = f.read()
    
    # マーカーがなければ追加する
    if START_MARKER not in content:
        content += f"\n\n## ドキュメント一覧\n\n{START_MARKER}\n{END_MARKER}\n"
    
    # docsディレクトリのツリーを生成
    docs_list = get_docs_tree()
    docs_content = "\n".join(docs_list)
    
    # 更新されたコンテンツ
    updated_content = re.sub(
        f"{START_MARKER}.*?{END_MARKER}",
        f"{START_MARKER}\n{docs_content}\n{END_MARKER}",
        content,
        flags=re.DOTALL
    )
    
    # 新しいコンテンツを書き込む
    with open("README.md", "w") as f:
        f.write(updated_content)
    
    print("README.md が更新されました")

if __name__ == "__main__":
    update_readme()
