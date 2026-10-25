#!/usr/bin/env python3
import os, sys, time, threading
from datetime import datetime

try:
    from neonize.client import NewClient
    from neonize.events import MessageEv, ConnectedEv
    try:
        from neonize.events import PairStatusEv, DisconnectedEv
    except:
        PairStatusEv = None
        DisconnectedEv = None
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Fix:\n  pkg install file\n  pip install neonize\n")
    sys.exit(1)

# ── Colors ────────────────────────────────────────────────
R="\033[0m";BD="\033[1m";DM="\033[2m"
GR="\033[32m";CY="\033[36m";YL="\033[33m";RD="\033[31m"
MG="\033[35m";WH="\033[37m";BL="\033[34m"
BG_GR="\033[42m";BG_BL="\033[44m";BG_MG="\033[45m"
LGR="\033[92m";LCY="\033[96m";LYL="\033[93m";LMG="\033[95m"

DB_NAME = "wa_session.db"

try: W = os.get_terminal_size().columns
except: W = 55
if W < 45: W = 45
if W > 70: W = 70

def ln(ch="─"): return ch*W

def now(): return datetime.now().strftime("%I:%M:%S %p")

mc = 0

def get_db():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)

def banner():
    os.system("clear")
    print(LCY+BD+"╔"+"═"*(W-2)+"╗"+R)
    lines = [
        (LGR, "📱  WHATSAPP TRACKER  -  TERMUX"),
        (LYL, "⚡  Developed by OFFICIAL_cyber_satyam27  ⚡"),
    ]
    for color, t in lines:
        p = (W-2-len(t))//2
        print(LCY+BD+"║"+R + " "*p + color+BD+t+R + " "*(W-2-p-len(t)) + LCY+BD+"║"+R)
    print(LCY+BD+"╚"+"═"*(W-2)+"╝"+R+"\n")

def is_linked():
    return os.path.exists(get_db())

# ── MENU ──────────────────────────────────────────────────
def menu():
    while True:
        banner()
        status = f"{LGR}{BD}● LINKED{R}" if is_linked() else f"{RD}{BD}○ NOT LINKED{R}"
        print(f"{DM}  Device Status : {R}{status}\n")
        print(LMG+BD+"  ┌"+"─"*(W-4)+"┐"+R)
        print(LMG+BD+"  │"+R+f"{WH}{BD}{'   M A I N   M E N U':<{W-5}}"+LMG+BD+"│"+R)
        print(LMG+BD+"  ├"+"─"*(W-4)+"┤"+R)
        opts = [
            ("1", "🔗", "Add Device  (Link WhatsApp)", LCY),
            ("2", "💬", "Chat View   (Live Tracker)",  LGR),
            ("3", "🚪", "Exit", RD),
        ]
        for k, ic, label, c in opts:
            print(LMG+BD+"  │  "+R + c+BD+f"[{k}] {ic}  {label}"+R + " "*(W-9-len(label)) + LMG+BD+"│"+R)
        print(LMG+BD+"  └"+"─"*(W-4)+"┘"+R)
        print(f"\n{YL}{BD}  >>> {R}", end="", flush=True)

        choice = input().strip()

        if choice == "1":
            add_device()
        elif choice == "2":
            chat_view()
        elif choice == "3":
            exit_app()
        else:
            print(RD+"\n  ❌ Galat choice! 1, 2 ya 3 daalo."+R)
            time.sleep(1.2)

def exit_app():
    banner()
    print(LYL+BD+ln()+R)
    print(f"{LGR}{BD}   👋  Dhanyavaad! Tracker band ho raha hai...{R}")
    print(f"{DM}   ⚡ Developed by OFFICIAL_cyber_satyam27 ⚡{R}")
    print(LYL+BD+ln()+R+"\n")
    sys.exit(0)

