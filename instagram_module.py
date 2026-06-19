"""
وحدة الانستجرام - تُستدعى من بوت فيروز فلورز
أضف هذا الملف لمشروع fflowers ثم استدعِ handle_instagram_photo من معالج الصور
"""
import requests
from datetime import datetime, timedelta

INSTAGRAM_API_URL = "https://1p0f.up.railway.app"

MUSIC_OPTIONS = [
    ("🎵 ترند حالي",    "trending upbeat background music"),
    ("🌸 رومانسي هادئ", "soft romantic ambient music"),
    ("✨ راقي فاخر",    "elegant luxury instrumental"),
    ("🎶 بدون موسيقى",  "cinematic natural sounds"),
]

# حالات المستخدمين المنتظرين ردّ انستجرام
ig_states: dict = {}


def ig_call(method, path, **kwargs):
    try:
        r = requests.request(method, f"{INSTAGRAM_API_URL}{path}", timeout=240, **kwargs)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def get_best_time() -> str:
    data = ig_call("GET", "/api/schedule/analyze")
    best_hours = data.get("bestHours", [9, 18])
    hour = best_hours[0] if best_hours else 9
    scheduled = datetime.utcnow().replace(hour=hour, minute=0, second=0, microsecond=0)
    if scheduled <= datetime.utcnow():
        scheduled += timedelta(days=1)
    return scheduled.isoformat() + "Z"


