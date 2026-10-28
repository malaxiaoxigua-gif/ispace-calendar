#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BNBU / UIC iSpace Calendar & Timetable Sync Engine
- Fetches raw iSpace Moodle calendar export URL
- Performs RFC 5545 line unfolding
- Formats course names & assignments cleanly
- Injects 2-day (TRIGGER:-P2D) and 2-hour (TRIGGER:-PT2H) alerts
- Merges semester timetable (classes) from encrypted secrets or local config
- Outputs standard iCalendar (.ics) with custom secret filename
"""

import os
import sys
import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

VTIMEZONE_SHANGHAI = """BEGIN:VTIMEZONE
TZID:Asia/Shanghai
X-LIC-LOCATION:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
TZNAME:CST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE"""

def fetch_ispace_calendar(url: str) -> str:
    """Download ICS content from iSpace URL."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def unfold_ics_lines(raw_ics: str) -> list:
    """Unfold lines according to RFC 5545."""
    raw_lines = raw_ics.replace("\r\n", "\n").split("\n")
    unfolded = []
    for line in raw_lines:
        if line.startswith(" ") or line.startswith("\t"):
            if unfolded:
                unfolded[-1] += line[1:]
        else:
            unfolded.append(line)
    return unfolded

def clean_course_name(categories: str) -> str:
    """Extract clean course title from CATEGORIES field."""
    text = categories.strip()
    if not text:
        return ""
    text = re.sub(r"\[Semester.*?\]", "", text).strip()
    text = re.sub(r"\(Dr\..*?\)", "", text).strip()
    text = re.sub(r"\(Prof\..*?\)", "", text).strip()
    return text.strip()

def process_ispace_ics(raw_ics: str) -> list:
    """Parse raw iSpace ICS and enhance event titles and alarms."""
    unfolded_lines = unfold_ics_lines(raw_ics)
    processed_events = []
    current_lines = []
    in_event = False

    for line in unfolded_lines:
        line_strip = line.strip()
        if line_strip == "BEGIN:VEVENT":
            in_event = True
            current_lines = [line]
        elif line_strip == "END:VEVENT":
            if in_event:
                current_lines.append(line)
                enhanced_lines = enhance_single_event(current_lines)
                processed_events.append("\n".join(enhanced_lines))
                in_event = False
                current_lines = []
        elif in_event:
            current_lines.append(line)

    return processed_events

def enhance_single_event(lines: list) -> list:
    """Add alarm and improve summary/description for an assignment event."""
    summary = ""
    categories = ""
    new_lines = []
    has_alarm = False

    for l in lines:
        if l.startswith("BEGIN:VALARM"):
            has_alarm = True
        if l.startswith("SUMMARY:"):
            summary = l[len("SUMMARY:"):].strip()
        elif l.startswith("CATEGORIES:"):
            categories = l[len("CATEGORIES:"):].strip()

    course_clean = clean_course_name(categories)
    
    display_title = summary
    if display_title.endswith(" is due"):
        display_title = display_title[:-7].strip()
    elif display_title.endswith(" closes"):
        display_title = display_title[:-7].strip()

    if course_clean:
        formatted_summary = f"SUMMARY:📝 [{course_clean}] {display_title}"
    else:
        formatted_summary = f"SUMMARY:📝 {display_title}"

    for l in lines:
        if l.startswith("SUMMARY:"):
            new_lines.append(formatted_summary)
        elif l.strip() == "END:VEVENT":
            if not has_alarm:
                alarm_block = [
                    "BEGIN:VALARM",
                    "ACTION:DISPLAY",
                    f"DESCRIPTION:【交作业提醒】还有2天截止: {display_title}",
                    "TRIGGER:-P2D",
                    "END:VALARM",
                    "BEGIN:VALARM",
                    "ACTION:DISPLAY",
                    f"DESCRIPTION:【紧急DDL】最后2小时提醒: {display_title}",
                    "TRIGGER:-PT2H",
                    "END:VALARM"
                ]
                new_lines.extend(alarm_block)
            new_lines.append(l)
        else:
            new_lines.append(l)

    return new_lines

