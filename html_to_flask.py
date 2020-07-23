import os
from bs4 import BeautifulSoup

TEMPLATES_BASE_DIR = 'templates'
HTML_EXTENSIONS = ('.html', '.htm', '.xhtml')
STATIC_FILE_EXTENSIONS = ('.js', '.css', '.map', '.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.mp4', '.mov', '.mkv', '.mp3')

def get_html_code(filepath=''):
    """
    Reads and returns the html code from the html file
    """
    try:
        html_file = open(filepath, 'r')
        html_code = html_file.read()
        html_file.close()
        return html_code
    except:
        return ''


def get_matches(html_code):
    """
    Searches and returns a set of the src paths and urls that need to be changed
    """
    bs4_obj = BeautifulSoup(html_code, 'lxml')
    matching_paths = set()
    invalid_start_str = ('http://', 'https://', '#', '//', '{{')
    for link in bs4_obj.find_all('a'):
        if 'href' in link.attrs:
            href = link['href']
            if not href.lower().startswith(invalid_start_str) and href.lower().endswith(STATIC_FILE_EXTENSIONS + HTML_EXTENSIONS):
                matching_paths.add(href)
    for link in bs4_obj.find_all('link'):
        if 'href' in link.attrs:
            href = link['href']
            if not href.lower().startswith(invalid_start_str) and href.lower().endswith(STATIC_FILE_EXTENSIONS + HTML_EXTENSIONS):
                matching_paths.add(href)
    for path in bs4_obj.find_all('img'):
        if 'src' in path.attrs:
            path = path['src']
            if not path.lower().startswith(invalid_start_str) and path.lower().endswith(STATIC_FILE_EXTENSIONS + HTML_EXTENSIONS):
                matching_paths.add(path)
    for path in bs4_obj.find_all('script'):
        if 'src' in path.attrs:
            path = path['src']
            if not path.lower().startswith(invalid_start_str) and path.lower().endswith(STATIC_FILE_EXTENSIONS + HTML_EXTENSIONS):
                matching_paths.add(path)
    return matching_paths


def get_edited_paths(matching_paths):
    """
    Edits matching paths to conform with the flask format and returns a dictionary mapping
    the usual path format to the flask format
    """
    edited_paths = dict()
    for path in matching_paths:
        if path.endswith(HTML_EXTENSIONS):
            route_func_name = os.path.basename(path).rsplit('.')[0].lower().replace("-", "_")
            if not path in edited_paths.keys():
                edited_paths[path] = "{{ url_for('" + route_func_name + "') }}"
        else:
            if not path in edited_paths.keys():
                edited_paths[path] = "{{ url_for('static', filename='" + path + "') }}"
    return edited_paths


def replace_urls(html_code, matched_paths_dict):
    """
    Replaces the html paths with flask type paths
    """
    for raw_path, flask_path in matched_paths_dict.items():
        html_code = html_code.replace(raw_path, flask_path)
    return html_code


def save_edited_html_code(filepath, edited_html_code):
    """
    Replaces the old file with the edited version
    """
    html_file = open(filepath, 'w')
    html_file.write(edited_html_code)
    html_file.flush()
    html_file.close()


def edit_all_html_files():
    """
    Applies editing to all html files in the templates folder
    """
    for filename in os.listdir(TEMPLATES_BASE_DIR):
        filepath = os.path.join(TEMPLATES_BASE_DIR, filename)
        html_code = get_html_code(filepath)
        matching_paths = get_matches(html_code)
        matched_paths_dict = get_edited_paths(matching_paths)
        edited_html_code = replace_urls(html_code, matched_paths_dict)
        save_edited_html_code(filepath, edited_html_code)


if __name__=='__main__':
    edit_all_html_files()