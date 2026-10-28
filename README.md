# BNBU iSpace 课表与作业日历自动同步系统

专为 BNBU (UIC) 学生设计的 Apple Calendar (iPhone 日历) 自动同步工具。

## ✨ 特性

- 📝 **自动同步 iSpace 作业 DDL**：实时拉取未交作业、测验与课程任务。
- ⏰ **强力提醒**：自动注入 **提前 2 天（48小时）响铃提醒** 与 **提前 2 小时紧急提醒**。
- 📚 **整合学期课表**：支持录入每周固定课表，自动生成整学期上课日程及课前 15 分钟提醒。
- 🔄 **全自动后台刷新**：部署在 GitHub Actions 上，每 3 小时自动同步一次，无需人工干预。
- 🔒 **安全隐私**：使用 iSpace 官方只读日历 Token，不保存任何学号密码。

---

## 🚀 方式一：手机立即体验（1分钟）

当前本地已生成测试日历文件：`calendar.ics`

1. 将项目根目录下的 [`calendar.ics`](./calendar.ics) 通过 **隔空投送 (AirDrop)**、**微信文件传输助手** 或 **邮件** 发送给你的 iPhone。
2. 在 iPhone 上点击打开该文件，系统会弹出「添加全部日历事件」。
3. 检查你的苹果日历：
   - 作业截止日期已经排好，点开可以看到课程名称、详细说明及 iSpace 跳转链接。
   - 打开作业详情，提醒已经设置为「提前 2 天」！

---

## 🔄 方式二：全自动云端同步（推荐，一劳永逸）

### 步骤 1：新建 GitHub 仓库
1. 打开 [GitHub](https://github.com) 并登录，点击右上角 **「New repository」**。
2. 仓库名填写例如：`ispace-calendar`，选择 **Public**（免费启用 Pages 服务）或 **Private**（如果你有 GitHub Pro）。
3. 点击 **Create repository**。

### 步骤 2：上传代码到该仓库
在当前文件夹打开终端，运行：
```bash
git init
git add .
git commit -m "feat: init calendar sync"
git branch -M main
git remote add origin https://github.com/<你的用户名>/ispace-calendar.git
git push -u origin main
```

### 步骤 3：在 GitHub 仓库中配置 Secret
1. 打开你刚建好的 GitHub 仓库页面，点击 **Settings** -> **Secrets and variables** -> **Actions**。
2. 点击 **New repository secret**：
   - Name: `ISPACE_CALENDAR_URL`
   - Secret: 粘贴你的 iSpace 专属链接：
     `https://ispace.bnbu.edu.cn/calendar/export_execute.php?userid=28434&authtoken=d2258618a4255942b0723969f4b30ae2ea68c691&preset_what=all&preset_time=recentupcoming`
3. 点击 **Add secret** 保存。

### 步骤 4：启用 GitHub Pages 服务
1. 在仓库的 **Actions** 标签页，点击左侧的 **Sync iSpace Calendar**，点击右侧 **Run workflow** 手动运行一次。
2. 运行成功后，进入仓库 **Settings** -> **Pages**。
3. 在 **Build and deployment** 下的 Source 选择 **Deploy from a branch**：
   - Branch 选择 `gh-pages`，文件夹选 `/(root)`。
   - 点击 **Save**。
4. 稍等 1 分钟刷新页面，你会看到类似网址：
   `https://<你的用户名>.github.io/ispace-calendar/calendar.ics`

### 步骤 5：在 iPhone 日历中订阅
1. 打开 iPhone 的 **「设置」** -> **「日历」**（iOS 18 在「设置」->「App」->「日历」）。
2. 点击 **「日历账户」** -> **「添加账户」**。
3. 选择 **「其他」** -> **「添加已订阅的日历」**。
4. 在「服务器」一栏粘贴你在步骤 4 获得的日历链接：
   `https://<你的用户名>.github.io/ispace-calendar/calendar.ics`
5. 点击「下一步」，开启「更新频率」（建议设为“每小时”），点击「存储」即可！

---

## 📅 如何修改你的课表

打开 [`timetable.json`](./timetable.json)：
* `semester_start_date`: 本学期开学第一周的周一日期（格式 `YYYY-MM-DD`）。
* `courses`: 每门课的名称、教室地点、星期几（1 代表周一，7 代表周日）、上课时间与下课时间。
修改并提交到 GitHub 后，下次自动化运行就会自动更新整学期的课表日程！
