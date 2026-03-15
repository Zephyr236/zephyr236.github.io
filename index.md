---
layout: default
title: Home
---

<div class="home">
    <h1>Welcome to Zephyr's Blog</h1>

    <h2>Recent Posts</h2>
    <ul class="post-list">
        {% for post in site.posts %}
        <li>
            <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        </li>
        {% endfor %}
    </ul>

    <h2>Articles</h2>
    <ul class="post-list">
        {% for file in site.static_files %}
            {% if file.path contains '.html' %}
            {% unless file.path contains 'index.html' or file.path contains '_layouts' or file.path contains '_includes' %}
            <li>
                <span class="post-date">{{ file.path | slice: 1, 10 }}</span>
                <a href="{{ file.url | relative_url }}">{{ file.name | remove: '.html' | replace: '-', ' ' | capitalize }}</a>
            </li>
            {% endunless %}
            {% endif %}
        {% endfor %}
    </ul>
</div>
