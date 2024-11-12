import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import os
import requests

# 定义获取教授信息的函数
def get_professor_info(name, institution=None):
    search_url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={(name + ' ' + institution) if institution else name}"
    print(search_url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        # 获取搜索结果页面
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # 如果请求失败，会抛出异常
        
        # 使用 BeautifulSoup 解析页面
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取第一个搜索结果的链接
        first_result = soup.find('h3', {'class': 'gs_ai_name'}).find('a')
        if not first_result:
            print(f"Error: No search results found for {name + ' ' + institution}")
            return None
        
        
        # 构造第一个结果的个人主页链接
        profile_link = "https://scholar.google.com" + first_result['href']
        # 确保返回英文结果
        if not profile_link.endswith("hl=en"):
            profile_link += "&hl=en"
            
        
        # 获取教授的主页页面
        profile_page = requests.get(profile_link, headers=headers)
        profile_soup = BeautifulSoup(profile_page.text, 'html.parser')
        
        # 获取机构信息
        # 获取机构信息
        institution_element = profile_soup.find('a', {'class': 'gsc_prf_ila'})
        institution = institution_element.text.strip() if institution_element else "No institution listed."
        
        
        # 获取引用数（从包含引用数据的表格中提取数字）
        citation_table = profile_soup.find('table', {'id': 'gsc_rsb_st'})
        if citation_table:
            citation_values = [td.text.strip() for td in citation_table.find_all('td', {'class': 'gsc_rsb_std'})]
        else:
            citation_values = ["No citation data available"]
            
        
        # 获取研究兴趣列表
        interests_div = profile_soup.find('div', {'id': 'gsc_prf_int'})
        if interests_div:
            interests_elements = interests_div.find_all('a', {'class': 'gsc_prf_inta'})
            research_interests = [interest.text.strip() for interest in interests_elements]
            # print(research_interests)
        else:
            research_interests = ["No research interests listed."]
        
        # 返回教授信息的字典
        return {
            'name': name,
            'institution': institution,
            'citation_count': citation_values,
            'research_interests': research_interests,
            'scholar_link': profile_link
        }
    except Exception as e:
        print(f"Error fetching data for {name}: {e}")
        return {
            'name': name,
            'institution': 'Not found',
            'citation_count': 'Not found',
            'research_interests': 'Not found',
            'scholar_link': 'Not found'
        }

# 批量处理多个教授
def get_multiple_professors_info(professor_list, institution=None):
    professors_info = []
    
    def fetch_info(professor, institution):
        return get_professor_info(professor, institution)
    print(f'Searching for {len(professor_list)} professors...')
    with ThreadPoolExecutor(max_workers=8) as executor:
        # 修改 `get_multiple_professors_info` 函数中executor.map的传参方式
        professors_info = list(executor.map(lambda prof: fetch_info(prof, institution), professor_list))

    
    return professors_info


API_KEY = os.getenv("API_KEY")  
API_ENDPOINT = "https://api.chatanywhere.tech/v1/chat/completions"

# 读取CSV文件并提取相关信息
def read_csv(file_path):
    mentors = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mentors.append({
                "name": row['name'],
                "institution": row['institution'],
                "citation_count": row['citation_count'],
                "research_interests": row['research_interests'],
                "scholar_link": row['scholar_link']
            })
    return mentors

# 调用LLM API分析导师信息并推荐机器人控制方向的导师
def analyze_mentors(mentors):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        "Content-Type": "application/json"
    }
    
    # 准备请求内容
    content = (
        "I have a list of mentors with their research interests, "
        "and I am looking for those in the field of robotics and control. "
        "Can you help me find all matching mentors for this area and provide a reason for each?"
        "Finally, I would like to know the top 3 recommended mentors from this list."
        "Here is the data:\n" + str(mentors)
    )
    
    # 构造API请求体
    data = {
        "model": "gpt-4o",  # 使用您需要的模型名称
        "messages": [
            {"role": "user", "content": content}
        ]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# 从HTML元素中提取教授名字
def extract_name_from_HTML(html):
    # 提取option标签中的教授名字
    soup = BeautifulSoup(html, 'html.parser')
    options = soup.find_all('option')
    names = [(option.text) for option in options if option['value']]
    print(names)
    return names



# 示例教授名单

institution = "INSTITUTION_NAME"
department = ""
HTML = """copy the whole select element from the website and paste it here (use developer tools to copy the select element)
"""

professor_list = extract_name_from_HTML(HTML)

filename = institution + '_' + department + '_' + 'professors_info.csv'
# 如果文件不存在，创建文件并写入数据
if not os.path.exists(filename):
    professors_info = get_multiple_professors_info(professor_list)
    # 存进文件csv
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=professors_info[0].keys())
        writer.writeheader()
        writer.writerows(professors_info)
    
mentors = read_csv(filename)
recommendation = analyze_mentors(mentors)
print("Recommended mentors for robotics and control direction:")
print(recommendation)

# 将推荐结果写入Markdown文件
markdown_filename = institution + '_' + department + '_' + 'recommended_mentors.md'
with open(markdown_filename, 'w', encoding='utf-8') as md_file:
    md_file.write("# Recommended Mentors for Robotics and Control Direction\n\n")
    md_file.write(recommendation)