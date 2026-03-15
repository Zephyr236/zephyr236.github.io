---
layout: default
title: Home
---

<div class="home">
    <h1>Welcome to My Blog</h1>
    <p>A personal blog built with Jekyll, supporting Markdown and LaTeX.</p>

    <h2>Recent Posts</h2>
    <ul class="post-list">
        {% for post in site.posts %}
        <li>
            <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        </li>
        {% endfor %}
    </ul>
</div>
