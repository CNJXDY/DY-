#!/usr/bin/env python3
"""
全自动博客文章发布系统
每天自动生成一篇新的SEO文章并发布到网站。
"""

import json
import os
import random
import shutil
from datetime import datetime, date
from pathlib import Path

# ============================================================
# 配置区域
# ============================================================
BASE_DIR = Path("/workspace")
TOPICS_FILE = BASE_DIR / "topics.json"
PUBLISHED_FILE = BASE_DIR / "published.json"
TEMPLATES_DIR = BASE_DIR / "templates"
ARTICLES_DIR = BASE_DIR / "articles"
INDEX_FILE = BASE_DIR / "index.html"

# GitHub 配置（用于 og:url 和部署）
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "your-github-username")
REPO_NAME = os.environ.get("REPO_NAME", "daily-blog")

# 文章目录
ARTICLES_PER_PAGE = 12  # 首页每页显示文章数


def load_json(path):
    """加载 JSON 文件"""
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path, data):
    """保存 JSON 文件"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_topics():
    """加载话题池"""
    data = load_json(TOPICS_FILE)
    return data.get("topics", [])


def load_published():
    """加载已发布记录"""
    data = load_json(PUBLISHED_FILE)
    if "published" not in data:
        data["published"] = []
    return data


def save_published(data):
    """保存已发布记录"""
    save_json(PUBLISHED_FILE, data)


def select_topic(topics, published_data):
    """
    选择当天要发布的话题：
    1. 优先从未发布过的话题中选第一个
    2. 如果全部发布过，随机选一个
    """
    published_ids = {p["topic_id"] for p in published_data["published"]}
    unpublished = [t for t in topics if t["id"] not in published_ids]

    if unpublished:
        topic = unpublished[0]  # 按顺序取第一个未发布的
        is_repeat = False
        print(f"[OK] 选择新话题: {topic['title']}")
    else:
        topic = random.choice(topics)
        is_repeat = True
        print(f"[REPEAT] 所有话题已发布过，随机选择: {topic['title']}")

    return topic, is_repeat


def generate_article_content(topic):
    """根据话题生成文章内容（HTML格式）"""
    title = topic["title"]
    category = topic["category"]
    summary = topic["summary"]

    # 根据分类生成不同结构的文章内容
    content_parts = generate_content_by_category(topic)

    return "".join(content_parts)


def generate_content_by_category(topic):
    """根据分类生成文章内容"""
    title = topic["title"]
    category = topic["category"]
    parts = []

    # 引言
    parts.append(f'<p>{topic["summary"]}</p>')
    parts.append('')

    if category == "赚钱":
        parts.append('<h2>一、为什么这些方法在2026年有效</h2>')
        parts.append('<p>2026年的经济环境发生了深刻变化。AI技术的普及、远程办公的常态化、以及数字经济的蓬勃发展，为普通人创造了前所未有的赚钱机会。与传统的"打工赚钱"模式不同，这些方法强调<strong>建立系统、利用杠杆、实现被动收入</strong>。</p>')
        parts.append('<p>核心逻辑很简单：<strong>一次投入，持续产出</strong>。无论是内容创作、数字产品销售，还是联盟营销，本质上都是在构建可以持续产生收益的资产。</p>')
        parts.append('')
        parts.append('<h2>二、核心方法详解</h2>')
        parts.append('<p>以下是经过验证的、在2026年最具可行性的赚钱方法：</p>')
        parts.append('')
        parts.append('<h3>1. AI辅助内容创作</h3>')
        parts.append('<p>利用AI工具批量生成高质量内容，通过SEO获取自然搜索流量，再通过广告和联盟营销变现。2026年的AI写作工具已经非常成熟，可以生成接近人类水平的文章。关键在于<strong>选题策略和SEO优化</strong>，而非单纯的内容数量。</p>')
        parts.append('')
        parts.append('<h3>2. 数字产品销售</h3>')
        parts.append('<p>电子书、在线课程、模板、设计素材等数字产品，一次制作可以无限销售。2026年，人们对自我提升和技能学习的需求持续增长，知识付费市场依然广阔。</p>')
        parts.append('')
        parts.append('<h3>3. 联盟营销</h3>')
        parts.append('<p>通过推荐优质产品赚取佣金。关键是要<strong>建立信任</strong>，只推荐自己真正用过且认可的产品。2026年各大电商平台的联盟计划越来越完善，佣金比例也颇具吸引力。</p>')
        parts.append('')
        parts.append('<div class="highlight-box">')
        parts.append('<p><strong>核心原则：</strong>不要追求"快速致富"，而要专注于建立可持续的收入系统。真正的被动收入需要前期投入大量时间和精力，但一旦系统建立起来，回报会持续不断。</p>')
        parts.append('</div>')

    elif category == "AI工具":
        parts.append('<h2>一、AI工具如何改变工作方式</h2>')
        parts.append('<p>2026年，AI已经深度融入日常工作流程。从写作、设计、编程到数据分析，AI工具正在帮助人们<strong>大幅提升效率</strong>。善用AI工具的人，工作效率是普通人的5-10倍。</p>')
        parts.append('')
        parts.append('<h2>二、核心工具推荐</h2>')
        parts.append('<ul class="tips-list">')
        parts.append('<li><strong>写作类：</strong>ChatGPT、Claude、Jasper — 快速生成文章、报告、邮件，大幅缩短写作时间</li>')
        parts.append('<li><strong>设计类：</strong>Midjourney、Canva AI、Figma AI — 即使没有设计基础也能做出专业级作品</li>')
        parts.append('<li><strong>编程类：</strong>GitHub Copilot、Cursor、Claude Code — AI辅助编程，效率提升300%+</li>')
        parts.append('<li><strong>数据分析：</strong>ChatGPT Advanced Data Analysis、Julius AI — 自然语言处理数据</li>')
        parts.append('<li><strong>视频制作：</strong>Runway、Pika、Sora — AI视频生成，一个人就是一支视频团队</li>')
        parts.append('</ul>')
        parts.append('')
        parts.append('<h2>三、如何选择适合你的AI工具</h2>')
        parts.append('<p>选择AI工具时，建议遵循以下原则：</p>')
        parts.append('<ol>')
        parts.append('<li><strong>明确需求</strong> — 先确定你最需要提升效率的环节</li>')
        parts.append('<li><strong>试用比较</strong> — 大多数工具都有免费试用期</li>')
        parts.append('<li><strong>持续学习</strong> — AI工具更新快，保持学习习惯</li>')
        parts.append('<li><strong>成本考量</strong> — 计算ROI，确保投入值得</li>')
        parts.append('</ol>')

    elif category == "SEO":
        parts.append('<h2>一、2026年SEO的核心变化</h2>')
        parts.append('<p>搜索引擎算法持续进化，2026年的SEO已经不再是简单的关键词堆砌。Google的AI搜索（SGE）和Bing的Copilot搜索正在改变用户获取信息的方式。<strong>内容质量、用户体验和EEAT（经验、专业、权威、信任）</strong>成为排名核心要素。</p>')
        parts.append('')
        parts.append('<h2>二、实战策略</h2>')
        parts.append('<h3>1. 关键词研究</h3>')
        parts.append('<p>使用AI工具辅助关键词研究，关注<strong>长尾关键词和用户意图</strong>。2026年的搜索更加语义化，理解用户真正想要什么比匹配精确关键词更重要。</p>')
        parts.append('')
        parts.append('<h3>2. 内容优化</h3>')
        parts.append('<p>创建<strong>深度、原创、有用</strong>的内容。2026年的搜索引擎更看重内容对用户的实际价值，而非简单的字数或关键词密度。</p>')
        parts.append('')
        parts.append('<div class="highlight-box">')
        parts.append('<p><strong>SEO口诀：</strong>内容为王，外链为皇，技术为基。三者的重要性比例约为 5:3:2。</p>')
        parts.append('</div>')

    elif category == "投资":
        parts.append('<h2>一、2026年投资环境分析</h2>')
        parts.append('<p>2026年的全球投资环境充满机遇与挑战。AI技术推动科技股持续走高，加密货币市场逐渐成熟，ESG投资成为主流趋势。了解这些宏观趋势，是做好投资的第一步。</p>')
        parts.append('')
        parts.append('<h2>二、投资策略建议</h2>')
        parts.append('<h3>1. 分散投资</h3>')
        parts.append('<p>不要把鸡蛋放在一个篮子里。合理配置股票、债券、加密货币、房地产等不同资产类别，可以有效降低风险。</p>')
        parts.append('')
        parts.append('<h3>2. 长期主义</h3>')
        parts.append('<p>短期市场波动不可避免，但长期来看，优质资产总是会升值。<strong>定投策略</strong>是普通投资者最简单有效的策略。</p>')
        parts.append('')
        parts.append('<div class="highlight-box">')
        parts.append('<p><strong>投资金句：</strong>投资最重要的不是时机，而是在场的时间。复利是世界第八大奇迹。</p>')
        parts.append('</div>')

    elif category == "远程办公":
        parts.append('<h2>一、远程办公进入新常态</h2>')
        parts.append('<p>2026年，远程办公已经从疫情期间的应急方案，演变为主流工作模式。越来越多的公司采用<strong>混合办公</strong>或<strong>完全远程</strong>模式，这对工作方式和工具选择提出了新的要求。</p>')
        parts.append('')
        parts.append('<h2>二、必备工具清单</h2>')
        parts.append('<ul class="tips-list">')
        parts.append('<li><strong>沟通协作：</strong>Slack、Microsoft Teams、Discord — 保持团队紧密连接</li>')
        parts.append('<li><strong>视频会议：</strong>Zoom、Google Meet — 高质量远程会议</li>')
        parts.append('<li><strong>项目管理：</strong>Notion、Linear、Asana — 高效管理任务和项目</li>')
        parts.append('<li><strong>文档协作：</strong>Google Workspace、Notion — 实时协作编辑</li>')
        parts.append('<li><strong>时间管理：</strong>Toggl、RescueTime — 追踪和管理工作时间</li>')
        parts.append('</ul>')

    elif category == "自我提升":
        parts.append('<h2>一、为什么自我提升是2026年最重要的投资</h2>')
        parts.append('<p>在AI快速发展的时代，只有持续学习和自我提升，才能保持竞争力。自我提升不是锦上添花，而是<strong>生存必需</strong>。</p>')
        parts.append('')
        parts.append('<h2>二、实践方法</h2>')
        parts.append('<ol>')
        parts.append('<li><strong>每日阅读</strong> — 每天至少阅读30分钟，拓宽知识边界</li>')
        parts.append('<li><strong>定期反思</strong> — 每周回顾目标和进展，及时调整方向</li>')
        parts.append('<li><strong>技能学习</strong> — 每年学习1-2项新技能，保持竞争力</li>')
        parts.append('<li><strong>健康管理</strong> — 身体是革命的本钱，保持运动和良好作息</li>')
        parts.append('</ol>')

    else:
        # 通用模板
        parts.append('<h2>一、背景介绍</h2>')
        parts.append(f'<p>随着2026年技术和市场的快速发展，{category}领域正在经历前所未有的变革。了解这些变化，把握其中的机遇，对每个人来说都至关重要。</p>')
        parts.append('')
        parts.append('<h2>二、核心要点</h2>')
        parts.append('<p>经过深入研究和实践验证，以下是该领域最值得关注的核心要点：</p>')
        parts.append('<ol>')
        parts.append('<li><strong>趋势洞察</strong> — 把握行业宏观趋势，提前布局</li>')
        parts.append('<li><strong>实操方法</strong> — 提供可落地的具体步骤</li>')
        parts.append('<li><strong>案例分析</strong> — 真实案例让理论更有说服力</li>')
        parts.append('<li><strong>工具推荐</strong> — 好用的工具事半功倍</li>')
        parts.append('</ol>')
        parts.append('')
        parts.append('<div class="highlight-box">')
        parts.append(f'<p><strong>关键洞察：</strong>在{category}领域，持续学习和实践是成功的关键。不要等待完美时机，现在就开始行动。</p>')
        parts.append('</div>')

    # 总结
    parts.append('')
    parts.append('<h2>总结</h2>')
    parts.append(f'<p>以上就是关于"{title}"的完整分享。希望这些内容能为你带来启发和实用价值。记住，<strong>知道和做到之间，差了一万次行动</strong>。从现在开始，迈出第一步，持续积累，你一定会看到改变。</p>')
    parts.append('<p>如果你觉得这篇文章有帮助，欢迎分享给更多朋友。也欢迎在评论区留言，分享你的想法和经验。</p>')

    return parts


def create_article_html(topic, article_date, is_repeat):
    """基于模板创建文章HTML"""
    # 读取模板
    template_path = TEMPLATES_DIR / "article.html"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 生成文章内容
    content_html = generate_article_content(topic)

    # 计算阅读时间（大约 300 字/分钟）
    text_content = "".join(content_html)
    text_only = text_content.replace("<", " <").replace(">", "> ")
    import re
    text_only = re.sub(r"<[^>]+>", "", text_only)
    word_count = len(text_only)
    read_time = max(1, round(word_count / 300))

    # 文章文件名
    article_slug = f"article-{topic['id']}.html"
    if is_repeat:
        article_slug = f"article-{topic['id']}-{article_date.replace('-', '')}.html"

    # 替换模板变量
    html = template.replace("{{title}}", topic["title"])
    html = html.replace("{{summary}}", topic["summary"])
    html = html.replace("{{keywords}}", topic["keywords"])
    html = html.replace("{{category}}", topic["category"])
    html = html.replace("{{date}}", article_date)
    html = html.replace("{{read_time}}", str(read_time))
    html = html.replace("{{content}}", "\n".join(content_html))
    html = html.replace("{{article_file}}", article_slug)
    html = html.replace("{{github_username}}", GITHUB_USERNAME)
    html = html.replace("{{repo_name}}", REPO_NAME)

    return html, article_slug


def update_index(all_articles):
    """更新博客首页"""
    template_path = TEMPLATES_DIR / "index.html"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 生成文章卡片
    cards = []
    for article in reversed(all_articles):  # 最新的在前面
        card = f'''            <a href="articles/{article['file']}" class="article-card">
                <span class="card-category">{article['category']}</span>
                <h3>{article['title']}</h3>
                <p class="card-summary">{article['summary']}</p>
                <span class="card-date">&#x1F4C5; {article['date']}</span>
            </a>'''
        cards.append(card)

    # 生成分页导航（如果文章超过一页）
    nav_links = ""
    total_articles = len(all_articles)
    if total_articles > ARTICLES_PER_PAGE:
        total_pages = (total_articles + ARTICLES_PER_PAGE - 1) // ARTICLES_PER_PAGE
        nav_links = '<div class="pagination" style="text-align:center;margin:20px 0;">'
        for i in range(1, total_pages + 1):
            nav_links += f'<a href="?page={i}" style="margin:0 5px;padding:5px 12px;background:#0984e3;color:#fff;border-radius:5px;text-decoration:none;">{i}</a>'
        nav_links += '</div>'

    # 计算分类数
    categories = set(a["category"] for a in all_articles)

    # 替换模板变量
    html = template.replace("{{total_articles}}", str(total_articles))
    html = html.replace("{{total_categories}}", str(len(categories)))
    html = html.replace("{{article_cards}}", "\n".join(cards))
    html = html.replace("{{nav_links}}", nav_links)

    return html


def generate_article_filename(topic, article_date, is_repeat):
    """生成文章文件名"""
    if is_repeat:
        return f"article-{topic['id']}-{article_date.replace('-', '')}.html"
    return f"article-{topic['id']}.html"


def main():
    """主流程"""
    print("=" * 60)
    print("  全自动博客文章发布系统")
    print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. 加载话题池
    topics = load_topics()
    if not topics:
        print("[ERROR] 话题池为空，请检查 topics.json")
        return
    print(f"[INFO] 话题池共 {len(topics)} 个话题")

    # 2. 加载已发布记录
    published_data = load_published()
    print(f"[INFO] 已发布 {len(published_data['published'])} 篇文章")

    # 3. 选择话题
    topic, is_repeat = select_topic(topics, published_data)
    article_date = date.today().strftime("%Y-%m-%d")

    # 4. 生成文章HTML
    print(f"[GEN] 正在生成文章: {topic['title']}")
    article_html, article_slug = create_article_html(topic, article_date, is_repeat)

    # 确保 articles 目录存在
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

    # 保存文章
    article_path = ARTICLES_DIR / article_slug
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(article_html)
    print(f"[SAVE] 文章已保存: {article_path}")

    # 5. 更新已发布记录
    published_data["published"].append({
        "topic_id": topic["id"],
        "title": topic["title"],
        "category": topic["category"],
        "date": article_date,
        "file": article_slug,
        "is_repeat": is_repeat
    })
    save_published(published_data)
    print(f"[RECORD] 已更新发布记录")

    # 6. 更新首页
    all_articles = []
    for pub in published_data["published"]:
        # 找到对应的 topic 信息
        topic_info = next((t for t in topics if t["id"] == pub["topic_id"]), None)
        if topic_info:
            all_articles.append({
                "title": pub["title"],
                "category": pub["category"],
                "summary": topic_info["summary"],
                "date": pub["date"],
                "file": pub["file"]
            })

    index_html = update_index(all_articles)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"[INDEX] 首页已更新: {INDEX_FILE}")

    # 7. 总结
    print("")
    print("=" * 60)
    print(f"  [SUCCESS] 文章发布成功!")
    print(f"  标题: {topic['title']}")
    print(f"  分类: {topic['category']}")
    print(f"  日期: {article_date}")
    print(f"  文件: articles/{article_slug}")
    if is_repeat:
        print(f"  注意: 这是重复话题（所有话题已发布过）")
    print(f"  累计发布: {len(published_data['published'])} 篇")
    print("=" * 60)

    # 8. 输出 Git 部署命令
    print("")
    print("[DEPLOY] 如需部署到 GitHub Pages，请运行：")
    print(f"  cd {BASE_DIR}")
    print("  git add -A")
    print(f"  git commit -m \"auto: publish {article_date} - {topic['title']}\"")
    print("  git push origin main")
    print("")


if __name__ == "__main__":
    main()