def fmt_time(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        dt_riyadh = dt + timedelta(hours=3)
        return dt_riyadh.strftime("%Y-%m-%d %I:%M %p") + " (توقيت الرياض)"
    except:
        return iso


def tg_send(bot_token, chat_id, text, buttons=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if buttons:
        kb = {"inline_keyboard": [[{"text": b["label"], "callback_data": b["data"]} for b in row] for row in buttons]}
        payload["reply_markup"] = kb
    try:
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload, timeout=10)
    except:
        pass


def tg_edit(bot_token, chat_id, msg_id, text, buttons=None):
    payload = {"chat_id": chat_id, "message_id": msg_id, "text": text, "parse_mode": "HTML"}
    if buttons:
        kb = {"inline_keyboard": [[{"text": b["label"], "callback_data": b["data"]} for b in row] for row in buttons]}
        payload["reply_markup"] = kb
    try:
        requests.post(f"https://api.telegram.org/bot{bot_token}/editMessageText", json=payload, timeout=10)
    except:
        pass


def handle_instagram_photo(bot_token, chat_id, file_id):
    """
    استدعِ هذه الدالة من معالج الصور في البوت
    لما يرسل المستخدم صورة مع كلمة انستجرام/reels/رييل في التعليق
    """
    # جيب رابط الصورة
    try:
        r = requests.get(f"https://api.telegram.org/bot{bot_token}/getFile",
                         params={"file_id": file_id}, timeout=10)
        fp = r.json()["result"]["file_path"]
        image_url = fp  # الرابط الكامل مع التوكن
    except:
        tg_send(bot_token, chat_id, "❌ تعذّر جلب الصورة")
        return

    tg_send(bot_token, chat_id, "🔍 جاري تحليل الصورة بكلود AI...")

    # تحليل الصورة
    analysis = ig_call("POST", "/api/ai/analyze-image", json={"imageUrl": image_url})
    caption = analysis.get("caption", "")
    hashtags = analysis.get("hashtags", "")
    vid_prompt = analysis.get("videoPrompt", "حركة ناعمة بطيئة")
    full_caption = f"{caption}\n\n{hashtags}"

    # احفظ الحالة
    ig_states[chat_id] = {
        "step": "music",
        "image_url": image_url,
        "caption": full_caption,
        "video_prompt": vid_prompt,
    }

    buttons = [[{"label": label, "data": f"ig_music_{i}"}] for i, (label, _) in enumerate(MUSIC_OPTIONS)]

    tg_send(bot_token, chat_id,
        f"✅ <b>تم التحليل!</b>\n\n"
        f"📝 <b>الكابشن:</b>\n{caption}\n\n"
        f"{hashtags}\n\n"
        f"🎬 <i>وصف الحركة: {vid_prompt}</i>\n\n"
        f"─────────────────\n"
        f"🎵 <b>اختر نوع الموسيقى:</b>",
        buttons
    )


def handle_instagram_callback(bot_token, chat_id, msg_id, data, user_id=None):
    """
    استدعِ هذه الدالة من معالج الـ callback_query
    للـ callbacks اللي تبدأ بـ ig_
    """
    uid = user_id or chat_id
    state = ig_states.get(uid, {})

    # ── اختيار الموسيقى ──
    if data.startswith("ig_music_"):
        idx = int(data.split("_")[-1])
        label, music_desc = MUSIC_OPTIONS[idx]
        state["music"] = music_desc
        state["music_label"] = label
        state["step"] = "generating"
        ig_states[uid] = state

        tg_edit(bot_token, chat_id, msg_id,
            f"🎵 اخترت: <b>{label}</b>\n\n"
            f"⏳ جاري توليد الفيديو بـ Kling AI...\n"
            f"<i>(قد يستغرق 1-3 دقائق) 🎬</i>"
        )

        # توليد الفيديو
        full_prompt = f"{state['video_prompt']}, {music_desc}"
        video_data = ig_call("POST", "/api/video", json={
            "imageUrl": state["image_url"],
            "prompt": full_prompt,
            "duration": 5,
            "ratio": "9:16",
            "mode": "image2video",
        })

        if not video_data.get("videoUrl"):
            tg_edit(bot_token, chat_id, msg_id,
                f"❌ فشل توليد الفيديو: {video_data.get('error', 'خطأ')}"
            )
            ig_states.pop(uid, None)
            return

        state["video_url"] = video_data["videoUrl"]
        state["step"] = "timing"
        ig_states[uid] = state

        buttons = [
            [{"label": "⏰ أفضل وقت تلقائياً", "data": "ig_time_auto"}],
            [{"label": "🚀 نشر الآن فوراً",     "data": "ig_time_now"}],
            [{"label": "📅 أحدد الوقت بنفسي",   "data": "ig_time_custom"}],
        ]
        tg_edit(bot_token, chat_id, msg_id,
            f"✅ <b>تم توليد الفيديو!</b>\n\n"
            f"🎵 الموسيقى: {label}\n\n"
            f"─────────────────\n"
            f"🕐 <b>متى تريد النشر؟</b>",
            buttons
        )

    # ── اختيار الوقت ──
    elif data == "ig_time_auto":
        scheduled_at = get_best_time()
        _schedule_ig(bot_token, chat_id, msg_id, uid, state, scheduled_at)

    elif data == "ig_time_now":
        scheduled_at = (datetime.utcnow() + timedelta(minutes=1)).isoformat() + "Z"
        _schedule_ig(bot_token, chat_id, msg_id, uid, state, scheduled_at)

    elif data == "ig_time_custom":
        ig_states[uid]["step"] = "awaiting_time"
        tg_edit(bot_token, chat_id, msg_id,
            "📅 <b>اكتب الوقت الذي تريده:</b>\n\n"
            "مثال: <code>2025-06-20 18:00</code>\n"
            "<i>(التوقيت: الرياض UTC+3)</i>"
        )

    # ── عرض المنشورات المجدولة ──
    elif data == "ig_pending":
        result = ig_call("GET", "/api/schedule")
        posts = [p for p in result.get("posts", []) if p.get("status") == "pending"]
        if not posts:
            tg_send(bot_token, chat_id, "✅ لا توجد منشورات في الانتظار")
        else:
            for p in posts[:5]:
                tg_send(bot_token, chat_id,
                    f"⏰ <b>{fmt_time(p['scheduledAt'])}</b>\n\n"
                    f"📝 {p.get('caption','')[:150]}...\n"
                    f"🆔 <code>{p['id']}</code>",
                    [[{"label": "🗑️ إلغاء", "data": f"ig_cancel_{p['id']}"}]]
                )

    elif data.startswith("ig_cancel_"):
        post_id = data.replace("ig_cancel_", "")
        result = ig_call("DELETE", f"/api/schedule?id={post_id}")
        tg_send(bot_token, chat_id, "🗑️ تم الإلغاء ✅" if result.get("success") else "❌ فشل الإلغاء")


def handle_instagram_time_text(bot_token, chat_id, text, user_id=None):
    """
    استدعِ هذه الدالة لما يكتب المستخدم وقت مخصص
    """
    uid = user_id or chat_id
    state = ig_states.get(uid, {})
    if state.get("step") != "awaiting_time":
        return False  # مش في حالة انتظار وقت

    try:
        dt_riyadh = datetime.strptime(text.strip(), "%Y-%m-%d %H:%M")
        dt_utc = dt_riyadh - timedelta(hours=3)
        scheduled_at = dt_utc.isoformat() + "Z"
    except:
        tg_send(bot_token, chat_id,
            "❌ صيغة غير صحيحة. اكتب مثل:\n<code>2025-06-20 18:00</code>"
        )
        return True

    _schedule_ig(bot_token, chat_id, None, uid, state, scheduled_at)
    return True


def _schedule_ig(bot_token, chat_id, msg_id, uid, state, scheduled_at):
    result = ig_call("POST", "/api/schedule", json={
        "videoUrl":    state.get("video_url"),
        "caption":     state.get("caption"),
        "scheduledAt": scheduled_at,
        "mediaType":   "REELS",
    })
    ig_states.pop(uid, None)

    text = (
        f"✅ <b>تمت الجدولة بنجاح!</b>\n\n"
        f"🕐 سيُنشر في: <b>{fmt_time(scheduled_at)}</b>\n\n"
        f"📝 {state.get('caption','')[:150]}..."
        if "post" in result else
        f"❌ فشلت الجدولة: {result.get('error','خطأ')}"
    )

    if msg_id:
        tg_edit(bot_token, chat_id, msg_id, text)
    else:
        tg_send(bot_token, chat_id, text)
