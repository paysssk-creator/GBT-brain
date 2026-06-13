# -*- coding: utf-8 -*-
"""
█████████████████████████████████████████████████████████████████
  GBT Brain Splash - 启动画面
  品牌: GBT小土豆全能开发者
█████████████████████████████████████████████████████████████████
"""
import sys, os, time, random

GT = "GBT"

SPLASH_V1 = r"""
  ██████████████████████████████████████████████████
  █                                                 █
  █   ╔═══╗╔═══╗╔══════╗   ╔═══╗                  █
  █   ║  ╔╝╚╗  ║║  ──  ║   ║   ║                  █
  █   ║  ╚╗ ║  ║╚╗    ╔╝   ║   ║                  █
  █   ║   ║ ║  ║ ╚╗  ╔╝    ║   ║                  █
  █   ╚═══╝ ╚══╝  ╚══╝     ╚═══╝                  █
  █                                                 █
  █     GBTxiaotudou All-in-One AI Developer        █
  █          GBT小土豆全能开发者                     █
  █                                                 █
  ██████████████████████████████████████████████████
"""

SPLASH_V2 = r"""
         ╭──────────────────────────────────────╮
         │                                      │
         │    ╔═══╗╔═══╗╔══════╗                │
         │    ║  ╔╝╚╗  ║║      ║  ┌─┐ ┌─┐      │
         │    ║  ╚╗ ║  ║╚╗    ╔╝  │  │ │  │     │
         │    ║   ║ ║  ║ ╚╗  ╔╝   └─┘ └─┘      │
         │    ╚═══╝ ╚══╝  ╚══╝    ▀▄▀ ▀▄▀      │
         │                                      │
         │    ⚕ GBT小土豆全能开发者              │
         │    GBT xiaotudou AI Developer         │
         │                                      │
         ╰──────────────────────────────────────╯
"""

SPLASH_BRAIN = r"""
       ╔══════════════════════════════════════════╗
       ║                                          ║
       ║     ███████╗ ██████╗ ████████╗           ║
       ║    ██╔════╝ ██╔══██╗╚══██╔══╝           ║
       ║    ██║  ███╗██████╔╝   ██║              ║
       ║    ██║   ██║██╔══██╗   ██║              ║
       ║    ╚██████╔╝██████╔╝   ██║              ║
       ║     ╚═════╝ ╚═════╝    ╚═╝              ║
       ║                                          ║
       ║   ⚕ GBT小土豆全能开发者 AI Brain v3.0     ║
       ║   Self-Evolving Multi-Dimensional AI     ║
       ║                                          ║
       ╚══════════════════════════════════════════╝
"""

SPLASH_NEURAL = r"""
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║    ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   ║
  ║    █     █    █     █       █  █  █     █     █  █     ║
  ║    █ ▄▄▄ █    █ ▄▄▄ █       █  █  █ ▄▄▄ █     █  █     ║
  ║    █ ███ █    █ ███ █       █  █  █ ███ █     █  █     ║
  ║    █     █    █     █       █  █  █     █     █  █     ║
  ║    ▀▀▀▀▀▀▀    ▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀   ║
  ║                                                          ║
  ║       ○ ◌ ○ neuron network active                        ║
  ║       ╲ │ ╱ synapse connecting                           ║
  ║        ◉─◉─◉  dendrite branching                         ║
  ║       ╱ │ ╲ axon firing                                  ║
  ║       ● ◌ ● firing patterns detected                     ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
"""

SPLASH_ACTIVE = r"""
 ╔══════════════════════════════════════════════════════════╗
 ║   ▀▀█▀▀ █ █▀▀█ █▀▀█ █▀▀█   █▀▀▀ █▀▀▀ █▀▀█ ▀ █▀▀▀    ║
 ║     █   █ █  █ █  █ █  █   ▀▀▀█ ▀▀▀█ █  █ █ █▀▀     ║
 ║     ▀   ▀ ▀  ▀ ▀  ▀ ▀▀▀▀   ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀ ▀▀▀▀    ║
 ║                                                          ║
 ║   ⚕ GBT小土豆全能开发者  |  GBT xiaotudou AI Dev        ║
 ║   v3.0  Brain-MindSpace-Dimension-Mirror-Evolve          ║
 ║──────────────────────────────────────────────────────────║
 ║   Modules:  Brain | MindSpace | SelfEvolve | Mirror      ║
 ║   Memory:  vectors.db (79 notes, 80 learnings)           ║
 ║   Schedule: daily 2:00 AM auto-evolve                    ║
 ╚══════════════════════════════════════════════════════════╝
"""

def splash(style="active", delay=0.02):
    """显示启动画面"""
    styles = {
        "v1": SPLASH_V1,
        "v2": SPLASH_V2,
        "brain": SPLASH_BRAIN,
        "neural": SPLASH_NEURAL,
        "active": SPLASH_ACTIVE,
    }
    art = styles.get(style, SPLASH_ACTIVE)

    # 彩色输出 (支持ANSI的终端)
    COLORS = {
        "head": "\033[1;36m",   # Cyan bold
        "body": "\033[0;32m",   # Green
        "border": "\033[0;33m", # Yellow
        "reset": "\033[0m",
    }

    for line in art.strip().split("\n"):
        if "╔" in line or "╚" in line or "═" in line:
            sys.stdout.write(COLORS.get("border", "") + line + COLORS["reset"] + "\n")
        elif "GBT" in line or "xiaotudou" in line or "小土豆" in line or "v3.0" in line:
            sys.stdout.write(COLORS.get("head", "") + line + COLORS["reset"] + "\n")
        else:
            sys.stdout.write(COLORS.get("body", "") + line + COLORS["reset"] + "\n")
        if delay:
            time.sleep(delay)
            sys.stdout.flush()

    time.sleep(0.5)
    print(f"\n{COLORS['head']}  ⚕ GBT小土豆全能开发者 - Brain System Booted{COLORS['reset']}")


if __name__ == "__main__":
    for style in ["active", "brain", "neural"]:
        splash(style, delay=0.01)
        print("\n")