def generate_timetable_events(timetable_file: str = "timetable.json") -> list:
    """Generate VEVENTs from TIMETABLE_JSON secret (priority) or local json file."""
    data = None

    # 1. 优先读取 GitHub Secrets 中的 TIMETABLE_JSON 环境变量（做到100%隐私脱敏）
    env_json = os.environ.get("TIMETABLE_JSON", "").strip()
    if env_json:
        try:
            data = json.loads(env_json, strict=False)
            print("已从加密密钥 (TIMETABLE_JSON) 成功加载课表配置！")
        except Exception as e:
            print(f"解析 TIMETABLE_JSON 失败: {e}")

    # 2. 次选本地文件
    if not data and timetable_file and os.path.exists(timetable_file):
        try:
            with open(timetable_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"已从本地文件 ({timetable_file}) 加载课表配置。")
        except Exception as e:
            print(f"读取本地课表文件失败: {e}")

    if not data:
        return []

    start_str = data.get("semester_start_date")
    if not start_str:
        return []

    try:
        semester_start = datetime.strptime(start_str, "%Y-%m-%d").date()
    except Exception as e:
        print(f"Error parsing semester_start_date: {e}")
        return []

    semester_monday = semester_start - timedelta(days=semester_start.weekday())

    events = []
    courses = data.get("courses", [])

    for course in courses:
        name = course.get("name", "未命名课程")
        location = course.get("location", "未指定地点")
        teacher = course.get("teacher", "")
        weekday = course.get("weekday", 1)
        start_time_str = course.get("start_time", "09:00")
        end_time_str = course.get("end_time", "10:00")
        weeks = course.get("weeks", list(range(1, 17)))
        alarm_min = course.get("alarm_minutes_before", 15)

        for week in weeks:
            course_date = semester_monday + timedelta(days=(week - 1) * 7 + (weekday - 1))
            dtstart_str = f"{course_date.strftime('%Y%m%d')}T{start_time_str.replace(':', '')}00"
            dtend_str = f"{course_date.strftime('%Y%m%d')}T{end_time_str.replace(':', '')}00"
            uid = f"class-{name}-w{week}-d{weekday}-{dtstart_str}@calendar-sync"

            desc_lines = [f"课程: {name}", f"地点: {location}", f"周次: 第{week}周"]
            if teacher:
                desc_lines.append(f"教师: {teacher}")
            desc_str = "\\n".join(desc_lines)

            event_lines = [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTART;TZID=Asia/Shanghai:{dtstart_str}",
                f"DTEND;TZID=Asia/Shanghai:{dtend_str}",
                f"SUMMARY:📚 {name}",
                f"LOCATION:{location}",
                f"DESCRIPTION:{desc_str}",
                "STATUS:CONFIRMED",
                "BEGIN:VALARM",
                "ACTION:DISPLAY",
                f"DESCRIPTION:即将上课: {name} ({location})",
                f"TRIGGER:-PT{alarm_min}M",
                "END:VALARM",
                "END:VEVENT"
            ]
            events.append("\n".join(event_lines))

    return events

def main():
    ispace_url = os.environ.get("ISPACE_CALENDAR_URL", "").strip()
    if len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        ispace_url = sys.argv[1].strip()

    all_events = []

    if ispace_url:
        print(f"正在从 iSpace 拉取作业日历数据...")
        try:
            raw_ics = fetch_ispace_calendar(ispace_url)
            ispace_events = process_ispace_ics(raw_ics)
            print(f"成功获取并解析了 {len(ispace_events)} 个 iSpace 作业/日程事件（已注入提前2天提醒）")
            all_events.extend(ispace_events)
        except Exception as e:
            print(f"警告: 拉取 iSpace 日历失败: {e}")
    else:
        print("未检测到 ISPACE_CALENDAR_URL，跳过 iSpace 作业抓取。")

    # 课表处理：优先读取 Secret 加密课表
    timetable_file = "timetable.json"
    if not os.path.exists(timetable_file) and os.path.exists("timetable.sample.json"):
        timetable_file = "timetable.sample.json"

    course_events = generate_timetable_events(timetable_file)
    if course_events:
        print(f"成功生成了 {len(course_events)} 节课表日程（已包含课前提醒）")
        all_events.extend(course_events)
    else:
        print("未检测到课表配置，跳过课表生成。")

    out_dir = "dist"
    os.makedirs(out_dir, exist_ok=True)
    
    filename = os.environ.get("CALENDAR_FILENAME", "").strip() or "calendar.ics"
    if not filename.endswith(".ics"):
        filename += ".ics"
    out_file = os.path.join(out_dir, filename)

    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//iSpace Timetable & Homework Calendar//CN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:课程表与作业提醒",
        "X-WR-TIMEZONE:Asia/Shanghai",
        VTIMEZONE_SHANGHAI
    ]
    ics_content.extend(all_events)
    ics_content.append("END:VCALENDAR")

    full_ics_text = "\r\n".join(ics_content) + "\r\n"
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        f.write(full_ics_text)

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>")

    print(f"\n[OK] 日历生成成功！输出路径: {out_file} (总计 {len(all_events)} 个日程事件)")

if __name__ == "__main__":
    main()
