from PIL import Image, ImageDraw, ImageFont
import os
from fontTools.ttLib import TTFont
import re

PANGRAM = """아앙 하악 흐읏 큭 간다 간닷
움찔 흠칫 두근 주르륵 끈적 질척 찔꺽
다람쥐 헌 쳇바퀴에 타고파…—♡♥!? 1234567890
닭 콩팥 훔친 집사
물컵 속 팥 찾던 형
동틀 녘 햇빛 포개짐
자동차 바퀴 틈새가 파랗니
닭 잡아서 치킨 파티 함
추운 겨울에는 따뜻한 커피와 티를 마셔야지요"""
IMAGE_SIZE = (960, 540)
TEXT_POSITION = (40, 60)
FONT_NAME_MARGIN = (20, 20)
TEXT_COLOR = "black"
BACKGROUND_COLOR = "white"
FONT_DIR = "Fonts"
OUTPUT_DIR = "Pangrams"
FONTSIZE = 10
LINE_SPACE = int(FONTSIZE * 2/3)


def get_font_name(font_path):
    font = TTFont(font_path)
    name_table = font["name"]

    for name in name_table.names:
        try:
            # 4번 : 폰트 풀네임
            if name.nameID == 4:
                # platformID : 0-유니코드, 1-맥, 2-ISO, 3-윈도우
                if name.platformID == 3:  
                    font_name = name.string.decode("utf-16-be", errors="ignore")
        except Exception:
            continue

    return font_name


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    font_files = [f for f in os.listdir(FONT_DIR) if f.lower().endswith((".ttf", ".otf"))]

    cnt = 0
    for font_file in font_files:
        cnt = cnt + 1
        font_path = os.path.join(FONT_DIR, font_file)
        font_name = get_font_name(font_path)
        
        try:
            # 폰트 로드
            font = ImageFont.truetype(font_path, FONTSIZE)
            font_small = ImageFont.truetype(font_path, FONTSIZE * 4/5)
            
            # 이미지 생성
            img = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
            draw = ImageDraw.Draw(img)
            
            # 팬그램 작성
            lines = PANGRAM.splitlines()
            y_position = TEXT_POSITION[1]
            for line in lines:
                bbox = draw.textbbox((TEXT_POSITION[0], y_position), line, font=font)
                text_height = bbox[3] - bbox[1]
                draw.text((TEXT_POSITION[0], y_position), line, font=font, fill=TEXT_COLOR)
                y_position += text_height + LINE_SPACE
            
            # 폰트 이름 작성
            font_name_bbox = draw.textbbox((0, 0), f"Font: {font_name}", font=font_small)
            font_name_width = font_name_bbox[2] - font_name_bbox[0]
            font_name_position = (IMAGE_SIZE[0] - font_name_width - FONT_NAME_MARGIN[0], FONT_NAME_MARGIN[1])
            draw.text(font_name_position, f"{font_name}", font=font_small, fill=TEXT_COLOR)
            
            # 저장            
            ## 폰트명 깨짐 확인
            if re.search(r'[가-힣A-Za-z]', font_name):
                output_path = os.path.join(OUTPUT_DIR, f"{font_name}.png")
                img.save(output_path)
                print(f"[{cnt}]✅ {output_path}")
            else:
                filename = os.path.splitext(os.path.basename(font_path))[0]
                font_name = f"{filename}_ERROR"
                output_path = os.path.join(OUTPUT_DIR, f"{font_name}.png")
                img.save(output_path)
                print(f"[{cnt}]❌ {font_name} - 폰트 인식 실패")
            
        
        except Exception as e:
            print(f"[{cnt}]❌ {font_name}: {e}")
            continue

    print(f"{cnt}개 생성")