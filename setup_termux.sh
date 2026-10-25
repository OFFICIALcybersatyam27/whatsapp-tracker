#!/data/data/com.termux/files/usr/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   📱 WhatsApp Tracker - Auto Setup   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}[1/5] Packages update...${NC}"
pkg update -y && pkg upgrade -y
echo -e "${GREEN}✅ Done${NC}"

echo -e "${CYAN}[2/5] Python install...${NC}"
pkg install python python-pip -y
echo -e "${GREEN}✅ Done${NC}"

echo -e "${CYAN}[3/5] libmagic install (neonize dependency)...${NC}"
pkg install file -y
echo -e "${GREEN}✅ Done${NC}"

echo -e "${CYAN}[4/5] neonize install...${NC}"
pip install neonize
echo -e "${GREEN}✅ Done${NC}"

echo -e "${CYAN}[5/5] Tracker ready...${NC}"
chmod +x whatsapp_tracker.py
echo -e "${GREEN}✅ Done${NC}"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ Setup complete! Ab chalao:      ║${NC}"
echo -e "${GREEN}║                                      ║${NC}"
echo -e "${YELLOW}║     python whatsapp_tracker.py       ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
