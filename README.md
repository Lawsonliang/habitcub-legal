# legal-site（隐私政策 / 订阅条款的线上版本）

App Store 要求**隐私政策必须有可公开访问的 URL**（EN_RELEASE V12 / D8）。这个目录就是那个 URL 对应的静态站。

## 已上线（2026-11-25）

| 页面 | 线上地址 |
|---|---|
| 入口 | https://lawsonliang.github.io/habitcub-legal/ |
| 隐私政策（英文，主） | https://lawsonliang.github.io/habitcub-legal/privacy.html |
| 隐私政策（简体中文） | https://lawsonliang.github.io/habitcub-legal/privacy-zh.html |
| 订阅条款 | https://lawsonliang.github.io/habitcub-legal/terms.html |

托管方式：独立 public 仓库 [Lawsonliang/habitcub-legal](https://github.com/Lawsonliang/habitcub-legal)，
Pages 从 `main` / 根目录发布，HTTPS 强制（http 访问 301 跳 https）。

> 为什么另建仓库：源码仓库是 private，GitHub 免费版 Pages 只服务 public 仓库；
> 把源码仓库转 public 会连代码一起公开，不可接受。

## 文件

| 文件 | 来源 | 说明 |
|---|---|---|
| `index.html` | 手写 | 入口页，链到下面三个文档 |
| `privacy.html` | **生成** | 由 `rewardsystem_app/assets/docs/privacy_policy_en.txt` 生成 |
| `privacy-zh.html` | **生成** | 由 `rewardsystem_app/assets/docs/privacy_policy_zh.txt` 生成 |
| `terms.html` | 手写 | 订阅条款 + Apple 标准 EULA 链接（3.1.2 要求的要素都在这里） |
| `style.css` | 手写 | 共用样式，跟随系统深浅色 |
| `build.py` | — | 生成器，只做排版转换，不改文字 |
| `publish.sh` | — | 一键发布（生成 → 守卫 → 推送） |

## 改文案的正确姿势

隐私政策的**唯一文本来源是 App 内那份 txt**（App 的「隐私政策」页读的是同一个文件）。
不要直接改 HTML —— 两份法律文本一旦漂移，就是「对外声明和 App 内不一致」。

```bash
# 1) 改文案
vim rewardsystem_app/assets/docs/privacy_policy_en.txt
# 2) 一键发布（内部会重建 HTML、跑守卫、推送到 public 仓库）
bash legal-site/publish.sh
# 3) 约 1 分钟后确认线上与本地一致
diff <(curl -s https://lawsonliang.github.io/habitcub-legal/privacy.html) legal-site/privacy.html
```

## 拿到 URL 后还要填三处

- App Store Connect → App 信息 → 隐私政策 URL：填上面的 `privacy.html`
- App Store Connect → App 信息 → 许可证协议：**留空＝Apple 标准 EULA**（或填 https://www.apple.com/legal/internet-services/itunes/dev/stdeula/ ）
- App 内会员页的披露区：隐私政策 + 订阅条款两个链接（对应 EN_RELEASE §5.1，尚未实现）

## 口径已统一（2026-11-25）

隐私政策正文已改为「for iPhone」，与 v1「仅 iPhone」的决策（EN_RELEASE D5）一致；
`TARGETED_DEVICE_FAMILY` 也已改为 `1` 并有守卫测试。将来若要上 iPad，两处要一起改。
