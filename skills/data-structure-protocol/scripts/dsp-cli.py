#!/usr/bin/env python3
"""
DSP CLI — Data Structure Protocol 命令行工具。
管理 .dsp/ 目录中的项目实体图谱：模块、函数、依赖关系和公共 API。
"""

import argparse
import json
import os
import sys
import hashlib
import time
from pathlib import Path
from typing import Optional


# ============================================================
# 工具函数
# ============================================================

def generate_uid(prefix: str) -> str:
    """生成唯一 ID：obj-<8hex> 或 func-<8hex>"""
    seed = f"{time.time_ns()}-{os.getpid()}-{id(object())}"
    return f"{prefix}-{hashlib.sha256(seed.encode()).hexdigest()[:8]}"


def get_dsp_root(project_root: str) -> Path:
    """获取 .dsp/ 目录路径"""
    return Path(project_root) / ".dsp"


def ensure_dsp_exists(dsp_root: Path) -> None:
    """确保 .dsp/ 目录已初始化"""
    if not dsp_root.exists():
        print(f"错误: .dsp/ 目录不存在于 {dsp_root.parent}。请先运行 'dsp-cli init'。", file=sys.stderr)
        sys.exit(1)


def load_entity(dsp_root: Path, uid: str) -> Optional[dict]:
    """加载实体元数据"""
    entity_file = dsp_root / "entities" / uid / "meta.json"
    if not entity_file.exists():
        return None
    with open(entity_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_entity(dsp_root: Path, uid: str, data: dict) -> None:
    """保存实体元数据"""
    entity_dir = dsp_root / "entities" / uid
    entity_dir.mkdir(parents=True, exist_ok=True)
    with open(entity_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_toc(dsp_root: Path, toc_uid: Optional[str] = None) -> dict:
    """加载 TOC（目录索引）"""
    if toc_uid:
        toc_file = dsp_root / "toc" / f"{toc_uid}.json"
    else:
        toc_file = dsp_root / "toc" / "default.json"
    if not toc_file.exists():
        return {"entries": []}
    with open(toc_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_toc(dsp_root: Path, toc_data: dict, toc_uid: Optional[str] = None) -> None:
    """保存 TOC"""
    toc_dir = dsp_root / "toc"
    toc_dir.mkdir(parents=True, exist_ok=True)
    if toc_uid:
        toc_file = toc_dir / f"{toc_uid}.json"
    else:
        toc_file = toc_dir / "default.json"
    with open(toc_file, "w", encoding="utf-8") as f:
        json.dump(toc_data, f, indent=2, ensure_ascii=False)


def load_source_index(dsp_root: Path) -> dict:
    """加载源文件索引（path -> uid 映射）"""
    index_file = dsp_root / "index" / "source-map.json"
    if not index_file.exists():
        return {}
    with open(index_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_source_index(dsp_root: Path, index: dict) -> None:
    """保存源文件索引"""
    index_dir = dsp_root / "index"
    index_dir.mkdir(parents=True, exist_ok=True)
    with open(index_dir / "source-map.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def add_to_toc(dsp_root: Path, uid: str, toc_uid: Optional[str] = None) -> None:
    """将实体添加到 TOC"""
    toc = load_toc(dsp_root, toc_uid)
    if uid not in toc["entries"]:
        toc["entries"].append(uid)
        save_toc(dsp_root, toc, toc_uid)


def remove_from_toc(dsp_root: Path, uid: str, toc_uid: Optional[str] = None) -> None:
    """从 TOC 中移除实体"""
    toc = load_toc(dsp_root, toc_uid)
    if uid in toc["entries"]:
        toc["entries"].remove(uid)
        save_toc(dsp_root, toc, toc_uid)


# ============================================================
# 命令实现
# ============================================================

def cmd_init(args) -> None:
    """初始化 .dsp/ 目录结构"""
    dsp_root = get_dsp_root(args.root)

    if dsp_root.exists():
        print(f"⚠️  .dsp/ 目录已存在于 {dsp_root}。跳过初始化。")
        return

    # 创建目录结构
    (dsp_root / "entities").mkdir(parents=True)
    (dsp_root / "toc").mkdir(parents=True)
    (dsp_root / "index").mkdir(parents=True)

    # 创建项目元数据
    project_meta = {
        "version": "1.0.0",
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "project_root": str(Path(args.root).resolve()),
        "description": "DSP 实体图谱"
    }
    with open(dsp_root / "project.json", "w", encoding="utf-8") as f:
        json.dump(project_meta, f, indent=2, ensure_ascii=False)

    # 初始化空的默认 TOC
    save_toc(dsp_root, {"entries": []})

    # 初始化空的源文件索引
    save_source_index(dsp_root, {})

    # 创建 .gitignore（不忽略 .dsp 本身的任何内容）
    with open(dsp_root / ".gitignore", "w", encoding="utf-8") as f:
        f.write("# DSP 图谱应纳入版本管理\n")

    print(f"✅ DSP 已初始化于 {dsp_root}")
    print(f"   目录结构:")
    print(f"   .dsp/")
    print(f"   ├── entities/    (实体存储)")
    print(f"   ├── toc/         (目录索引)")
    print(f"   ├── index/       (源文件映射)")
    print(f"   └── project.json (项目元数据)")


def cmd_create_object(args) -> None:
    """创建 Object 实体（模块/文件/外部依赖）"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    uid = generate_uid("obj")
    kind = args.kind if args.kind else "module"

    entity = {
        "uid": uid,
        "type": "object",
        "kind": kind,
        "source": args.source,
        "purpose": args.purpose,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "imports": [],
        "shared": []
    }
    save_entity(dsp_root, uid, entity)

    # 更新源文件索引
    if kind != "external":
        source_index = load_source_index(dsp_root)
        source_index[args.source] = uid
        save_source_index(dsp_root, source_index)

    # 添加到 TOC
    toc_uid = args.toc if args.toc else None
    add_to_toc(dsp_root, uid, toc_uid)

    # 创建 exports 目录
    exports_dir = dsp_root / "entities" / uid / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    print(f"✅ 已创建 Object: {uid}")
    print(f"   源: {args.source}")
    print(f"   用途: {args.purpose}")
    print(f"   类型: {kind}")


def cmd_create_function(args) -> None:
    """创建 Function 实体"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    uid = generate_uid("func")

    entity = {
        "uid": uid,
        "type": "function",
        "source": args.source,
        "purpose": args.purpose,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "owner": args.owner if args.owner else None,
        "imports": []
    }
    save_entity(dsp_root, uid, entity)

    # 更新源文件索引
    source_index = load_source_index(dsp_root)
    source_index[args.source] = uid
    save_source_index(dsp_root, source_index)

    # 添加到 TOC
    toc_uid = args.toc if args.toc else None
    add_to_toc(dsp_root, uid, toc_uid)

    # 如果有 owner，将函数添加到 owner 的子实体列表
    if args.owner:
        owner = load_entity(dsp_root, args.owner)
        if owner:
            if "children" not in owner:
                owner["children"] = []
            if uid not in owner["children"]:
                owner["children"].append(uid)
                save_entity(dsp_root, args.owner, owner)

    print(f"✅ 已创建 Function: {uid}")
    print(f"   源: {args.source}")
    print(f"   用途: {args.purpose}")
    if args.owner:
        print(f"   所属: {args.owner}")


def cmd_create_shared(args) -> None:
    """注册导出（公共 API）"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    exporter = load_entity(dsp_root, args.exporter_uid)
    if not exporter:
        print(f"错误: 找不到导出者实体 {args.exporter_uid}", file=sys.stderr)
        sys.exit(1)

    if "shared" not in exporter:
        exporter["shared"] = []

    for shared_uid in args.shared_uids:
        shared = load_entity(dsp_root, shared_uid)
        if not shared:
            print(f"⚠️  跳过: 找不到共享实体 {shared_uid}", file=sys.stderr)
            continue
        if shared_uid not in exporter["shared"]:
            exporter["shared"].append(shared_uid)
            print(f"   ✅ 已注册导出: {shared_uid}")

    save_entity(dsp_root, args.exporter_uid, exporter)
    print(f"✅ 导出注册完成: {args.exporter_uid}")


def cmd_add_import(args) -> None:
    """添加导入关系"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    importer = load_entity(dsp_root, args.importer_uid)
    if not importer:
        print(f"错误: 找不到导入者实体 {args.importer_uid}", file=sys.stderr)
        sys.exit(1)

    imported = load_entity(dsp_root, args.imported_uid)
    if not imported:
        print(f"错误: 找不到被导入实体 {args.imported_uid}", file=sys.stderr)
        sys.exit(1)

    if "imports" not in importer:
        importer["imports"] = []

    # 检查是否已存在
    for imp in importer["imports"]:
        if imp["uid"] == args.imported_uid:
            print(f"⚠️  导入关系已存在: {args.importer_uid} -> {args.imported_uid}")
            return

    import_entry = {
        "uid": args.imported_uid,
        "why": args.why,
    }
    if args.exporter:
        import_entry["via"] = args.exporter

    importer["imports"].append(import_entry)
    save_entity(dsp_root, args.importer_uid, importer)

    # 创建反向索引（谁导入了此实体）
    exports_dir = dsp_root / "entities" / args.imported_uid / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    reverse_file = exports_dir / f"{args.importer_uid}.json"
    with open(reverse_file, "w", encoding="utf-8") as f:
        json.dump({
            "importer": args.importer_uid,
            "why": args.why,
            "via": args.exporter if args.exporter else None
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ 已添加导入: {args.importer_uid} -> {args.imported_uid}")
    print(f"   原因: {args.why}")


def cmd_remove_import(args) -> None:
    """移除导入关系"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    importer = load_entity(dsp_root, args.importer_uid)
    if not importer:
        print(f"错误: 找不到导入者实体 {args.importer_uid}", file=sys.stderr)
        sys.exit(1)

    original_len = len(importer.get("imports", []))
    importer["imports"] = [
        imp for imp in importer.get("imports", [])
        if imp["uid"] != args.imported_uid
    ]

    if len(importer["imports"]) == original_len:
        print(f"⚠️  未找到导入关系: {args.importer_uid} -> {args.imported_uid}")
        return

    save_entity(dsp_root, args.importer_uid, importer)

    # 删除反向索引
    reverse_file = dsp_root / "entities" / args.imported_uid / "exports" / f"{args.importer_uid}.json"
    if reverse_file.exists():
        reverse_file.unlink()

    print(f"✅ 已移除导入: {args.importer_uid} -> {args.imported_uid}")


def cmd_remove_shared(args) -> None:
    """移除导出"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    exporter = load_entity(dsp_root, args.exporter_uid)
    if not exporter:
        print(f"错误: 找不到导出者实体 {args.exporter_uid}", file=sys.stderr)
        sys.exit(1)

    if args.shared_uid in exporter.get("shared", []):
        exporter["shared"].remove(args.shared_uid)
        save_entity(dsp_root, args.exporter_uid, exporter)
        print(f"✅ 已移除导出: {args.exporter_uid} -> {args.shared_uid}")
    else:
        print(f"⚠️  未找到导出关系: {args.exporter_uid} -> {args.shared_uid}")


def cmd_remove_entity(args) -> None:
    """删除实体（级联清理）"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    entity = load_entity(dsp_root, args.uid)
    if not entity:
        print(f"错误: 找不到实体 {args.uid}", file=sys.stderr)
        sys.exit(1)

    # 从所有 TOC 中移除
    toc_dir = dsp_root / "toc"
    if toc_dir.exists():
        for toc_file in toc_dir.glob("*.json"):
            with open(toc_file, "r", encoding="utf-8") as f:
                toc = json.load(f)
            if args.uid in toc.get("entries", []):
                toc["entries"].remove(args.uid)
                with open(toc_file, "w", encoding="utf-8") as f:
                    json.dump(toc, f, indent=2, ensure_ascii=False)

    # 从源文件索引中移除
    source_index = load_source_index(dsp_root)
    keys_to_remove = [k for k, v in source_index.items() if v == args.uid]
    for key in keys_to_remove:
        del source_index[key]
    save_source_index(dsp_root, source_index)

    # 清理其他实体中的 imports 引用
    entities_dir = dsp_root / "entities"
    if entities_dir.exists():
        for entity_dir in entities_dir.iterdir():
            if entity_dir.is_dir() and entity_dir.name != args.uid:
                meta_file = entity_dir / "meta.json"
                if meta_file.exists():
                    with open(meta_file, "r", encoding="utf-8") as f:
                        other = json.load(f)
                    changed = False
                    # 移除 imports 中的引用
                    if "imports" in other:
                        new_imports = [i for i in other["imports"] if i["uid"] != args.uid]
                        if len(new_imports) != len(other["imports"]):
                            other["imports"] = new_imports
                            changed = True
                    # 移除 shared 中的引用
                    if "shared" in other:
                        if args.uid in other["shared"]:
                            other["shared"].remove(args.uid)
                            changed = True
                    # 移除 children 中的引用
                    if "children" in other:
                        if args.uid in other["children"]:
                            other["children"].remove(args.uid)
                            changed = True
                    if changed:
                        with open(meta_file, "w", encoding="utf-8") as f:
                            json.dump(other, f, indent=2, ensure_ascii=False)

    # 删除实体目录
    import shutil
    entity_dir = dsp_root / "entities" / args.uid
    if entity_dir.exists():
        shutil.rmtree(entity_dir)

    print(f"✅ 已删除实体: {args.uid} (已级联清理)")


def cmd_move_entity(args) -> None:
    """移动/重命名实体的源路径"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    entity = load_entity(dsp_root, args.uid)
    if not entity:
        print(f"错误: 找不到实体 {args.uid}", file=sys.stderr)
        sys.exit(1)

    old_source = entity["source"]
    entity["source"] = args.new_source
    save_entity(dsp_root, args.uid, entity)

    # 更新源文件索引
    source_index = load_source_index(dsp_root)
    if old_source in source_index:
        del source_index[old_source]
    source_index[args.new_source] = args.uid
    save_source_index(dsp_root, source_index)

    print(f"✅ 已移动实体 {args.uid}: {old_source} -> {args.new_source}")


def cmd_update_description(args) -> None:
    """更新实体描述"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    entity = load_entity(dsp_root, args.uid)
    if not entity:
        print(f"错误: 找不到实体 {args.uid}", file=sys.stderr)
        sys.exit(1)

    if args.source:
        entity["source"] = args.source
    if args.purpose:
        entity["purpose"] = args.purpose
    if args.kind:
        entity["kind"] = args.kind

    save_entity(dsp_root, args.uid, entity)
    print(f"✅ 已更新实体 {args.uid} 的描述")


def cmd_get_entity(args) -> None:
    """获取实体详情"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    entity = load_entity(dsp_root, args.uid)
    if not entity:
        print(f"错误: 找不到实体 {args.uid}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(entity, indent=2, ensure_ascii=False))


def cmd_get_children(args) -> None:
    """获取实体的子依赖"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    depth = args.depth if args.depth else 1
    visited = set()

    def traverse(uid: str, current_depth: int, indent: int = 0):
        if current_depth > depth or uid in visited:
            return
        visited.add(uid)
        entity = load_entity(dsp_root, uid)
        if not entity:
            return
        prefix = "  " * indent
        print(f"{prefix}{'└── ' if indent > 0 else ''}{uid} [{entity.get('type', '?')}] {entity.get('source', '?')}")
        print(f"{prefix}    用途: {entity.get('purpose', '?')}")
        for imp in entity.get("imports", []):
            traverse(imp["uid"], current_depth + 1, indent + 1)

    traverse(args.uid, 1)


def cmd_get_parents(args) -> None:
    """获取依赖此实体的父实体"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    exports_dir = dsp_root / "entities" / args.uid / "exports"
    if not exports_dir.exists():
        print(f"无父依赖: {args.uid}")
        return

    print(f"依赖 {args.uid} 的实体:")
    for reverse_file in exports_dir.glob("*.json"):
        with open(reverse_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        importer_uid = data["importer"]
        importer = load_entity(dsp_root, importer_uid)
        source = importer.get("source", "?") if importer else "?"
        print(f"  └── {importer_uid} [{source}]")
        print(f"      原因: {data.get('why', '?')}")


def cmd_search(args) -> None:
    """搜索实体"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    query = args.query.lower()
    results = []

    entities_dir = dsp_root / "entities"
    if not entities_dir.exists():
        print("无实体")
        return

    for entity_dir in entities_dir.iterdir():
        if entity_dir.is_dir():
            meta_file = entity_dir / "meta.json"
            if meta_file.exists():
                with open(meta_file, "r", encoding="utf-8") as f:
                    entity = json.load(f)
                # 在 uid、source、purpose 中搜索
                searchable = f"{entity.get('uid', '')} {entity.get('source', '')} {entity.get('purpose', '')}".lower()
                if query in searchable:
                    results.append(entity)

    if not results:
        print(f"未找到匹配 '{args.query}' 的实体")
        return

    print(f"找到 {len(results)} 个匹配:")
    for entity in results:
        print(f"  {entity['uid']} [{entity.get('type', '?')}:{entity.get('kind', '?')}] {entity.get('source', '?')}")
        print(f"    用途: {entity.get('purpose', '?')}")


def cmd_find_by_source(args) -> None:
    """通过源路径查找实体"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    source_index = load_source_index(dsp_root)

    # 精确匹配
    if args.path in source_index:
        uid = source_index[args.path]
        entity = load_entity(dsp_root, uid)
        if entity:
            print(json.dumps(entity, indent=2, ensure_ascii=False))
            return

    # 模糊匹配
    matches = [(k, v) for k, v in source_index.items() if args.path in k or k in args.path]
    if matches:
        print(f"找到 {len(matches)} 个部分匹配:")
        for source, uid in matches:
            entity = load_entity(dsp_root, uid)
            if entity:
                print(f"  {uid} [{entity.get('type', '?')}] {source}")
                print(f"    用途: {entity.get('purpose', '?')}")
    else:
        print(f"未找到源路径匹配: {args.path}")


def cmd_read_toc(args) -> None:
    """读取 TOC 目录索引"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    toc_uid = args.toc if args.toc else None
    toc = load_toc(dsp_root, toc_uid)

    toc_name = toc_uid if toc_uid else "default"
    print(f"📋 TOC: {toc_name} ({len(toc['entries'])} 个实体)")
    print()

    for uid in toc["entries"]:
        entity = load_entity(dsp_root, uid)
        if entity:
            kind = entity.get("kind", "?")
            etype = entity.get("type", "?")
            source = entity.get("source", "?")
            purpose = entity.get("purpose", "?")
            imports_count = len(entity.get("imports", []))
            shared_count = len(entity.get("shared", []))
            print(f"  {uid} [{etype}:{kind}] {source}")
            print(f"    用途: {purpose}")
            print(f"    导入: {imports_count}  导出: {shared_count}")
        else:
            print(f"  {uid} [⚠️ 实体缺失]")


def cmd_get_stats(args) -> None:
    """获取图谱统计信息"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    entities_dir = dsp_root / "entities"
    if not entities_dir.exists():
        print("图谱为空")
        return

    total = 0
    objects = 0
    functions = 0
    externals = 0
    total_imports = 0
    total_shared = 0

    for entity_dir in entities_dir.iterdir():
        if entity_dir.is_dir():
            meta_file = entity_dir / "meta.json"
            if meta_file.exists():
                with open(meta_file, "r", encoding="utf-8") as f:
                    entity = json.load(f)
                total += 1
                if entity.get("type") == "object":
                    if entity.get("kind") == "external":
                        externals += 1
                    else:
                        objects += 1
                elif entity.get("type") == "function":
                    functions += 1
                total_imports += len(entity.get("imports", []))
                total_shared += len(entity.get("shared", []))

    print(f"📊 DSP 图谱统计")
    print(f"   总实体数: {total}")
    print(f"   ├── 模块/文件: {objects}")
    print(f"   ├── 函数: {functions}")
    print(f"   └── 外部依赖: {externals}")
    print(f"   总导入边: {total_imports}")
    print(f"   总导出边: {total_shared}")


def cmd_detect_cycles(args) -> None:
    """检测循环依赖"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    # 构建邻接表
    graph = {}
    entities_dir = dsp_root / "entities"
    if not entities_dir.exists():
        print("图谱为空，无循环依赖")
        return

    for entity_dir in entities_dir.iterdir():
        if entity_dir.is_dir():
            meta_file = entity_dir / "meta.json"
            if meta_file.exists():
                with open(meta_file, "r", encoding="utf-8") as f:
                    entity = json.load(f)
                uid = entity["uid"]
                graph[uid] = [imp["uid"] for imp in entity.get("imports", [])]

    # DFS 检测环
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in graph}
    cycles = []

    def dfs(u, path):
        color[u] = GRAY
        path.append(u)
        for v in graph.get(u, []):
            if v not in color:
                continue
            if color[v] == GRAY:
                cycle_start = path.index(v)
                cycles.append(path[cycle_start:] + [v])
            elif color[v] == WHITE:
                dfs(v, path)
        path.pop()
        color[u] = BLACK

    for u in graph:
        if color[u] == WHITE:
            dfs(u, [])

    if not cycles:
        print("✅ 未检测到循环依赖")
    else:
        print(f"⚠️  检测到 {len(cycles)} 个循环依赖:")
        for i, cycle in enumerate(cycles, 1):
            print(f"  循环 {i}: {' -> '.join(cycle)}")


def cmd_get_orphans(args) -> None:
    """查找孤立实体"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    # 收集所有实体
    entities = {}
    imported_uids = set()
    entities_dir = dsp_root / "entities"
    if not entities_dir.exists():
        print("图谱为空")
        return

    for entity_dir in entities_dir.iterdir():
        if entity_dir.is_dir():
            meta_file = entity_dir / "meta.json"
            if meta_file.exists():
                with open(meta_file, "r", encoding="utf-8") as f:
                    entity = json.load(f)
                entities[entity["uid"]] = entity
                for imp in entity.get("imports", []):
                    imported_uids.add(imp["uid"])

    # 获取 TOC 入口
    toc_entries = set()
    toc_dir = dsp_root / "toc"
    if toc_dir.exists():
        for toc_file in toc_dir.glob("*.json"):
            with open(toc_file, "r", encoding="utf-8") as f:
                toc = json.load(f)
            toc_entries.update(toc.get("entries", []))

    # 查找没有被任何实体导入，也不在 TOC 中的叶子实体
    orphans = []
    for uid, entity in entities.items():
        # 检查是否有反向依赖
        exports_dir = dsp_root / "entities" / uid / "exports"
        has_importers = exports_dir.exists() and any(exports_dir.glob("*.json"))
        is_in_toc = uid in toc_entries
        has_children = bool(entity.get("children", []))
        has_owner = bool(entity.get("owner"))

        if not has_importers and not is_in_toc and not has_children and not has_owner:
            orphans.append(entity)

    if not orphans:
        print("✅ 未发现孤立实体")
    else:
        print(f"⚠️  发现 {len(orphans)} 个孤立实体:")
        for entity in orphans:
            print(f"  {entity['uid']} [{entity.get('type', '?')}] {entity.get('source', '?')}")
            print(f"    用途: {entity.get('purpose', '?')}")


def cmd_update_import_why(args) -> None:
    """更新导入原因"""
    dsp_root = get_dsp_root(args.root)
    ensure_dsp_exists(dsp_root)

    importer = load_entity(dsp_root, args.importer_uid)
    if not importer:
        print(f"错误: 找不到导入者实体 {args.importer_uid}", file=sys.stderr)
        sys.exit(1)

    found = False
    for imp in importer.get("imports", []):
        if imp["uid"] == args.imported_uid:
            imp["why"] = args.new_why
            found = True
            break

    if not found:
        print(f"错误: 未找到导入关系 {args.importer_uid} -> {args.imported_uid}", file=sys.stderr)
        sys.exit(1)

    save_entity(dsp_root, args.importer_uid, importer)

    # 更新反向索引
    reverse_file = dsp_root / "entities" / args.imported_uid / "exports" / f"{args.importer_uid}.json"
    if reverse_file.exists():
        with open(reverse_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["why"] = args.new_why
        with open(reverse_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 已更新导入原因: {args.importer_uid} -> {args.imported_uid}")


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="DSP CLI — 项目实体图谱管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", default=".", help="项目根目录（默认当前目录）")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init
    subparsers.add_parser("init", help="初始化 .dsp/ 目录")

    # create-object
    p = subparsers.add_parser("create-object", help="创建 Object 实体")
    p.add_argument("source", help="源路径")
    p.add_argument("purpose", help="用途描述")
    p.add_argument("--kind", default=None, help="类型: module（默认）, external")
    p.add_argument("--toc", default=None, help="TOC UID")

    # create-function
    p = subparsers.add_parser("create-function", help="创建 Function 实体")
    p.add_argument("source", help="源路径 (path#symbol)")
    p.add_argument("purpose", help="用途描述")
    p.add_argument("--owner", default=None, help="所属 Object UID")
    p.add_argument("--toc", default=None, help="TOC UID")

    # create-shared
    p = subparsers.add_parser("create-shared", help="注册导出")
    p.add_argument("exporter_uid", help="导出者 UID")
    p.add_argument("shared_uids", nargs="+", help="被导出实体 UID 列表")

    # add-import
    p = subparsers.add_parser("add-import", help="添加导入关系")
    p.add_argument("importer_uid", help="导入者 UID")
    p.add_argument("imported_uid", help="被导入实体 UID")
    p.add_argument("why", help="导入原因")
    p.add_argument("--exporter", default=None, help="通过哪个模块导出")

    # remove-import
    p = subparsers.add_parser("remove-import", help="移除导入关系")
    p.add_argument("importer_uid", help="导入者 UID")
    p.add_argument("imported_uid", help="被导入实体 UID")
    p.add_argument("--exporter", default=None, help="通过哪个模块导出")

    # remove-shared
    p = subparsers.add_parser("remove-shared", help="移除导出")
    p.add_argument("exporter_uid", help="导出者 UID")
    p.add_argument("shared_uid", help="被导出实体 UID")

    # remove-entity
    p = subparsers.add_parser("remove-entity", help="删除实体")
    p.add_argument("uid", help="实体 UID")

    # move-entity
    p = subparsers.add_parser("move-entity", help="移动实体源路径")
    p.add_argument("uid", help="实体 UID")
    p.add_argument("new_source", help="新源路径")

    # update-description
    p = subparsers.add_parser("update-description", help="更新实体描述")
    p.add_argument("uid", help="实体 UID")
    p.add_argument("--source", default=None, help="新源路径")
    p.add_argument("--purpose", default=None, help="新用途")
    p.add_argument("--kind", default=None, help="新类型")

    # update-import-why
    p = subparsers.add_parser("update-import-why", help="更新导入原因")
    p.add_argument("importer_uid", help="导入者 UID")
    p.add_argument("imported_uid", help="被导入实体 UID")
    p.add_argument("new_why", help="新的导入原因")

    # get-entity
    p = subparsers.add_parser("get-entity", help="获取实体详情")
    p.add_argument("uid", help="实体 UID")

    # get-children
    p = subparsers.add_parser("get-children", help="获取子依赖")
    p.add_argument("uid", help="实体 UID")
    p.add_argument("--depth", type=int, default=1, help="遍历深度")

    # get-parents
    p = subparsers.add_parser("get-parents", help="获取父依赖")
    p.add_argument("uid", help="实体 UID")
    p.add_argument("--depth", type=int, default=1, help="遍历深度")

    # search
    p = subparsers.add_parser("search", help="搜索实体")
    p.add_argument("query", help="搜索关键词")

    # find-by-source
    p = subparsers.add_parser("find-by-source", help="通过源路径查找实体")
    p.add_argument("path", help="源路径")

    # read-toc
    p = subparsers.add_parser("read-toc", help="读取 TOC")
    p.add_argument("--toc", default=None, help="TOC UID")

    # get-stats
    subparsers.add_parser("get-stats", help="获取图谱统计")

    # detect-cycles
    subparsers.add_parser("detect-cycles", help="检测循环依赖")

    # get-orphans
    subparsers.add_parser("get-orphans", help="查找孤立实体")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 分发命令
    commands = {
        "init": cmd_init,
        "create-object": cmd_create_object,
        "create-function": cmd_create_function,
        "create-shared": cmd_create_shared,
        "add-import": cmd_add_import,
        "remove-import": cmd_remove_import,
        "remove-shared": cmd_remove_shared,
        "remove-entity": cmd_remove_entity,
        "move-entity": cmd_move_entity,
        "update-description": cmd_update_description,
        "update-import-why": cmd_update_import_why,
        "get-entity": cmd_get_entity,
        "get-children": cmd_get_children,
        "get-parents": cmd_get_parents,
        "search": cmd_search,
        "find-by-source": cmd_find_by_source,
        "read-toc": cmd_read_toc,
        "get-stats": cmd_get_stats,
        "detect-cycles": cmd_detect_cycles,
        "get-orphans": cmd_get_orphans,
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"未知命令: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
