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

    <h2>Articles (HTML)</h2>
    <ul class="post-list">
        {% assign html_files = site.html_files | sort: 'name' | reverse %}
        {% for file in html_files %}
            {% unless file.name contains 'layout' or file.name contains 'default' or file.name == 'index.html' %}
            <li>
                <span class="post-date">{{ file.name | slice: 0, 10 }}</span>
                <a href="{{ file.url | relative_url }}">{{ file.name | remove: '.html' | replace: '-', ' ' | capitalize }}</a>
            </li>
            {% endunless %}
        {% endfor %}
    </ul>
</div>
