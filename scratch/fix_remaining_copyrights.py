import sys

# Force stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# File 1: books/seneca_on_happiness/copyright_ko.txt
file1 = 'books/seneca_on_happiness/copyright_ko.txt'
print(f"Cleaning {file1}...")
with open(file1, 'r', encoding='utf-8') as f:
    text1 = f.read()

target1 = "본 출판물의 어떤 부분도 출판사의 사전 서면 동의 없이는 복사, 녹음, 기타 전자적 또는 기계적 방법을 포함한 어떠한 형태나 수단으로도 복제, 배포 또는 전송될 수 없습니다. 단, 저작권법이 허용하는 비상업적 사용 및 비평이나 리뷰를 위한 짧은 인용의 경우는 예외로 합니다."
if target1 in text1:
    text1 = text1.replace(target1, "")
    # Clean double newlines
    import re
    text1 = re.sub(r'\n{3,}', '\n\n', text1).strip() + "\n"
    with open(file1, 'w', encoding='utf-8') as f:
        f.write(text1)
    print("  Successfully cleaned!")
else:
    print("  Target not found in file 1.")

# File 2: books/seneca_shortness_of_life/copyright_ko.txt
file2 = 'books/seneca_shortness_of_life/copyright_ko.txt'
print(f"Cleaning {file2}...")
with open(file2, 'r', encoding='utf-8') as f:
    text2 = f.read()

target2 = "저작권법에 의해 허용된 비상업적 목적의 사용이나 비평을 위해 짧게 인용하는 경우를 제외하고, 본 출판물의 어떤 부분도 출판사의 사전 서면 동의 없이 복사, 녹음 등 전자적 혹은 기계적인 방법을 포함한 어떠한 형태나 수단으로도 복제, 배포, 또는 전송될 수 없습니다."
if target2 in text2:
    text2 = text2.replace(target2, "")
    text2 = re.sub(r'\n{3,}', '\n\n', text2).strip() + "\n"
    with open(file2, 'w', encoding='utf-8') as f:
        f.write(text2)
    print("  Successfully cleaned!")
else:
    print("  Target not found in file 2.")

# File 3: books/thirty_six_stratagems/copyright_en.txt
file3 = 'books/thirty_six_stratagems/copyright_en.txt'
print(f"Cleaning {file3}...")
with open(file3, 'r', encoding='utf-8') as f:
    text3 = f.read()

target3 = "All rights reserved. This modernized translation, formatting, and electronic packaging are protected under copyright law. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law."
if target3 in text3:
    text3 = text3.replace(target3, "")
    text3 = re.sub(r'\n{3,}', '\n\n', text3).strip() + "\n"
    with open(file3, 'w', encoding='utf-8') as f:
        f.write(text3)
    print("  Successfully cleaned!")
else:
    print("  Target not found in file 3.")