# ── ADD DEVICE (LINK) ────────────────────────────────────
def add_device():
    banner()
    DB = get_db()
    print(LCY+BD+"  ┌"+"─"*(W-4)+"┐"+R)
    print(LCY+BD+"  │"+R+f"{WH}{BD}{'      🔗  ADD DEVICE  🔗':<{W-5}}"+LCY+BD+"│"+R)
    print(LCY+BD+"  └"+"─"*(W-4)+"┘"+R+"\n")

    print(LYL+BD+"  ┌"+"─"*(W-4)+"┐"+R)
    print(LYL+BD+"  │  "+R+f"{WH}Apna WhatsApp number daalo{' '*(W-33)}"+LYL+BD+"│"+R)
    print(LYL+BD+"  │  "+R+f"{DM}(jaise: 917086852797){' '*(W-28)}"+LYL+BD+"│"+R)
    print(LYL+BD+"  │  "+R+f"{DM}Ya sirf Enter dabao (pehle se linked){' '*(W-43)}"+LYL+BD+"│"+R)
    print(LYL+BD+"  └"+"─"*(W-4)+"┘"+R)
    print(f"\n{LGR}{BD}  >>> {R}", end="", flush=True)

    phone = input().strip().replace("+", "").replace(" ", "")

    if phone:
        if os.path.exists(DB):
            os.remove(DB)
            print(DM+"\n  (Purani session hata di)"+R)
        print(YL+f"\n  📞 Number: +{phone}"+R)
        print(YL+"  ⏳ Connect ho raha hai..."+R+"\n")
    else:
        if not os.path.exists(DB):
            print(RD+"\n  ❌ Koi saved session nahi mili. Pehle number daalo!"+R)
            input(DM+"\n  Enter dabao MENU par jaane ke liye..."+R)
            return
        print(GR+"\n  ✅ Existing session se connect ho raha hai..."+R+"\n")
        phone = None

    client = NewClient(DB)

    @client.event(ConnectedEv)
    def on_connect(cli, ev):
        print(LGR+BD+"\n  ✅ WhatsApp Device Linked Successfully!"+R)
        print(DM+ln()+R+"\n")

    if PairStatusEv:
        @client.event(PairStatusEv)
        def on_pair(cli, ev):
            try: print(LGR+BD+f"\n  ✅ Linked: +{ev.ID.User}\n"+R)
            except: print(LGR+BD+"\n  ✅ Linked!\n"+R)

    if DisconnectedEv:
        @client.event(DisconnectedEv)
        def on_dc(cli, ev):
            print(RD+BD+"\n  ❌ Disconnect!\n"+R)

    if phone:
        conn_t = threading.Thread(target=client.connect)
        conn_t.daemon = True
        conn_t.start()

        print(YL+"  Pairing code ke liye 5 second wait karo..."+R)
        for i in range(5, 0, -1):
            print(YL+f"  {i}..."+R, end="\r", flush=True)
            time.sleep(1)

        print(YL+"\n  Pairing code maang raha hai...\n"+R)
        try:
            code = client.PairPhone(phone, True)
            print(LGR+BD+"\n  ✅ PAIRING CODE MILA!\n"+R)
            print(BD+"  ╔"+"═"*(W-4)+"╗")
            ctext = f"🔑  CODE :  {code}"
            p = (W-4-len(ctext))//2
            print(BD+"  ║"+" "*p+LGR+BD+ctext+R+BD+" "*(W-4-p-len(ctext))+"║")
            print(BD+"  ╚"+"═"*(W-4)+"╝"+R)
            print(LYL+BD+"\n  Ab WhatsApp mein ye karo:"+R)
            print(WH+"  1. Settings > Linked Devices"+R)
            print(WH+"  2. Link a Device"+R)
            print(WH+"  3. 'Link with phone number' dabao"+R)
            print(WH+f"  4. Code daalo:  {LGR}{BD}{code}{R}\n")
        except Exception as e:
            print(RD+f"\n  Pairing Error: {e}\n"+R)
            print(YL+"  QR code try karo - dusre phone se scan karo\n"+R)

        print(DM+"  (Ctrl+C dabao menu par wapas jaane ke liye)"+R)
        try:
            conn_t.join()
        except KeyboardInterrupt:
            pass
    else:
        print(DM+"  (Ctrl+C dabao menu par wapas jaane ke liye)"+R)
        try:
            client.connect()
        except KeyboardInterrupt:
            pass

    input(DM+"\n  Enter dabao MENU par jaane ke liye..."+R)

