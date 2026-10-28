# 📅 iSpace / Moodle Calendar Sync

> 一个基于 GitHub Actions 的自动化日历同步工具。自动抓取高校 iSpace (Moodle) 教学系统的作业与测验 DDL，注入强力提前提醒，融合学期课表，并生成标准的 Apple Calendar / Google Calendar 订阅源。

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-iOS%20%7C%20macOS%20%7C%20Android%20%7C%20Windows-lightgrey?logo=apple)](https://apple.com)
[![Sync Status](https://img.shields.io/badge/Sync-Every%203%20Hours-orange?logo=githubactions)](https://github.com/features/actions)

---

## ✨ 核心特性

- 🔄 **云端全自动同步**：依托 GitHub Actions 免费算力，每 3 小时自动增量刷新，手机后台静默同步，无需保持电脑开机。
- ⏰ **强力提前提醒**：
  - 📝 **提前 2 天（48 小时）**：作业截止前强提醒，防止遗漏。
  - 🚨 **提前 2 小时**：DDL 冲刺提醒，做最后提交检查。
  - 🔔 **上课前 15 分钟**：课前教室地点提醒。
- 📚 **学期课表融合**：支持一键导入每周固定课表，自动计算 1~16 周日程，课程与作业一网打尽。
- 🔒 **隐私与安全隔离**：
  - 基于 Moodle 官方只读日历 Token，**无需输入任何账号密码**。
  - 支持 **Secret 暗号文件名**（链接不公开），防止未授权访问。
  - 仓库内不存储任何个人作业、成绩或明文数据。

---

## 🛠️ 架构设计

```text
  [ iSpace / Moodle ] (只读日历源)
          │
          ▼
  [ GitHub Actions (定时任务) ]
          │
          ├─► 抓取作业与 DDL 截止时间
          ├─► 智能清洗课程标题
          ├─► 强制注入提前 2 天 / 2 小时 VALARM 强提醒
          └─► 拼入 timetable.json 学期课表
          │
          ▼
  [ GitHub Pages ] 部署加密订阅源
          │
          ▼ (webcal:// 原生订阅)
  [ iPhone / iPad / Mac / Android ]
