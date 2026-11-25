# legal-site（隐私政策 / 订阅条款的线上版本）

App Store 要求**隐私政策必须有可公开访问的 URL**（EN_RELEASE V12 / D8）。这个目录就是那个 URL 对应的静态站。

## 文件

| 文件 | 来源 | 说明 |
|---|---|---|
| `index.html` | 手写 | 入口页，链到下面三个文档 |
| `privacy.html` | **生成** | 由 `rewardsystem_app/assets/docs/privacy_policy_en.txt` 生成 |
| `privacy-zh.html` | **生成** | 由 `rewardsystem_app/assets/docs/privacy_policy_zh.txt` 生成 |
| `terms.html` | 手写 | 订阅条款 + Apple 标准 EULA 链接（3.1.2 要求的六要素都在这里） |
| `style.css` | 手写 | 两端共用样式，跟随系统深浅色 |
| `build.py` | — | 生成器，只做排版转换，不改文字 |

## 改文案的正确姿势

隐私政策的**唯一文本来源是 App 内那份 txt**（App 的「隐私政策」页读的是同一个文件）。
不要直接改 HTML —— 两份法律文本一旦漂移，就是「对外声明和 App 内不一致」。

```bash
# 1. 改 txt
vim rewardsystem_app/assets/docs/privacy_policy_en.txt
# 2. 重新生成
python3 legal-site/build.py
# 3. 跑守卫测试（会比对 html 与 txt 是否一致）
cd rewardsystem_app && flutter test --no-pub test/legal_site_test.dart
```

## 发布到 GitHub Pages（尚未上线，卡在仓库权限）

**约束**：源仓库 `Lawsonliang/rewardsystem` 是 **private**，GitHub 免费版 Pages 只支持 public 仓库。
所以不要把这个仓库改成 public（会连源码一起公开），而是**另建一个只放本目录内容的 public 仓库**。

一次性操作：

1. GitHub 网页新建 public 仓库，例如 `habitcub-legal`，**不要**勾 README（保持空仓库）。
2. 在仓库根执行（把内容推成该仓库的 `main`）：
```bash
git subtree split --prefix legal-site -b legal-site-only
git push https://github.com/<你的用户名>/habitcub-legal.git legal-site-only:main
git branch -D legal-site-only
```
3. 该仓库 Settings → Pages → Source 选 `Deploy from a branch` → 分支 `main` / 目录 `/(root)` → Save。
4. 等 1–2 分钟，访问 `https://<你的用户名>.github.io/habitcub-legal/privacy.html` 确认能打开。

拿到 URL 后要填三处：
- App Store Connect → App 信息 → 隐私政策 URL
- App Store Connect → App 信息 → 许可证协议（留空＝Apple 标准 EULA；也可填 `https://www.apple.com/legal/internet-services/itunes/dev/stdeula/`）
- App 内会员页的披露区（见 EN_RELEASE §5.1）
