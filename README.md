为你量身设计了一份**非常高大上、排版精致、并且完全脱敏（绝不泄露你的学校、个人隐私或真实学号）**的开源项目风格 `README.md`！

任何人点进你的 GitHub 仓库，都会觉得这是一个专业、优雅的开源日历同步工具。

---

### 操作方法（10秒钟）：

1. 打开这个网页：[https://github.com/malaxiaoxigua-gif/ispace-calendar/blob/main/README.md](https://github.com/malaxiaoxigua-gif/ispace-calendar/blob/main/README.md)
2. 点击右上角的 **小铅笔图标 ✏️（Edit）**。
3. 按 **`Ctrl + A`（全选）** 清空，把下面整段内容完整粘贴进去：

```markdown
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
```

---

## 🚀 快速使用指南

### 1. 获取 iSpace 只读日历链接
1. 登录学校 iSpace / Moodle 教学平台。
2. 进入 **日历 (Calendar)** 页面，滚动至底部点击 **「导出日历 (Export calendar)」**。
3. 选择 **「所有事件」** 和 **「最近和未来 60 天」**，点击 **「获取日历 URL」** 并复制。

### 2. 配置 GitHub 仓库密钥 (Secrets)
进入仓库 **Settings** -> **Secrets and variables** -> **Actions**，添加以下密钥：

| Secret 名称 | 说明 | 示例 |
| :--- | :--- | :--- |
| `ISPACE_CALENDAR_URL` | iSpace 导出的只读日历 URL | `https://.../calendar/export_execute.php?...` |
| `CALENDAR_FILENAME` | *(可选)* 自定义暗号文件名，保障隐私 | `my_schedule_98k2.ics` |

### 3. 配置学期课表
编辑根目录下的 [`timetable.json`](./timetable.json)，按实际情况修改开学日期、上课时间、星期与教室：

```json
{
  "semester_start_date": "2026-09-01",
  "total_weeks": 16,
  "courses": [
    {
      "name": "课程名称",
      "location": "教学楼 T2-201",
      "teacher": "任课教师",
      "weekday": 1,
      "start_time": "09:00",
      "end_time": "10:50",
      "weeks": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
      "alarm_minutes_before": 15
    }
  ]
}
```

### 4. 在手机中添加订阅

1. 打开 iPhone **「设置」** -> **「日历」** -> **「日历账户」**。
2. 点击 **「添加账户」** -> **「其他」** -> **「添加已订阅的日历」**。
3. 输入你的订阅链接：
   ```text
   https://<你的用户名>.github.io/<仓库名>/<你的文件名>.ics
   ```
4. 确认 **「移除提醒」处于关闭状态**，点击存储即可完成！

---

## 📄 开源许可

本项目采用 [MIT 许可证](LICENSE) 开源。
```

4. 滚动到页面底部，点击绿色的 **「Commit changes...」** 提交保存！

---

保存后回到你仓库的主页面，排版精美、有架构图、有盾牌徽章的专业开源门面就瞬间齐备了！
