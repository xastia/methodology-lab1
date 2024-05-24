import argparse
import sys
import re

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def write_file(content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def parse_markdown(md_content):
    html_content = ""
    
    # Regex patterns for basic markdown elements
    patterns = {
        'bold': re.compile(r'\*\*(.*?)\*\*'),
        'italic': re.compile(r'_(.*?)_'),
        'monospaced': re.compile(r'`(.*?)`'),
        'preformatted': re.compile(r'```(.*?)```', re.DOTALL)
    }

    in_preformatted_block = False

    lines = md_content.split('\n')
    for line in lines:
        # Preformatted text
        if line.strip().startswith("```"):
            if in_preformatted_block:
                in_preformatted_block = False
                html_content += f"<pre>{preformatted_content}</pre>\n"
            else:
                in_preformatted_block = True
                preformatted_content = ""
            continue

        if in_preformatted_block:
            preformatted_content += line + '\n'
            continue

        # Bold
        line = patterns['bold'].sub(r'<b>\1</b>', line)
        
        # Italic
        line = patterns['italic'].sub(r'<i>\1</i>', line)
        
        # Monospaced
        line = patterns['monospaced'].sub(r'<tt>\1</tt>', line)
        
        # Paragraphs
        if line.strip():
            html_content += f"{line}\n"
        else:
            html_content += "</p>\n<p>"
    
    # Adding the last preformatted block if it's incomplete
    if in_preformatted_block:
        html_content += f"<pre>{preformatted_content}</pre>\n"
    else:
        html_content = "<p>" + html_content.strip() + "</p>"
    
    return html_content

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown file to HTML.')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    parser.add_argument('--out', dest='output_file', help='Path to the output HTML file')
    
    args = parser.parse_args()
    
    md_content = read_file(args.input_file)
    html_content = parse_markdown(md_content)
    
    if args.output_file:
        write_file(html_content, args.output_file)
    else:
        print(html_content)

if __name__ == '__main__':
    main()



