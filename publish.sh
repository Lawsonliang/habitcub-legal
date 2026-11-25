#!/usr/bin/env bash
# 把 legal-site/ 发布到独立 public 仓库（GitHub Pages 的源）。
#
# 为什么要独立仓库：源码仓库 Lawsonliang/rewardsystem 是 private，
# GitHub 免费版 Pages 只服务 public 仓库；把源码仓库转 public 会连代码一起公开。
#
# 用法：bash legal-site/publish.sh
# 它做四件事：重新生成 HTML → 跑一致性守卫 → 切 subtree → 推到 habitcub-legal 的 main。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "== 1/4 重新生成 HTML（源：rewardsystem_app/assets/docs/*.txt）=="
python3 legal-site/build.py

echo "== 2/4 一致性守卫（防「改了 txt 忘了重建」）=="
(cd rewardsystem_app && flutter test --no-pub test/legal_site_test.dart)

echo "== 3/4 切 subtree =="
git branch -D legal-site-publish 2>/dev/null || true
# git subtree 会把进度条打到 stderr，噪音很大；只在失败时才让它露出来。
if ! git subtree split --prefix legal-site -b legal-site-publish >/dev/null 2>/tmp/legal-subtree.err; then
  cat /tmp/legal-subtree.err
  exit 1
fi

echo "== 4/4 推送 =="
REMOTE="https://github.com/Lawsonliang/habitcub-legal.git"
# 本机全局 git 配了 socks5 代理；代理没开时推送会失败，此时退化为「临时绕过代理」。
git push "$REMOTE" legal-site-publish:main || \
  git -c http.proxy= -c https.proxy= push "$REMOTE" legal-site-publish:main

git branch -D legal-site-publish >/dev/null
echo
echo "已发布。等约 1 分钟后生效："
echo "  https://lawsonliang.github.io/habitcub-legal/privacy.html"