# ── CHAT VIEW (LIVE TRACKER) ─────────────────────────────
def get_text(msg):
    try:
        m = msg.Message
        if m.conversation: return m.conversation
        if m.extendedTextMessage.text: return m.extendedTextMessage.text
        if m.imageMessage.caption: return m.imageMessage.caption
        if m.videoMessage.caption: return m.videoMessage.caption
        for a, l in [("imageMessage","🖼️ IMAGE"),("videoMessage","🎥 VIDEO"),
                     ("audioMessage","🎵 AUDIO"),("documentMessage","📄 DOCUMENT"),
                     ("stickerMessage","🎭 STICKER"),("locationMessage","📍 LOCATION")]:
            try:
                if getattr(m, a).ByteSize() > 0: return f"[{l}]"
            except: pass
        return "[MEDIA]"
    except: return "[MESSAGE]"

def show(d, name, num, chat, text):
    global mc; mc += 1
    b = (BG_BL+WH+BD+" 📤 BHEJA (SENT)    "+R) if d == "SENT" \
        else (BG_GR+WH+BD+" 📥 AAYA (RECEIVED) "+R)
    print(DM+ln()+R)
    print(f"{b}  {DM}{now()} #{mc}{R}")
    print(f"{CY}{BD}  👤 Naam    : {R}{WH}{name}{R}")
    print(f"{CY}{BD}  📞 Number  : {R}{YL}+{num}{R}")
    print(f"{CY}{BD}  💬 Chat    : {R}{DM}{chat}{R}")
    is_m = text.startswith("[") and text.endswith("]")
    clr = YL+DM if is_m else WH
    icon = "📎 Media  " if is_m else "📝 Message"
    max_w = W-16
    if not is_m and len(text) > max_w:
        print(f"{MG}{BD}  {icon}: {R}{clr}{text[:max_w]}{R}")
        for i in range(max_w, len(text), max_w):
            print(f"              {clr}{text[i:i+max_w]}{R}")
    else:
        print(f"{MG}{BD}  {icon}: {R}{clr}{text}{R}")
    print()

def chat_view():
    global mc
    mc = 0
    banner()
    DB = get_db()

    if not os.path.exists(DB):
        print(RD+BD+"  ❌ Koi device linked nahi hai!"+R)
        print(YL+"  Pehle MENU se [1] Add Device use karo.\n"+R)
        input(DM+"  Enter dabao MENU par jaane ke liye..."+R)
        return

    print(LGR+BD+"  ┌"+"─"*(W-4)+"┐"+R)
    print(LGR+BD+"  │"+R+f"{WH}{BD}{'      💬  CHAT VIEW  💬':<{W-5}}"+LGR+BD+"│"+R)
    print(LGR+BD+"  └"+"─"*(W-4)+"┘"+R)
    print(DM+"  Messages yahan live dikhenge... (Ctrl+C = menu par wapas)"+R+"\n")

    client = NewClient(DB)

    @client.event(ConnectedEv)
    def on_connect(cli, ev):
        print(LGR+BD+"  ✅ Connected! Live tracking shuru..."+R)
        print(DM+ln()+R+"\n")

    if DisconnectedEv:
        @client.event(DisconnectedEv)
        def on_dc(cli, ev):
            print(RD+BD+"\n  ❌ Disconnect!\n"+R)

    @client.event(MessageEv)
    def on_msg(cli, msg):
        try:
            info = msg.Info; src = info.MessageSource
            is_me = src.IsFromMe; is_g = src.IsGroup
            fj = src.Chat.User; sj = src.Sender.User if is_g else fj
            name = info.Pushname or "Unknown"
            if is_g:
                try: chat = f"Group: {cli.GetGroupInfo(src.Chat).Name}"
                except: chat = f"Group: {fj}"
            else:
                chat = "Private chat"
            if is_me: name, num = "Aap (You)", fj
            else: num = sj
            show("SENT" if is_me else "RECEIVED", name, num, chat, get_text(msg))
        except Exception as e:
            print(RD+DM+f"  [err: {e}]"+R)

    try:
        client.connect()
    except KeyboardInterrupt:
        pass

    print(YL+BD+f"\n  📊 Total messages track kiye: {mc}"+R)
    input(DM+"\n  Enter dabao MENU par jaane ke liye..."+R)

# ── MAIN ──────────────────────────────────────────────────
def main():
    try:
        menu()
    except KeyboardInterrupt:
        exit_app()

if __name__ == "__main__":
    main()
