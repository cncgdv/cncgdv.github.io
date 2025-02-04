import json
import os
import shutil

# Paths
template_path = 'index.template.html'
locales_dir = 'locales'
output_dir = 'dist'
images_dir = 'images'
assets_dir = 'assets'

# Load template
with open(template_path, 'r', encoding='utf-8') as file:
    template = file.read()

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Find all placeholders in the template
import re
placeholders = re.findall(r'\{\{(.*?)\}\}', template)

# Function to copy static files
def copy_static_files(src_dir, dest_dir):
    if os.path.exists(src_dir):
        shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)

# Copy static assets to dist
copy_static_files(images_dir, f'{output_dir}/images')
copy_static_files(assets_dir, f'{output_dir}/assets')

# Process each language file
for locale_file in os.listdir(locales_dir):
    lang = locale_file.split('.')[0]
    with open(f'{locales_dir}/{locale_file}', 'r', encoding='utf-8') as file:
        translations = json.load(file)

    # Replace placeholders and check for missing translations
    localized_html = template
    missing_keys = []

    for key in placeholders:
        if key in translations:
            localized_html = localized_html.replace(f'{{{{{key}}}}}', translations[key])
        else:
            missing_keys.append(key)
            localized_html = localized_html.replace(f'{{{{{key}}}}}', f'[MISSING: {key}]')

    # Report missing translations
    if missing_keys:
        print(f'Missing translations for "{lang}" locale: {", ".join(missing_keys)}')

    # Determine output path
    if lang == 'en':
        output_path = f'{output_dir}/index.html'
    else:
        lang_dir = f'{output_dir}/{lang}'
        os.makedirs(lang_dir, exist_ok=True)
        output_path = f'{lang_dir}/index.html'

    # Save localized HTML
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(localized_html)

    print(f'Generated {output_path}')
