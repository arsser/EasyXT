"""
QMT 路径配置

只使用大 QMT（XtItClient + datadir / userdata）。
miniQMT（XtMiniQmt / userdata_mini / 58610）已停用，不要再作为默认路径。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

GALAXY_QMT_ROOT = Path(r"D:/qt/银河证券QMT实盘 - 交易终端-北京")

QMT_POSSIBLE_PATHS = [
    str(GALAXY_QMT_ROOT).replace("\\", "/"),
    "D:/qt/银河证券QMT实盘 - 交易终端-北京",
    "D:/国金QMT交易端模拟",
    "C:/国金QMT交易端模拟",
    "D:/QMT",
    "C:/QMT",
]

# 大 QMT 用户数据子目录（交易）；行情缓存是同级的 datadir
QMT_USERDATA_SUBPATH = "userdata"

QMT_SIMULATED_KEYWORDS = ["模拟", "mini"]

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_dotenv(key: str) -> Optional[str]:
    value = os.environ.get(key)
    if value and value.strip():
        return value.strip()

    env_path = _PROJECT_ROOT / ".env"
    if not env_path.exists():
        return None

    try:
        with env_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key:
                    v = v.strip().strip('"').strip("'")
                    return v or None
    except OSError:
        return None
    return None


def _looks_like_datadir(path: Path) -> bool:
    return path.is_dir() and (path / "SH" / "86400").is_dir()


def resolve_big_qmt_root() -> Optional[Path]:
    """解析大 QMT 安装根目录。"""
    exe = _read_dotenv("QMT_EXE_PATH_BIG")
    if exe:
        exe_path = Path(exe)
        if exe_path.exists():
            return exe_path.parent.parent

    for key in ("QMT_MARKET_DIR", "QMT_DATA_DIR", "QMT_USERDATA_PATH"):
        raw = _read_dotenv(key)
        if not raw:
            continue
        p = Path(raw)
        if p.name.lower() in {"datadir", "userdata", "userdata_mini"}:
            root = p.parent
        else:
            root = p
        if (root / "bin.x64" / "XtItClient.exe").exists() or (root / "datadir").exists():
            return root

    if (GALAXY_QMT_ROOT / "datadir").exists():
        return GALAXY_QMT_ROOT

    qt_root = Path(r"D:/qt")
    if qt_root.is_dir():
        for child in qt_root.iterdir():
            if child.is_dir() and _looks_like_datadir(child / "datadir"):
                return child

    for candidate in QMT_POSSIBLE_PATHS:
        root = Path(candidate)
        if _looks_like_datadir(root / "datadir"):
            return root

    return None


def resolve_big_qmt_datadir() -> Path:
    """解析大 QMT 行情缓存目录（datadir，含 SH/86400/*.DAT）。"""
    market_dir = _read_dotenv("QMT_MARKET_DIR")
    if market_dir:
        p = Path(market_dir)
        if p.exists():
            return p

    root = resolve_big_qmt_root()
    if root:
        datadir = root / "datadir"
        if datadir.exists():
            return datadir

    fallback = GALAXY_QMT_ROOT / "datadir"
    if fallback.exists():
        return fallback

    raise FileNotFoundError(
        "未找到大 QMT datadir。请在 .env 设置 QMT_MARKET_DIR，"
        "或确认已安装银河证券大 QMT。"
    )


def resolve_big_qmt_userdata() -> Path:
    """解析大 QMT 交易用户目录（userdata，不要用 userdata_mini）。"""
    for key in ("QMT_USERDATA_PATH", "QMT_DATA_DIR"):
        raw = _read_dotenv(key)
        if raw:
            p = Path(raw)
            if p.exists() and p.name.lower() != "userdata_mini":
                return p
            if p.parent.exists():
                userdata = p.parent / "userdata"
                if userdata.exists():
                    return userdata

    root = resolve_big_qmt_root()
    if root:
        userdata = root / "userdata"
        if userdata.exists():
            return userdata

    return GALAXY_QMT_ROOT / "userdata"
