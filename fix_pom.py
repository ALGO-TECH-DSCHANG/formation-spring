import os
import glob
import re

for pom in glob.glob("backend/*/pom.xml"):
    with open(pom, "r") as f:
        content = f.read()
    
    # We remove the entire maven-compiler-plugin plugin block
    new_content = re.sub(r'<plugin>\s*<groupId>org\.apache\.maven\.plugins</groupId>\s*<artifactId>maven-compiler-plugin</artifactId>.*?</plugin>', '', content, flags=re.DOTALL)
    
    # Let's also remove the spring-boot-maven-plugin excludes that exclude lombok (it's useless and sometimes messes up repackaging)
    new_content = re.sub(r'<plugin>\s*<groupId>org\.springframework\.boot</groupId>\s*<artifactId>spring-boot-maven-plugin</artifactId>.*?</plugin>', '', new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(pom, "w") as f:
            f.write(new_content)
        print("Fixed", pom)
